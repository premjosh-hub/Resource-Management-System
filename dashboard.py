import tkinter as tk



class Dashboard:


    def __init__(self, parent, db):

        self.parent = parent
        self.db = db

        self.create_dashboard()



    def create_dashboard(self):


        self.frame = tk.Frame(
            self.parent,
            bg="#ECF0F1"
        )

        self.frame.pack(
            fill="both",
            expand=True
        )



        title = tk.Label(

            self.frame,

            text="Dashboard",

            font=("Arial",26,"bold"),

            bg="#ECF0F1",

            fg="#2C3E50"

        )


        title.pack(
            pady=20
        )



        # Database Counts

        users = self.db.count("users")

        projects = self.db.count("projects")

        resources = self.db.count("resources")

        assignments = self.db.count("assignments")

        leaves = self.db.count("leave_requests")




        card_frame = tk.Frame(

            self.frame,

            bg="#ECF0F1"

        )


        card_frame.pack(
            pady=20
        )




        cards = [

            ("Users", users),

            ("Projects", projects),

            ("Resources", resources),

            ("Assignments", assignments),

            ("Leave Requests", leaves)

        ]



        row = 0

        column = 0



        for name, value in cards:



            card = tk.Frame(

                card_frame,

                width=200,

                height=120,

                bg="white",

                relief="raised",

                bd=2

            )


            card.grid(

                row=row,

                column=column,

                padx=20,

                pady=20

            )


            card.pack_propagate(False)



            tk.Label(

                card,

                text=name,

                font=("Arial",14,"bold"),

                bg="white"

            ).pack(
                pady=10
            )



            tk.Label(

                card,

                text=str(value),

                font=("Arial",28,"bold"),

                fg="#1ABC9C",

                bg="white"

            ).pack()



            column += 1



            if column == 3:

                row += 1

                column = 0





        info_frame = tk.Frame(

            self.frame,

            bg="white"

        )


        info_frame.pack(

            fill="x",

            padx=40,

            pady=20

        )




        tk.Label(

            info_frame,

            text="System Information",

            font=("Arial",16,"bold"),

            bg="white"

        ).pack(

            pady=10

        )




        tk.Label(

            info_frame,

            text="Resource Management System Dashboard",

            font=("Arial",12),

            bg="white"

        ).pack()