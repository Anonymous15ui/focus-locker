"""Tkinter front end for the focus locker."""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from . import habits, i18n, theme
from .controller import BREAK, FOCUS, IDLE, Controller
from .i18n import t

PAD = {"padx": 8, "pady": 6}
MODES = ["suspend", "close"]
# the controller's break reasons, as keys into i18n
REASONS = {"task finished": "reason_task", "list finished": "reason_list",
           "manual break": "reason_manual"}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("860x620")
        self.minsize(720, 560)
        self._log_lines = []                  # kept so a language switch doesn't wipe the log
        self._pending_log = []                # filled from any thread, drained on the main one
        self._break_total = None              # full length of the running break, for the ring
        self.ctl = Controller(log=self.log)
        i18n.set_language(self.ctl.cfg["language"])
        self._habit_day = habits.today()
        theme.apply(self, self.ctl.cfg["theme"])

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(1000, self._tick)
        if not self.ctl.admin():
            self.log(t("not_admin"))

    # -- layout -------------------------------------------------------------
    def _build_ui(self, tab=0):
        """Build every widget in the current language. Called again on a language switch."""
        rtl = i18n.is_rtl()
        # "near" is where a line of text starts, "far" where it ends
        self.near, self.far = ("right", "left") if rtl else ("left", "right")
        self.anchor = "e" if rtl else "w"
        self.justify = "right" if rtl else "left"
        self.title(t("title"))

        self.scene = theme.Scene(self)
        self.scene.pack(fill="x", side="top")
        self._build_hero()
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=14, pady=(4, 12))
        self._build_tasks(self.nb)
        self._build_habits(self.nb)
        self._build_list_tab(self.nb, t("tab_blocked_apps"), "blocked_apps",
                             t("hint_blocked_apps"))
        self._build_list_tab(self.nb, t("tab_blocked_sites"), "blocked_sites",
                             t("hint_blocked_sites"))
        self._build_list_tab(self.nb, t("tab_allowed_sites"), "allowed_sites",
                             t("hint_allowed_sites"))
        self._build_settings(self.nb)
        self._build_log(self.nb)
        self.nb.select(tab)

        self.refresh_tasks()
        self.refresh_habits()

    def _build_hero(self):
        """The panel that tells you, at a glance, what the app is doing to you."""
        card = ttk.Frame(self, style="Card.TFrame")
        card.pack(fill="x", padx=14, pady=(14, 8))

        self.ring = theme.Ring(card)
        self.ring.pack(side=self.near, padx=18, pady=16)

        buttons = ttk.Frame(card, style="Card.TFrame")
        buttons.pack(side=self.far, padx=18)
        self.start_btn = theme.PillButton(buttons, t("start"), self.on_start,
                                          kind="primary", bg=theme.SURFACE)
        self.start_btn.pack(pady=3)
        theme.PillButton(buttons, t("break_now"), self.on_break_now,
                         kind="break", bg=theme.SURFACE).pack(pady=3)
        theme.PillButton(buttons, t("stop"), self.on_stop,
                         kind="danger", bg=theme.SURFACE).pack(pady=3)
        # one click walks to the next scheme; the full list lives in Settings
        theme.PillButton(buttons, self._next_scheme().title(), self.on_next_scheme,
                         kind="ghost", bg=theme.SURFACE).pack(pady=3)

        middle = ttk.Frame(card, style="Card.TFrame")
        middle.pack(side=self.near, fill="both", expand=True, pady=16)
        # These three labels all shrink as the state changes ("Locked in" -> "Breathe").
        # A label that resizes leaves the tail of the old text painted on the panel
        # behind it, so each one spans the full width instead and lets `anchor` place
        # the text. Filling beats a fixed width, which would clip a longer language.
        self.headline = ttk.Label(middle, style="Card.TLabel", anchor=self.anchor,
                                  font=theme.fonts()["display"], justify=self.justify)
        self.headline.pack(fill="x")
        self.status = ttk.Label(middle, style="Card.TLabel", foreground=theme.MUTED,
                                anchor=self.anchor, justify=self.justify)
        self.status.pack(fill="x", pady=(2, 10))
        self.progress = ttk.Progressbar(middle, style="Bar.Horizontal.TProgressbar",
                                        length=260, maximum=100)
        self.progress.pack(anchor=self.anchor)
        self.progress_label = ttk.Label(middle, style="Card.TLabel", foreground=theme.DIM,
                                        anchor=self.anchor, font=theme.fonts()["small"],
                                        justify=self.justify)
        self.progress_label.pack(fill="x", pady=(4, 0))

    def _build_tasks(self, nb):
        frame = ttk.Frame(nb)
        nb.add(frame, text=t("tab_todo"))
        entry_row = ttk.Frame(frame)
        entry_row.pack(fill="x", **PAD)
        ttk.Label(entry_row, text=t("task")).pack(side=self.near)
        self.task_entry = ttk.Entry(entry_row, justify=self.justify)
        self.task_entry.pack(side=self.near, fill="x", expand=True, padx=(6, 12))
        self.task_entry.bind("<Return>", lambda _e: self.on_add_task())
        ttk.Label(entry_row, text=t("link_optional")).pack(side=self.near)
        self.link_entry = ttk.Entry(entry_row, width=24)
        self.link_entry.pack(side=self.near, padx=6)
        self.link_entry.bind("<Return>", lambda _e: self.on_add_task())
        theme.PillButton(entry_row, t("add"), self.on_add_task,
                         kind="primary").pack(side=self.near, padx=6)
        ttk.Label(frame, text=t("link_hint"), style="Muted.TLabel",
                  justify=self.justify).pack(anchor=self.anchor, padx=8)

        # the action row is packed first, against the bottom, so a long task list
        # can never push it off the window
        row = ttk.Frame(frame)
        row.pack(side="bottom", fill="x", **PAD)
        self.task_list = theme.RowList(frame, on_toggle=self.on_row_toggle,
                                       on_activate=self.on_row_toggle, rtl=i18n.is_rtl())
        self.task_list.pack(fill="both", expand=True, **PAD)

        theme.PillButton(row, t("mark_done"), self.on_complete,
                         kind="break").pack(side=self.near)
        ttk.Button(row, text=t("open_link"), command=self.on_open_link).pack(side=self.near, padx=6)
        ttk.Button(row, text=t("edit_link"), command=self.on_edit_link).pack(side=self.near)
        ttk.Button(row, text=t("undo_done"), command=self.on_uncomplete).pack(side=self.near, padx=6)
        ttk.Button(row, text=t("delete"), command=self.on_delete_task).pack(side=self.near)

    def _build_habits(self, nb):
        frame = ttk.Frame(nb)
        nb.add(frame, text=t("tab_habits"))
        entry_row = ttk.Frame(frame)
        entry_row.pack(fill="x", **PAD)
        ttk.Label(entry_row, text=t("habit")).pack(side=self.near)
        self.habit_entry = ttk.Entry(entry_row, justify=self.justify)
        self.habit_entry.pack(side=self.near, fill="x", expand=True, padx=6)
        self.habit_entry.bind("<Return>", lambda _e: self.on_add_habit())
        theme.PillButton(entry_row, t("add"), self.on_add_habit,
                         kind="primary").pack(side=self.near, padx=6)
        ttk.Label(frame, text=t("habit_hint"), style="Muted.TLabel",
                  justify=self.justify).pack(anchor=self.anchor, padx=8)

        row = ttk.Frame(frame)
        row.pack(side="bottom", fill="x", **PAD)
        self.habit_list = theme.RowList(frame, on_toggle=self.on_habit_row_toggle,
                                        on_activate=self.on_habit_row_toggle,
                                        rtl=i18n.is_rtl())
        self.habit_list.pack(fill="both", expand=True, **PAD)

        theme.PillButton(row, t("habit_toggle"), self.on_toggle_habit,
                         kind="break").pack(side=self.near)
        ttk.Button(row, text=t("delete"), command=self.on_delete_habit).pack(side=self.near, padx=6)

    def _build_list_tab(self, nb, title, key, hint):
        frame = ttk.Frame(nb)
        nb.add(frame, text=title)
        ttk.Label(frame, text=hint, style="Muted.TLabel").pack(anchor=self.anchor, **PAD)
        listbox = theme.listbox(frame, font=theme.fonts()["mono"])
        listbox.pack(fill="both", expand=True, **PAD)
        row = ttk.Frame(frame)
        row.pack(fill="x", **PAD)
        entry = ttk.Entry(row)
        entry.pack(side=self.near, fill="x", expand=True)

        def refill():
            listbox.delete(0, "end")
            for item in self.ctl.cfg[key]:
                listbox.insert("end", "  " + item)

        def add(_e=None):
            value = entry.get().strip()
            if value and value not in self.ctl.cfg[key]:
                self.ctl.cfg[key].append(value)
                self.ctl.save()
                refill()
            entry.delete(0, "end")

        def remove():
            sel = listbox.curselection()
            if sel:
                self.ctl.cfg[key].pop(sel[0])
                self.ctl.save()
                refill()

        entry.bind("<Return>", add)
        theme.PillButton(row, t("add"), add, kind="primary").pack(side=self.near, padx=6)
        ttk.Button(row, text=t("remove_selected"), command=remove).pack(side=self.near)
        refill()

    def _build_settings(self, nb):
        frame = ttk.Frame(nb)
        nb.add(frame, text=t("tab_settings"))
        cfg = self.ctl.cfg
        self.v_lang = tk.StringVar(value=i18n.LANGUAGES[i18n.current()])
        self.v_each = tk.BooleanVar(value=cfg["break_after_each_task"])
        self.v_task_min = tk.StringVar(value=str(cfg["task_break_minutes"]))
        self.v_list_on = tk.BooleanVar(value=cfg["break_after_list_enabled"])
        self.v_list_min = tk.StringVar(value=str(cfg["break_after_list_minutes"]))
        self.mode_names = [t("mode_" + m) for m in MODES]
        mode = cfg["block_mode"] if cfg["block_mode"] in MODES else MODES[0]
        self.v_mode = tk.StringVar(value=self.mode_names[MODES.index(mode)])
        self.v_sites = tk.BooleanVar(value=cfg["block_websites"])
        self.v_close_browsers = tk.BooleanVar(value=cfg["close_browsers_on_lock"])
        self.v_poll = tk.StringVar(value=str(cfg["poll_seconds"]))

        # labels sit on the reading-start side, their inputs after them
        lab, inp = (1, 0) if i18n.is_rtl() else (0, 1)
        whole = {"column": 0, "columnspan": 2, "sticky": self.anchor}
        r = 0
        ttk.Label(frame, text=t("language")).grid(row=r, column=lab, sticky=self.anchor, **PAD)
        lang_box = ttk.Combobox(frame, textvariable=self.v_lang, width=24, state="readonly",
                                values=list(i18n.LANGUAGES.values()))
        lang_box.grid(row=r, column=inp, sticky=self.anchor, **PAD)
        lang_box.bind("<<ComboboxSelected>>", self.on_language)
        r += 1
        self.v_scheme = tk.StringVar(value=theme.MODE)
        ttk.Label(frame, text=t("scheme")).grid(row=r, column=lab, sticky=self.anchor, **PAD)
        scheme_box = ttk.Combobox(frame, textvariable=self.v_scheme, width=24, state="readonly",
                                  values=list(theme.SCHEMES))
        scheme_box.grid(row=r, column=inp, sticky=self.anchor, **PAD)
        scheme_box.bind("<<ComboboxSelected>>", self.on_pick_scheme)
        r += 1
        ttk.Checkbutton(frame, text=t("set_each"), variable=self.v_each).grid(row=r, **whole, **PAD)
        r += 1
        ttk.Label(frame, text=t("set_each_min")).grid(row=r, column=lab, sticky=self.anchor, **PAD)
        ttk.Entry(frame, textvariable=self.v_task_min, width=8).grid(row=r, column=inp,
                                                                    sticky=self.anchor, **PAD)
        r += 1
        ttk.Checkbutton(frame, text=t("set_list_on"), variable=self.v_list_on).grid(row=r, **whole,
                                                                                    **PAD)
        r += 1
        ttk.Label(frame, text=t("set_list_min")).grid(row=r, column=lab, sticky=self.anchor, **PAD)
        ttk.Entry(frame, textvariable=self.v_list_min, width=8).grid(row=r, column=inp,
                                                                     sticky=self.anchor, **PAD)
        r += 1
        ttk.Label(frame, text=t("set_mode")).grid(row=r, column=lab, sticky=self.anchor, **PAD)
        ttk.Combobox(frame, textvariable=self.v_mode, width=24, state="readonly",
                     values=self.mode_names).grid(row=r, column=inp, sticky=self.anchor, **PAD)
        r += 1
        ttk.Label(frame, text=t("mode_hint"), style="Muted.TLabel",
                  justify=self.justify).grid(row=r, **whole, **PAD)
        r += 1
        ttk.Checkbutton(frame, text=t("set_sites"), variable=self.v_sites).grid(row=r, **whole, **PAD)
        r += 1
        ttk.Checkbutton(frame, text=t("set_close_browsers"),
                        variable=self.v_close_browsers).grid(row=r, **whole, **PAD)
        r += 1
        ttk.Label(frame, text=t("set_poll")).grid(row=r, column=lab, sticky=self.anchor, **PAD)
        ttk.Entry(frame, textvariable=self.v_poll, width=8).grid(row=r, column=inp,
                                                                 sticky=self.anchor, **PAD)
        r += 1
        holder = ttk.Frame(frame)
        holder.grid(row=r, column=lab, sticky=self.anchor, **PAD)
        theme.PillButton(holder, t("save_settings"), self.on_save_settings,
                         kind="primary").pack()

    def _build_log(self, nb):
        frame = ttk.Frame(nb)
        nb.add(frame, text=t("tab_activity"))
        self.log_box = theme.text(frame, height=10)
        self.log_box.pack(fill="both", expand=True, **PAD)
        self.log_box.insert("end", "".join(line + "\n" for line in self._log_lines))
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    # -- actions ------------------------------------------------------------
    def _rebuild(self):
        """Tear the window down and build it again - for a language or theme switch."""
        tab = self.nb.index("current")
        self.log_box = None                   # log() skips the box until it's rebuilt
        for child in self.winfo_children():
            child.destroy()
        self._build_ui(tab)
        # _build_ui fills the lists while the new widgets are built but not yet on
        # screen, and a Listbox filled before it is realised paints nothing - the
        # rows are there, just invisible until something forces a repaint. Fill
        # them again once Tk has laid the window out.
        self.after_idle(self._refill_lists)

    def _refill_lists(self):
        self.refresh_tasks()
        self.refresh_habits()

    def on_language(self, _e=None):
        names = list(i18n.LANGUAGES.values())
        code = list(i18n.LANGUAGES)[names.index(self.v_lang.get())]
        if code == i18n.current():
            return
        self.ctl.cfg["language"] = code
        self.ctl.save()
        i18n.set_language(code)
        self._rebuild()

    def _next_scheme(self):
        names = list(theme.SCHEMES)
        return names[(names.index(theme.MODE) + 1) % len(names)]

    def on_next_scheme(self):
        self.set_scheme(self._next_scheme())

    def on_pick_scheme(self, _e=None):
        self.set_scheme(self.v_scheme.get())

    def set_scheme(self, name):
        if name not in theme.SCHEMES or name == theme.MODE:
            return
        self.ctl.cfg["theme"] = name
        self.ctl.save()
        theme.apply(self, name)
        self._rebuild()

    def on_add_task(self):
        self.ctl.add_task(self.task_entry.get(), self.link_entry.get())
        self.task_entry.delete(0, "end")
        self.link_entry.delete(0, "end")
        self.refresh_tasks()

    def on_open_link(self):
        idx = self._selected()
        if idx is None:
            return
        ok, detail = self.ctl.open_task_link(idx)
        self.log(detail)
        if not ok:
            messagebox.showinfo(t("no_link_title") if "no link" in detail
                                else t("open_failed_title"), detail)

    def on_edit_link(self):
        idx = self._selected()
        if idx is None:
            return
        link = simpledialog.askstring(t("link_title"), t("link_prompt"),
                                      initialvalue=self.ctl.task_link(idx), parent=self)
        if link is not None:
            self.ctl.set_task_link(idx, link)
            self.refresh_tasks()

    def _selected(self):
        return self.task_list.selected()

    def on_row_toggle(self, index):
        """Clicking a task's box (or double-clicking the row) ticks it both ways."""
        self.task_list.select(index)
        if self.ctl.tasks[index]["done"]:
            self.on_uncomplete()
        else:
            self.on_complete()

    def on_complete(self):
        idx = self._selected()
        if idx is None:
            return
        was_pending = not self.ctl.tasks[idx]["done"]
        self.ctl.complete_task(idx)
        if was_pending:
            self.ring.pulse()                 # a small reward for ticking one off
        self.refresh_tasks()

    def on_uncomplete(self):
        idx = self._selected()
        if idx is not None:
            changed = self.ctl.uncomplete_task(idx)   # ends a break, if one was running
            if changed:
                self.log(changed)
            self.refresh_tasks()

    def on_delete_task(self):
        idx = self._selected()
        if idx is not None:
            self.ctl.remove_task(idx)
            self.refresh_tasks()

    def _selected_habit(self):
        return self.habit_list.selected()

    def on_habit_row_toggle(self, index):
        self.habit_list.select(index)
        self.on_toggle_habit()

    def on_add_habit(self):
        self.ctl.add_habit(self.habit_entry.get())
        self.habit_entry.delete(0, "end")
        self.refresh_habits()

    def on_toggle_habit(self):
        idx = self._selected_habit()
        if idx is not None:
            self.ctl.toggle_habit(idx)
            self.ring.pulse()
            self.refresh_habits()

    def on_delete_habit(self):
        idx = self._selected_habit()
        if idx is not None:
            self.ctl.remove_habit(idx)
            self.refresh_habits()

    def on_start(self):
        if self.ctl.pending_count() == 0:
            messagebox.showinfo(t("nothing_title"), t("nothing_body"))
            return
        if self.ctl.cfg["block_websites"] and not self.ctl.admin():
            messagebox.showwarning(t("sites_warn_title"), t("sites_warn_body"))
        self.ctl.start_focus()
        self.refresh_tasks()

    def on_break_now(self):
        self.ctl.start_break(self.ctl.cfg["task_break_minutes"], "manual break")
        self.refresh_tasks()

    def on_stop(self):
        self.ctl.stop()
        self.refresh_tasks()

    def on_save_settings(self):
        cfg = self.ctl.cfg
        try:
            cfg["task_break_minutes"] = max(0.1, float(self.v_task_min.get()))
            cfg["break_after_list_minutes"] = max(0.1, float(self.v_list_min.get()))
            cfg["poll_seconds"] = max(1, int(float(self.v_poll.get())))
        except ValueError:
            messagebox.showerror(t("bad_value_title"), t("bad_value_body"))
            return
        cfg["break_after_each_task"] = self.v_each.get()
        cfg["break_after_list_enabled"] = self.v_list_on.get()
        cfg["block_mode"] = MODES[self.mode_names.index(self.v_mode.get())]
        cfg["block_websites"] = self.v_sites.get()
        cfg["close_browsers_on_lock"] = self.v_close_browsers.get()
        self.ctl.save()
        self.log(t("settings_saved"))

    def on_close(self):
        if self.ctl.state != IDLE and not messagebox.askyesno(
            t("still_locked_title"), t("still_locked_body")
        ):
            return
        self.ctl.stop()
        self.destroy()

    # -- view ---------------------------------------------------------------
    def refresh_tasks(self):
        rows = []
        for position, task in enumerate(self.ctl.tasks):
            rows.append({
                "checked": task["done"],
                "text": task["text"],
                "trail": task.get("link") or "",
                "accent": theme.ACCENTS[position % len(theme.ACCENTS)],
            })
        self.task_list.set_rows(rows)
        self.refresh_status()

    def refresh_habits(self):
        rows = []
        for position, habit in enumerate(self.ctl.habits):
            streak = habits.streak(habit)
            rows.append({
                "checked": habits.is_done(habit),
                "text": habit["name"],
                "dots": habits.last_days(habit),
                "note": t("habit_streak", n=streak),
                "star": streak >= 3,          # a real star once it is a run worth keeping
                "accent": theme.ACCENTS[position % len(theme.ACCENTS)],
            })
        self.habit_list.set_rows(rows)

    def refresh_status(self):
        state = self.ctl.state
        left = self.ctl.pending_count()
        total = len(self.ctl.tasks)
        done = total - left

        if state == FOCUS:
            self._break_total = None
            text, colour = t("status_focus", n=left), theme.FOCUS_C
            headline = t("headline_focus")
            self.ring.set(done / total if total else 0, f"{done}/{total}",
                          t("ring_focus_sub"), theme.FOCUS_C)
        elif state == BREAK:
            secs = self.ctl.seconds_left()
            if self._break_total is None:     # first sight of this break: that is its length
                self._break_total = max(secs, 1)
            reason = self.ctl.break_reason
            reason = t(REASONS[reason]) if reason in REASONS else reason
            text = t("status_break", m=secs // 60, s="{:02d}".format(secs % 60), reason=reason)
            colour = theme.BREAK_C
            headline = t("headline_break")
            self.ring.set(secs / self._break_total,
                          "{}:{:02d}".format(secs // 60, secs % 60),
                          t("ring_break_sub"), theme.BREAK_C)
        else:
            self._break_total = None
            text, colour = t("status_idle"), theme.IDLE_C
            headline = t("headline_idle")
            self.ring.set(done / total if total else 0, f"{done}/{total}" if total else "0",
                          t("ring_idle_sub"), theme.IDLE_C)

        self.scene.render(state)              # night while locked, daylight on a break
        self.headline.config(text=headline, foreground=colour)
        self.status.config(text=text)
        self.progress.config(value=(done / total * 100) if total else 0)
        self.progress_label.config(text=t("progress", done=done, total=total))
        self.start_btn.set_enabled(state != FOCUS)

    def log(self, message):
        """Queue a line for the Activity tab.

        The app blocker calls this from its watchdog thread, and Tk is not
        thread-safe, so nothing here touches a widget. `_drain_log` empties the
        queue on the main thread a second later.
        """
        self._pending_log.append(str(message).rstrip())

    def _drain_log(self):
        if not self._pending_log:
            return
        lines, self._pending_log = self._pending_log, []
        self._log_lines.extend(lines)
        box = getattr(self, "log_box", None)
        if box is None:
            return                            # mid-rebuild; the text is kept above
        box.config(state="normal")
        for line in lines:
            box.insert("end", line + "\n")
        box.see("end")
        box.config(state="disabled")

    def _tick(self):
        self._drain_log()
        changed = self.ctl.tick()
        if changed:
            self.log(changed)
            self.refresh_tasks()
        if habits.today() != self._habit_day:     # past midnight: today's ticks reset
            self._habit_day = habits.today()
            self.refresh_habits()
        self.refresh_status()
        self.after(1000, self._tick)


def main():
    App().mainloop()
