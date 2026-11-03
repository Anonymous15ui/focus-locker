"""Dark theme: palette, ttk styling, and the two custom widgets the UI leans on.

Tk gives you grey boxes and square corners. Everything here is about getting past
that without pulling in a UI toolkit: ttk restyled for dark, plus a pill button and
a progress ring drawn on canvases, because Tk cannot round a corner by itself.
"""
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

# --- palette ---------------------------------------------------------------
BG = "#0f1118"          # window
SURFACE = "#171a24"     # panels
SURFACE_2 = "#1f2330"   # inputs, list rows
LINE = "#2a2f40"        # hairlines
TEXT = "#e9ebf3"
MUTED = "#878ea6"
DIM = "#5d6479"

FOCUS_C = "#8b7bff"     # locked in
BREAK_C = "#3ddc97"     # breathing
IDLE_C = "#5d6479"      # nothing running
DANGER = "#ff6b6b"
DONE_C = "#3ddc97"

UI = "Segoe UI"


def fonts():
    return {
        "display": (UI, 30, "bold"),
        "title": (UI, 15, "bold"),
        "body": (UI, 10),
        "small": (UI, 9),
        "list": (UI, 11),
        "mono": ("Consolas", 9),
    }


def apply(root):
    """Dark-mode every ttk widget class the app uses."""
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
    style.map("TEntry", fieldbackground=[("focus", SURFACE_2)],
              bordercolor=[("focus", FOCUS_C)], lightcolor=[("focus", FOCUS_C)])

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

    # Notebook: flat tabs, accent on the active one, no 3D anything
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
    f = fonts()
    options = dict(
        bg=SURFACE, fg=TEXT, font=f["list"], activestyle="none",
        selectbackground=SURFACE_2, selectforeground=TEXT,
        highlightthickness=0, borderwidth=0, relief="flat", takefocus=True,
    )
    options.update(kw)
    return tk.Listbox(parent, **options)


def text(parent, **kw):
    f = fonts()
    options = dict(bg=SURFACE, fg=MUTED, font=f["mono"], highlightthickness=0,
                   borderwidth=0, relief="flat", insertbackground=TEXT, padx=10, pady=8)
    options.update(kw)
    return tk.Text(parent, **options)


class PillButton(tk.Canvas):
    """A rounded button, because ttk cannot round a corner.

    Drawn as a rounded rectangle plus a label, with its own hover and press
    colours so it feels alive under the cursor.
    """

    def __init__(self, parent, text, command, kind="ghost", width=None, bg=BG):
        self.palette = {
            "primary": (FOCUS_C, "#9d90ff", "#ffffff"),
            "break": (BREAK_C, "#5ae7ab", "#06281b"),
            "danger": (SURFACE_2, LINE, DANGER),
            "ghost": (SURFACE_2, LINE, TEXT),
        }[kind]
        f = tkfont.Font(font=fonts()["body"])
        # NOT self._w: Tkinter keeps the widget path name there
        self._px = width or f.measure(text) + 34
        super().__init__(parent, width=self._px, height=34, bg=bg,
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
        if not self._enabled:
            return
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

    def __init__(self, parent, bg=SURFACE):
        super().__init__(parent, width=self.SIZE, height=self.SIZE, bg=bg,
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
        # a language switch tears every widget down and rebuilds it, so the loop
        # has to notice when its own canvas has gone
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
        elif float(self.itemcget(self._arc, "width") or 0) != self.WIDTH:   # Tk returns "11.0"
            self.itemconfig(self._arc, width=self.WIDTH)
        self.after(40, self._animate)
