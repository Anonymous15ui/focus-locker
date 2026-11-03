# Focus Locker

A Windows app that locks the apps and websites you pick while you work through a
to-do list, and unlocks them for a break when you finish something.

## Download

Click **FocusLocker.exe** above, then the download button. One file — no Python,
no installer, no setup.

Two things to expect the first time:

- Windows will ask for **administrator**. That is how it edits the hosts file to
  block websites; without it, only apps get blocked.
- **"Windows protected your PC"** → *More info* → *Run anyway*. That is
  SmartScreen flagging an unsigned program, not a virus. Signing costs money.

Some antivirus tools are suspicious of this kind of build on principle. If yours
quarantines it, that is a false positive, and the source it was built from is in
this repository's history.

## How it works

Add your tasks, press **Start focus**, and everything on your blocked list is
frozen the moment it runs while blocked domains stop resolving.

- **Finish a task** → a break starts (5 minutes by default) and everything
  unlocks. When the timer runs out it locks again by itself, with a 30-second
  warning first.
- **Finish the whole list** → the longer end-of-list break runs (15 minutes by
  default), and then nothing re-locks, because there is nothing left to do.
- **Undo done** on a finished task ends the break it earned and locks straight
  back in.
- **Break now** starts an unscheduled break; **Stop / unlock** ends the session.

Each task can carry an optional **link** — a website, or a folder or file on this
computer — so "Open link" takes you straight to where the work happens.

The header shows where you stand: a ring counting the break down or filling with
tasks done, and a sky that follows the session. Starting one slides the sun down
behind the hills while the moon climbs and the stars come out.

## Habits

The **Habits** tab tracks things you want to do every day, separately from the
to-do list. Each habit keeps a streak and its own colour. Habits never lock or
unlock anything; they are just tracked.

## Settings

| Setting | Meaning |
| --- | --- |
| Language | English, العربية, Français, Español. Arabic flips the layout right to left |
| Colour scheme | Nine schemes, each with a light and a dark variant |
| Break after each task | Off = only the end-of-list break |
| Break lengths | Default 5 minutes per task, 15 at the end of the list |
| How blocked apps are handled | `suspend` freezes the app so nothing is lost; `close` terminates it |
| Also block websites | Needs administrator; edits the Windows hosts file |
| Close browsers when locking | On by default — see the note below |
| Check interval | How often the watchdog looks for blocked apps |

**Blocked apps** take process names as Task Manager shows them (`chrome.exe`).
Windows' own critical processes are ignored even if you add them, so you cannot
freeze your desktop by mistake. **Blocked sites** take domains (`youtube.com`).
**Always allowed sites** is for your school portal and the like — domains only,
since a hosts file knows nothing about paths.

## Things worth knowing

- **Why browsers get closed when a lock starts.** The hosts file only affects new
  DNS lookups. A tab already playing a blocked site has an open connection and
  cached DNS, so it can carry on for several minutes after the lock. Closing the
  browser is what makes the block bite immediately. Turn it off and expect that
  lag back.
- If the app is killed while locked, run it again and press **Stop / unlock** to
  clear the leftover hosts entries.
- This is a focus aid, not parental-control software. It does not defend itself:
  it can be closed, and its settings file edited. The point is to make the
  distraction cost effort, not to be unbeatable.
- Your tasks, habits, blocklists and settings live in `data\config.json` beside
  the app. Nothing leaves your computer.

## Source code

This page carries the app and this README only. The Python source it is built
from is still in the repository's history — nothing was lost. To get it back:

```
git clone https://github.com/Anonymous15ui/focus-locker.git
cd focus-locker
git checkout e6db372
```

That commit has the full project: the `focus` package, the tests, and
`build_exe.bat`, which rebuilds `FocusLocker.exe`.

**The .exe does not update itself.** Changing the source means rebuilding it and
uploading the new file.
