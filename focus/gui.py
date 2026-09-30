"""Tkinter front end for the focus locker."""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from .controller import BREAK, FOCUS, IDLE, Controller

PAD = {"padx": 8, "pady": 6}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Focus Locker")
        self.geometry("720x560")
        self.minsize(620, 480)
        self.ctl = Controller(log=self.log)

        self._build_header()
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, **PAD)
        self._build_tasks(nb)
        self._build_list_tab(nb, "Blocked apps", "blocked_apps",
                             "Process name as it appears in Task Manager, e.g. chrome.exe")
        self._build_list_tab(nb, "Blocked sites", "blocked_sites",
                             "Domain only, e.g. youtube.com (www. is added for you)")
        self._build_list_tab(nb, "Always allowed sites", "allowed_sites",
                             "Never blocked, e.g. your school portal: myschool.edu")
        self._build_settings(nb)
        self._build_log(nb)

        self.refresh_tasks()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(1000, self._tick)
        if not self.ctl.admin():
            self.log("Not running as administrator - website blocking will be skipped.")

    # -- layout -------------------------------------------------------------
    def _build_header(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", **PAD)
        self.status = ttk.Label(bar, text="Unlocked", font=("Segoe UI", 13, "bold"))
        self.status.pack(side="left")
        ttk.Button(bar, text="Stop / unlock", command=self.on_stop).pack(side="right", padx=4)
        ttk.Button(bar, text="Break now", command=self.on_break_now).pack(side="right", padx=4)
        self.start_btn = ttk.Button(bar, text="Start focus", command=self.on_start)
        self.start_btn.pack(side="right", padx=4)

    def _build_tasks(self, nb):
        frame = ttk.Frame(nb)
        nb.add(frame, text="To-do")
        entry_row = ttk.Frame(frame)
        entry_row.pack(fill="x", **PAD)
        ttk.Label(entry_row, text="Task").pack(side="left")
        self.task_entry = ttk.Entry(entry_row)
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(6, 12))
        self.task_entry.bind("<Return>", lambda _e: self.on_add_task())
        ttk.Label(entry_row, text="Link (optional)").pack(side="left")
        self.link_entry = ttk.Entry(entry_row, width=28)
        self.link_entry.pack(side="left", padx=6)
        self.link_entry.bind("<Return>", lambda _e: self.on_add_task())
        ttk.Button(entry_row, text="Add", command=self.on_add_task).pack(side="left", padx=6)
        ttk.Label(frame, text="A link can be a website, or a folder or file on this "
                              "computer - wherever the task actually gets done.",
                  foreground="#555").pack(anchor="w", padx=8)

        self.task_list = tk.Listbox(frame, activestyle="none", font=("Segoe UI", 11))
        self.task_list.pack(fill="both", expand=True, **PAD)
        self.task_list.bind("<Double-Button-1>", lambda _e: self.on_complete())

        row = ttk.Frame(frame)
        row.pack(fill="x", **PAD)
        ttk.Button(row, text="Mark done (starts break)", command=self.on_complete).pack(side="left")
        ttk.Button(row, text="Open link", command=self.on_open_link).pack(side="left", padx=6)
        ttk.Button(row, text="Edit link", command=self.on_edit_link).pack(side="left")
        ttk.Button(row, text="Undo done", command=self.on_uncomplete).pack(side="left", padx=6)
        ttk.Button(row, text="Delete", command=self.on_delete_task).pack(side="left")

    def _build_list_tab(self, nb, title, key, hint):
        frame = ttk.Frame(nb)
        nb.add(frame, text=title)
        ttk.Label(frame, text=hint, foreground="#555").pack(anchor="w", **PAD)
        listbox = tk.Listbox(frame, font=("Consolas", 10))
        listbox.pack(fill="both", expand=True, **PAD)
        row = ttk.Frame(frame)
        row.pack(fill="x", **PAD)
        entry = ttk.Entry(row)
        entry.pack(side="left", fill="x", expand=True)

        def refill():
            listbox.delete(0, "end")
            for item in self.ctl.cfg[key]:
                listbox.insert("end", item)

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
        ttk.Button(row, text="Add", command=add).pack(side="left", padx=6)
        ttk.Button(row, text="Remove selected", command=remove).pack(side="left")
        refill()

    def _build_settings(self, nb):
        frame = ttk.Frame(nb)
        nb.add(frame, text="Settings")
        cfg = self.ctl.cfg
        self.v_each = tk.BooleanVar(value=cfg["break_after_each_task"])
        self.v_task_min = tk.StringVar(value=str(cfg["task_break_minutes"]))
        self.v_list_on = tk.BooleanVar(value=cfg["break_after_list_enabled"])
        self.v_list_min = tk.StringVar(value=str(cfg["break_after_list_minutes"]))
        self.v_mode = tk.StringVar(value=cfg["block_mode"])
        self.v_sites = tk.BooleanVar(value=cfg["block_websites"])
        self.v_close_browsers = tk.BooleanVar(value=cfg["close_browsers_on_lock"])
        self.v_poll = tk.StringVar(value=str(cfg["poll_seconds"]))

        r = 0
        ttk.Checkbutton(frame, text="Take a break after each finished task",
                        variable=self.v_each).grid(row=r, column=0, columnspan=2,
                                                   sticky="w", **PAD)
        r += 1
        ttk.Label(frame, text="Break after each task (minutes)").grid(row=r, column=0,
                                                                     sticky="w", **PAD)
        ttk.Entry(frame, textvariable=self.v_task_min, width=8).grid(row=r, column=1,
                                                                    sticky="w", **PAD)
        r += 1
        ttk.Checkbutton(frame, text="Take a longer break when the whole list is finished",
                        variable=self.v_list_on).grid(row=r, column=0, columnspan=2,
                                                      sticky="w", **PAD)
        r += 1
        ttk.Label(frame, text="Break after whole list (minutes)").grid(row=r, column=0,
                                                                      sticky="w", **PAD)
        ttk.Entry(frame, textvariable=self.v_list_min, width=8).grid(row=r, column=1,
                                                                     sticky="w", **PAD)
        r += 1
        ttk.Label(frame, text="How blocked apps are handled").grid(row=r, column=0,
                                                                   sticky="w", **PAD)
        ttk.Combobox(frame, textvariable=self.v_mode, width=24, state="readonly",
                     values=["suspend", "close"]).grid(row=r, column=1, sticky="w", **PAD)
        r += 1
        ttk.Label(frame, text="suspend = freeze the app, nothing is lost (recommended)\n"
                             "close = terminate it, unsaved work may be lost",
                  foreground="#555").grid(row=r, column=0, columnspan=2, sticky="w", **PAD)
        r += 1
        ttk.Checkbutton(frame, text="Also block websites (needs the app run as administrator)",
                        variable=self.v_sites).grid(row=r, column=0, columnspan=2,
                                                    sticky="w", **PAD)
        r += 1
        ttk.Checkbutton(frame, text="Close browsers when locking (otherwise an open "
                                    "YouTube tab keeps playing for minutes)",
                        variable=self.v_close_browsers).grid(row=r, column=0, columnspan=2,
                                                             sticky="w", **PAD)
        r += 1
        ttk.Label(frame, text="Check for blocked apps every (seconds)").grid(row=r, column=0,
                                                                            sticky="w", **PAD)
        ttk.Entry(frame, textvariable=self.v_poll, width=8).grid(row=r, column=1,
                                                                 sticky="w", **PAD)
        r += 1
        ttk.Button(frame, text="Save settings", command=self.on_save_settings)\
            .grid(row=r, column=0, sticky="w", **PAD)

    def _build_log(self, nb):
        frame = ttk.Frame(nb)
        nb.add(frame, text="Activity")
        self.log_box = tk.Text(frame, height=10, state="disabled", font=("Consolas", 9))
        self.log_box.pack(fill="both", expand=True, **PAD)

    # -- actions ------------------------------------------------------------
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
            messagebox.showinfo("No link" if "no link" in detail else "Could not open",
                                detail)

    def on_edit_link(self):
        idx = self._selected()
        if idx is None:
            return
        link = simpledialog.askstring(
            "Link", "Where does this task get done?\n"
                    "A website, or a folder or file on this computer:",
            initialvalue=self.ctl.task_link(idx), parent=self)
        if link is not None:
            self.ctl.set_task_link(idx, link)
            self.refresh_tasks()

    def _selected(self):
        sel = self.task_list.curselection()
        return sel[0] if sel else None

    def on_complete(self):
        idx = self._selected()
        if idx is None:
            return
        self.ctl.complete_task(idx)
        self.refresh_tasks()

    def on_uncomplete(self):
        idx = self._selected()
        if idx is not None:
            self.ctl.uncomplete_task(idx)
            self.refresh_tasks()

    def on_delete_task(self):
        idx = self._selected()
        if idx is not None:
            self.ctl.remove_task(idx)
            self.refresh_tasks()

    def on_start(self):
        if self.ctl.pending_count() == 0:
            messagebox.showinfo("Nothing to do", "Add at least one task first.")
            return
        if self.ctl.cfg["block_websites"] and not self.ctl.admin():
            messagebox.showwarning(
                "Websites will not be blocked",
                "Editing the hosts file needs administrator rights.\n"
                "Apps will still be locked. Restart the app as administrator "
                "(run_as_admin.bat) to block websites too.",
            )
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
            messagebox.showerror("Bad value", "Break lengths and interval must be numbers.")
            return
        cfg["break_after_each_task"] = self.v_each.get()
        cfg["break_after_list_enabled"] = self.v_list_on.get()
        cfg["block_mode"] = self.v_mode.get()
        cfg["block_websites"] = self.v_sites.get()
        cfg["close_browsers_on_lock"] = self.v_close_browsers.get()
        self.ctl.save()
        self.log("settings saved")

    def on_close(self):
        if self.ctl.state != IDLE and not messagebox.askyesno(
            "Still locked", "Quitting will unlock everything. Quit anyway?"
        ):
            return
        self.ctl.stop()
        self.destroy()

    # -- view ---------------------------------------------------------------
    def refresh_tasks(self):
        sel = self._selected()
        self.task_list.delete(0, "end")
        for task in self.ctl.tasks:
            mark = "[x]" if task["done"] else "[ ]"
            line = mark + " " + task["text"]
            if task.get("link"):
                line += "   ->  " + task["link"]
            self.task_list.insert("end", line)
            if task["done"]:
                self.task_list.itemconfig("end", foreground="#888")
        if sel is not None and sel < self.task_list.size():
            self.task_list.selection_set(sel)
        self.refresh_status()

    def refresh_status(self):
        state = self.ctl.state
        left = self.ctl.pending_count()
        if state == FOCUS:
            text, color = "LOCKED - {} task(s) left".format(left), "#b00020"
        elif state == BREAK:
            secs = self.ctl.seconds_left()
            text = "BREAK - {}:{:02d} left ({})".format(secs // 60, secs % 60,
                                                        self.ctl.break_reason)
            color = "#0b6b2f"
        else:
            text, color = "Unlocked - not in a focus session", "#333"
        self.status.config(text=text, foreground=color)
        self.start_btn.config(state="disabled" if state == FOCUS else "normal")

    def log(self, message):
        box = getattr(self, "log_box", None)
        if box is None:
            return
        box.config(state="normal")
        box.insert("end", str(message).rstrip() + "\n")
        box.see("end")
        box.config(state="disabled")

    def _tick(self):
        changed = self.ctl.tick()
        if changed:
            self.log(changed)
            self.refresh_tasks()
        self.refresh_status()
        self.after(1000, self._tick)


def main():
    App().mainloop()
