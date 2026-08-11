import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


class Timesheets:

    def __init__(self, parent, db, user_id, role_name):

        self.parent = parent
        self.db = db
        self.user_id = user_id
        self.role_name = role_name
        self.selected_id = None

        self.create_ui()
        self.load_logged_in_user()
        self.load_projects()
        self.load_timesheets()

    # =====================================
    # CREATE UI
    # =====================================

    def create_ui(self):

        self.frame = tk.Frame(self.parent, bg="white")
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame,
            text="Timesheet Management",
            font=("Arial", 24, "bold"),
            bg="white"
        ).pack(pady=15)

        self.user = tk.StringVar()
        self.project = tk.StringVar()
        self.hours = tk.StringVar(value="0.00")

        form = tk.Frame(self.frame, bg="white")
        form.pack(pady=10)

        # Employee

        tk.Label(
            form,
            text="Employee",
            bg="white"
        ).grid(row=0, column=0, padx=10, pady=8)

        self.user_box = ttk.Combobox(
            form,
            textvariable=self.user,
            width=25,
            state="readonly"
        )

        self.user_box.grid(
            row=0,
            column=1,
            padx=10,
            pady=8
        )

        # Project

        tk.Label(
            form,
            text="Project",
            bg="white"
        ).grid(row=1, column=0, padx=10, pady=8)

        self.project_box = ttk.Combobox(
            form,
            textvariable=self.project,
            width=25,
            state="readonly"
        )

        self.project_box.grid(
            row=1,
            column=1,
            padx=10,
            pady=8
        )

        # Work Date

        tk.Label(
            form,
            text="Work Date",
            bg="white"
        ).grid(row=0, column=2, padx=10, pady=8)

        self.work_date = DateEntry(
            form,
            width=15,
            date_pattern="yyyy-mm-dd"
        )

        self.work_date.grid(
            row=0,
            column=3,
            padx=10,
            pady=8
        )

        # Hours

        tk.Label(
            form,
            text="Hours",
            bg="white"
        ).grid(row=1, column=2, padx=10, pady=8)

        tk.Entry(
            form,
            textvariable=self.hours,
            width=17
        ).grid(
            row=1,
            column=3,
            padx=10,
            pady=8
        )

        # Description

        tk.Label(
            form,
            text="Description",
            bg="white"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=8,
            sticky="nw"
        )

        self.description = tk.Text(
            form,
            width=35,
            height=4
        )

        self.description.grid(
            row=2,
            column=1,
            padx=10,
            pady=8
        )

        # Buttons

        button_frame = tk.Frame(
            self.frame,
            bg="white"
        )

        button_frame.pack(pady=10)

        if self.role_name == "Employee":

            tk.Button(
                button_frame,
                text="Add",
                width=15,
                command=self.add_timesheet
            ).pack(
                side="left",
                padx=5
            )

        else:

            tk.Button(
                button_frame,
                text="Approve",
                width=15,
                command=self.approve_timesheet
            ).pack(
                side="left",
                padx=5
            )

            tk.Button(
                button_frame,
                text="Delete",
                width=15,
                command=self.delete_timesheet
            ).pack(
                side="left",
                padx=5
            )

        tk.Button(
            button_frame,
            text="Clear",
            width=15,
            command=self.clear
        ).pack(
            side="left",
            padx=5
        )

        # Table

        columns = (
            "ID",
            "Employee",
            "Project",
            "Date",
            "Hours",
            "Description",
            "Approved"
        )

        self.table = ttk.Treeview(
            self.frame,
            columns=columns,
            show="headings"
        )

        for col in columns:

            self.table.heading(
                col,
                text=col
            )

        self.table.column("ID", width=60)
        self.table.column("Employee", width=150)
        self.table.column("Project", width=150)
        self.table.column("Date", width=110)
        self.table.column("Hours", width=80)
        self.table.column("Description", width=250)
        self.table.column("Approved", width=100)

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.table.bind(
            "<ButtonRelease-1>",
            self.select_timesheet
        )

    # =====================================
    # LOAD LOGGED-IN USER
    # =====================================

    def load_logged_in_user(self):

        self.users = {}

        if self.user_id is None:

            messagebox.showwarning(
                "Warning",
                "No logged-in user found."
            )

            return

        sql = """
            SELECT
                user_id,
                CONCAT(first_name, ' ', last_name) AS name
            FROM users
            WHERE user_id = %s
        """

        try:

            data = self.db.fetch_all(
                sql,
                (self.user_id,)
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        values = []

        for row in data:

            self.users[row["name"]] = row["user_id"]
            values.append(row["name"])

        self.user_box["values"] = values

        if values:

            self.user.set(values[0])

    # =====================================
    # LOAD PROJECTS
    # =====================================

    def load_projects(self):

        self.projects = {}

        try:

            data = self.db.fetch_all(
                """
                SELECT
                    project_id,
                    project_name
                FROM projects
                ORDER BY project_name
                """
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        values = []

        for row in data:

            self.projects[row["project_name"]] = row["project_id"]
            values.append(row["project_name"])

        self.project_box["values"] = values

    # =====================================
    # LOAD TIMESHEETS
    # =====================================

    def load_timesheets(self):

        for item in self.table.get_children():

            self.table.delete(item)

        sql = """
            SELECT
                t.timesheet_id,
                CONCAT(
                    u.first_name,
                    ' ',
                    u.last_name
                ) AS employee,
                p.project_name,
                t.work_date,
                t.hours_worked,
                t.description,
                t.approved
            FROM timesheets t
            LEFT JOIN users u
                ON t.user_id = u.user_id
            LEFT JOIN projects p
                ON t.project_id = p.project_id
            WHERE t.user_id = %s
            ORDER BY t.work_date DESC
        """

        try:

            data = self.db.fetch_all(
                sql,
                (self.user_id,)
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        for row in data:

            if row["approved"] in (
                1,
                True,
                "1",
                "True",
                "true"
            ):

                approved = "✓ Approved"

            else:

                approved = "Pending"

            self.table.insert(
                "",
                "end",
                values=(
                    row["timesheet_id"],
                    row["employee"],
                    row["project_name"],
                    row["work_date"],
                    row["hours_worked"],
                    row["description"],
                    approved
                )
            )

    # =====================================
    # ADD TIMESHEET
    # =====================================

    def add_timesheet(self):

        if self.project.get() == "":

            messagebox.showwarning(
                "Warning",
                "Please select a project."
            )

            return

        try:

            hours = float(
                self.hours.get()
            )

            if hours <= 0:

                messagebox.showwarning(
                    "Warning",
                    "Enter valid hours."
                )

                return

        except ValueError:

            messagebox.showwarning(
                "Warning",
                "Hours must be a number."
            )

            return

        description = self.description.get(
            "1.0",
            tk.END
        ).strip()

        try:

            self.db.execute(
                """
                INSERT INTO timesheets
                (
                    user_id,
                    project_id,
                    work_date,
                    hours_worked,
                    description,
                    approved
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    self.user_id,
                    self.projects[self.project.get()],
                    self.work_date.get(),
                    hours,
                    description,
                    False
                )
            )

            messagebox.showinfo(
                "Success",
                "Timesheet Added Successfully."
            )

            self.load_timesheets()
            self.clear()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =====================================
    # SELECT
    # =====================================

    def select_timesheet(self, event):

        item = self.table.focus()

        if not item:
            return

        values = self.table.item(
            item,
            "values"
        )

        if values:

            self.selected_id = values[0]

    # =====================================
    # APPROVE
    # =====================================

    def approve_timesheet(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Warning",
                "Select a timesheet first."
            )

            return

        try:

            self.db.execute(
                """
                UPDATE timesheets
                SET approved = TRUE
                WHERE timesheet_id = %s
                """,
                (self.selected_id,)
            )

            messagebox.showinfo(
                "Success",
                "Timesheet Approved."
            )

            self.selected_id = None

            self.load_timesheets()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =====================================
    # DELETE
    # =====================================

    def delete_timesheet(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Warning",
                "Select a timesheet first."
            )

            return

        answer = messagebox.askyesno(
            "Delete",
            "Do you want to delete this timesheet?"
        )

        if not answer:
            return

        try:

            self.db.execute(
                """
                DELETE FROM timesheets
                WHERE timesheet_id = %s
                """,
                (self.selected_id,)
            )

            messagebox.showinfo(
                "Success",
                "Timesheet Deleted."
            )

            self.selected_id = None

            self.load_timesheets()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =====================================
    # CLEAR
    # =====================================

    def clear(self):

        if self.users:

            employee_name = list(
                self.users.keys()
            )[0]

            self.user.set(
                employee_name
            )

        self.project.set("")

        self.hours.set("0.00")

        self.description.delete(
            "1.0",
            tk.END
        )

        self.selected_id = None