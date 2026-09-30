"""Persistent settings / tasks / blocklists, stored as one JSON file."""
import json
import os
import threading

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(APP_DIR, "data")
# FOCUS_LOCKER_CONFIG lets tests point at a scratch file instead of real settings
CONFIG_PATH = os.environ.get("FOCUS_LOCKER_CONFIG") or os.path.join(DATA_DIR, "config.json")

DEFAULTS = {
    # --- breaks ---
    "break_after_each_task": True,
    "task_break_minutes": 5,
    "break_after_list_minutes": 15,
    "break_after_list_enabled": True,
    "warn_before_break_ends_seconds": 30,
    # --- how blocking behaves ---
    "block_mode": "suspend",          # "suspend" (freeze, nothing lost) or "close"
    "block_websites": True,
    "poll_seconds": 2,
    # A browser that is already showing a blocked page keeps it alive for minutes:
    # the hosts file only affects new DNS lookups, and the open connection plus the
    # browser's own DNS cache survive it. Closing browsers at lock time is what
    # makes the block actually bite the moment a break ends.
    "close_browsers_on_lock": True,
    "browser_processes": [
        "chrome.exe", "msedge.exe", "firefox.exe", "brave.exe",
        "opera.exe", "opera_gx.exe", "vivaldi.exe",
    ],
    # --- what gets locked ---
    "blocked_apps": [
        "chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe",
        "Discord.exe", "Steam.exe", "steamwebhelper.exe", "Spotify.exe",
        "WhatsApp.exe", "Telegram.exe",
    ],
    "blocked_sites": [
        "youtube.com", "www.youtube.com", "m.youtube.com",
        "tiktok.com", "instagram.com", "reddit.com", "x.com", "twitter.com",
        "facebook.com", "twitch.tv", "netflix.com",
    ],
    "allowed_sites": [],              # never written to hosts, even if listed above
    # --- tasks ---
    # [{"text": str, "done": bool, "link": str}] - link is optional and may be a
    # URL, a folder or a file: wherever the task actually gets done.
    "tasks": [],
}

_lock = threading.Lock()


def load():
    cfg = dict(DEFAULTS)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
            stored = json.load(fh)
    except (OSError, ValueError):
        stored = {}
    if isinstance(stored, dict):
        # Only keys we still know about: settings from older versions are dropped
        # rather than carried around forever.
        cfg.update({k: v for k, v in stored.items() if k in DEFAULTS})
    for key, default in DEFAULTS.items():
        if not isinstance(cfg.get(key), type(default)):
            cfg[key] = default
    cfg["tasks"] = [_clean_task(t) for t in cfg["tasks"] if isinstance(t, dict) and t.get("text")]
    return cfg


def _clean_task(task):
    """Fill in anything a task from an older version is missing."""
    return {
        "text": str(task.get("text", "")),
        "done": bool(task.get("done", False)),
        "link": str(task.get("link", "")),
    }


def save(cfg):
    os.makedirs(DATA_DIR, exist_ok=True)
    tmp = CONFIG_PATH + ".tmp"
    with _lock:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump({k: v for k, v in cfg.items() if k in DEFAULTS}, fh, indent=2)
        os.replace(tmp, CONFIG_PATH)
