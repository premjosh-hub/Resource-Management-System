import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv



class Reports:


    def __init__(self, parent, db):

        self.parent = parent
        self.db = db

        self.current_data = []
        self.current_columns = []

        self.create_ui()



    # =========================
    # UI
    # =========================

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
            text="Reports",
            font=("Arial",24,"bold"),
            bg="white"
        ).pack(
            pady=15
        )



        button_frame = tk.Frame(
            self.frame,
            bg="white"
        )

        button_frame.pack()



        buttons = [

            ("Users", self.users_report),

            ("Departments", self.department_report),

            ("Projects", self.projects_report),

            ("Resources", self.resources_report),

            ("Assignments", self.assignment_report),

            ("Leave", self.leave_report),

            ("Timesheet", self.timesheet_report),

            ("Export CSV", self.export_csv)

        ]



        for text,command in buttons:

            tk.Button(
                button_frame,
                text=text,
                width=15,
                command=command
            ).pack(
                side="left",
                padx=3,
                pady=5
            )



        self.table = ttk.Treeview(
            self.frame
        )


        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )



    # =========================
    # Display Data
    # =========================

    def display_data(self, columns, data):


        self.table.delete(
            *self.table.get_children()
        )


        self.table["columns"] = columns

        self.table["show"] = "headings"



        for col in columns:

            self.table.heading(
                col,
                text=col
            )


            self.table.column(
                col,
                width=130
            )



        for row in data:


            self.table.insert(
                "",
                "end",
                values=[
                    row[col]
                    for col in columns
                ]
            )



        self.current_columns = columns

        self.current_data = data



    # =========================
    # Users Report
    # =========================

    def users_report(self):

        sql = """

        SELECT

        u.user_id,

        u.first_name,

        u.last_name,

        u.email,

        d.department_name,

        r.role_name,

        u.status


        FROM users u


        LEFT JOIN departments d

        ON u.department_id=d.department_id


        LEFT JOIN roles r

        ON u.role_id=r.role_id


        """



        data=self.db.fetch_all(sql)


        columns=[

            "user_id",
            "first_name",
            "last_name",
            "email",
            "department_name",
            "role_name",
            "status"

        ]


        self.display_data(
            columns,
            data
        )



    # =========================
    # Department Report
    # =========================

    def department_report(self):

        sql="""

        SELECT

        department_id,

        department_name,

        description,

        created_at


        FROM departments

        """



        data=self.db.fetch_all(sql)



        columns=[

            "department_id",
            "department_name",
            "description",
            "created_at"

        ]



        self.display_data(
            columns,
            data
        )



    # =========================
    # Project Report
    # =========================

    def projects_report(self):

        sql="""

        SELECT

        p.project_id,

        p.project_name,

        p.client_name,

        CONCAT(
        u.first_name,' ',
        u.last_name
        ) manager,

        p.budget,

        p.status


        FROM projects p


        LEFT JOIN users u

        ON p.project_manager=u.user_id


        """



        data=self.db.fetch_all(sql)



        columns=[

            "project_id",
            "project_name",
            "client_name",
            "manager",
            "budget",
            "status"

        ]


        self.display_data(
            columns,
            data
        )



    # =========================
    # Resource Report
    # =========================

    def resources_report(self):

        sql="""

        SELECT

        r.resource_id,

        r.resource_name,

        t.type_name,

        r.serial_number,

        r.value,

        r.status


        FROM resources r


        LEFT JOIN resource_types t

        ON r.type_id=t.type_id


        """



        data=self.db.fetch_all(sql)



        columns=[

            "resource_id",
            "resource_name",
            "type_name",
            "serial_number",
            "value",
            "status"

        ]


        self.display_data(
            columns,
            data
        )



    # =========================
    # Assignment Report
    # =========================

    def assignment_report(self):

        sql="""

        SELECT

        a.assignment_id,

        p.project_name,

        CONCAT(
        u.first_name,' ',
        u.last_name
        ) employee,

        r.resource_name,

        a.allocation_percent,

        a.assigned_from,

        a.assigned_to,

        a.assignment_status


        FROM assignments a


        LEFT JOIN projects p

        ON a.project_id=p.project_id


        LEFT JOIN users u

        ON a.user_id=u.user_id


        LEFT JOIN resources r

        ON a.resource_id=r.resource_id


        """



        data=self.db.fetch_all(sql)



        columns=[

            "assignment_id",
            "project_name",
            "employee",
            "resource_name",
            "allocation_percent",
            "assigned_from",
            "assigned_to",
            "assignment_status"

        ]



        self.display_data(
            columns,
            data
        )



    # =========================
    # Leave Report
    # =========================

    def leave_report(self):

        sql="""

        SELECT

        l.leave_id,

        CONCAT(
        u.first_name,' ',
        u.last_name
        ) employee,

        t.leave_name,

        l.start_date,

        l.end_date,

        l.status


        FROM leave_requests l


        LEFT JOIN users u

        ON l.user_id=u.user_id


        LEFT JOIN leave_types t

        ON l.leave_type_id=t.leave_type_id


        """



        data=self.db.fetch_all(sql)



        columns=[

            "leave_id",
            "employee",
            "leave_name",
            "start_date",
            "end_date",
            "status"

        ]


        self.display_data(
            columns,
            data
        )



    # =========================
    # Timesheet Report
    # =========================

    def timesheet_report(self):

        sql="""

        SELECT

        t.timesheet_id,

        CONCAT(
        u.first_name,' ',
        u.last_name
        ) employee,

        p.project_name,

        t.work_date,

        t.hours_worked,

        t.approved


        FROM timesheets t


        LEFT JOIN users u

        ON t.user_id=u.user_id


        LEFT JOIN projects p

        ON t.project_id=p.project_id


        """



        data=self.db.fetch_all(sql)



        columns=[

            "timesheet_id",
            "employee",
            "project_name",
            "work_date",
            "hours_worked",
            "approved"

        ]



        self.display_data(
            columns,
            data
        )



    # =========================
    # Export CSV
    # =========================

    def export_csv(self):


        if not self.current_data:

            messagebox.showwarning(
                "Export",
                "Generate report first"
            )

            return



        file=filedialog.asksaveasfilename(

            defaultextension=".csv",

            filetypes=[
                (
                    "CSV Files",
                    "*.csv"
                )
            ]

        )



        if file:


            with open(
                file,
                "w",
                newline="",
                encoding="utf-8"
            ) as f:


                writer=csv.DictWriter(
                    f,
                    fieldnames=self.current_columns
                )


                writer.writeheader()


                writer.writerows(
                    self.current_data
                )



            messagebox.showinfo(
                "Export",
                "CSV exported successfully"
            )