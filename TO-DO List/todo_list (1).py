import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
import datetime

# ── Config ─────────────────────────────────────────────────────────
FILE = "tasks.json"

PRIORITIES = ["High", "Medium", "Low"]
PRIORITY_COLORS = {
    "High":   {"bg": "#FEECEC", "fg": "#A32D2D", "dot": "#E53E3E"},
    "Medium": {"bg": "#FEF6E4", "fg": "#7A4F00", "dot": "#D97706"},
    "Low":    {"bg": "#EAF4EA", "fg": "#1A5C2A", "dot": "#38A169"},
}
CATEGORIES = ["Work", "Personal", "Shopping", "Health", "Study", "Other"]

# ── Colors ──────────────────────────────────────────────────────────
BG        = "#F0EFEA"
CARD_BG   = "#FFFFFF"
SIDE_BG   = "#1E1E2E"
SIDE_FG   = "#CDD6F4"
ACCENT    = "#534AB7"
ACCENT_LT = "#EEEDFE"
TEXT_PRI  = "#1A1A18"
TEXT_SEC  = "#6B6B67"
TEXT_TER  = "#9B9B96"
BORDER    = "#D0D0CC"
GREEN     = "#38A169"
RED       = "#E53E3E"

# ── Data ────────────────────────────────────────────────────────────
def load_tasks():
    if os.path.exists(FILE):
        with open(FILE) as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1

# ── Main App ─────────────────────────────────────────────────────────
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("860x620")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self.root.minsize(720, 500)

        self.tasks        = load_tasks()
        self.filter_status = tk.StringVar(value="All")
        self.filter_priority = tk.StringVar(value="All")
        self.filter_cat   = tk.StringVar(value="All")
        self.search_var   = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.render_tasks())

        self._styles()
        self._build_ui()
        self.render_tasks()
        self.update_stats()

    # ── Styles ──────────────────────────────────────────────────────
    def _styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
            fieldbackground="#F5F5F4", background="#F5F5F4",
            foreground=TEXT_PRI, bordercolor=BORDER,
            arrowcolor=TEXT_SEC, relief="flat", padding=6)
        style.map("TCombobox",
            fieldbackground=[("readonly", "#F5F5F4")],
            foreground=[("readonly", TEXT_PRI)])
        style.configure("Vertical.TScrollbar",
            background=BG, troughcolor=BG,
            bordercolor=BG, arrowcolor=TEXT_SEC, relief="flat")

    # ── UI ──────────────────────────────────────────────────────────
    def _build_ui(self):
        # Main layout
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Sidebar
        side = tk.Frame(self.root, bg=SIDE_BG, width=200)
        side.grid(row=0, column=0, sticky="nsew")
        side.grid_propagate(False)
        self._build_sidebar(side)

        # Main area
        main = tk.Frame(self.root, bg=BG)
        main.grid(row=0, column=1, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)
        self._build_main(main)

    def _build_sidebar(self, parent):
        # Logo
        tk.Label(parent, text="✅  To-Do", font=("Helvetica", 16, "bold"),
                 bg=SIDE_BG, fg="#CDD6F4").pack(pady=(24, 4), padx=20, anchor="w")
        tk.Label(parent, text="Stay organised",
                 font=("Helvetica", 10), bg=SIDE_BG, fg="#6C7086").pack(padx=20, anchor="w")

        tk.Frame(parent, bg="#313244", height=1).pack(fill="x", padx=16, pady=16)

        # Stats
        self.stat_frame = tk.Frame(parent, bg=SIDE_BG)
        self.stat_frame.pack(fill="x", padx=16, pady=(0, 8))
        self._stat_card(self.stat_frame, "Total",     "0", "#CDD6F4", "s_total")
        self._stat_card(self.stat_frame, "Pending",   "0", "#F38BA8", "s_pending")
        self._stat_card(self.stat_frame, "Done",      "0", "#A6E3A1", "s_done")
        self._stat_card(self.stat_frame, "Overdue",   "0", "#FAB387", "s_overdue")

        tk.Frame(parent, bg="#313244", height=1).pack(fill="x", padx=16, pady=12)

        # Filters label
        tk.Label(parent, text="FILTERS", font=("Helvetica", 9, "bold"),
                 bg=SIDE_BG, fg="#6C7086").pack(padx=20, anchor="w", pady=(0,8))

        # Status filter
        tk.Label(parent, text="Status", font=("Helvetica", 10),
                 bg=SIDE_BG, fg=SIDE_FG).pack(padx=20, anchor="w")
        for s in ["All", "Pending", "Done"]:
            self._side_btn(parent, s, self.filter_status, self.render_tasks)

        tk.Frame(parent, bg="#313244", height=1).pack(fill="x", padx=16, pady=10)

        # Priority filter
        tk.Label(parent, text="Priority", font=("Helvetica", 10),
                 bg=SIDE_BG, fg=SIDE_FG).pack(padx=20, anchor="w")
        for p in ["All"] + PRIORITIES:
            self._side_btn(parent, p, self.filter_priority, self.render_tasks)

        tk.Frame(parent, bg="#313244", height=1).pack(fill="x", padx=16, pady=10)

        # Category filter
        tk.Label(parent, text="Category", font=("Helvetica", 10),
                 bg=SIDE_BG, fg=SIDE_FG).pack(padx=20, anchor="w")
        for c in ["All"] + CATEGORIES:
            self._side_btn(parent, c, self.filter_cat, self.render_tasks)

    def _stat_card(self, parent, label, val, color, attr):
        f = tk.Frame(parent, bg="#313244", pady=6)
        f.pack(fill="x", pady=3)
        tk.Label(f, text=label, font=("Helvetica", 9),
                 bg="#313244", fg="#6C7086").pack(side="left", padx=10)
        lbl = tk.Label(f, text=val, font=("Helvetica", 11, "bold"),
                       bg="#313244", fg=color)
        lbl.pack(side="right", padx=10)
        setattr(self, attr, lbl)

    def _side_btn(self, parent, text, var, cmd):
        def click():
            var.set(text)
            cmd()
        f = tk.Frame(parent, bg=SIDE_BG, cursor="hand2")
        f.pack(fill="x", padx=12, pady=1)
        lbl = tk.Label(f, text=text, font=("Helvetica", 10),
                       bg=SIDE_BG, fg="#6C7086", anchor="w", padx=8, pady=4)
        lbl.pack(fill="x")
        lbl.bind("<Button-1>", lambda e: click())
        f.bind("<Button-1>", lambda e: click())

        def on_enter(e):
            if var.get() != text:
                lbl.config(fg=SIDE_FG)
        def on_leave(e):
            if var.get() != text:
                lbl.config(fg="#6C7086")
        lbl.bind("<Enter>", on_enter)
        lbl.bind("<Leave>", on_leave)

    def _build_main(self, parent):
        # Top bar
        top = tk.Frame(parent, bg=BG)
        top.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        top.columnconfigure(0, weight=1)

        tk.Label(top, text="My Tasks", font=("Helvetica", 18, "bold"),
                 bg=BG, fg=TEXT_PRI).grid(row=0, column=0, sticky="w")

        # Search
        search_frame = tk.Frame(top, bg="#F5F5F4",
                                highlightbackground=BORDER, highlightthickness=1)
        search_frame.grid(row=0, column=1, padx=(0,10))
        tk.Label(search_frame, text="🔍", bg="#F5F5F4", fg=TEXT_SEC,
                 font=("Helvetica", 11)).pack(side="left", padx=(8,4))
        tk.Entry(search_frame, textvariable=self.search_var,
                 font=("Helvetica", 11), relief="flat",
                 bg="#F5F5F4", fg=TEXT_PRI, width=18,
                 insertbackground=TEXT_PRI).pack(side="left", ipady=6, padx=(0,8))

        # Add button
        tk.Button(top, text="＋  Add Task",
                  font=("Helvetica", 11, "bold"),
                  bg=ACCENT, fg="white", relief="flat",
                  padx=16, pady=6, cursor="hand2",
                  activebackground="#3C3489", activeforeground="white",
                  command=self.open_add_dialog).grid(row=0, column=2)

        # Tasks area
        container = tk.Frame(parent, bg=BG)
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,20))
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        # Canvas + scrollbar
        self.canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        scrollbar   = ttk.Scrollbar(container, orient="vertical",
                                     command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.task_frame = tk.Frame(self.canvas, bg=BG)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.task_frame, anchor="nw")

        self.task_frame.bind("<Configure>", self._on_frame_config)
        self.canvas.bind("<Configure>", self._on_canvas_config)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_frame_config(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_config(self, e):
        self.canvas.itemconfig(self.canvas_window, width=e.width)

    def _on_mousewheel(self, e):
        self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")

    # ── Render Tasks ────────────────────────────────────────────────
    def render_tasks(self):
        for w in self.task_frame.winfo_children():
            w.destroy()

        tasks = self._filtered()
        if not tasks:
            tk.Label(self.task_frame, text="No tasks found  ✨",
                     font=("Helvetica", 14), bg=BG,
                     fg=TEXT_TER).pack(pady=60)
            return

        # Group by priority
        groups = {"High": [], "Medium": [], "Low": []}
        for t in tasks:
            groups[t["priority"]].append(t)

        for pri in PRIORITIES:
            if not groups[pri]: continue
            c = PRIORITY_COLORS[pri]
            tk.Label(self.task_frame,
                     text=f"  ● {pri} Priority",
                     font=("Helvetica", 11, "bold"),
                     bg=BG, fg=c["dot"]).pack(anchor="w", pady=(12, 4))
            for task in groups[pri]:
                self._task_card(self.task_frame, task)

        self.update_stats()

    def _task_card(self, parent, task):
        done  = task["done"]
        c     = PRIORITY_COLORS[task["priority"]]
        today = datetime.date.today().strftime("%Y-%m-%d")
        overdue = task["due"] and task["due"] < today and not done

        card = tk.Frame(parent, bg=CARD_BG,
                        highlightbackground="#E0E0DC" if not done else "#C8F0C8",
                        highlightthickness=1)
        card.pack(fill="x", pady=3, ipady=2)

        # Left color bar
        bar_color = c["dot"] if not done else GREEN
        tk.Frame(card, bg=bar_color, width=4).pack(side="left", fill="y")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(side="left", fill="both", expand=True, padx=12, pady=10)
        inner.columnconfigure(0, weight=1)

        # Row 1: checkbox + title
        row1 = tk.Frame(inner, bg=CARD_BG)
        row1.grid(row=0, column=0, sticky="ew")
        row1.columnconfigure(1, weight=1)

        chk_var = tk.BooleanVar(value=done)
        chk = tk.Checkbutton(row1, variable=chk_var, bg=CARD_BG,
                              activebackground=CARD_BG,
                              selectcolor=CARD_BG,
                              command=lambda t=task, v=chk_var: self.toggle_done(t, v))
        chk.grid(row=0, column=0, padx=(0,6))

        title_font = ("Helvetica", 12, "bold")
        title_color = TEXT_TER if done else TEXT_PRI
        title = tk.Label(row1, text=task["title"],
                         font=title_font, bg=CARD_BG, fg=title_color,
                         anchor="w")
        title.grid(row=0, column=1, sticky="ew")
        if done:
            title.config(font=("Helvetica", 12, "overstrike"))

        # Row 2: meta info
        row2 = tk.Frame(inner, bg=CARD_BG)
        row2.grid(row=1, column=0, sticky="ew", pady=(4,0))

        # Category badge
        tk.Label(row2, text=task["category"],
                 font=("Helvetica", 9), bg="#F0EFEA",
                 fg=TEXT_SEC, padx=6, pady=2).pack(side="left", padx=(0,6))

        # Priority badge
        tk.Label(row2, text=task["priority"],
                 font=("Helvetica", 9), bg=c["bg"],
                 fg=c["fg"], padx=6, pady=2).pack(side="left", padx=(0,6))

        # Due date
        if task["due"]:
            due_color = RED if overdue else TEXT_SEC
            due_text  = f"⏰ Due: {task['due']}" + (" (Overdue!)" if overdue else "")
            tk.Label(row2, text=due_text,
                     font=("Helvetica", 9), bg=CARD_BG,
                     fg=due_color).pack(side="left", padx=(0,6))

        # Note
        if task.get("note"):
            tk.Label(inner, text=task["note"],
                     font=("Helvetica", 9), bg=CARD_BG,
                     fg=TEXT_SEC, anchor="w",
                     wraplength=500).grid(row=2, column=0, sticky="ew", pady=(4,0))

        # Buttons
        btn_frame = tk.Frame(card, bg=CARD_BG)
        btn_frame.pack(side="right", padx=10)

        tk.Button(btn_frame, text="✏️", relief="flat", bg=CARD_BG,
                  font=("Helvetica", 13), cursor="hand2",
                  activebackground=ACCENT_LT,
                  command=lambda t=task: self.open_edit_dialog(t)).pack(side="left", padx=2)

        tk.Button(btn_frame, text="🗑", relief="flat", bg=CARD_BG,
                  font=("Helvetica", 13), cursor="hand2",
                  activebackground="#FEECEC",
                  command=lambda t=task: self.delete_task(t)).pack(side="left", padx=2)

    # ── Filter ──────────────────────────────────────────────────────
    def _filtered(self):
        tasks = self.tasks[:]
        fs = self.filter_status.get()
        fp = self.filter_priority.get()
        fc = self.filter_cat.get()
        kw = self.search_var.get().lower()

        if fs == "Pending": tasks = [t for t in tasks if not t["done"]]
        if fs == "Done":    tasks = [t for t in tasks if t["done"]]
        if fp != "All":     tasks = [t for t in tasks if t["priority"] == fp]
        if fc != "All":     tasks = [t for t in tasks if t["category"] == fc]
        if kw:              tasks = [t for t in tasks if kw in t["title"].lower()
                                     or kw in t.get("note","").lower()]
        return tasks

    # ── Stats ────────────────────────────────────────────────────────
    def update_stats(self):
        today   = datetime.date.today().strftime("%Y-%m-%d")
        total   = len(self.tasks)
        done    = sum(1 for t in self.tasks if t["done"])
        pending = total - done
        overdue = sum(1 for t in self.tasks if t["due"] and t["due"] < today and not t["done"])
        self.s_total.config(text=str(total))
        self.s_pending.config(text=str(pending))
        self.s_done.config(text=str(done))
        self.s_overdue.config(text=str(overdue))

    # ── Actions ──────────────────────────────────────────────────────
    def toggle_done(self, task, var):
        for t in self.tasks:
            if t["id"] == task["id"]:
                t["done"] = var.get()
                break
        save_tasks(self.tasks)
        self.render_tasks()

    def delete_task(self, task):
        if messagebox.askyesno("Delete", f"Delete '{task['title']}'?"):
            self.tasks = [t for t in self.tasks if t["id"] != task["id"]]
            save_tasks(self.tasks)
            self.render_tasks()

    # ── Add Dialog ───────────────────────────────────────────────────
    def open_add_dialog(self):
        self._task_dialog()

    def open_edit_dialog(self, task):
        self._task_dialog(task)

    def _task_dialog(self, task=None):
        dlg = tk.Toplevel(self.root)
        dlg.title("Edit Task" if task else "Add Task")
        dlg.geometry("440x420")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)
        dlg.grab_set()
        dlg.transient(self.root)

        tk.Label(dlg, text="Edit Task" if task else "New Task",
                 font=("Helvetica", 16, "bold"),
                 bg=BG, fg=TEXT_PRI).pack(anchor="w", padx=24, pady=(20,16))

        card = tk.Frame(dlg, bg=CARD_BG,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", padx=20)

        def row(label, widget_fn, default=""):
            f = tk.Frame(card, bg=CARD_BG)
            f.pack(fill="x", padx=16, pady=6)
            tk.Label(f, text=label, font=("Helvetica", 9, "bold"),
                     bg=CARD_BG, fg=TEXT_SEC,
                     width=12, anchor="w").pack(side="left")
            w = widget_fn(f)
            w.pack(side="left", fill="x", expand=True)
            return w

        # Title
        title_var = tk.StringVar(value=task["title"] if task else "")
        title_e = row("Title", lambda f: tk.Entry(
            f, textvariable=title_var, font=("Helvetica", 11),
            relief="flat", bg="#F5F5F4", fg=TEXT_PRI,
            insertbackground=TEXT_PRI))

        # Priority
        pri_var = tk.StringVar(value=task["priority"] if task else "Medium")
        row("Priority", lambda f: ttk.Combobox(
            f, textvariable=pri_var, values=PRIORITIES,
            state="readonly", font=("Helvetica", 11)))

        # Category
        cat_var = tk.StringVar(value=task["category"] if task else "Personal")
        row("Category", lambda f: ttk.Combobox(
            f, textvariable=cat_var, values=CATEGORIES,
            state="readonly", font=("Helvetica", 11)))

        # Due date
        due_var = tk.StringVar(value=task["due"] if task else "")
        row("Due Date", lambda f: tk.Entry(
            f, textvariable=due_var, font=("Helvetica", 11),
            relief="flat", bg="#F5F5F4", fg=TEXT_PRI,
            insertbackground=TEXT_PRI))
        tk.Label(card, text="  Date format: YYYY-MM-DD",
                 font=("Helvetica", 8), bg=CARD_BG, fg=TEXT_TER).pack(anchor="w", padx=16)

        # Note
        tk.Label(card, text="Note", font=("Helvetica", 9, "bold"),
                 bg=CARD_BG, fg=TEXT_SEC).pack(anchor="w", padx=16, pady=(8,2))
        note_txt = tk.Text(card, font=("Helvetica", 11), relief="flat",
                           bg="#F5F5F4", fg=TEXT_PRI, height=3,
                           insertbackground=TEXT_PRI)
        note_txt.pack(fill="x", padx=16, pady=(0,12))
        if task and task.get("note"):
            note_txt.insert("1.0", task["note"])

        # Buttons
        btn_row = tk.Frame(dlg, bg=BG)
        btn_row.pack(fill="x", padx=20, pady=16)

        def save():
            title = title_var.get().strip()
            if not title:
                messagebox.showwarning("Warning", "Title cannot be empty!", parent=dlg)
                return
            note = note_txt.get("1.0", "end").strip()
            if task:
                for t in self.tasks:
                    if t["id"] == task["id"]:
                        t.update({"title": title, "priority": pri_var.get(),
                                  "category": cat_var.get(), "due": due_var.get(),
                                  "note": note})
                        break
            else:
                self.tasks.append({
                    "id": next_id(self.tasks),
                    "title": title,
                    "priority": pri_var.get(),
                    "category": cat_var.get(),
                    "due": due_var.get(),
                    "note": note,
                    "done": False
                })
            save_tasks(self.tasks)
            dlg.destroy()
            self.render_tasks()

        tk.Button(btn_row, text="Save Task",
                  font=("Helvetica", 11, "bold"),
                  bg=ACCENT, fg="white", relief="flat",
                  padx=20, pady=7, cursor="hand2",
                  activebackground="#3C3489",
                  command=save).pack(side="left", padx=(0,8))

        tk.Button(btn_row, text="Cancel",
                  font=("Helvetica", 11), relief="flat",
                  bg="#E8E7E2", fg=TEXT_PRI,
                  padx=16, pady=7, cursor="hand2",
                  command=dlg.destroy).pack(side="left")

        title_e.focus()
        dlg.bind("<Return>", lambda e: save())

# ── Run ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.tk_setPalette(background=BG)
    app = ToDoApp(root)
    root.mainloop()
