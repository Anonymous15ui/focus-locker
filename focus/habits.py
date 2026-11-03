"""Daily habits: tick each one off once a day and keep the streak going.

A habit is {"name": str, "done": ["YYYY-MM-DD", ...]} - the days it was ticked.
"""
import datetime


def today():
    return datetime.date.today()


def is_done(habit, day=None):
    return (day or today()).isoformat() in habit["done"]


def toggle_day(habit, day=None):
    """Tick the day off, or untick it if it already was."""
    key = (day or today()).isoformat()
    if key in habit["done"]:
        habit["done"].remove(key)
    else:
        habit["done"].append(key)
        habit["done"].sort()


def streak(habit, day=None):
    """Days in a row ending today - or ending yesterday if today isn't ticked yet,
    so a streak doesn't look broken first thing in the morning."""
    day = day or today()
    done = set(habit["done"])
    if day.isoformat() not in done:
        day -= datetime.timedelta(days=1)
    count = 0
    while day.isoformat() in done:
        count += 1
        day -= datetime.timedelta(days=1)
    return count


def last_days(habit, count=7, day=None):
    """[bool] for the last `count` days, oldest first, ending today."""
    day = day or today()
    done = set(habit["done"])
    return [(day - datetime.timedelta(days=i)).isoformat() in done
            for i in range(count - 1, -1, -1)]
