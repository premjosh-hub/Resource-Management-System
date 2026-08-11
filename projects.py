import tkinter as tk
from tkinter import ttk, messagebox



class Projects:


    def __init__(self, parent, db):

        self.parent = parent
        self.db = db

        self.selected_id = None

        self.create_ui()

        self.load_managers()

        self.load_projects()



    # =================================
    # CREATE UI
    # =================================

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
            text="Project Management",
            font=("Arial",24,"bold"),
            bg="white"
        ).pack(
            pady=15
        )



        # Variables

        self.project_name = tk.StringVar()

        self.client_name = tk.StringVar()

        self.budget = tk.StringVar()

        self.start_date = tk.StringVar()

        self.end_date = tk.StringVar()

        self.manager = tk.StringVar()

        self.status = tk.StringVar(
            value="Planning"
        )



        form = tk.Frame(
            self.frame,
            bg="white"
        )

        form.pack(
            pady=10
        )



        fields=[

            ("Project Name",self.project_name),

            ("Client Name",self.client_name),

            ("Budget",self.budget),

            ("Start Date",self.start_date),

            ("End Date",self.end_date)

        ]



        row=0


        for label,var in fields:


            tk.Label(
                form,
                text=label,
                bg="white"
            ).grid(
                row=row,
                column=0,
                padx=10,
                pady=5
            )


            tk.Entry(
                form,
                textvariable=var,
                width=30
            ).grid(
                row=row,
                column=1
            )


            row+=1




        # Manager

        tk.Label(
            form,
            text="Project Manager",
            bg="white"
        ).grid(
            row=0,
            column=2
        )



        self.manager_box=ttk.Combobox(
            form,
            textvariable=self.manager,
            width=25
        )


        self.manager_box.grid(
            row=0,
            column=3
        )




        # Status


        tk.Label(
            form,
            text="Status",
            bg="white"
        ).grid(
            row=1,
            column=2
        )



        self.status_box=ttk.Combobox(

            form,

            textvariable=self.status,

            values=[

                "Planning",

                "Active",

                "Completed",

                "On Hold",

                "Cancelled"

            ],

            width=25

        )


        self.status_box.grid(
            row=1,
            column=3
        )





        # Buttons

        btn=tk.Frame(
            self.frame,
            bg="white"
        )

        btn.pack(
            pady=10
        )



        for text,cmd in [

            ("Add",self.add_project),

            ("Update",self.update_project),

            ("Delete",self.delete_project),

            ("Clear",self.clear)

        ]:


            tk.Button(

                btn,

                text=text,

                width=15,

                command=cmd

            ).pack(

                side="left",

                padx=5

            )






        # Table

        columns=(

            "ID",

            "Project Name",

            "Client",

            "Manager",

            "Budget",

            "Start",

            "End",

            "Status"

        )



        self.table=ttk.Treeview(

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

            self.select_project

        )





    # =================================
    # LOAD MANAGERS
    # =================================

    def load_managers(self):


        users=self.db.fetch_all(

            """

            SELECT user_id,first_name,last_name

            FROM users

            """

        )


        self.managers={}

        values=[]



        for user in users:


            name=(

                user["first_name"]

                +" "

                +user["last_name"]

            )


            self.managers[name]=user["user_id"]


            values.append(name)



        self.manager_box["values"]=values





    # =================================
    # LOAD PROJECTS
    # =================================

    def load_projects(self):


        for row in self.table.get_children():

            self.table.delete(row)



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

        p.start_date,

        p.end_date,

        p.status



        FROM projects p


        LEFT JOIN users u

        ON p.project_manager=u.user_id


        """



        data=self.db.fetch_all(sql)



        for p in data:


            self.table.insert(

                "",

                "end",

                values=(

                    p["project_id"],

                    p["project_name"],

                    p["client_name"],

                    p["manager"],

                    p["budget"],

                    p["start_date"],

                    p["end_date"],

                    p["status"]

                )

            )






    # =================================
    # ADD PROJECT
    # =================================

    def add_project(self):


        if self.project_name.get()=="":


            messagebox.showwarning(

                "Warning",

                "Enter project name"

            )

            return




        sql="""


        INSERT INTO projects


        (

        project_name,

        client_name,

        project_manager,

        start_date,

        end_date,

        budget,

        status

        )


        VALUES

        (%s,%s,%s,%s,%s,%s,%s)


        """



        self.db.execute(

            sql,

            (

                self.project_name.get(),

                self.client_name.get(),

                self.managers[self.manager.get()],


                self.start_date.get(),

                self.end_date.get(),

                self.budget.get(),

                self.status.get()

            )

        )



        messagebox.showinfo(

            "Success",

            "Project Added"

        )



        self.load_projects()

        self.clear()





    # =================================
    # SELECT
    # =================================

    def select_project(self,event):


        selected=self.table.focus()


        data=self.table.item(selected)["values"]



        if data:


            self.selected_id=data[0]


            self.project_name.set(data[1])

            self.client_name.set(data[2])

            self.budget.set(data[4])

            self.start_date.set(data[5])

            self.end_date.set(data[6])

            self.status.set(data[7])





    # =================================
    # UPDATE
    # =================================

    def update_project(self):


        if self.selected_id is None:

            return



        sql="""


        UPDATE projects SET


        project_name=%s,

        client_name=%s,

        budget=%s,

        start_date=%s,

        end_date=%s,

        status=%s



        WHERE project_id=%s


        """



        self.db.execute(

            sql,

            (

                self.project_name.get(),

                self.client_name.get(),

                self.budget.get(),

                self.start_date.get(),

                self.end_date.get(),

                self.status.get(),

                self.selected_id

            )

        )


        self.load_projects()

        self.clear()





    # =================================
    # DELETE
    # =================================

    def delete_project(self):


        if self.selected_id:


            answer=messagebox.askyesno(

                "Delete",

                "Delete this project?"

            )


            if answer:


                self.db.execute(

                    """

                    DELETE FROM projects

                    WHERE project_id=%s

                    """,

                    (

                        self.selected_id,

                    )

                )


                messagebox.showinfo(

                    "Success",

                    "Project Deleted"

                )


                self.load_projects()

                self.clear()





    # =================================
    # CLEAR
    # =================================

    def clear(self):


        self.project_name.set("")

        self.client_name.set("")

        self.budget.set("")

        self.start_date.set("")

        self.end_date.set("")

        self.manager.set("")

        self.status.set("Planning")


        self.selected_id=None