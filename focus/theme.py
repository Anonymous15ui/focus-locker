"""Look and feel: colour schemes, ttk styling, and the custom widgets.

Tk gives you grey boxes, square corners and text-only lists. Everything here is
about getting past that without pulling in a UI toolkit:

* a set of schemes that can be swapped at runtime - `set_mode` rebinds the
  module-level colour names, so the rest of the app keeps saying `theme.TEXT`
  and gets whichever scheme is current
* pill buttons and a progress ring drawn on canvases
* `RowList`, a list whose rows are drawn rather than typed, which is the only way
  to get a coloured checkbox, arrow and dots on one line - a Listbox can colour a
  whole row and nothing finer
* `Scene`, the sky across the top, where one eased number slides the sun down and
  the moon up as a session starts
"""
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk


def _scheme(bg, surface, surface_2, line, text, muted, dim, focus, brk, sky,
            hills, star, accents, danger="#ff6b6b"):
    """One colour scheme. Everything the app paints comes from here."""
    return {
        "BG": bg, "SURFACE": surface, "SURFACE_2": surface_2, "LINE": line,
        "TEXT": text, "MUTED": muted, "DIM": dim,
        "FOCUS_C": focus, "BREAK_C": brk, "IDLE_C": dim,
        "DANGER": danger, "DONE_C": brk,
        "SKY": sky, "HILLS": hills, "STAR": star, "ACCENTS": accents,
    }


# Each sky is (break, idle, focus): bright daylight, sunrise, night. The scene
# slides between them, so they want to be in that order of darkness.
SCHEMES = {
    "dark": _scheme(
        "#0f1118", "#171a24", "#1f2330", "#2a2f40", "#e9ebf3", "#878ea6", "#5d6479",
        "#8b7bff", "#3ddc97",
        {"break": ("#17384f", "#2c6f7a"), "idle": ("#1b2340", "#3b3160"),
         "focus": ("#0d1030", "#241c4a")},
        ("#232a44", "#1a2036"), "#f2f4ff",
        ["#8b7bff", "#22c3e6", "#f6a609", "#ff6b9a", "#3ddc97", "#ff9f5a", "#5bc0f8"]),
    "light": _scheme(
        "#f3f5fb", "#ffffff", "#e9edf6", "#d5dbe8", "#1b1f2b", "#5b6376", "#8c93a6",
        "#6c5ce7", "#0faf74",
        {"break": ("#9fe0f5", "#d8f4e4"), "idle": ("#bcd8f7", "#f6d5b8"),
         "focus": ("#8fa8e8", "#c9b6f0")},
        ("#8fa4c8", "#6d82a8"), "#fffdf2",
        ["#6c5ce7", "#0d9bbd", "#d98300", "#e0558c", "#0faf74", "#e07a3f", "#2f8fd0"],
        danger="#e03131"),
    "rose": _scheme(
        "#1a0f17", "#261522", "#331d2d", "#45283c", "#fbeaf3", "#c08fa8", "#8c6378",
        "#ff6b9a", "#ffb37a",
        {"break": ("#5d2340", "#b5607e"), "idle": ("#3a1430", "#8d3a5c"),
         "focus": ("#1d0a18", "#4a1733")},
        ("#3b1a2e", "#2a1121"), "#ffe9f3",
        ["#ff6b9a", "#ffb37a", "#c77dff", "#ff8fab", "#7ae0c3", "#ffd166", "#f06595"]),
    "ocean": _scheme(
        "#07131f", "#0d2032", "#132c42", "#1d3f58", "#e3f2fb", "#7fa6bf", "#55788f",
        "#2ec5d3", "#4dd98f",
        {"break": ("#0d4f66", "#36b3c4"), "idle": ("#0a3350", "#1f7f9c"),
         "focus": ("#04101d", "#0d3450")},
        ("#10293d", "#0a1c2c"), "#eaf8ff",
        ["#2ec5d3", "#4dd98f", "#ffd166", "#6aa9ff", "#ff8fa3", "#9ad6e8", "#f6a609"]),
    "forest": _scheme(
        "#0c1510", "#14211a", "#1b2d23", "#27402f", "#e8f3e9", "#8fae97", "#5f7d69",
        "#6cc47f", "#e2b253",
        {"break": ("#2c6b4a", "#8fd0a0"), "idle": ("#1d4a36", "#79a05c"),
         "focus": ("#071009", "#163222")},
        ("#1a3326", "#11221a"), "#f2ffe9",
        ["#6cc47f", "#e2b253", "#a0d468", "#4fb0a5", "#ffd97d", "#c3e88d", "#79a05c"]),
    "sunset": _scheme(
        "#1b1016", "#271822", "#35212c", "#48303c", "#ffeee6", "#c99a8c", "#8f6a60",
        "#ff8364", "#ffc95c",
        {"break": ("#f08a5d", "#ffd98e"), "idle": ("#7d3b55", "#ff8f5e"),
         "focus": ("#1a0d1c", "#4a2240")},
        ("#3b2130", "#281622"), "#fff3e2",
        ["#ff8364", "#ffc95c", "#f06292", "#b388ff", "#4dd0c0", "#ffab73", "#ff7070"]),
    "calm": _scheme(
        "#f5f2ec", "#fffdf9", "#ebe5da", "#dcd4c6", "#2c2a26", "#6b6459", "#948c7f",
        "#8a7a5e", "#6f9c7a",
        {"break": ("#cfe3d4", "#f2efe4"), "idle": ("#e4d7c3", "#f6e9d8"),
         "focus": ("#b4b9c9", "#d7cdd9")},
        ("#b6ac97", "#948a76"), "#fffdf0",
        ["#8a7a5e", "#6f9c7a", "#c08457", "#9c7a8a", "#5f8aa0", "#c9a227", "#a0785a"],
        danger="#c0392b"),
    "sky": _scheme(
        "#eef5fd", "#ffffff", "#e0ebf8", "#c9dcf0", "#15283c", "#51708e", "#8099b3",
        "#2f7fd0", "#17a98a",
        {"break": ("#8fd4f7", "#d9f1ff"), "idle": ("#aacdf0", "#ffe3c4"),
         "focus": ("#5f8ac4", "#a9bfe4")},
        ("#8fa9c9", "#6b87ab"), "#ffffff",
        ["#2f7fd0", "#17a98a", "#e08a1e", "#d4557f", "#7a5cd0", "#38b6e0", "#f2a93b"],
        danger="#d64545"),
    "grape": _scheme(
        "#140f1f", "#1f1830", "#2a2040", "#3a2d57", "#f0eafc", "#a492c6", "#776796",
        "#b388ff", "#5ee0b0",
        {"break": ("#3e2a6b", "#8f6fd4"), "idle": ("#2a1b4a", "#6d4aa8"),
         "focus": ("#0d0818", "#2a1550")},
        ("#2b2145", "#1d1631"), "#f6f0ff",
        ["#b388ff", "#5ee0b0", "#ffd166", "#ff8fab", "#6aa9ff", "#e0aaff", "#ffa94d"]),
}

UI = "Segoe UI"
MODE = "dark"


def set_mode(name):
    """Swap the scheme. Rebinds the module-level colour names."""
    global MODE
    MODE = name if name in SCHEMES else "dark"
    globals().update(SCHEMES[MODE])
    return MODE


set_mode("dark")                        # import leaves a usable palette


def is_light():
    """Pale schemes need darker shadows and lighter ticks than dark ones."""
    return int(BG[1:3], 16) > 0x80


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
    """Blend two #rrggbb colours: t=0 gives a, t=1 gives b."""
    t = max(0.0, min(1.0, t))
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(x + (y - x) * t) for x, y in zip(pa, pb))


def apply(root, mode=None):
    """Dress every ttk widget class the app uses in the current scheme."""
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
    # clam draws a scrollbar out of several colours; miss one and a white bar
    # appears in the middle of a dark scheme
    style.configure("Scheme.Vertical.TScrollbar", background=SURFACE_2, troughcolor=SURFACE,
                    bordercolor=SURFACE, arrowcolor=MUTED, darkcolor=SURFACE_2,
                    lightcolor=SURFACE_2, borderwidth=0, arrowsize=12)
    style.map("Scheme.Vertical.TScrollbar", background=[("active", LINE)])
    return style


def listbox(parent, **kw):
    """A plain tk.Listbox in scheme colours - used where rows are just text."""
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


# --- little drawings, shared by the widgets below --------------------------
def round_rect(canvas, x1, y1, x2, y2, r, **kw):
    points = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
              x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
    return canvas.create_polygon(points, smooth=True, **kw)


def star_points(cx, cy, outer, inner=None, points=5):
    """A real five-pointed star, not an asterisk."""
    import math
    inner = inner or outer * 0.45
    out = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = -math.pi / 2 + i * math.pi / points
        out += [cx + r * math.cos(a), cy + r * math.sin(a)]
    return out


def arrow_points(x, y, size, rtl=False):
    """A chevron pointing at whatever comes next, in reading direction."""
    d = -1 if rtl else 1
    return [x, y - size, x + size * d, y, x, y + size]


class PillButton(tk.Canvas):
    """A rounded button, because ttk cannot round a corner."""

    def __init__(self, parent, text, command, kind="ghost", width=None, bg=None):
        self.palette = {
            "primary": (FOCUS_C, mix(FOCUS_C, "#ffffff", 0.22), "#ffffff"),
            "break": (BREAK_C, mix(BREAK_C, "#ffffff", 0.22),
                      "#0b2a1e" if not is_light() else "#07301f"),
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
        self._shape = round_rect(self, 1, 1, self._px - 1, 33, 17, fill=self.palette[0])
        self._label = self.create_text(self._px / 2, 17, text=text, fill=self.palette[2],
                                       font=fonts()["body"])
        self.bind("<Enter>", lambda _e: self._paint(1))
        self.bind("<Leave>", lambda _e: self._paint(0))
        self.bind("<Button-1>", self._press)
        self.bind("<ButtonRelease-1>", self._release)
        self.configure(cursor="hand2")

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
    """The progress ring: a break counting down, or tasks ticked off."""

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
        self._pulse = 10

    def _animate(self):
        # a scheme or language switch tears every widget down, so the loop has to
        # notice when its own canvas has gone
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


class RowList(tk.Frame):
    """A list whose rows are drawn: coloured checkbox, arrow, dots, stars.

    A Listbox can colour a whole row and nothing finer, so anything with more than
    one colour on a line has to be drawn. Rows are dicts:

        checked  bool    draws a filled box with a tick, or an empty outline
        text     str     the task or habit name
        trail    str     shown after a chevron, e.g. a task's link
        dots     [bool]  the last few days of a habit
        note     str     trailing label, e.g. a streak
        star     bool    a real five-pointed star beside the note
        accent   colour  this row's colour
    """

    ROW_H = 34
    BOX = 18

    def __init__(self, parent, on_toggle=None, on_activate=None, rtl=False):
        super().__init__(parent, bg=SURFACE, highlightthickness=0, bd=0)
        self.on_toggle = on_toggle
        self.on_activate = on_activate
        self.rtl = rtl
        self.rows = []
        self._selected = None
        self.canvas = tk.Canvas(self, bg=SURFACE, highlightthickness=0, bd=0)
        self.bar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview,
                                 style="Scheme.Vertical.TScrollbar")
        self.canvas.configure(yscrollcommand=self.bar.set)
        self.bar.pack(side="left" if rtl else "right", fill="y")
        self.canvas.pack(side="right" if rtl else "left", fill="both", expand=True)
        self.canvas.bind("<Button-1>", self._click)
        self.canvas.bind("<Double-Button-1>", self._double)
        self.canvas.bind("<Configure>", lambda _e: self.redraw())
        self.canvas.bind("<MouseWheel>", self._wheel)

    # -- data ---------------------------------------------------------------
    def set_rows(self, rows):
        self.rows = rows
        if self._selected is not None and self._selected >= len(rows):
            self._selected = None
        self.redraw()

    def selected(self):
        return self._selected

    def select(self, index):
        self._selected = index if index is not None and 0 <= index < len(self.rows) else None
        self.redraw()

    # -- input --------------------------------------------------------------
    def _row_at(self, event):
        y = self.canvas.canvasy(event.y)
        index = int(y // self.ROW_H)
        return index if 0 <= index < len(self.rows) else None

    def _click(self, event):
        index = self._row_at(event)
        if index is None:
            return
        self._selected = index
        x = self.canvas.canvasx(event.x)
        box_side = self.canvas.winfo_width() - 14 - self.BOX if self.rtl else 14
        if box_side - 4 <= x <= box_side + self.BOX + 4 and self.on_toggle:
            self.on_toggle(index)        # hitting the box toggles straight away
            return
        self.redraw()

    def _double(self, event):
        index = self._row_at(event)
        if index is not None and self.on_activate:
            self.on_activate(index)

    def _wheel(self, event):
        if len(self.rows) * self.ROW_H > self.canvas.winfo_height():
            self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    # -- drawing ------------------------------------------------------------
    def redraw(self):
        c = self.canvas
        c.delete("all")
        width = max(c.winfo_width(), 60)
        f = fonts()
        tick = "#ffffff" if not is_light() else "#ffffff"

        for i, row in enumerate(self.rows):
            top = i * self.ROW_H
            mid = top + self.ROW_H / 2
            accent = row.get("accent", FOCUS_C)
            checked = row.get("checked", False)

            if i == self._selected:
                round_rect(c, 3, top + 2, width - 3, top + self.ROW_H - 2, 9,
                           fill=SURFACE_2, outline="")

            # checkbox: filled and ticked, or an empty rounded outline
            bx = width - 14 - self.BOX if self.rtl else 14
            round_rect(c, bx, mid - self.BOX / 2, bx + self.BOX, mid + self.BOX / 2, 5,
                       fill=accent if checked else SURFACE,
                       outline=accent if checked else LINE, width=2)
            if checked:
                c.create_line(bx + 4, mid, bx + 7.5, mid + 4, bx + 14, mid - 4.5,
                              fill=tick, width=2.4, capstyle="round", joinstyle="round")

            # name
            tx = bx - 12 if self.rtl else bx + self.BOX + 12
            c.create_text(tx, mid, text=row.get("text", ""), font=f["list"],
                          fill=DIM if checked else TEXT,
                          anchor="e" if self.rtl else "w")
            step = -1 if self.rtl else 1
            used = tkfont.Font(font=f["list"]).measure(row.get("text", ""))
            cursor = tx + step * (used + 16)

            # link, behind a chevron pointing the way you read
            if row.get("trail"):
                c.create_polygon(arrow_points(cursor, mid, 5, self.rtl),
                                 fill=accent, outline="")
                cursor += step * 12
                c.create_text(cursor, mid, text=row["trail"], font=f["small"],
                              fill=MUTED, anchor="e" if self.rtl else "w")
                cursor += step * (tkfont.Font(font=f["small"]).measure(row["trail"]) + 16)

            # one dot per day, filled for the days it was done
            for done in (row.get("dots") or []):
                r = 4.5
                c.create_oval(cursor - r, mid - r, cursor + r, mid + r,
                              fill=accent if done else SURFACE,
                              outline=accent if done else LINE, width=1.6)
                cursor += step * 13
            if row.get("dots"):
                cursor += step * 6

            if row.get("star"):
                c.create_polygon(star_points(cursor + step * 7, mid, 8),
                                 fill=ACCENTS[2], outline="")
                cursor += step * 22

            if row.get("note"):
                c.create_text(cursor, mid, text=row["note"], font=f["small"],
                              fill=accent if checked else MUTED,
                              anchor="e" if self.rtl else "w")

        content = len(self.rows) * self.ROW_H
        c.configure(scrollregion=(0, 0, width, max(content, c.winfo_height())))
        # a scrollbar for four tasks is just clutter
        if content > c.winfo_height():
            if not self.bar.winfo_ismapped():
                self.bar.pack(side="left" if self.rtl else "right", fill="y")
        elif self.bar.winfo_ismapped():
            self.bar.pack_forget()


class Scene(tk.Canvas):
    """The sky across the top, with the sun and moon on one slider.

    A single eased number runs from 0 (bright daylight, a break) through sunrise
    (nothing running) to 1 (night, locked in). The sun sinks below the hills as
    the moon climbs, the sky colours cross-fade, and the stars come out, so
    starting a session reads as dusk falling rather than a repaint.
    """

    HEIGHT = 104
    PHASE = {"break": 0.0, "idle": 0.45, "focus": 1.0}
    STARS = ((0.08, 0.3, 1.6), (0.17, 0.55, 1.1), (0.3, 0.22, 1.4), (0.44, 0.45, 1.0),
             (0.57, 0.26, 1.5), (0.68, 0.6, 1.1), (0.79, 0.33, 1.3), (0.9, 0.5, 1.0),
             (0.96, 0.2, 1.4))
    BANDS = 24

    def __init__(self, parent, bg=None):
        super().__init__(parent, height=self.HEIGHT, bg=bg or BG,
                         highlightthickness=0, borderwidth=0)
        self._state = "idle"
        self.phase = self.PHASE["idle"]
        self.target = self.phase
        self.bind("<Configure>", lambda _e: self._draw())
        self._animate()

    def render(self, state, force=False):
        state = state if state in self.PHASE else "idle"
        if state != self._state or force:
            self._state = state
            self.target = self.PHASE[state]

    def _sky(self, phase):
        """Cross-fade break -> idle -> focus as the phase climbs."""
        a, b = SKY["break"], SKY["idle"]
        t = phase / self.PHASE["idle"]
        if phase > self.PHASE["idle"]:
            a, b = SKY["idle"], SKY["focus"]
            t = (phase - self.PHASE["idle"]) / (1 - self.PHASE["idle"])
        return mix(a[0], b[0], t), mix(a[1], b[1], t)

    def _animate(self):
        if not self.winfo_exists():
            return
        if abs(self.target - self.phase) > 0.001:
            self.phase += (self.target - self.phase) * 0.06   # the slide
            self._draw()
        self.after(40, self._animate)

    def _draw(self):
        self.delete("all")
        w = max(self.winfo_width(), 10)
        h = self.HEIGHT
        p = self.phase
        top, bottom = self._sky(p)

        for i in range(self.BANDS):
            self.create_rectangle(0, h * i / self.BANDS, w, h * (i + 1) / self.BANDS + 1,
                                  fill=mix(top, bottom, i / (self.BANDS - 1)), outline="")

        # stars fade in over the second half of the slide
        star_t = max(0.0, (p - 0.5) * 2)
        if star_t > 0.02:
            for x, y, r in self.STARS:
                cx, cy = w * x, h * y
                self.create_oval(cx - r, cy - r, cx + r, cy + r,
                                 fill=mix(mix(top, bottom, y), STAR, star_t), outline="")

        # sun: high at break, low at sunrise, well under the hills at night
        sun_y = h * (0.26 + p * 1.1)
        sun_x = w * (0.84 + p * 0.1)
        if sun_y < h * 1.1:
            glow = mix("#fff1b8", "#ffb570", min(1.0, p * 1.8))
            for rr, tint in ((30, 0.18), (22, 0.42), (15, 1.0)):
                self.create_oval(sun_x - rr, sun_y - rr, sun_x + rr, sun_y + rr,
                                 fill=mix(mix(top, bottom, 0.5), glow, tint), outline="")

        # moon rises as the sun sets, trailing in from the far side
        moon_y = h * (1.5 - p * 1.16)
        moon_x = w * (1.0 - p * 0.14)
        if moon_y < h * 1.1:
            mr = 15
            self.create_oval(moon_x - mr, moon_y - mr, moon_x + mr, moon_y + mr,
                             fill=STAR, outline="")
            self.create_oval(moon_x - mr + 7, moon_y - mr - 3, moon_x + mr + 7,
                             moon_y + mr - 3, fill=mix(top, bottom, moon_y / h),
                             outline="")

        # clouds only in daylight, fading as dusk comes on
        cloud_t = max(0.0, 1 - p * 2.2)
        if cloud_t > 0.02:
            cloud = mix(mix(top, bottom, 0.3), "#ffffff", 0.55 * cloud_t)
            for cx, cy, s in ((w * 0.2, h * 0.34, 1.0), (w * 0.52, h * 0.24, 0.7)):
                for dx, dy, r in ((0, 0, 13), (14, 3, 10), (-14, 3, 9), (5, -7, 9)):
                    self.create_oval(cx + dx * s - r * s, cy + dy * s - r * s,
                                     cx + dx * s + r * s, cy + dy * s + r * s,
                                     fill=cloud, outline="")

        far, near = HILLS
        self.create_polygon(0, h, 0, h * 0.72, w * 0.18, h * 0.46, w * 0.37, h * 0.7,
                            w * 0.55, h * 0.4, w * 0.75, h * 0.66, w, h * 0.5, w, h,
                            fill=far, outline="", smooth=True)
        self.create_polygon(0, h, 0, h * 0.86, w * 0.22, h * 0.66, w * 0.45, h * 0.88,
                            w * 0.68, h * 0.62, w * 0.88, h * 0.82, w, h * 0.74, w, h,
                            fill=near, outline="", smooth=True)
