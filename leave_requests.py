import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


class LeaveRequests:


    def __init__(self, parent, db, user_id, role_name):

        self.parent = parent
        self.db = db

        self.user_id = user_id
        self.role_name = role_name

        self.selected_id = None

        self.create_ui()

        self.load_leave_types()

        self.load_requests()



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


        tk.Label(
            self.frame,
            text="Leave Request Management",
            font=("Arial",24,"bold"),
            bg="white"
        ).pack(pady=15)



        self.leave_type = tk.StringVar()

        self.status = tk.StringVar(
            value="Pending"
        )



        form = tk.Frame(
            self.frame,
            bg="white"
        )

        form.pack(pady=10)



        # Leave Type

        tk.Label(
            form,
            text="Leave Type",
            bg="white"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )


        self.type_box = ttk.Combobox(

            form,

            textvariable=self.leave_type,

            width=25,

            state="readonly"

        )


        self.type_box.grid(
            row=0,
            column=1
        )



        # Start Date

        tk.Label(
            form,
            text="Start Date",
            bg="white"
        ).grid(
            row=0,
            column=2
        )


        self.start_date = DateEntry(

            form,

            width=15,

            date_pattern="yyyy-mm-dd"

        )


        self.start_date.grid(
            row=0,
            column=3
        )



        # End Date


        tk.Label(
            form,
            text="End Date",
            bg="white"
        ).grid(
            row=1,
            column=2
        )


        self.end_date = DateEntry(

            form,

            width=15,

            date_pattern="yyyy-mm-dd"

        )


        self.end_date.grid(
            row=1,
            column=3
        )



        # Reason


        tk.Label(
            form,
            text="Reason",
            bg="white"
        ).grid(
            row=1,
            column=0
        )


        self.reason = tk.Text(

            form,

            width=30,

            height=4

        )


        self.reason.grid(
            row=1,
            column=1
        )



        # Status


        tk.Label(
            form,
            text="Status",
            bg="white"
        ).grid(
            row=2,
            column=0
        )


        self.status_box = ttk.Combobox(

            form,

            textvariable=self.status,

            values=[

                "Pending",

                "Approved",

                "Rejected"

            ],

            state="readonly"

        )


        self.status_box.grid(
            row=2,
            column=1
        )



        # Buttons


        buttons = tk.Frame(
            self.frame,
            bg="white"
        )


        buttons.pack(
            pady=10
        )



        if self.role_name == "Employee":


            button_list = [

                ("Submit", self.add_request),

                ("Clear", self.clear)

            ]


        else:


            button_list = [

                ("Approve", self.approve_request),

                ("Reject", self.reject_request),

                ("Delete", self.delete_request),

                ("Clear", self.clear)

            ]



        for text, command in button_list:


            tk.Button(

                buttons,

                text=text,

                width=15,

                command=command

            ).pack(

                side="left",

                padx=5

            )



        # Table


        columns = (

            "ID",

            "Employee",

            "Leave Type",

            "Start",

            "End",

            "Reason",

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

            self.select_request

        )



    # =====================================
    # Load Leave Types
    # =====================================


    def load_leave_types(self):


        data = self.db.fetch_all(

            """

            SELECT *

            FROM leave_types

            """

        )


        self.leave_types = {}

        values = []



        for row in data:


            self.leave_types[

                row["leave_name"]

            ] = row["leave_type_id"]


            values.append(

                row["leave_name"]

            )



        self.type_box["values"] = values

    # =====================================
    # Load Requests
    # =====================================


    def load_requests(self):


        for row in self.table.get_children():

            self.table.delete(row)



        if self.role_name == "Employee":


            sql = """

            SELECT

            l.leave_id,

            CONCAT(
            u.first_name,' ',
            u.last_name
            ) employee,

            t.leave_name,

            l.start_date,

            l.end_date,

            l.reason,

            l.status


            FROM leave_requests l


            LEFT JOIN users u

            ON l.user_id=u.user_id


            LEFT JOIN leave_types t

            ON l.leave_type_id=t.leave_type_id


            WHERE l.user_id=%s


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

            l.leave_id,

            CONCAT(
            u.first_name,' ',
            u.last_name
            ) employee,

            t.leave_name,

            l.start_date,

            l.end_date,

            l.reason,

            l.status


            FROM leave_requests l


            LEFT JOIN users u

            ON l.user_id=u.user_id


            LEFT JOIN leave_types t

            ON l.leave_type_id=t.leave_type_id


            """


            data = self.db.fetch_all(sql)




        for row in data:


            self.table.insert(

                "",

                "end",

                values=(

                    row["leave_id"],

                    row["employee"],

                    row["leave_name"],

                    row["start_date"],

                    row["end_date"],

                    row["reason"],

                    row["status"]

                )

            )





    # =====================================
    # Add Leave Request
    # =====================================


    def add_request(self):


        if self.leave_type.get() == "":


            messagebox.showwarning(

                "Warning",

                "Select leave type"

            )

            return



        self.db.execute(

            """

            INSERT INTO leave_requests

            (

            user_id,

            leave_type_id,

            start_date,

            end_date,

            reason,

            status

            )


            VALUES

            (%s,%s,%s,%s,%s,%s)


            """,

            (

                self.user_id,

                self.leave_types[self.leave_type.get()],

                self.start_date.get(),

                self.end_date.get(),

                self.reason.get(

                    "1.0",

                    tk.END

                ),

                "Pending"

            )

        )



        messagebox.showinfo(

            "Success",

            "Leave Request Submitted"

        )


        self.load_requests()

        self.clear()





    # =====================================
    # Select
    # =====================================


    def select_request(self,event):


        item = self.table.focus()


        data = self.table.item(item)["values"]


        if data:


            self.selected_id = data[0]





    # =====================================
    # Approve Leave
    # =====================================


    def approve_request(self):


        if self.selected_id:


            self.db.execute(

                """

                UPDATE leave_requests

                SET status='Approved'

                WHERE leave_id=%s


                """,

                (

                    self.selected_id,

                )

            )


            self.load_requests()





    # =====================================
    # Reject Leave
    # =====================================


    def reject_request(self):


        if self.selected_id:


            self.db.execute(

                """

                UPDATE leave_requests

                SET status='Rejected'

                WHERE leave_id=%s


                """,

                (

                    self.selected_id,

                )

            )


            self.load_requests()





    # =====================================
    # Delete
    # =====================================


    def delete_request(self):


        if self.selected_id:


            self.db.execute(

                """

                DELETE FROM leave_requests

                WHERE leave_id=%s


                """,

                (

                    self.selected_id,

                )

            )


            self.load_requests()

            self.clear()





    # =====================================
    # Clear
    # =====================================


    def clear(self):


        self.leave_type.set("")

        self.status.set("Pending")


        self.reason.delete(

            "1.0",

            tk.END

        )


        self.selected_id = None