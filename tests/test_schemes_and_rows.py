"""Every scheme is complete, and the drawn rows survive switching between them."""
import datetime
import json
import os
import sys
import tempfile

scratch = tempfile.mkdtemp()
os.environ["FOCUS_LOCKER_CONFIG"] = os.path.join(scratch, "config.json")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

today = datetime.date.today().isoformat()
json.dump({"tasks": [{"text": "Study", "done": True, "link": "school.example"},
                     {"text": "bio quiz", "done": False, "link": ""}],
           "habits": [{"name": "Read", "done": [today]}, {"name": "Walk", "done": []}]},
          open(os.environ["FOCUS_LOCKER_CONFIG"], "w"))

from focus import theme                                # noqa: E402

# 1. no scheme is missing a colour the app paints with
needed = {"BG", "SURFACE", "SURFACE_2", "LINE", "TEXT", "MUTED", "DIM", "FOCUS_C",
          "BREAK_C", "IDLE_C", "DANGER", "DONE_C", "SKY", "HILLS", "STAR", "ACCENTS"}
for name, scheme in theme.SCHEMES.items():
    missing = needed - set(scheme)
    assert not missing, f"{name} is missing {missing}"
    assert set(scheme["SKY"]) == {"break", "idle", "focus"}, f"{name} sky states"
    assert len(scheme["ACCENTS"]) >= 5, f"{name} needs more accents"
    for key in ("BG", "SURFACE", "TEXT", "FOCUS_C"):
        assert scheme[key].startswith("#") and len(scheme[key]) == 7, f"{name}.{key}"
    # text has to be readable on the background it sits on
    contrast = abs(int(scheme["TEXT"][1:3], 16) - int(scheme["BG"][1:3], 16))
    assert contrast > 0x60, f"{name}: text too close to background"
print(f"{len(theme.SCHEMES)} schemes, all complete and legible")

from focus.gui import App                              # noqa: E402

app = App()
app.update()

# 2. rows are built as data, with the bits the drawing needs
rows = app.task_list.rows
assert len(rows) == 2 and rows[0]["checked"] and not rows[1]["checked"]
assert rows[0]["trail"] == "school.example"
assert rows[0]["accent"] != rows[1]["accent"], "rows should not all be one colour"
habit_rows = app.habit_list.rows
assert habit_rows[0]["checked"] and habit_rows[0]["dots"], habit_rows[0]
print("task and habit rows carry checkbox, link, dots and colour")

# 3. switching scheme keeps the rows and repaints in the new colours
for name in theme.SCHEMES:
    app.set_scheme(name)
    app.update()
    assert theme.MODE == name
    assert len(app.task_list.rows) == 2, f"rows lost switching to {name}"
    assert len(app.habit_list.rows) == 2, f"habit rows lost switching to {name}"
    assert app.ctl.cfg["theme"] == name, "scheme should be remembered"
print("every scheme applied without losing a row")

# 4. the sky slides rather than jumping. The app re-renders the scene from the
#    session state every tick, so this has to go through a real session.
import time                                            # noqa: E402

app.set_scheme("dark")
app.ctl.cfg.update(block_websites=False, blocked_apps=[], close_browsers_on_lock=False)
start = app.scene.phase
app.ctl.start_focus()
app.refresh_status()
assert app.scene.target == 1.0, "a session should send the sky toward night"
assert app.scene.phase == start, "the phase should ease, not snap to its target"
for _ in range(40):            # the slide runs on a 40ms timer, so time must pass
    time.sleep(0.05)
    app.update()
assert start < app.scene.phase < 1.0, f"expected a partial slide, got {app.scene.phase}"
print("sun/moon slide eases toward night instead of jumping")

# 5. a checkbox click ticks the task
app.task_list.on_toggle(1)
assert app.ctl.tasks[1]["done"], "clicking the box should tick the task"
app.task_list.on_toggle(1)
assert not app.ctl.tasks[1]["done"], "clicking it again should untick"
print("checkbox clicks tick and untick")

app.ctl.stop()
app.destroy()
print("SCHEMES AND ROWS VERIFIED")
