"""Locking of apps (process watchdog) and websites (hosts file)."""
import ctypes
import os
import subprocess
import threading
import time

import psutil

HOSTS_PATH = os.path.join(
    os.environ.get("SystemRoot", r"C:\Windows"), "System32", "drivers", "etc", "hosts"
)
MARK_START = "# === focus-locker start (do not edit inside) ==="
MARK_END = "# === focus-locker end ==="

# Never touch these, whatever the blocklist says -- suspending them wedges Windows.
PROTECTED = {
    "system", "system idle process", "registry", "smss.exe", "csrss.exe",
    "wininit.exe", "winlogon.exe", "services.exe", "lsass.exe", "svchost.exe",
    "explorer.exe", "dwm.exe", "ctfmon.exe", "fontdrvhost.exe", "taskhostw.exe",
    "sihost.exe", "runtimebroker.exe", "audiodg.exe", "conhost.exe",
    "shellexperiencehost.exe", "searchhost.exe", "startmenuexperiencehost.exe",
    "msmpeng.exe", "wudfhost.exe", "dllhost.exe", "spoolsv.exe",
}

user32 = ctypes.windll.user32


def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _minimize_windows_of(pid):
    """Get a frozen window out of the way before we suspend it."""
    SW_MINIMIZE = 6
    proto = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def cb(hwnd, _lparam):
        owner = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(owner))
        if owner.value == pid and user32.IsWindowVisible(hwnd):
            user32.ShowWindow(hwnd, SW_MINIMIZE)
        return True

    try:
        user32.EnumWindows(proto(cb), None)
    except Exception:
        pass


def close_processes(names, log=print):
    """One-shot: ask the named processes to quit, then kill whatever ignores it.

    Used at lock time for browsers -- freezing them is not enough when the point is
    to drop the connection that is still feeding an already-open blocked page.
    """
    targets = {n.strip().lower() for n in names if n.strip()} - PROTECTED
    if not targets:
        return 0
    victims = []
    for proc in psutil.process_iter(["pid", "name"]):
        if (proc.info["name"] or "").lower() in targets and proc.pid != os.getpid():
            victims.append(proc)
    for proc in victims:
        try:
            proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    gone, alive = psutil.wait_procs(victims, timeout=5)
    for proc in alive:
        try:
            proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    if victims:
        log("closed {} browser process(es)".format(len(victims)))
    return len(victims)


class AppBlocker:
    """Background thread that keeps blocked apps frozen (or closed) while locked."""

    def __init__(self, get_blocked_names, get_mode, get_interval, log=print):
        self._get_names = get_blocked_names
        self._get_mode = get_mode
        self._get_interval = get_interval
        self._log = log
        self._thread = None
        self._stop = threading.Event()
        self._suspended = set()          # pids we froze, so we can thaw exactly those
        # never freeze ourselves or the shell that launched us
        self._own_pids = {os.getpid()}
        try:
            parent = psutil.Process().parent()
            while parent is not None:
                self._own_pids.add(parent.pid)
                parent = parent.parent()
        except psutil.Error:
            pass

    # -- lifecycle ----------------------------------------------------------
    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=3)
            self._thread = None
        self.release_all()

    @property
    def running(self):
        return bool(self._thread and self._thread.is_alive())

    # -- guts ---------------------------------------------------------------
    def _targets(self):
        return {n.strip().lower() for n in self._get_names() if n.strip()} - PROTECTED

    def _loop(self):
        while not self._stop.is_set():
            try:
                self._sweep()
            except Exception as exc:                     # never let the watchdog die
                self._log(f"blocker error: {exc}")
            self._stop.wait(max(1, int(self._get_interval())))

    def _sweep(self):
        targets = self._targets()
        mode = self._get_mode()
        if not targets:
            return
        for proc in psutil.process_iter(["pid", "name", "status"]):
            info = proc.info
            name = (info.get("name") or "").lower()
            if name not in targets or info["pid"] in self._own_pids:
                continue
            try:
                if mode == "close":
                    self._log(f"closing {info['name']} ({info['pid']})")
                    proc.terminate()
                else:
                    if info.get("status") == psutil.STATUS_STOPPED:
                        self._suspended.add(info["pid"])
                        continue
                    _minimize_windows_of(info["pid"])
                    proc.suspend()
                    self._suspended.add(info["pid"])
                    self._log(f"froze {info['name']} ({info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
                self._log(f"could not block {info['name']}: {type(exc).__name__}")

    def release_all(self):
        """Thaw everything we froze. Called on break / unlock / shutdown."""
        for pid in list(self._suspended):
            try:
                psutil.Process(pid).resume()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            self._suspended.discard(pid)


class SiteBlocker:
    """Blocks domains by writing a marked block into the Windows hosts file."""

    def __init__(self, log=print):
        self._log = log
        self.active = False

    def _read(self):
        with open(HOSTS_PATH, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()

    def _write(self, text):
        with open(HOSTS_PATH, "w", encoding="utf-8") as fh:
            fh.write(text)

    @staticmethod
    def _strip_block(text):
        if MARK_START not in text:
            return text
        head, rest = text.split(MARK_START, 1)
        tail = rest.split(MARK_END, 1)[1] if MARK_END in rest else ""
        return (head.rstrip() + "\n" + tail.lstrip("\n")).rstrip() + "\n"

    def apply(self, domains, allowed):
        """Block `domains` minus `allowed`. Returns (ok, message)."""
        allow = {d.strip().lower().lstrip("*.") for d in allowed if d.strip()}
        wanted = []
        for raw in domains:
            d = raw.strip().lower().replace("https://", "").replace("http://", "").strip("/")
            if not d or d in allow or any(d.endswith("." + a) or d == a for a in allow):
                continue
            wanted.append(d)
            if not d.startswith("www."):
                wanted.append("www." + d)
        try:
            body = self._strip_block(self._read())
            if wanted:
                lines = [MARK_START] + [f"0.0.0.0 {d}" for d in dict.fromkeys(wanted)] + [MARK_END]
                body = body.rstrip() + "\n" + "\n".join(lines) + "\n"
            self._write(body)
            self._flush_dns()
            self.active = bool(wanted)
            return True, f"{len(set(wanted))} host entries written"
        except PermissionError:
            return False, "no admin rights - run the app as administrator to block websites"
        except OSError as exc:
            return False, f"hosts file error: {exc}"

    def clear(self):
        try:
            self._write(self._strip_block(self._read()))
            self._flush_dns()
            self.active = False
            return True, "websites unblocked"
        except PermissionError:
            return False, "no admin rights - hosts entries left in place"
        except OSError as exc:
            return False, f"hosts file error: {exc}"

    def _flush_dns(self):
        try:
            subprocess.run(
                ["ipconfig", "/flushdns"],
                capture_output=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                timeout=10,
            )
        except Exception:
            pass
