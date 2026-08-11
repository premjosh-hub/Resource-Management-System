import tkinter as tk
from tkinter import ttk, messagebox


class Settings:

    def __init__(self, parent, db, user_id=None):

        self.parent = parent
        self.db = db
        self.user_id = user_id

        self.create_ui()

    # =====================================
    # UI
    # =====================================

    def create_ui(self):

        self.frame = tk.Frame(
            self.parent,
            bg="white"
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        # =====================================
        # Title
        # =====================================

        tk.Label(
            self.frame,
            text="System Settings",
            font=("Arial", 24, "bold"),
            bg="white"
        ).pack(
            pady=20
        )

        # =====================================
        # Database Status
        # =====================================

        db_frame = tk.LabelFrame(
            self.frame,
            text="Database Information",
            bg="white",
            font=("Arial", 12, "bold")
        )

        db_frame.pack(
            padx=40,
            pady=10,
            fill="x"
        )

        try:

            if self.db.connection is not None:
                status = "Connected"
            else:
                status = "Disconnected"

        except AttributeError:

            status = "Unknown"

        tk.Label(
            db_frame,
            text="MySQL Database : " + status,
            bg="white",
            font=("Arial", 12)
        ).pack(
            pady=10
        )

        # =====================================
        # Theme Settings
        # =====================================

        theme_frame = tk.LabelFrame(
            self.frame,
            text="Theme Settings",
            bg="white",
            font=("Arial", 12, "bold")
        )

        theme_frame.pack(
            padx=40,
            pady=10,
            fill="x"
        )

        self.theme = tk.StringVar(
            value="Light"
        )

        self.theme_box = ttk.Combobox(
            theme_frame,
            textvariable=self.theme,
            values=[
                "Light",
                "Dark"
            ],
            state="readonly",
            width=20
        )

        self.theme_box.pack(
            pady=10
        )

        tk.Button(
            theme_frame,
            text="Apply Theme",
            width=20,
            command=self.apply_theme
        ).pack(
            pady=10
        )

        # =====================================
        # Change Password
        # =====================================

        password_frame = tk.LabelFrame(
            self.frame,
            text="Change Password",
            bg="white",
            font=("Arial", 12, "bold")
        )

        password_frame.pack(
            padx=40,
            pady=10,
            fill="x"
        )

        self.old_password = tk.StringVar()
        self.new_password = tk.StringVar()

        # Old Password
        tk.Label(
            password_frame,
            text="Old Password",
            bg="white"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        tk.Entry(
            password_frame,
            textvariable=self.old_password,
            show="*",
            width=30
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # New Password
        tk.Label(
            password_frame,
            text="New Password",
            bg="white"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        tk.Entry(
            password_frame,
            textvariable=self.new_password,
            show="*",
            width=30
        ).grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        # Update Password Button
        tk.Button(
            password_frame,
            text="Update Password",
            width=20,
            command=self.change_password
        ).grid(
            row=2,
            column=1,
            pady=15
        )

        # =====================================
        # Application
        # =====================================

        app_frame = tk.LabelFrame(
            self.frame,
            text="Application",
            bg="white",
            font=("Arial", 12, "bold")
        )

        app_frame.pack(
            padx=40,
            pady=10,
            fill="x"
        )

        # =====================================
        # Logout Button
        # =====================================

        tk.Button(
            app_frame,
            text="Logout",
            width=20,
            bg="orange",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.logout
        ).pack(
            pady=5
        )

        # =====================================
        # Exit Button
        # =====================================

        tk.Button(
            app_frame,
            text="Exit",
            width=20,
            bg="red",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.exit_application
        ).pack(
            pady=5
        )

    # =====================================
    # Theme
    # =====================================

    def apply_theme(self):

        if self.theme.get() == "Dark":

            self.frame.configure(
                bg="#2C3E50"
            )

            messagebox.showinfo(
                "Theme",
                "Dark Theme Applied Successfully"
            )

        else:

            self.frame.configure(
                bg="white"
            )

            messagebox.showinfo(
                "Theme",
                "Light Theme Applied Successfully"
            )

    # =====================================
    # Change Password
    # =====================================

    def change_password(self):

        # Check logged-in user
        if self.user_id is None:

            messagebox.showwarning(
                "Warning",
                "No Logged-in User."
            )

            return

        # Get passwords
        old_password = self.old_password.get().strip()
        new_password = self.new_password.get().strip()

        # Check empty fields
        if old_password == "" or new_password == "":

            messagebox.showwarning(
                "Warning",
                "Enter Old and New Password."
            )

            return

        # =====================================
        # Check Old Password
        # =====================================

        sql = """
            SELECT *
            FROM users
            WHERE user_id = %s
            AND password_hash = %s
        """

        try:

            user = self.db.fetch_one(
                sql,
                (
                    self.user_id,
                    old_password
                )
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                "Unable to verify password.\n\n" + str(e)
            )

            return

        if user is None:

            messagebox.showerror(
                "Error",
                "Old Password Incorrect."
            )

            return

        # =====================================
        # Update Password
        # =====================================

        update_sql = """
            UPDATE users
            SET password_hash = %s
            WHERE user_id = %s
        """

        try:

            self.db.execute(
                update_sql,
                (
                    new_password,
                    self.user_id
                )
            )

            messagebox.showinfo(
                "Success",
                "Password Updated Successfully."
            )

            # Clear password fields
            self.old_password.set("")
            self.new_password.set("")

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                "Unable to update password.\n\n" + str(e)
            )

    # =====================================
    # Open Login Screen
    # =====================================

    def open_login(self):

        try:

            # Close the current application window
            current_window = self.parent.winfo_toplevel()

            current_window.destroy()

            # Import Login
            from login import Login

            # Create Login window
            login_root = tk.Tk()

            Login(login_root)

            login_root.mainloop()

        except Exception as e:

            messagebox.showerror(
                "Login Error",
                "Unable to open Login screen.\n\n" + str(e)
            )

    # =====================================
    # Logout
    # =====================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Do you want to logout?"
        )

        if not answer:
            return

        # Logout returns to Login screen
        self.open_login()

    # =====================================
    # Exit Application
    # =====================================

    def exit_application(self):

        answer = messagebox.askyesno(
            "Exit Application",
            "Do you really want to close the application?"
        )

        if not answer:
            return

        # Completely close the application
        self.parent.winfo_toplevel().destroy()