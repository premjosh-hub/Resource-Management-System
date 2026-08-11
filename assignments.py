import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry



class Assignments:


    def __init__(self, parent, db, user_id, role_name):

        self.parent = parent

        self.db = db

        self.user_id = user_id

        self.role_name = role_name

        self.selected_id = None


        self.create_ui()

        self.load_projects()

        self.load_users()

        self.load_resources()

        self.load_assignments()



    # ======================================
    # UI
    # ======================================


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

            text="Project Assignment Management",

            font=("Arial",24,"bold"),

            bg="white"

        ).pack(

            pady=15

        )



        self.project = tk.StringVar()

        self.user = tk.StringVar()

        self.resource = tk.StringVar()

        self.percent = tk.StringVar(

            value="100"

        )

        self.status = tk.StringVar(

            value="Assigned"

        )




        form = tk.Frame(

            self.frame,

            bg="white"

        )


        form.pack(

            pady=10

        )




        # Project


        tk.Label(

            form,

            text="Project",

            bg="white"

        ).grid(

            row=0,

            column=0,

            padx=10,

            pady=5

        )


        self.project_box = ttk.Combobox(

            form,

            textvariable=self.project,

            width=25,

            state="readonly"

        )


        self.project_box.grid(

            row=0,

            column=1

        )





        # Employee


        tk.Label(

            form,

            text="Employee",

            bg="white"

        ).grid(

            row=1,

            column=0,

            padx=10

        )


        self.user_box = ttk.Combobox(

            form,

            textvariable=self.user,

            width=25,

            state="readonly"

        )


        self.user_box.grid(

            row=1,

            column=1

        )





        # Resource


        tk.Label(

            form,

            text="Resource",

            bg="white"

        ).grid(

            row=2,

            column=0,

            padx=10

        )



        self.resource_box = ttk.Combobox(

            form,

            textvariable=self.resource,

            width=25,

            state="readonly"

        )


        self.resource_box.grid(

            row=2,

            column=1

        )





        # Allocation


        tk.Label(

            form,

            text="Allocation %",

            bg="white"

        ).grid(

            row=0,

            column=2

        )



        tk.Entry(

            form,

            textvariable=self.percent,

            width=20

        ).grid(

            row=0,

            column=3

        )





        # From Date


        tk.Label(

            form,

            text="From Date",

            bg="white"

        ).grid(

            row=1,

            column=2

        )


        self.from_date = DateEntry(

            form,

            width=18,

            date_pattern="yyyy-mm-dd"

        )


        self.from_date.grid(

            row=1,

            column=3

        )





        # To Date


        tk.Label(

            form,

            text="To Date",

            bg="white"

        ).grid(

            row=2,

            column=2

        )


        self.to_date = DateEntry(

            form,

            width=18,

            date_pattern="yyyy-mm-dd"

        )


        self.to_date.grid(

            row=2,

            column=3

        )





        # Status


        tk.Label(

            form,

            text="Status",

            bg="white"

        ).grid(

            row=3,

            column=0

        )



        self.status_box = ttk.Combobox(

            form,

            textvariable=self.status,

            values=[

                "Assigned",

                "Completed",

                "Cancelled"

            ],

            state="readonly"

        )


        self.status_box.grid(

            row=3,

            column=1

        )





        # Buttons


        button_frame = tk.Frame(

            self.frame,

            bg="white"

        )


        button_frame.pack(

            pady=10

        )



        self.add_btn = tk.Button(

            button_frame,

            text="Assign",

            width=15,

            command=self.add_assignment

        )


        self.add_btn.pack(

            side="left",

            padx=5

        )



        self.update_btn = tk.Button(

            button_frame,

            text="Update",

            width=15,

            command=self.update_assignment

        )


        self.update_btn.pack(

            side="left",

            padx=5

        )



        self.delete_btn = tk.Button(

            button_frame,

            text="Delete",

            width=15,

            command=self.delete_assignment

        )


        self.delete_btn.pack(

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





        # Employee restriction


        if self.role_name == "Employee":


            self.add_btn.config(

                state="disabled"

            )


            self.update_btn.config(

                state="disabled"

            )


            self.delete_btn.config(

                state="disabled"

            )



        # Table


        columns = (

            "ID",

            "Project",

            "Employee",

            "Resource",

            "Allocation",

            "From",

            "To",

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

                col,

                width=130

            )



        self.table.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=20

        )



        self.table.bind(

            "<ButtonRelease-1>",

            self.select_assignment

        )

    # ======================================
    # Load Projects
    # ======================================


    def load_projects(self):


        data = self.db.fetch_all(

            """

            SELECT

            project_id,

            project_name

            FROM projects

            """

        )


        self.projects = {}

        values = []


        for row in data:


            self.projects[

                row["project_name"]

            ] = row["project_id"]



            values.append(

                row["project_name"]

            )


        self.project_box["values"] = values





    # ======================================
    # Load Users
    # ======================================


    def load_users(self):


        data = self.db.fetch_all(

            """

            SELECT

            user_id,

            CONCAT(first_name,' ',last_name) name

            FROM users

            """

        )


        self.users = {}

        values = []



        for row in data:


            self.users[

                row["name"]

            ] = row["user_id"]



            values.append(

                row["name"]

            )



        self.user_box["values"] = values





    # ======================================
    # Load Resources
    # ======================================


    def load_resources(self):


        data = self.db.fetch_all(

            """

            SELECT

            resource_id,

            resource_name

            FROM resources

            """

        )


        self.resources = {}

        values = []



        for row in data:


            self.resources[

                row["resource_name"]

            ] = row["resource_id"]



            values.append(

                row["resource_name"]

            )



        self.resource_box["values"] = values





    # ======================================
    # Load Assignments
    # ======================================


    def load_assignments(self):


        for row in self.table.get_children():

            self.table.delete(row)



        if self.role_name == "Employee":


            sql = """

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


            WHERE a.user_id=%s


            """



            data = self.db.fetch_all(

                sql,

                (

                    self.user_id,

                )

            )



        else:


            sql = """

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



            data = self.db.fetch_all(sql)




        for row in data:


            self.table.insert(

                "",

                "end",

                values=(

                    row["assignment_id"],

                    row["project_name"],

                    row["employee"],

                    row["resource_name"],

                    row["allocation_percent"],

                    row["assigned_from"],

                    row["assigned_to"],

                    row["assignment_status"]

                )

            )





    # ======================================
    # Add Assignment
    # ======================================


    def add_assignment(self):


        if self.project.get() == "":


            messagebox.showwarning(

                "Warning",

                "Select project"

            )

            return



        if self.user.get() == "":


            messagebox.showwarning(

                "Warning",

                "Select employee"

            )

            return




        self.db.execute(

            """

            INSERT INTO assignments

            (

            project_id,

            user_id,

            resource_id,

            allocation_percent,

            assigned_from,

            assigned_to,

            assignment_status

            )


            VALUES

            (%s,%s,%s,%s,%s,%s,%s)


            """,

            (

                self.projects[self.project.get()],

                self.users[self.user.get()],

                self.resources[self.resource.get()],

                self.percent.get(),

                self.from_date.get(),

                self.to_date.get(),

                self.status.get()

            )

        )



        messagebox.showinfo(

            "Success",

            "Assignment Created"

        )


        self.load_assignments()

        self.clear()





    # ======================================
    # Select
    # ======================================


    def select_assignment(self,event):


        item = self.table.focus()


        data = self.table.item(item)["values"]



        if data:


            self.selected_id = data[0]





    # ======================================
    # Update
    # ======================================


    def update_assignment(self):


        if self.selected_id is None:

            return



        self.db.execute(

            """

            UPDATE assignments SET


            allocation_percent=%s,

            assigned_from=%s,

            assigned_to=%s,

            assignment_status=%s


            WHERE assignment_id=%s


            """,

            (

                self.percent.get(),

                self.from_date.get(),

                self.to_date.get(),

                self.status.get(),

                self.selected_id

            )

        )



        self.load_assignments()

        self.clear()





    # ======================================
    # Delete
    # ======================================


    def delete_assignment(self):


        if self.selected_id:


            self.db.execute(

                """

                DELETE FROM assignments

                WHERE assignment_id=%s


                """,

                (

                    self.selected_id,

                )

            )


            self.load_assignments()

            self.clear()





    # ======================================
    # Clear
    # ======================================


    def clear(self):


        self.project.set("")

        self.user.set("")

        self.resource.set("")

        self.percent.set("100")

        self.status.set("Assigned")


        self.selected_id = None