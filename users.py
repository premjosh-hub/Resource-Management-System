import tkinter as tk
from tkinter import ttk, messagebox


class Users:

    def __init__(self, parent, db):

        self.parent = parent
        self.db = db

        self.selected_id = None

        self.create_ui()

        self.load_departments()
        self.load_roles()
        self.load_users()

    # ==============================
    # UI
    # ==============================

    def create_ui(self):

        self.frame = tk.Frame(
            self.parent,
            bg="white"
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            self.frame,
            text="User Management",
            font=("Arial", 24, "bold"),
            bg="white"
        ).pack(pady=10)

        # Variables

        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.phone = tk.StringVar()
        self.job_title = tk.StringVar()
        self.department_name = tk.StringVar()
        self.role_name = tk.StringVar()

        form = tk.Frame(
            self.frame,
            bg="white"
        )

        form.pack(pady=10)

        fields = [

            ("First Name", self.first_name),
            ("Last Name", self.last_name),
            ("Email", self.email),
            ("Password", self.password),
            ("Phone", self.phone),
            ("Job Title", self.job_title)

        ]

        row = 0

        for label, var in fields:

            tk.Label(
                form,
                text=label,
                bg="white"
            ).grid(
                row=row,
                column=0,
                padx=10,
                pady=5,
                sticky="w"
            )

            tk.Entry(
                form,
                textvariable=var,
                width=25
            ).grid(
                row=row,
                column=1,
                padx=10,
                pady=5
            )

            row += 1

        # ==============================
        # Department
        # ==============================

        tk.Label(
            form,
            text="Department",
            bg="white"
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.department = ttk.Combobox(
            form,
            textvariable=self.department_name,
            width=25,
            state="readonly"
        )

        self.department.grid(
            row=0,
            column=3,
            padx=10,
            pady=5
        )

        # ==============================
        # Role
        # ==============================

        tk.Label(
            form,
            text="Role",
            bg="white"
        ).grid(
            row=1,
            column=2,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.role = ttk.Combobox(
            form,
            textvariable=self.role_name,
            width=25,
            state="readonly"
        )

        self.role.grid(
            row=1,
            column=3,
            padx=10,
            pady=5
        )

        # ==============================
        # Buttons
        # ==============================

        btn = tk.Frame(
            self.frame,
            bg="white"
        )

        btn.pack(pady=10)

        tk.Button(
            btn,
            text="Add",
            width=15,
            command=self.add_user
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            btn,
            text="Update",
            width=15,
            command=self.update_user
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            btn,
            text="Delete",
            width=15,
            command=self.delete_user
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            btn,
            text="Clear",
            width=15,
            command=self.clear
        ).pack(
            side="left",
            padx=5
        )

        # ==============================
        # Table
        # ==============================

        columns = (
            "ID",
            "First Name",
            "Last Name",
            "Email",
            "Phone",
            "Department",
            "Role",
            "Status"
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

        self.table.column(
            "ID",
            width=60
        )

        self.table.column(
            "First Name",
            width=120
        )

        self.table.column(
            "Last Name",
            width=120
        )

        self.table.column(
            "Email",
            width=180
        )

        self.table.column(
            "Phone",
            width=120
        )

        self.table.column(
            "Department",
            width=130
        )

        self.table.column(
            "Role",
            width=120
        )

        self.table.column(
            "Status",
            width=100
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.table.bind(
            "<ButtonRelease-1>",
            self.select_user
        )

    # ==============================
    # Load Departments
    # ==============================

    def load_departments(self):

        try:

            data = self.db.fetch_all(
                """
                SELECT
                    department_id,
                    department_name
                FROM departments
                ORDER BY department_name
                """
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                "Unable to load departments.\n\n" + str(e)
            )

            return

        self.departments = {}

        values = []

        for row in data:

            self.departments[
                row["department_name"]
            ] = row["department_id"]

            values.append(
                row["department_name"]
            )

        self.department["values"] = values

    # ==============================
    # Load Roles
    # ==============================

    def load_roles(self):

        try:

            data = self.db.fetch_all(
                """
                SELECT
                    role_id,
                    role_name
                FROM roles
                ORDER BY role_name
                """
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                "Unable to load roles.\n\n" + str(e)
            )

            return

        self.roles = {}

        values = []

        for row in data:

            self.roles[
                row["role_name"]
            ] = row["role_id"]

            values.append(
                row["role_name"]
            )

        self.role["values"] = values

    # ==============================
    # Load Users
    # ==============================

    def load_users(self):

        for row in self.table.get_children():

            self.table.delete(row)

        sql = """
            SELECT

                u.user_id,

                u.first_name,

                u.last_name,

                u.email,

                u.phone,

                d.department_name,

                r.role_name,

                u.status

            FROM users u

            LEFT JOIN departments d
                ON u.department_id = d.department_id

            LEFT JOIN roles r
                ON u.role_id = r.role_id

            ORDER BY u.user_id
        """

        try:

            data = self.db.fetch_all(
                sql
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                "Unable to load users.\n\n" + str(e)
            )

            return

        for user in data:

            self.table.insert(
                "",
                "end",
                values=(

                    user["user_id"],

                    user["first_name"],

                    user["last_name"],

                    user["email"],

                    user["phone"],

                    user["department_name"],

                    user["role_name"],

                    user["status"]

                )
            )

    # ==============================
    # Validate Form
    # ==============================

    def validate_form(self):

        first_name = self.first_name.get().strip()
        last_name = self.last_name.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        job_title = self.job_title.get().strip()
        department = self.department_name.get().strip()
        role = self.role_name.get().strip()

        if first_name == "":

            messagebox.showwarning(
                "Warning",
                "Please enter first name."
            )

            return False

        if last_name == "":

            messagebox.showwarning(
                "Warning",
                "Please enter last name."
            )

            return False

        if email == "":

            messagebox.showwarning(
                "Warning",
                "Please enter email."
            )

            return False

        if "@" not in email:

            messagebox.showwarning(
                "Warning",
                "Please enter a valid email address."
            )

            return False

        if department == "":

            messagebox.showwarning(
                "Warning",
                "Please select department."
            )

            return False

        if department not in self.departments:

            messagebox.showwarning(
                "Warning",
                "Selected department is invalid."
            )

            return False

        if role == "":

            messagebox.showwarning(
                "Warning",
                "Please select user role."
            )

            return False

        if role not in self.roles:

            messagebox.showwarning(
                "Warning",
                "Selected role is invalid."
            )

            return False

        return True

    # ==============================
    # Check Duplicate Email
    # ==============================

    def email_exists(self, email, user_id=None):

        if user_id is None:

            sql = """
                SELECT user_id
                FROM users
                WHERE email = %s
            """

            params = (
                email,
            )

        else:

            sql = """
                SELECT user_id
                FROM users
                WHERE email = %s
                AND user_id != %s
            """

            params = (
                email,
                user_id
            )

        try:

            result = self.db.fetch_one(
                sql,
                params
            )

            return result is not None

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                "Unable to check email.\n\n" + str(e)
            )

            return True

    # ==============================
    # Add User
    # ==============================

    def add_user(self):

        if not self.validate_form():

            return

        first_name = self.first_name.get().strip()
        last_name = self.last_name.get().strip()
        email = self.email.get().strip()
        password = self.password.get().strip()
        phone = self.phone.get().strip()
        job_title = self.job_title.get().strip()
        department = self.department_name.get()
        role = self.role_name.get()

        if password == "":

            messagebox.showwarning(
                "Warning",
                "Please enter password."
            )

            return

        # Check duplicate email

        if self.email_exists(email):

            messagebox.showerror(
                "Duplicate Email",
                "The email '" + email +
                "' already exists.\n\n"
                "Please use a different email address."
            )

            return

        sql = """
            INSERT INTO users
            (
                first_name,
                last_name,
                email,
                password_hash,
                phone,
                department_id,
                role_id,
                job_title,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                'Active'
            )
        """

        try:

            self.db.execute(
                sql,
                (
                    first_name,
                    last_name,
                    email,
                    password,
                    phone,
                    self.departments[department],
                    self.roles[role],
                    job_title
                )
            )

            messagebox.showinfo(
                "Success",
                "User Created Successfully."
            )

            self.load_users()

            self.clear()

        except Exception as e:

            error_text = str(e)

            if "Duplicate entry" in error_text:

                messagebox.showerror(
                    "Duplicate Email",
                    "This email address already exists."
                )

            else:

                messagebox.showerror(
                    "Database Error",
                    error_text
                )

    # ==============================
    # Select User
    # ==============================

    def select_user(self, event):

        item = self.table.focus()

        if not item:

            return

        data = self.table.item(
            item,
            "values"
        )

        if not data:

            return

        self.selected_id = data[0]

        # First Name

        self.first_name.set(
            data[1]
        )

        # Last Name

        self.last_name.set(
            data[2]
        )

        # Email

        self.email.set(
            data[3]
        )

        # Phone

        self.phone.set(
            data[4]
        )

        # Department

        department_name = data[5]

        if department_name in self.departments:

            self.department_name.set(
                department_name
            )

        else:

            self.department_name.set("")

        # Role

        role_name = data[6]

        if role_name in self.roles:

            self.role_name.set(
                role_name
            )

        else:

            self.role_name.set("")

        # Status is not currently editable

    # ==============================
    # Update User
    # ==============================

    def update_user(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Warning",
                "Please select a user first."
            )

            return

        if not self.validate_form():

            return

        first_name = self.first_name.get().strip()
        last_name = self.last_name.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        job_title = self.job_title.get().strip()
        department = self.department_name.get()
        role = self.role_name.get()

        # Check duplicate email

        if self.email_exists(
            email,
            self.selected_id
        ):

            messagebox.showerror(
                "Duplicate Email",
                "The email '" + email +
                "' is already used by another user."
            )

            return

        sql = """
            UPDATE users
            SET

                first_name = %s,

                last_name = %s,

                email = %s,

                phone = %s,

                department_id = %s,

                job_title = %s,

                role_id = %s

            WHERE user_id = %s
        """

        try:

            self.db.execute(
                sql,
                (
                    first_name,
                    last_name,
                    email,
                    phone,
                    self.departments[department],
                    job_title,
                    self.roles[role],
                    self.selected_id
                )
            )

            messagebox.showinfo(
                "Success",
                "User Updated Successfully."
            )

            self.load_users()

            self.clear()

        except Exception as e:

            error_text = str(e)

            if "Duplicate entry" in error_text:

                messagebox.showerror(
                    "Duplicate Email",
                    "This email address already exists."
                )

            else:

                messagebox.showerror(
                    "Database Error",
                    error_text
                )

    # ==============================
    # Delete User
    # ==============================

    def delete_user(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Warning",
                "Please select a user first."
            )

            return

        answer = messagebox.askyesno(
            "Delete User",
            "Are you sure you want to delete this user?"
        )

        if not answer:

            return

        try:

            self.db.execute(
                """
                DELETE FROM users
                WHERE user_id = %s
                """,
                (
                    self.selected_id,
                )
            )

            messagebox.showinfo(
                "Success",
                "User Deleted Successfully."
            )

            self.selected_id = None

            self.load_users()

            self.clear()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                "Unable to delete user.\n\n" + str(e)
            )

    # ==============================
    # Clear
    # ==============================

    def clear(self):

        self.first_name.set("")
        self.last_name.set("")
        self.email.set("")
        self.password.set("")
        self.phone.set("")
        self.job_title.set("")
        self.department_name.set("")
        self.role_name.set("")

        self.selected_id = None

        # Remove table selection

        for item in self.table.selection():

            self.table.selection_remove(item)