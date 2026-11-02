import json
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

DB_FILE = "money_counter.db"

# (name, value in cents, roll size). Bills have roll_size=None.
DENOMINATIONS = [
    ("Penny", 1, 50, "coin"),
    ("Nickel", 5, 40, "coin"),
    ("Dime", 10, 50, "coin"),
    ("Quarter", 25, 40, "coin"),
    ("Half Dollar", 50, 20, "coin"),
    ("Dollar Coin", 100, 25, "coin"),
    ("$1 Bill", 100, None, "bill"),
    ("$2 Bill", 200, None, "bill"),
    ("$5 Bill", 500, None, "bill"),
    ("$10 Bill", 1000, None, "bill"),
    ("$20 Bill", 2000, None, "bill"),
    ("$50 Bill", 5000, None, "bill"),
    ("$100 Bill", 10000, None, "bill"),
]

# Dark theme palette
BG = "#0B1120"
HEADER = "#080E1B"
CARD = "#121C2E"
CARD_ALT = "#19263B"
INPUT_BG = "#091426"
BORDER = "#2B3A52"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"
GREEN = "#10B981"
GREEN_DARK = "#064E3B"
BLUE = "#2563EB"
RED = "#DC4545"
WHITE = "#FFFFFF"


def money(cents):
    cents = int(cents)
    sign = "-" if cents < 0 else ""
    dollars, remainder = divmod(abs(cents), 100)
    return f"{sign}${dollars:,}.{remainder:02d}"


class MoneyCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("Money Counter | Guided Cash Count")
        self.root.geometry("900x760")
        self.root.minsize(760, 650)
        self.root.configure(bg=BG)

        self.index = 0
        self.values = [
            {"loose": 0, "rolls": 0} if kind == "coin"
            else {"quantity": 0}
            for _, _, _, kind in DENOMINATIONS
        ]
        self.current_entries = {}
        self._init_db()
        self._configure_styles()
        self._build_shell()
        self.show_step()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _init_db(self):
        with sqlite3.connect(DB_FILE) as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS cash_counts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    total_cents INTEGER NOT NULL,
                    details TEXT NOT NULL
                )
            """)

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Dark.Treeview", background=CARD, foreground=TEXT,
            fieldbackground=CARD, rowheight=34, borderwidth=0,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Dark.Treeview.Heading", background=CARD_ALT,
            foreground=GREEN, font=("Segoe UI", 9, "bold"),
            padding=9, relief="flat"
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", "#24415A")],
            foreground=[("selected", WHITE)]
        )
        style.configure(
            "Dark.Vertical.TScrollbar", background=CARD_ALT,
            troughcolor=BG, bordercolor=BG, arrowcolor=TEXT
        )

    def _label(self, parent, text, size=10, color=TEXT,
               bold=False, bg=CARD, **kwargs):
        return tk.Label(
            parent, text=text, bg=bg, fg=color,
            font=("Segoe UI", size, "bold" if bold else "normal"),
            **kwargs
        )

    def _button(self, parent, text, command, color=GREEN, **kwargs):
        return tk.Button(
            parent, text=text, command=command,
            bg=color, fg=WHITE, activebackground=color,
            activeforeground=WHITE, font=("Segoe UI", 10, "bold"),
            padx=18, pady=11, relief="flat", bd=0,
            cursor="hand2", **kwargs
        )

    def _entry(self, parent):
        entry = tk.Entry(
            parent, width=18, justify="center",
            font=("Segoe UI", 17, "bold"),
            bg=INPUT_BG, fg=WHITE, insertbackground=GREEN,
            selectbackground="#245B4A", selectforeground=WHITE,
            relief="flat", bd=0, highlightthickness=1,
            highlightbackground=BORDER, highlightcolor=GREEN
        )
        entry.insert(0, "0")
        return entry

    def _build_shell(self):
        header = tk.Frame(self.root, bg=HEADER, height=86)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=HEADER)
        left.pack(side="left", padx=26, pady=14)
        self._label(
            left, "◈  MONEY COUNTER", 20, WHITE, True, HEADER
        ).pack(anchor="w")
        self._label(
            left, "GUIDED DENOMINATION COUNT", 8, MUTED, False, HEADER
        ).pack(anchor="w", pady=(3, 0))
        self._label(
            header, "SQLITE • DARK MODE", 8, GREEN, True, HEADER
        ).pack(side="right", padx=25)

        # Running total banner
        banner = tk.Frame(
            self.root, bg=GREEN_DARK, padx=22, pady=13,
            highlightthickness=1, highlightbackground="#087F5B"
        )
        banner.pack(fill="x", padx=24, pady=(18, 12))

        self._label(
            banner, "RUNNING CASH TOTAL", 8, "#A7F3D0", True, GREEN_DARK
        ).pack(anchor="w")
        line = tk.Frame(banner, bg=GREEN_DARK)
        line.pack(fill="x")
        self.total_var = tk.StringVar(value="$0.00")
        self.count_var = tk.StringVar(value="0 items counted")
        self._label(
            line, "", 27, WHITE, True, GREEN_DARK,
            textvariable=self.total_var
        ).pack(side="left")
        self._label(
            line, "", 9, "#A7F3D0", False, GREEN_DARK,
            textvariable=self.count_var
        ).pack(side="right", pady=(12, 0))

        # Progress
        progress_area = tk.Frame(self.root, bg=BG)
        progress_area.pack(fill="x", padx=26, pady=(2, 12))
        self.progress_text = tk.StringVar()
        self._label(
            progress_area, "", 9, MUTED, True, BG,
            textvariable=self.progress_text
        ).pack(anchor="w")
        self.progress_canvas = tk.Canvas(
            progress_area, height=7, bg=CARD_ALT,
            highlightthickness=0, bd=0
        )
        self.progress_canvas.pack(fill="x", pady=(7, 0))

        self.stage = tk.Frame(self.root, bg=BG)
        self.stage.pack(fill="both", expand=True, padx=24, pady=4)

        self.footer = tk.Frame(self.root, bg=BG)
        self.footer.pack(fill="x", padx=24, pady=18)

        self.status_var = tk.StringVar(value="Enter each denomination one step at a time.")
        status = tk.Frame(self.root, bg=HEADER, height=28)
        status.pack(fill="x", side="bottom")
        status.pack_propagate(False)
        self._label(
            status, "●", 8, GREEN, True, HEADER
        ).pack(side="left", padx=(12, 5))
        self._label(
            status, "", 8, MUTED, False, HEADER,
            textvariable=self.status_var
        ).pack(side="left")

    def _clear_stage(self):
        for widget in self.stage.winfo_children():
            widget.destroy()
        for widget in self.footer.winfo_children():
            widget.destroy()

    def _current_total(self):
        total = 0
        count = 0
        for (name, value, roll_size, kind), entry_data in zip(
            DENOMINATIONS, self.values
        ):
            if kind == "coin":
                qty = entry_data["loose"] + entry_data["rolls"] * roll_size
            else:
                qty = entry_data["quantity"]
            total += qty * value
            count += qty
        return total, count

    def _step_subtotal(self, idx):
        name, value, roll_size, kind = DENOMINATIONS[idx]
        data = self.values[idx]
        if kind == "coin":
            quantity = data["loose"] + data["rolls"] * roll_size
        else:
            quantity = data["quantity"]
        return quantity, quantity * value

    def _update_summary(self):
        total, count = self._current_total()
        self.total_var.set(money(total))
        self.count_var.set(f"{count:,} coins and bills entered")

    def _update_progress(self):
        total_steps = len(DENOMINATIONS)
        self.progress_text.set(
            f"STEP {self.index + 1} OF {total_steps}   •   "
            f"{'COINS' if DENOMINATIONS[self.index][3] == 'coin' else 'BILLS'}"
        )
        self.progress_canvas.delete("all")
        width = max(self.progress_canvas.winfo_width(), 300)
        self.progress_canvas.create_rectangle(
            0, 0, width, 7, fill=CARD_ALT, outline=CARD_ALT
        )
        self.progress_canvas.create_rectangle(
            0, 0, width * (self.index + 1) / total_steps, 7,
            fill=GREEN, outline=GREEN
        )

    def show_step(self):
        self._clear_stage()
        self._update_summary()

        name, value, roll_size, kind = DENOMINATIONS[self.index]
        data = self.values[self.index]

        card = tk.Frame(
            self.stage, bg=CARD, padx=30, pady=25,
            highlightthickness=1, highlightbackground=BORDER
        )
        card.pack(fill="both", expand=True)

        self._label(
            card, "CURRENT DENOMINATION", 9, GREEN, True
        ).pack(anchor="w")
        self._label(
            card, name.upper(), 25, WHITE, True
        ).pack(anchor="w", pady=(5, 0))
        self._label(
            card, f"Value per {'coin' if kind == 'coin' else 'bill'}: {money(value)}",
            11, MUTED
        ).pack(anchor="w", pady=(3, 20))

        separator = tk.Frame(card, bg=BORDER, height=1)
        separator.pack(fill="x", pady=(0, 20))

        self.current_entries = {}
        if kind == "coin":
            self._label(
                card, f"How many loose {name.lower()}s?", 11, TEXT, True
            ).pack(anchor="w")
            loose = self._entry(card)
            loose.pack(anchor="w", pady=(8, 18), ipady=9)
            loose.delete(0, "end")
            loose.insert(0, str(data["loose"]))
            self.current_entries["loose"] = loose

            self._label(
                card, f"How many rolls?  ({roll_size} coins per roll)",
                11, TEXT, True
            ).pack(anchor="w")
            rolls = self._entry(card)
            rolls.pack(anchor="w", pady=(8, 18), ipady=9)
            rolls.delete(0, "end")
            rolls.insert(0, str(data["rolls"]))
            self.current_entries["rolls"] = rolls

            self._label(
                card,
                f"One full roll = {money(value * roll_size)}",
                9, MUTED
            ).pack(anchor="w")
        else:
            self._label(
                card, f"How many {name.lower()}s?", 11, TEXT, True
            ).pack(anchor="w")
            quantity = self._entry(card)
            quantity.pack(anchor="w", pady=(8, 18), ipady=9)
            quantity.delete(0, "end")
            quantity.insert(0, str(data["quantity"]))
            self.current_entries["quantity"] = quantity

        self.step_subtotal_var = tk.StringVar(value=money(self._step_subtotal(self.index)[1]))
        subtotal_box = tk.Frame(card, bg=CARD_ALT, padx=15, pady=12)
        subtotal_box.pack(fill="x", pady=(10, 0))
        self._label(
            subtotal_box, "THIS DENOMINATION SUBTOTAL", 8,
            MUTED, True, CARD_ALT
        ).pack(anchor="w")
        self._label(
            subtotal_box, "", 19, GREEN, True, CARD_ALT,
            textvariable=self.step_subtotal_var
        ).pack(anchor="w")

        for entry in self.current_entries.values():
            entry.bind("<KeyRelease>", self._preview_step_total)
            entry.bind("<Return>", lambda _e: self.next_step())

        self._update_progress()
        self.root.after(30, self._update_progress)

        self._button(
            self.footer, "‹  PREVIOUS", self.previous_step, CARD_ALT
        ).pack(side="left")
        if self.index < len(DENOMINATIONS) - 1:
            self._button(
                self.footer, "SAVE & NEXT  ›", self.next_step, GREEN
            ).pack(side="right")
        else:
            self._button(
                self.footer, "REVIEW FINAL COUNT  ›",
                self.open_review, BLUE
            ).pack(side="right")

        self._button(
            self.footer, "RESET ALL", self.reset, RED
        ).pack(side="right", padx=10)

        if self.index == 0:
            # Previous remains visible but disabled on first step.
            for child in self.footer.winfo_children():
                if child.cget("text").startswith("‹"):
                    child.configure(state="disabled")

        self.status_var.set(f"Entering {name}. Your progress is retained as you move between steps.")

    def _preview_step_total(self, _event=None):
        try:
            self._read_current_step()
            quantity, subtotal = self._step_subtotal(self.index)
            self.step_subtotal_var.set(money(subtotal))
            self._update_summary()
            self.status_var.set("Live totals updated.")
        except ValueError:
            self.step_subtotal_var.set("Enter a whole number")
            self._update_summary()

    def _parse_entry(self, key, label):
        raw = self.current_entries[key].get().strip() or "0"
        try:
            value = int(raw)
        except ValueError:
            raise ValueError(f"{label}: enter a whole number.")
        if value < 0:
            raise ValueError(f"{label}: quantity cannot be negative.")
        return value

    def _read_current_step(self):
        name, _value, _roll_size, kind = DENOMINATIONS[self.index]
        if kind == "coin":
            self.values[self.index]["loose"] = self._parse_entry(
                "loose", f"{name} loose count"
            )
            self.values[self.index]["rolls"] = self._parse_entry(
                "rolls", f"{name} roll count"
            )
        else:
            self.values[self.index]["quantity"] = self._parse_entry(
                "quantity", name
            )

    def next_step(self):
        try:
            self._read_current_step()
        except ValueError as error:
            messagebox.showerror("Check Quantity", str(error), parent=self.root)
            return
        if self.index < len(DENOMINATIONS) - 1:
            self.index += 1
            self.show_step()

    def previous_step(self):
        try:
            self._read_current_step()
        except ValueError:
            pass
        if self.index > 0:
            self.index -= 1
            self.show_step()

    def _build_results(self):
        results = {}
        total = 0
        item_count = 0
        for (name, value, roll_size, kind), data in zip(
            DENOMINATIONS, self.values
        ):
            if kind == "coin":
                quantity = data["loose"] + data["rolls"] * roll_size
                item = {
                    "type": "coin",
                    "loose": data["loose"],
                    "rolls": data["rolls"],
                    "roll_size": roll_size,
                    "quantity": quantity,
                    "unit_value_cents": value,
                    "subtotal_cents": quantity * value,
                }
            else:
                quantity = data["quantity"]
                item = {
                    "type": "bill",
                    "quantity": quantity,
                    "unit_value_cents": value,
                    "subtotal_cents": quantity * value,
                }
            results[name] = item
            total += item["subtotal_cents"]
            item_count += quantity
        return results, total, item_count

    def open_review(self):
        try:
            self._read_current_step()
        except ValueError as error:
            messagebox.showerror("Check Quantity", str(error), parent=self.root)
            return

        results, total, item_count = self._build_results()
        window = tk.Toplevel(self.root)
        window.title("Review Final Cash Count")
        window.geometry("850x690")
        window.minsize(700, 520)
        window.configure(bg=BG)
        window.transient(self.root)

        head = tk.Frame(window, bg=HEADER, padx=20, pady=15)
        head.pack(fill="x")
        self._label(
            head, "REVIEW FINAL COUNT", 18, WHITE, True, HEADER
        ).pack(anchor="w")
        self._label(
            head, "Check every denomination before saving.",
            9, MUTED, False, HEADER
        ).pack(anchor="w", pady=(3, 0))

        total_box = tk.Frame(window, bg=GREEN_DARK, padx=18, pady=12)
        total_box.pack(fill="x", padx=16, pady=12)
        self._label(
            total_box, "GRAND TOTAL", 8, "#A7F3D0", True, GREEN_DARK
        ).pack(anchor="w")
        self._label(
            total_box, money(total), 25, WHITE, True, GREEN_DARK
        ).pack(anchor="w")
        self._label(
            total_box, f"{item_count:,} total coins and bills",
            9, "#A7F3D0", False, GREEN_DARK
        ).pack(anchor="w")

        table_frame = tk.Frame(window, bg=BG, padx=16)
        table_frame.pack(fill="both", expand=True)
        columns = ("denom", "loose", "rolls", "quantity", "subtotal")
        tree = ttk.Treeview(
            table_frame, columns=columns, show="headings",
            style="Dark.Treeview"
        )
        for col, title, width, anchor in [
            ("denom", "DENOMINATION", 170, "w"),
            ("loose", "LOOSE", 85, "center"),
            ("rolls", "ROLLS", 85, "center"),
            ("quantity", "TOTAL COUNT", 115, "center"),
            ("subtotal", "SUBTOTAL", 130, "e"),
        ]:
            tree.heading(col, text=title)
            tree.column(col, width=width, anchor=anchor)

        scroll = ttk.Scrollbar(
            table_frame, orient="vertical", command=tree.yview,
            style="Dark.Vertical.TScrollbar"
        )
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        coin_total = 0
        bill_total = 0
        for name, _value, _roll_size, kind in DENOMINATIONS:
            item = results[name]
            if kind == "coin":
                coin_total += item["subtotal_cents"]
                loose, rolls = item["loose"], item["rolls"]
            else:
                bill_total += item["subtotal_cents"]
                loose, rolls = "—", "—"
            tree.insert(
                "", "end",
                values=(
                    name, loose, rolls, item["quantity"],
                    money(item["subtotal_cents"])
                )
            )

        tree.insert(
            "", "end",
            values=("COINS TOTAL", "—", "—", "—", money(coin_total)),
            tags=("subtotal",)
        )
        tree.insert(
            "", "end",
            values=("BILLS TOTAL", "—", "—", "—", money(bill_total)),
            tags=("subtotal",)
        )
        tree.insert(
            "", "end",
            values=("GRAND TOTAL", "—", "—", item_count, money(total)),
            tags=("grand",)
        )
        tree.tag_configure("subtotal", background=CARD_ALT, foreground=TEXT)
        tree.tag_configure("grand", background=GREEN_DARK, foreground=WHITE)

        buttons = tk.Frame(window, bg=BG, padx=16, pady=14)
        buttons.pack(fill="x")
        self._button(
            buttons, "BACK TO COUNT", window.destroy, CARD_ALT
        ).pack(side="left")
        self._button(
            buttons, "SAVE FINAL COUNT", lambda: self.save_results(results, total, window),
            GREEN
        ).pack(side="right")

    def save_results(self, results, total, review_window=None):
        try:
            with sqlite3.connect(DB_FILE) as db:
                db.execute(
                    """INSERT INTO cash_counts (created_at, total_cents, details)
                       VALUES (?, ?, ?)""",
                    (
                        datetime.now().isoformat(timespec="seconds"),
                        int(total),
                        json.dumps(results),
                    )
                )
            self.status_var.set(f"Saved final count: {money(total)}")
            if review_window is not None:
                review_window.destroy()
            messagebox.showinfo(
                "Count Saved",
                f"Cash count saved successfully.\n\nTotal: {money(total)}",
                parent=self.root
            )
        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error", f"Could not save count:\n{error}",
                parent=self.root
            )

    def show_history(self):
        window = tk.Toplevel(self.root)
        window.title("Cash Count History")
        window.geometry("740x480")
        window.configure(bg=BG)

        header = tk.Frame(window, bg=HEADER, padx=20, pady=15)
        header.pack(fill="x")
        self._label(
            header, "SAVED COUNT HISTORY", 17, WHITE, True, HEADER
        ).pack(anchor="w")

        body = tk.Frame(window, bg=BG, padx=16, pady=16)
        body.pack(fill="both", expand=True)
        tree = ttk.Treeview(
            body, columns=("id", "date", "total"),
            show="headings", style="Dark.Treeview"
        )
        tree.heading("id", text="COUNT #")
        tree.heading("date", text="DATE / TIME")
        tree.heading("total", text="TOTAL CASH")
        tree.column("id", width=80, anchor="center")
        tree.column("date", width=390)
        tree.column("total", width=150, anchor="e")
        tree.pack(fill="both", expand=True)

        try:
            with sqlite3.connect(DB_FILE) as db:
                rows = db.execute(
                    """SELECT id, created_at, total_cents
                       FROM cash_counts ORDER BY id DESC LIMIT 500"""
                ).fetchall()
            for record in rows:
                tree.insert(
                    "", "end",
                    values=(record[0], record[1], money(record[2]))
                )
            if not rows:
                self._label(
                    body, "No saved counts yet.", 10, MUTED, bg=BG
                ).pack(pady=8)
        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error), parent=window)

    def reset(self):
        if not messagebox.askyesno(
            "Start Over",
            "Clear all entered denomination quantities?\nSaved history will remain.",
            parent=self.root
        ):
            return
        self.values = [
            {"loose": 0, "rolls": 0} if kind == "coin"
            else {"quantity": 0}
            for _, _, _, kind in DENOMINATIONS
        ]
        self.index = 0
        self.show_step()
        self.status_var.set("New count started. All denomination entries cleared.")

    def close(self):
        self.root.destroy()


def main():
    root = tk.Tk()
    MoneyCounter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
