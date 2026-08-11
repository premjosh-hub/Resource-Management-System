import tkinter as tk

from database import Database

from dashboard import Dashboard
from users import Users
from departments import Departments
from projects import Projects
from resources import Resources
from assignments import Assignments
from leave_requests import LeaveRequests
from timesheets import Timesheets
from reports import Reports
from settings import Settings


class ResourceManagementApp:

    def __init__(self, root, user_id, role_name):

        self.root = root
        self.user_id = user_id
        self.role_name = role_name

        self.root.title(
            "Resource Management System"
        )

        self.root.geometry(
            "1200x700"
        )

        self.root.minsize(
            1000,
            600
        )

        self.db = Database()

        self.create_ui()

    # ==================================
    # CREATE UI
    # ==================================

    def create_ui(self):

        # ==================================
        # LEFT SIDEBAR
        # ==================================

        self.menu = tk.Frame(
            self.root,
            bg="#2C3E50",
            width=220
        )

        self.menu.pack(
            side="left",
            fill="y"
        )

        self.menu.pack_propagate(False)

        # ==================================
        # CONTENT AREA
        # ==================================

        self.content = tk.Frame(
            self.root,
            bg="white"
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ==================================
        # ROLE TITLE
        # ==================================

        tk.Label(
            self.menu,
            text="Resource Management",
            bg="#2C3E50",
            fg="white",
            font=("Arial", 14, "bold")
        ).pack(
            pady=(20, 5)
        )

        tk.Label(
            self.menu,
            text="Role: " + str(self.role_name),
            bg="#2C3E50",
            fg="#D5D8DC",
            font=("Arial", 11)
        ).pack(
            pady=(0, 20)
        )

        # ==================================
        # ADMIN
        # ==================================

        if self.role_name == "Admin":

            buttons = [

                ("Dashboard", self.show_dashboard),

                ("Users", self.show_users),

                ("Departments", self.show_departments),

                ("Projects", self.show_projects),

                ("Resources", self.show_resources),

                ("Assignments", self.show_assignments),

                ("Leave Requests", self.show_leave),

                ("Timesheets", self.show_timesheets),

                ("Reports", self.show_reports),

                ("Settings", self.show_settings)

            ]

        # ==================================
        # MANAGER
        # ==================================

        elif self.role_name == "Manager":

            buttons = [

                ("Dashboard", self.show_dashboard),

                ("Projects", self.show_projects),

                ("Assignments", self.show_assignments),

                ("Leave Approval", self.show_leave),

                ("Timesheet Approval", self.show_timesheets),

                ("Reports", self.show_reports),

                ("Settings", self.show_settings)

            ]

        # ==================================
        # NORMAL USER
        # ==================================

        else:

            buttons = [

                ("Dashboard", self.show_dashboard),

                ("My Assignments", self.show_assignments),

                ("Apply Leave", self.show_leave),

                ("My Timesheets", self.show_timesheets),

                ("Settings", self.show_settings)

            ]

        # ==================================
        # SIDEBAR BUTTONS
        # ==================================

        for text, command in buttons:

            tk.Button(
                self.menu,
                text=text,
                width=22,
                command=command,
                bg="#34495E",
                fg="white",
                activebackground="#1ABC9C",
                activeforeground="white",
                relief="flat",
                font=("Arial", 10, "bold"),
                cursor="hand2"
            ).pack(
                pady=4,
                padx=10
            )

        # ==================================
        # SHOW DASHBOARD
        # ==================================

        self.show_dashboard()

    # ==================================
    # CLEAR CONTENT
    # ==================================

    def clear(self):

        for widget in self.content.winfo_children():

            widget.destroy()

    # ==================================
    # DASHBOARD
    # ==================================

    def show_dashboard(self):

        self.clear()

        Dashboard(
            self.content,
            self.db
        )

    # ==================================
    # USERS
    # ==================================

    def show_users(self):

        self.clear()

        Users(
            self.content,
            self.db
        )

    # ==================================
    # DEPARTMENTS
    # ==================================

    def show_departments(self):

        self.clear()

        Departments(
            self.content,
            self.db
        )

    # ==================================
    # PROJECTS
    # ==================================

    def show_projects(self):

        self.clear()

        Projects(
            self.content,
            self.db
        )

    # ==================================
    # RESOURCES
    # ==================================

    def show_resources(self):

        self.clear()

        Resources(
            self.content,
            self.db
        )

    # ==================================
    # ASSIGNMENTS
    # ==================================

    def show_assignments(self):

        self.clear()

        Assignments(
            self.content,
            self.db,
            self.user_id,
            self.role_name
        )

    # ==================================
    # LEAVE REQUESTS
    # ==================================

    def show_leave(self):

        self.clear()

        LeaveRequests(
            self.content,
            self.db,
            self.user_id,
            self.role_name
        )

    # ==================================
    # TIMESHEETS
    # ==================================

    def show_timesheets(self):

        self.clear()

        Timesheets(
            self.content,
            self.db,
            self.user_id,
            self.role_name
        )

    # ==================================
    # REPORTS
    # ==================================

    def show_reports(self):

        self.clear()

        Reports(
            self.content,
            self.db
        )

    # ==================================
    # SETTINGS
    # ==================================

    def show_settings(self):

        self.clear()

        Settings(
            self.content,
            self.db,
            self.user_id
        )


# ==================================
# TEST RUN ONLY
# ==================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ResourceManagementApp(
        root,
        1,
        "Admin"
    )

    root.mainloop()