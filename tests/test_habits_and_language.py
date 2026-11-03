"""Habit tracking (ticks, streaks, saving) and the translations behind the language setting."""
import datetime
import json
import os
import string
import sys
import tempfile

scratch = tempfile.mkdtemp()
os.environ["FOCUS_LOCKER_CONFIG"] = os.path.join(scratch, "config.json")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# a config written by the previous version: no habits, no language
json.dump({"tasks": [{"text": "Study", "done": False, "link": ""}]},
          open(os.environ["FOCUS_LOCKER_CONFIG"], "w"))

from focus import habits, i18n                          # noqa: E402
from focus.controller import Controller                 # noqa: E402

day = datetime.date(2026, 10, 31)
ago = lambda n: day - datetime.timedelta(days=n)
c = Controller(log=lambda m: None)

# 1. an old config loads with no habits and English
assert c.habits == [] and c.cfg["language"] == "en"
print("old config migrates: no habits, English")

# 2. adding, ignoring blanks and duplicates
c.add_habit("Read 20 minutes")
c.add_habit("   ")
c.add_habit("Read 20 minutes")
c.add_habit("Exercise")
assert [h["name"] for h in c.habits] == ["Read 20 minutes", "Exercise"], c.habits
print("habits added, blanks and duplicates ignored")

# 3. ticking, unticking, and streaks
read = c.habits[0]
for n in (4, 3, 2, 1):                                 # four days running, up to yesterday
    c.toggle_habit(0, ago(n))
assert habits.streak(read, day) == 4, "an unticked today must not break the streak yet"
c.toggle_habit(0, day)
assert habits.is_done(read, day) and habits.streak(read, day) == 5
c.toggle_habit(0, day)                                 # tapped by mistake: undo
assert not habits.is_done(read, day) and habits.streak(read, day) == 4
c.toggle_habit(0, ago(2))                              # a missed day breaks it
assert habits.streak(read, day) == 1
assert habits.last_days(read, 7, day) == [False, False, True, True, False, True, False]
assert habits.streak(c.habits[1], day) == 0
print("ticks, undo, streaks and the 7-day row all correct")

# 4. everything is on disk, and survives a reload
again = Controller(log=lambda m: None)
assert again.habits == c.habits, (again.habits, c.habits)
c.remove_habit(1)
assert [h["name"] for h in Controller(log=lambda m: None).habits] == ["Read 20 minutes"]
print("habits saved, reloaded and deleted")

# 5. junk in the file can't crash the app
json.dump({"habits": [{"name": "ok", "done": "nope"}, {"done": []}, "junk"],
           "language": 5}, open(os.environ["FOCUS_LOCKER_CONFIG"], "w"))
junk = Controller(log=lambda m: None)
assert junk.habits == [{"name": "ok", "done": []}] and junk.cfg["language"] == "en"
print("bad habit data cleaned up on load")

# 6. every language has every key, with the same {placeholders} as English
fields = lambda s: sorted(f for _, f, _, _ in string.Formatter().parse(s) if f)
english = i18n.STRINGS["en"]
for code in i18n.LANGUAGES:
    strings = i18n.STRINGS[code]
    assert set(strings) == set(english), (code, set(english) ^ set(strings))
    for key, text in strings.items():
        assert fields(text) == fields(english[key]), (code, key)
print("all", len(i18n.LANGUAGES), "languages complete, placeholders match")

# 7. switching language, right-to-left, and unknown codes
i18n.set_language("ar")
assert i18n.is_rtl() and i18n.t("tab_habits") == "العادات"
assert "3" in i18n.t("habit_streak", n=3)
i18n.set_language("fr")
assert not i18n.is_rtl() and i18n.t("tab_habits") == "Habitudes"
i18n.set_language("xx")
assert i18n.current() == "en" and i18n.t("tab_habits") == "Habits"
print("language switching, RTL and fallback work")

print("HABITS AND LANGUAGES VERIFIED")
