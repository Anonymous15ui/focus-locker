"""Optional per-task links: storage, migration, and opening them."""
import json
import os
import sys
import tempfile

scratch = tempfile.mkdtemp()
os.environ["FOCUS_LOCKER_CONFIG"] = os.path.join(scratch, "config.json")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# a config written by the previous version: tasks with no "link" key at all
json.dump({"tasks": [{"text": "Study", "done": False},
                     {"text": "Quran", "done": True}]},
          open(os.environ["FOCUS_LOCKER_CONFIG"], "w"))

from focus import controller as controller_module      # noqa: E402
from focus.controller import FOCUS, Controller         # noqa: E402

log = lambda m: print("  log:", m, flush=True)
c = Controller(log=log)

# 1. old tasks still load, and simply have an empty link
assert [t["text"] for t in c.tasks] == ["Study", "Quran"]
assert all(t["link"] == "" for t in c.tasks), c.tasks
print("old tasks migrate with an empty link")

# 2. adding with and without a link
c.add_task("Jeel Academy", "app.edu-nation.app/lessons")
c.add_task("hadith")
assert c.task_link(2) == "app.edu-nation.app/lessons"
assert c.task_link(3) == ""
c.set_task_link(3, "  https://example.edu/reading  ")
assert c.task_link(3) == "https://example.edu/reading", "link should be trimmed"
assert json.load(open(os.environ["FOCUS_LOCKER_CONFIG"]))["tasks"][2]["link"]
print("links stored, trimmed, and saved to disk")

# 3. opening: a task with no link says so rather than opening anything
opened = []
controller_module.webbrowser.open = lambda url: opened.append(url)
ok, detail = c.open_task_link(0)
assert not ok and "no link" in detail
assert not opened

# 4. a bare domain gets https:// put in front of it
ok, detail = c.open_task_link(2)
assert ok and opened == ["https://app.edu-nation.app/lessons"], opened
print("bare domain opened as https")

# 5. a folder or file on this computer opens instead of a browser
started = []
controller_module.os.startfile = lambda path: started.append(path)
c.add_task("homework folder", scratch)
ok, detail = c.open_task_link(4)
assert ok and started == [scratch] and len(opened) == 1, (started, opened)
print("local folder opened without the browser")

# 6. during a session, a link to a blocked site is refused with a reason
c.cfg["blocked_sites"] = ["youtube.com"]
c.cfg["allowed_sites"] = ["app.edu-nation.app"]
c.add_task("watch something", "https://www.youtube.com/watch?v=x")
c.state = FOCUS
ok, detail = c.open_task_link(5)
assert not ok and "blocked list" in detail, detail
assert len(opened) == 1, "must not open a blocked site mid-session"
# but an allowed site still opens while locked
ok, detail = c.open_task_link(2)
assert ok and len(opened) == 2
print("blocked link refused mid-session, allowed link still opens")

print("TASK LINKS VERIFIED")
