import tkinter as tk
from tkinter import ttk, messagebox



class Resources:


    def __init__(self, parent, db):

        self.parent = parent
        self.db = db

        self.selected_id = None

        self.create_ui()

        self.load_types()

        self.load_resources()



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
            text="Resource Management",
            font=("Arial",24,"bold"),
            bg="white"
        ).pack(
            pady=15
        )



        self.resource_name = tk.StringVar()

        self.serial_number = tk.StringVar()

        self.purchase_date = tk.StringVar()

        self.value = tk.StringVar()

        self.resource_type = tk.StringVar()

        self.status = tk.StringVar(
            value="Available"
        )



        form=tk.Frame(
            self.frame,
            bg="white"
        )

        form.pack(
            pady=10
        )



        fields=[

            ("Resource Name",self.resource_name),

            ("Serial Number",self.serial_number),

            ("Purchase Date",self.purchase_date),

            ("Value",self.value)

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




        tk.Label(
            form,
            text="Resource Type",
            bg="white"
        ).grid(
            row=0,
            column=2
        )


        self.type_box=ttk.Combobox(
            form,
            textvariable=self.resource_type,
            width=25
        )


        self.type_box.grid(
            row=0,
            column=3
        )




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

                "Available",

                "Assigned",

                "Maintenance",

                "Retired"

            ],

            width=25

        )


        self.status_box.grid(
            row=1,
            column=3
        )




        buttons=tk.Frame(
            self.frame,
            bg="white"
        )

        buttons.pack(
            pady=10
        )


        for text,cmd in [

            ("Add",self.add_resource),

            ("Update",self.update_resource),

            ("Delete",self.delete_resource),

            ("Clear",self.clear)

        ]:


            tk.Button(

                buttons,

                text=text,

                width=15,

                command=cmd

            ).pack(

                side="left",

                padx=5

            )






        columns=(

            "ID",

            "Name",

            "Type",

            "Serial",

            "Purchase Date",

            "Value",

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

            self.select_resource

        )





    # =========================
    # Load Types
    # =========================

    def load_types(self):


        data=self.db.fetch_all(

            "SELECT * FROM resource_types"

        )


        self.types={}

        values=[]


        for row in data:


            self.types[
                row["type_name"]
            ] = row["type_id"]


            values.append(
                row["type_name"]
            )


        self.type_box["values"]=values





    # =========================
    # Load Resources
    # =========================

    def load_resources(self):


        for row in self.table.get_children():

            self.table.delete(row)




        sql="""


        SELECT

        r.resource_id,

        r.resource_name,

        t.type_name,

        r.serial_number,

        r.purchase_date,

        r.value,

        r.status


        FROM resources r


        LEFT JOIN resource_types t


        ON r.type_id=t.type_id



        """



        data=self.db.fetch_all(sql)



        for r in data:


            self.table.insert(

                "",

                "end",

                values=(

                    r["resource_id"],

                    r["resource_name"],

                    r["type_name"],

                    r["serial_number"],

                    r["purchase_date"],

                    r["value"],

                    r["status"]

                )

            )






    # =========================
    # Add
    # =========================

    def add_resource(self):


        if self.resource_name.get()=="":


            messagebox.showwarning(

                "Warning",

                "Enter resource name"

            )

            return



        if self.resource_type.get() not in self.types:


            messagebox.showwarning(

                "Warning",

                "Select resource type"

            )

            return




        sql="""


        INSERT INTO resources

        (

        resource_name,

        type_id,

        serial_number,

        purchase_date,

        value,

        status

        )


        VALUES(%s,%s,%s,%s,%s,%s)


        """



        self.db.execute(

            sql,

            (

                self.resource_name.get(),

                self.types[
                    self.resource_type.get()
                ],

                self.serial_number.get(),

                self.purchase_date.get(),

                self.value.get(),

                self.status.get()

            )

        )


        messagebox.showinfo(

            "Success",

            "Resource Added"

        )


        self.load_resources()

        self.clear()






    # =========================
    # Select
    # =========================

    def select_resource(self,event):


        item=self.table.focus()

        data=self.table.item(item)["values"]



        if data:


            self.selected_id=data[0]


            self.resource_name.set(data[1])


            self.resource_type.set(data[2])


            self.serial_number.set(data[3])


            self.purchase_date.set(data[4])


            self.value.set(data[5])


            self.status.set(data[6])







    # =========================
    # Update
    # =========================

    def update_resource(self):


        if self.selected_id is None:

            return



        sql="""


        UPDATE resources SET


        resource_name=%s,

        type_id=%s,

        serial_number=%s,

        purchase_date=%s,

        value=%s,

        status=%s


        WHERE resource_id=%s



        """



        self.db.execute(

            sql,

            (

                self.resource_name.get(),

                self.types[
                    self.resource_type.get()
                ],

                self.serial_number.get(),

                self.purchase_date.get(),

                self.value.get(),

                self.status.get(),

                self.selected_id

            )

        )


        messagebox.showinfo(

            "Success",

            "Resource Updated"

        )


        self.load_resources()

        self.clear()





    # =========================
    # Delete
    # =========================

    def delete_resource(self):


        if self.selected_id:


            confirm=messagebox.askyesno(

                "Delete",

                "Delete this resource?"

            )


            if confirm:


                self.db.execute(

                    """

                    DELETE FROM resources

                    WHERE resource_id=%s

                    """,

                    (

                        self.selected_id,

                    )

                )


                messagebox.showinfo(

                    "Success",

                    "Resource Deleted"

                )


                self.load_resources()

                self.clear()





    # =========================
    # Clear
    # =========================

    def clear(self):


        self.resource_name.set("")

        self.resource_type.set("")

        self.serial_number.set("")

        self.purchase_date.set("")

        self.value.set("")

        self.status.set("Available")


        self.selected_id=None