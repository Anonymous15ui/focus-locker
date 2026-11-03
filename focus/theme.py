"""Look and feel: two palettes, ttk styling, and the custom widgets.

Tk gives you grey boxes and square corners. Everything here is about getting past
that without pulling in a UI toolkit: a dark and a light palette that can be
swapped at runtime, a pill button and a progress ring drawn on canvases, and a
small illustration that changes with what the app is doing.

Colours are module-level names that `set_mode` rebinds, so the rest of the app can
keep saying `theme.TEXT` and get whichever palette is current.
"""
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

PALETTES = {
    "dark": {
        "BG": "#0f1118", "SURFACE": "#171a24", "SURFACE_2": "#1f2330", "LINE": "#2a2f40",
        "TEXT": "#e9ebf3", "MUTED": "#878ea6", "DIM": "#5d6479",
        "FOCUS_C": "#8b7bff", "BREAK_C": "#3ddc97", "IDLE_C": "#5d6479",
        "DANGER": "#ff6b6b", "DONE_C": "#3ddc97",
        # the sky in the banner, top colour to bottom colour, per state
        "SKY": {"idle": ("#1b2340", "#3b3160"), "focus": ("#0d1030", "#241c4a"),
                "break": ("#17384f", "#2c6f7a")},
        "HILLS": ("#232a44", "#1a2036"),
        "STAR": "#f2f4ff",
    },
    "light": {
        "BG": "#f3f5fb", "SURFACE": "#ffffff", "SURFACE_2": "#e9edf6", "LINE": "#d5dbe8",
        "TEXT": "#1b1f2b", "MUTED": "#5b6376", "DIM": "#8c93a6",
        "FOCUS_C": "#6c5ce7", "BREAK_C": "#0faf74", "IDLE_C": "#9aa1b4",
        "DANGER": "#e03131", "DONE_C": "#0faf74",
        "SKY": {"idle": ("#bcd8f7", "#f6d5b8"), "focus": ("#8fa8e8", "#c9b6f0"),
                "break": ("#9fe0f5", "#d8f4e4")},
        "HILLS": ("#8fa4c8", "#6d82a8"),
        "STAR": "#fffdf2",
    },
}

# Accents for things that just want to be distinguishable and cheerful: habit
# dots, list bullets. They read on either palette.
ACCENTS = ["#8b7bff", "#22c3e6", "#f6a609", "#ff6b9a", "#3ddc97", "#ff9f5a", "#5bc0f8"]

UI = "Segoe UI"
MODE = "dark"


def set_mode(name):
    """Swap the palette. Rebinds the module-level colour names."""
    global MODE
    MODE = name if name in PALETTES else "dark"
    globals().update(PALETTES[MODE])
    return MODE


set_mode("dark")                        # module import leaves a usable palette


def other_mode():
    return "light" if MODE == "dark" else "dark"


def fonts():
    return {
        "display": (UI, 30, "bold"),
        "title": (UI, 15, "bold"),
        "body": (UI, 10),
        "small": (UI, 9),
        "list": (UI, 11),
        "mono": ("Consolas", 9),
    }


def mix(a, b, t):
    """Blend two #rrggbb colours, t=0 gives a, t=1 gives b."""
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(x + (y - x) * t) for x, y in zip(pa, pb))


def apply(root, mode=None):
    """Dress every ttk widget class the app uses in the current palette."""
    if mode:
        set_mode(mode)
    root.configure(bg=BG)
    style = ttk.Style(root)
    style.theme_use("clam")
    f = fonts()

    style.configure(".", background=BG, foreground=TEXT, fieldbackground=SURFACE_2,
                    bordercolor=LINE, lightcolor=SURFACE, darkcolor=SURFACE, font=f["body"])
    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=SURFACE)
    style.configure("TLabel", background=BG, foreground=TEXT)
    style.configure("Card.TLabel", background=SURFACE, foreground=TEXT)
    style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=f["small"])
    style.configure("Title.TLabel", background=BG, foreground=TEXT, font=f["title"])

    style.configure("TEntry", insertcolor=TEXT, padding=6,
                    fieldbackground=SURFACE_2, foreground=TEXT, borderwidth=0)
    style.map("TEntry", bordercolor=[("focus", FOCUS_C)], lightcolor=[("focus", FOCUS_C)])

    style.configure("TButton", background=SURFACE_2, foreground=TEXT, borderwidth=0,
                    padding=(12, 7), font=f["body"])
    style.map("TButton", background=[("active", LINE), ("disabled", SURFACE)],
              foreground=[("disabled", DIM)])

    style.configure("TCheckbutton", background=BG, foreground=TEXT, focuscolor=BG)
    style.map("TCheckbutton", background=[("active", BG)],
              indicatorcolor=[("selected", FOCUS_C), ("!selected", SURFACE_2)])

    style.configure("TCombobox", fieldbackground=SURFACE_2, background=SURFACE_2,
                    foreground=TEXT, arrowcolor=MUTED, borderwidth=0, padding=5)
    style.map("TCombobox", fieldbackground=[("readonly", SURFACE_2)],
              selectbackground=[("readonly", SURFACE_2)],
              selectforeground=[("readonly", TEXT)])
    root.option_add("*TCombobox*Listbox.background", SURFACE_2)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*TCombobox*Listbox.selectBackground", FOCUS_C)
    root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")

    style.configure("TNotebook", background=BG, borderwidth=0, tabmargins=(2, 6, 2, 0))
    style.configure("TNotebook.Tab", background=BG, foreground=MUTED, borderwidth=0,
                    padding=(14, 8), font=f["body"])
    style.map("TNotebook.Tab",
              background=[("selected", SURFACE)], foreground=[("selected", TEXT)],
              expand=[("selected", (0, 0, 0, 0))])

    style.configure("Bar.Horizontal.TProgressbar", background=FOCUS_C, troughcolor=SURFACE_2,
                    borderwidth=0, thickness=6)
    return style


def listbox(parent, **kw):
    """A tk.Listbox that does not look like 1996."""
    options = dict(
        bg=SURFACE, fg=TEXT, font=fonts()["list"], activestyle="none",
        selectbackground=SURFACE_2, selectforeground=TEXT,
        highlightthickness=0, borderwidth=0, relief="flat", takefocus=True,
    )
    options.update(kw)
    return tk.Listbox(parent, **options)


def text(parent, **kw):
    options = dict(bg=SURFACE, fg=MUTED, font=fonts()["mono"], highlightthickness=0,
                   borderwidth=0, relief="flat", insertbackground=TEXT, padx=10, pady=8)
    options.update(kw)
    return tk.Text(parent, **options)


class PillButton(tk.Canvas):
    """A rounded button, because ttk cannot round a corner."""

    def __init__(self, parent, text, command, kind="ghost", width=None, bg=None):
        self.palette = {
            "primary": (FOCUS_C, mix(FOCUS_C, "#ffffff", 0.2), "#ffffff"),
            "break": (BREAK_C, mix(BREAK_C, "#ffffff", 0.2), "#06281b"),
            "danger": (SURFACE_2, LINE, DANGER),
            "ghost": (SURFACE_2, LINE, TEXT),
        }[kind]
        f = tkfont.Font(font=fonts()["body"])
        # NOT self._w: Tkinter keeps the widget path name there
        self._px = width or f.measure(text) + 34
        super().__init__(parent, width=self._px, height=34, bg=bg or BG,
                         highlightthickness=0, borderwidth=0)
        self.command = command
        self._enabled = True
        self._shape = self._round_rect(1, 1, self._px - 1, 33, 17, fill=self.palette[0])
        self._label = self.create_text(self._px / 2, 17, text=text, fill=self.palette[2],
                                       font=fonts()["body"])
        self.bind("<Enter>", lambda _e: self._paint(1))
        self.bind("<Leave>", lambda _e: self._paint(0))
        self.bind("<Button-1>", self._press)
        self.bind("<ButtonRelease-1>", self._release)
        self.configure(cursor="hand2")

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        points = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
                  x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        return self.create_polygon(points, smooth=True, **kw)

    def _paint(self, hover):
        if self._enabled:
            self.itemconfig(self._shape, fill=self.palette[1 if hover else 0])

    def _press(self, _e):
        if self._enabled:
            self.move(self._label, 0, 1)

    def _release(self, _e):
        if not self._enabled:
            return
        self.move(self._label, 0, -1)
        self.command()

    def set_enabled(self, enabled):
        self._enabled = enabled
        # a disabled pill still has to look like a button, so it keeps a filled
        # shape rather than dissolving into the panel behind it
        self.itemconfig(self._shape, fill=self.palette[0] if enabled else SURFACE_2)
        self.itemconfig(self._label, fill=self.palette[2] if enabled else DIM)
        self.configure(cursor="hand2" if enabled else "arrow")

    def set_text(self, label):
        self.itemconfig(self._label, text=label)


class Ring(tk.Canvas):
    """The progress ring: a break counting down, or tasks ticked off.

    Its value eases toward the target a few times a second instead of jumping, which
    is the whole difference between a progress indicator and something satisfying.
    """

    SIZE = 132
    WIDTH = 11

    def __init__(self, parent, bg=None):
        super().__init__(parent, width=self.SIZE, height=self.SIZE, bg=bg or SURFACE,
                         highlightthickness=0, borderwidth=0)
        pad = self.WIDTH / 2 + 2
        box = (pad, pad, self.SIZE - pad, self.SIZE - pad)
        self._track = self.create_oval(*box, outline=SURFACE_2, width=self.WIDTH)
        self._arc = self.create_arc(*box, start=90, extent=-0.1, style="arc",
                                    outline=IDLE_C, width=self.WIDTH)
        self._big = self.create_text(self.SIZE / 2, self.SIZE / 2 - 7, text="",
                                     fill=TEXT, font=(UI, 22, "bold"))
        self._small = self.create_text(self.SIZE / 2, self.SIZE / 2 + 18, text="",
                                       fill=MUTED, font=(UI, 9))
        self._shown = 0.0
        self._target = 0.0
        self._pulse = 0
        self._animate()

    def set(self, fraction, big, small, color):
        self._target = max(0.0, min(1.0, float(fraction)))
        self.itemconfig(self._big, text=big)
        self.itemconfig(self._small, text=small)
        self.itemconfig(self._arc, outline=color)

    def pulse(self):
        """A quick thickening of the ring - used when a task gets ticked off."""
        self._pulse = 10

    def _animate(self):
        # a theme or language switch tears every widget down and rebuilds it, so the
        # loop has to notice when its own canvas has gone
        if not self.winfo_exists():
            return
        self._shown += (self._target - self._shown) * 0.25
        if abs(self._target - self._shown) < 0.001:
            self._shown = self._target
        extent = -359.999 * self._shown if self._shown >= 0.999 else -360 * self._shown
        self.itemconfig(self._arc, extent=extent if abs(extent) > 0.1 else -0.1)
        if self._pulse:
            self._pulse -= 1
            grow = self._pulse if self._pulse < 6 else 10 - self._pulse
            self.itemconfig(self._arc, width=self.WIDTH + grow)
        elif float(self.itemcget(self._arc, "width") or 0) != self.WIDTH:
            self.itemconfig(self._arc, width=self.WIDTH)
        self.after(40, self._animate)


class Scene(tk.Canvas):
    """A small landscape across the top that changes with the session.

    Drawn rather than bundled as images: a drawing recolours itself for the light
    and dark palettes and for each state, weighs nothing in the .exe, and comes
    with no licence attached. Night and stars while you are locked in, daylight
    on a break, sunrise when nothing is running.
    """

    HEIGHT = 104

    def __init__(self, parent, width=900):
        super().__init__(parent, height=self.HEIGHT, bg=BG,
                         highlightthickness=0, borderwidth=0)
        self._state = None
        self.bind("<Configure>", lambda _e: self.render(self._state, force=True))

    def render(self, state, force=False):
        if state == self._state and not force:
            return
        self._state = state or "idle"
        self.delete("all")
        w = max(self.winfo_width(), 10)
        h = self.HEIGHT
        top, bottom = SKY.get(self._state, SKY["idle"])

        # sky: a stack of thin bands, which is as close to a gradient as a canvas gets
        bands = 26
        for i in range(bands):
            self.create_rectangle(0, h * i / bands, w, h * (i + 1) / bands + 1,
                                  fill=mix(top, bottom, i / (bands - 1)), outline="")

        if self._state == "focus":
            for x, y, r in ((0.08, 0.3, 1.6), (0.17, 0.55, 1.1), (0.3, 0.22, 1.4),
                            (0.44, 0.45, 1.0), (0.57, 0.26, 1.5), (0.68, 0.6, 1.1),
                            (0.79, 0.33, 1.3), (0.9, 0.5, 1.0), (0.96, 0.2, 1.4)):
                cx, cy = w * x, h * y
                self.create_oval(cx - r, cy - r, cx + r, cy + r, fill=STAR, outline="")
            # crescent: a bright disc with a sky-coloured disc bitten out of it
            mx, my, mr = w * 0.86, h * 0.34, 15
            self.create_oval(mx - mr, my - mr, mx + mr, my + mr, fill=STAR, outline="")
            self.create_oval(mx - mr + 7, my - mr - 3, mx + mr + 7, my + mr - 3,
                             fill=mix(top, bottom, 0.3), outline="")
        else:
            # sun, low and warm for idle, high and bright on a break
            sx, sy = (w * 0.86, h * 0.62) if self._state == "idle" else (w * 0.84, h * 0.3)
            glow = "#ffd27a" if self._state == "idle" else "#fff1b8"
            for rr, tint in ((30, 0.18), (22, 0.4), (15, 1.0)):
                self.create_oval(sx - rr, sy - rr, sx + rr, sy + rr,
                                 fill=mix(mix(top, bottom, 0.4), glow, tint), outline="")
            if self._state == "break":
                for cx, cy, s in ((w * 0.2, h * 0.34, 1.0), (w * 0.52, h * 0.24, 0.7)):
                    cloud = mix(STAR, "#ffffff", 0.5)
                    for dx, dy, r in ((0, 0, 13), (14, 3, 10), (-14, 3, 9), (5, -7, 9)):
                        self.create_oval(cx + dx * s - r * s, cy + dy * s - r * s,
                                         cx + dx * s + r * s, cy + dy * s + r * s,
                                         fill=cloud, outline="")

        # two ridges of hills, far one paler, so the band has some depth
        far, near = HILLS
        self.create_polygon(0, h, 0, h * 0.72, w * 0.18, h * 0.46, w * 0.37, h * 0.7,
                            w * 0.55, h * 0.4, w * 0.75, h * 0.66, w, h * 0.5, w, h,
                            fill=far, outline="", smooth=True)
        self.create_polygon(0, h, 0, h * 0.86, w * 0.22, h * 0.66, w * 0.45, h * 0.88,
                            w * 0.68, h * 0.62, w * 0.88, h * 0.82, w, h * 0.74, w, h,
                            fill=near, outline="", smooth=True)
