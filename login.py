import tkinter as tk
from tkinter import messagebox

from database import Database
from main import ResourceManagementApp
class Login:


    def __init__(self, root):


        self.root = root

        self.root.title(
            "Login - Resource Management System"
        )


        self.root.geometry(
            "400x300"
        )


        self.db = Database()


        self.create_ui()





    # =================================
    # UI
    # =================================

    def create_ui(self):


        tk.Label(

            self.root,

            text="Resource Management Login",

            font=("Arial",18,"bold")

        ).pack(

            pady=20

        )



        tk.Label(

            self.root,

            text="Email"

        ).pack()



        self.email = tk.Entry(

            self.root,

            width=30

        )


        self.email.pack()



        tk.Label(

            self.root,

            text="Password"

        ).pack()



        self.password = tk.Entry(

            self.root,

            width=30,

            show="*"

        )


        self.password.pack()



        tk.Button(

            self.root,

            text="Login",

            width=15,

            command=self.login

        ).pack(

            pady=20

        )





    # =================================
    # LOGIN CHECK
    # =================================

    def login(self):


        email = self.email.get()

        password = self.password.get()



        if email == "" or password == "":


            messagebox.showwarning(

                "Warning",

                "Enter email and password"

            )

            return





        sql = """

        SELECT

        u.user_id,

        u.first_name,

        u.last_name,

        r.role_name


        FROM users u


        LEFT JOIN roles r

        ON u.role_id=r.role_id


        WHERE u.email=%s

        AND u.password_hash=%s

        AND u.status='Active'


        """



        user = self.db.fetch_one(

            sql,

            (

                email,

                password

            )

        )



        if user:


            self.root.destroy()



            main_root = tk.Tk()



            app = ResourceManagementApp(

                main_root,

                user["user_id"],

                user["role_name"]

            )



            main_root.mainloop()



        else:


            messagebox.showerror(

                "Login Failed",

                "Invalid email or password"

            )






# =================================
# RUN
# =================================

if __name__ == "__main__":


    root = tk.Tk()


    app = Login(root)


    root.mainloop()