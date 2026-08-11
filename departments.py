import tkinter as tk
from tkinter import ttk, messagebox



class Departments:


    def __init__(self, parent, db):

        self.parent = parent
        self.db = db

        self.selected_id = None

        self.create_ui()

        self.load_departments()



    # ==================================
    # Create UI
    # ==================================

    def create_ui(self):


        self.frame = tk.Frame(

            self.parent,

            bg="white"

        )


        self.frame.pack(

            fill="both",

            expand=True

        )



        title = tk.Label(

            self.frame,

            text="Department Management",

            font=("Arial",24,"bold"),

            bg="white"

        )


        title.pack(

            pady=15

        )



        # Variables

        self.department_name = tk.StringVar()



        # Form Frame

        form = tk.Frame(

            self.frame,

            bg="white"

        )


        form.pack(

            pady=10

        )




        # Department Name

        tk.Label(

            form,

            text="Department Name",

            bg="white"

        ).grid(

            row=0,

            column=0,

            padx=10,

            pady=5

        )



        tk.Entry(

            form,

            textvariable=self.department_name,

            width=30

        ).grid(

            row=0,

            column=1,

            padx=10

        )




        # Description

        tk.Label(

            form,

            text="Description",

            bg="white"

        ).grid(

            row=1,

            column=0,

            padx=10,

            pady=5

        )



        self.description = tk.Text(

            form,

            width=30,

            height=4

        )


        self.description.grid(

            row=1,

            column=1,

            padx=10

        )





        # Buttons

        btn_frame = tk.Frame(

            self.frame,

            bg="white"

        )


        btn_frame.pack(

            pady=10

        )



        buttons = [

            ("Add", self.add_department),

            ("Update", self.update_department),

            ("Delete", self.delete_department),

            ("Clear", self.clear)

        ]



        for text, command in buttons:


            tk.Button(

                btn_frame,

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

            "Department Name",

            "Description",

            "Created Date"

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

                width=180

            )



        self.table.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=20

        )



        self.table.bind(

            "<ButtonRelease-1>",

            self.select_department

        )





    # ==================================
    # Load Departments
    # ==================================

    def load_departments(self):


        for row in self.table.get_children():

            self.table.delete(row)




        sql = """

        SELECT *

        FROM departments

        ORDER BY department_id DESC

        """



        data = self.db.fetch_all(sql)




        for dep in data:


            self.table.insert(

                "",

                "end",

                values=(

                    dep["department_id"],

                    dep["department_name"],

                    dep["description"],

                    dep["created_at"]

                )

            )





    # ==================================
    # Add Department
    # ==================================

    def add_department(self):


        if self.department_name.get().strip() == "":


            messagebox.showwarning(

                "Warning",

                "Enter department name"

            )

            return




        sql = """

        INSERT INTO departments

        (

        department_name,

        description

        )

        VALUES

        (%s,%s)

        """



        self.db.execute(

            sql,

            (

                self.department_name.get(),

                self.description.get(

                    "1.0",

                    tk.END

                ).strip()

            )

        )



        messagebox.showinfo(

            "Success",

            "Department Added Successfully"

        )



        self.load_departments()

        self.clear()





    # ==================================
    # Select Department
    # ==================================

    def select_department(self,event):


        selected = self.table.focus()


        data = self.table.item(selected)["values"]



        if data:


            self.selected_id = data[0]



            self.department_name.set(

                data[1]

            )



            self.description.delete(

                "1.0",

                tk.END

            )



            self.description.insert(

                tk.END,

                data[2]

            )





    # ==================================
    # Update Department
    # ==================================

    def update_department(self):


        if self.selected_id is None:


            messagebox.showwarning(

                "Warning",

                "Select department first"

            )


            return




        sql = """

        UPDATE departments

        SET

        department_name=%s,

        description=%s

        WHERE department_id=%s

        """



        self.db.execute(

            sql,

            (

                self.department_name.get(),

                self.description.get(

                    "1.0",

                    tk.END

                ).strip(),

                self.selected_id

            )

        )



        messagebox.showinfo(

            "Success",

            "Department Updated"

        )



        self.load_departments()

        self.clear()





    # ==================================
    # Delete Department
    # ==================================

    def delete_department(self):


        if self.selected_id is None:


            return




        answer = messagebox.askyesno(

            "Delete",

            "Delete this department?"

        )



        if answer:


            self.db.execute(

                """

                DELETE FROM departments

                WHERE department_id=%s

                """,

                (

                    self.selected_id,

                )

            )



            messagebox.showinfo(

                "Success",

                "Department Deleted"

            )



            self.load_departments()

            self.clear()





    # ==================================
    # Clear
    # ==================================

    def clear(self):


        self.department_name.set("")


        self.description.delete(

            "1.0",

            tk.END

        )


        self.selected_id = None