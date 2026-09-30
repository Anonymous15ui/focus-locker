"""The focus/break state machine that decides when things are locked."""
import os
import time
import webbrowser

from . import config
from .blocker import AppBlocker, SiteBlocker, close_processes, is_admin

IDLE, FOCUS, BREAK = "idle", "focus", "break"


class Controller:
    def __init__(self, log=print):
        self.cfg = config.load()
        self.state = IDLE
        self.break_until = 0.0
        self.break_reason = ""
        self.log = log
        self._warned = False
        self.apps = AppBlocker(
            get_blocked_names=lambda: self.cfg["blocked_apps"],
            get_mode=lambda: self.cfg["block_mode"],
            get_interval=lambda: self.cfg["poll_seconds"],
            log=log,
        )
        self.sites = SiteBlocker(log=log)

    # -- persistence --------------------------------------------------------
    def save(self):
        config.save(self.cfg)

    # -- task helpers -------------------------------------------------------
    @property
    def tasks(self):
        return self.cfg["tasks"]

    def add_task(self, text, link=""):
        text = text.strip()
        if text:
            self.tasks.append({"text": text, "done": False, "link": link.strip()})
            self.save()

    def task_link(self, index):
        if 0 <= index < len(self.tasks):
            return self.tasks[index].get("link", "")
        return ""

    def set_task_link(self, index, link):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["link"] = link.strip()
            self.save()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save()

    def pending_count(self):
        return sum(1 for t in self.tasks if not t["done"])

    def complete_task(self, index):
        """Mark done and start whatever break should follow."""
        if not (0 <= index < len(self.tasks)) or self.tasks[index]["done"]:
            return None
        self.tasks[index]["done"] = True
        self.save()
        if self.state == IDLE:
            return None
        if self.pending_count() == 0:
            if self.cfg["break_after_list_enabled"]:
                return self.start_break(self.cfg["break_after_list_minutes"], "list finished")
            self.stop()
            return None
        if self.cfg["break_after_each_task"]:
            return self.start_break(self.cfg["task_break_minutes"], "task finished")
        return None

    def uncomplete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["done"] = False
            self.save()

    def open_task_link(self, index):
        """Open a task's link: a website, or a folder or file on this computer."""
        link = self.task_link(index)
        if not link:
            return False, "that task has no link"
        if os.path.exists(link):
            try:
                os.startfile(link)                    # folder or file
            except OSError as exc:
                return False, f"could not open it: {exc}"
            return True, f"opened {link}"

        url = link if "://" in link else "https://" + link
        host = url.split("://", 1)[1].split("/", 1)[0].lower()
        if self.state == FOCUS and self._is_blocked_host(host):
            return False, (f"{host} is on your blocked list, so it will not load "
                           "during a session. Add it to Always allowed sites if you "
                           "need it for this task.")
        try:
            webbrowser.open(url)
        except Exception as exc:
            return False, f"could not open it: {exc}"
        return True, f"opened {host}"

    def _is_blocked_host(self, host):
        allowed = {a.strip().lower().lstrip("*.") for a in self.cfg["allowed_sites"] if a.strip()}
        if any(host == a or host.endswith("." + a) for a in allowed):
            return False
        for raw in self.cfg["blocked_sites"]:
            blocked = raw.strip().lower().replace("https://", "").replace("http://", "").strip("/")
            if blocked and (host == blocked or host.endswith("." + blocked)):
                return True
        return False

    # -- locking ------------------------------------------------------------
    def start_focus(self):
        self.state = FOCUS
        self.break_until = 0.0
        self.apps.start()
        msg = "apps locked"
        if self.cfg["block_websites"]:
            ok, detail = self.sites.apply(self.cfg["blocked_sites"], self.cfg["allowed_sites"])
            msg += f"; sites: {detail}"
            if not ok:
                self.log(detail)
            elif self.cfg["close_browsers_on_lock"]:
                # hosts rules only apply to new lookups, so a tab that is already
                # streaming survives them; closing the browser is what stops it now
                close_processes(self.cfg["browser_processes"], self.log)
        self.log(msg)
        return msg

    def start_break(self, minutes, reason=""):
        minutes = max(0.1, float(minutes))
        self.state = BREAK
        self.break_reason = reason
        self._warned = False
        self.apps.stop()                      # stops watchdog and thaws everything
        if self.cfg["block_websites"]:
            self.sites.clear()
        # start the clock only once everything is actually unlocked, otherwise the
        # unlock work (a process sweep can take a second or two) eats into the break
        self.break_until = time.time() + minutes * 60
        self.log(f"break started ({minutes:g} min) - {reason}")
        return self.break_until

    def end_break(self):
        """Break timer ran out -> lock again, unless the list is done."""
        self.break_until = 0.0
        if self.pending_count() == 0:
            self.stop()
            return "all tasks done - staying unlocked"
        return self.start_focus()

    def stop(self):
        self.state = IDLE
        self.break_until = 0.0
        self.apps.stop()
        if self.sites.active or self.cfg["block_websites"]:
            self.sites.clear()
        self.log("everything unlocked")

    def seconds_left(self):
        return max(0, int(round(self.break_until - time.time()))) if self.state == BREAK else 0

    def tick(self):
        """Called once a second by the UI. Returns a message when something changes."""
        if self.state != BREAK:
            return None
        if time.time() >= self.break_until:
            return self.end_break()
        warn_at = self.cfg["warn_before_break_ends_seconds"]
        if not self._warned and 0 < self.seconds_left() <= warn_at:
            self._warned = True
            return (f"heads up: {self.seconds_left()}s of break left - "
                    "browsers will be closed when it locks again")
        return None

    @staticmethod
    def admin():
        return is_admin()
