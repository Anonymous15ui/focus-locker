# Focus Locker

A Windows to-do app that locks the apps and websites you pick while you work, and
unlocks them for a break when you finish a task.

## Setup

Needs Windows and Python 3.9+. From the project folder, once:

```
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

That creates the `.venv` folder the launchers expect. It isn't in the repo, so
this step is required after cloning.

## Run it

```
run.bat                 # apps are locked, websites are not
run_as_admin.bat        # apps AND websites are locked (hosts file needs admin)
```

Or manually, from the project folder: `.venv\Scripts\python.exe main.py`

## How it works

- **To-do tab** — add tasks, double-click (or "Mark done") to complete one.
  Each task can carry an optional **link**: type it in the second box when you add
  the task, or select a task and press "Edit link". Select a task and press
  "Open link" to jump straight there. A link can be a website (`app.edu-nation.app`
  — no need to type `https://`), or a folder or file on this computer, which opens
  in Explorer or its usual app instead of a browser. Tasks with a link show it
  after an arrow in the list.
- **Start focus** — from that moment, every app on your blocked list gets frozen
  the instant it is running, and blocked domains stop resolving.
- **Finish a task** → a break starts (5 minutes by default). Everything unlocks.
  When the timer runs out, it locks again automatically and you carry on. You get
  a 30-second warning in the Activity log before that happens.
- **Finish the whole list** → the longer end-of-list break starts (15 min default),
  and after that nothing re-locks, because there is nothing left to do.
- **Break now** starts an unscheduled break; **Stop / unlock** ends the session.

## Settings

| Setting | Meaning |
| --- | --- |
| Break after each task | Off = only the end-of-list break |
| Break after each task (minutes) | Default 5 |
| Break after whole list (minutes) | Default 15 |
| How blocked apps are handled | `suspend` freezes the app — nothing is lost, tabs survive. `close` terminates it, unsaved work can be lost |
| Also block websites | Needs admin; edits the Windows hosts file |
| Close browsers when locking | On by default — see the note below on why this is needed |
| Check interval | How often the watchdog sweeps for blocked apps |

## Lists

- **Blocked apps** — process names as Task Manager shows them (`chrome.exe`).
  Windows' own critical processes are ignored even if you add them, so you can't
  freeze your desktop by mistake.
- **Blocked sites** — domains (`youtube.com`); `www.` is added for you.
- **Always allowed sites** — your school portal etc. Never blocked, even if a
  parent domain is on the blocked list. Domains only: `app.edu-nation.app` works,
  `docs.google.com/slideshow` does not, because a hosts file has no idea about
  paths. Use the bare domain.

## Things worth knowing

- Website blocking works by pointing domains at `0.0.0.0` in
  `C:\Windows\System32\drivers\etc\hosts`, inside a marked block the app owns.
  It only rewrites its own block, and removes it on unlock or exit.
  If the app is killed hard while locked, run it again and press
  "Stop / unlock" to clean the entries up.
- **Why browsers get closed when a lock starts.** The hosts file only affects new
  DNS lookups. A tab that is already playing a blocked site has an open connection
  and buffered data, and the browser keeps its own DNS cache, so it can carry on for
  several minutes after the lock. Closing the browser is what makes the block bite
  immediately — that is the "Close browsers when locking" setting. With it off, a
  video that is already playing will keep playing for a while.
- This is a focus aid, not parental-control software. It doesn't defend itself:
  you can always close it or edit `data/config.json`. That's deliberate — the
  point is to make the distraction take effort, not to be unbeatable.
- All state lives in `data/config.json`. Settings from older versions are dropped
  automatically the next time it saves.

## Tests

```
.venv\Scripts\python.exe tests\test_focus_flow.py
```

Tests point `FOCUS_LOCKER_CONFIG` at a scratch file so they can never overwrite
real settings, and use a fake hosts file.
