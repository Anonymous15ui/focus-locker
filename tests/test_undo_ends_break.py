"""Un-ticking a finished task ends the break it earned."""
import os
import sys
import tempfile

scratch = tempfile.mkdtemp()
os.environ["FOCUS_LOCKER_CONFIG"] = os.path.join(scratch, "config.json")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from focus import blocker                                      # noqa: E402
from focus.controller import BREAK, FOCUS, IDLE, Controller    # noqa: E402

blocker.HOSTS_PATH = os.path.join(scratch, "hosts")
open(blocker.HOSTS_PATH, "w").write("127.0.0.1 localhost\n")
log = lambda m: print("  log:", m, flush=True)

c = Controller(log=log)
c.cfg.update(block_websites=True, close_browsers_on_lock=False, blocked_apps=[],
             blocked_sites=["youtube.com"], allowed_sites=[], poll_seconds=1, tasks=[])
c.add_task("first")
c.add_task("second")

c.start_focus()
c.complete_task(0)
assert c.state == BREAK, c.state
assert "0.0.0.0" not in open(blocker.HOSTS_PATH).read(), "break should unblock"

# the actual ask: taking the tick back ends the break
c.uncomplete_task(0)
assert c.state == FOCUS, c.state
assert c.seconds_left() == 0
assert not c.tasks[0]["done"]
assert "0.0.0.0 youtube.com" in open(blocker.HOSTS_PATH).read(), "should be locked again"
print("un-ticking during a break goes straight back to focus")

# un-ticking a task that was not done changes nothing
assert c.uncomplete_task(1) is None
assert c.state == FOCUS
print("un-ticking an unfinished task is a no-op")

# and outside a session it stays out of the way
c.complete_task(0)
c.stop()
assert c.state == IDLE
assert c.uncomplete_task(0) is None
assert c.state == IDLE, "un-ticking must not start a session on its own"
print("outside a session, nothing gets locked")

c.stop()
print("UNDO ENDS BREAK VERIFIED")
