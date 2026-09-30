"""The whole focus/break cycle, on scratch files so real settings are untouched."""
import os
import subprocess
import sys
import tempfile
import time

scratch = tempfile.mkdtemp()
os.environ["FOCUS_LOCKER_CONFIG"] = os.path.join(scratch, "config.json")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psutil                                          # noqa: E402

from focus import blocker                              # noqa: E402
from focus.controller import BREAK, FOCUS, IDLE, Controller  # noqa: E402

blocker.HOSTS_PATH = os.path.join(scratch, "hosts")
open(blocker.HOSTS_PATH, "w").write("127.0.0.1 localhost\n")
log = lambda m: print("  log:", m, flush=True)


def notepads():
    return [p for p in psutil.process_iter(["name"])
            if (p.info["name"] or "").lower() == "notepad.exe"]


# --- 1. hosts file handling -------------------------------------------------
sites = blocker.SiteBlocker(log=log)
ok, detail = sites.apply(["youtube.com", "https://tiktok.com/", "school.edu"], ["school.edu"])
text = open(blocker.HOSTS_PATH).read()
assert ok and "0.0.0.0 www.youtube.com" in text
assert "school.edu" not in text, "an allowed site must never be blocked"
sites.apply(["reddit.com"], [])                        # re-apply replaces, never stacks
text = open(blocker.HOSTS_PATH).read()
assert text.count("focus-locker start") == 1 and "youtube" not in text
sites.clear()
assert open(blocker.HOSTS_PATH).read() == "127.0.0.1 localhost\n"
print("hosts file: blocked, allowed-list respected, replaced not stacked, restored")

# --- 2. a real process gets frozen and thawed -------------------------------
for p in notepads():                                   # clean slate
    p.terminate()
time.sleep(1)
subprocess.Popen(["notepad.exe"])
time.sleep(4)
assert notepads(), "stand-in app did not start"

c = Controller(log=log)
c.cfg.update(block_websites=True, close_browsers_on_lock=True,
             browser_processes=[], blocked_apps=["notepad.exe"],
             blocked_sites=["youtube.com"], allowed_sites=[], poll_seconds=1,
             task_break_minutes=0.1, warn_before_break_ends_seconds=3, tasks=[])
c.add_task("first")
c.add_task("second")

c.start_focus()
for _ in range(8):
    time.sleep(1)
    if all(p.status() == psutil.STATUS_STOPPED for p in notepads()):
        break
assert notepads() and all(p.status() == psutil.STATUS_STOPPED for p in notepads())
assert "0.0.0.0 youtube.com" in open(blocker.HOSTS_PATH).read()
print("focus: blocked app frozen, sites blocked")

# --- 3. finishing a task unlocks for a break --------------------------------
c.complete_task(0)
assert c.state == BREAK
assert all(p.status() != psutil.STATUS_STOPPED for p in notepads()), "break must thaw apps"
assert "0.0.0.0" not in open(blocker.HOSTS_PATH).read(), "break must unblock sites"
print("break: app thawed, sites unblocked")

# --- 4. the break ends on time and re-locks ---------------------------------
warned = None
for _ in range(10):
    time.sleep(1)
    message = c.tick()
    if message and "heads up" in str(message):
        warned = message
    if c.state == FOCUS:
        break
assert warned, "no warning before the break ended"
assert c.state == FOCUS, c.state
assert "0.0.0.0 youtube.com" in open(blocker.HOSTS_PATH).read(), "did not re-lock on time"
print("relock: warned first, then locked again the moment the timer ran out")

# --- 5. finishing the list leaves everything unlocked -----------------------
c.cfg["break_after_list_minutes"] = 0.1
c.complete_task(1)
assert c.state == BREAK
for _ in range(10):
    time.sleep(1)
    c.tick()
    if c.state == IDLE:
        break
assert c.state == IDLE, c.state
assert "0.0.0.0" not in open(blocker.HOSTS_PATH).read()
assert all(p.status() != psutil.STATUS_STOPPED for p in notepads())
print("list finished: stays unlocked")

c.stop()
for p in notepads():
    p.terminate()
print("FOCUS FLOW VERIFIED")
