import tkinter as tk
from tkinter import ttk,messagebox
from Controller.auth_controller import AuthController

class LoginView(tk.Tk):
    def __init__(self, on_login=None):
        super().__init__()
        self.auth_controller = AuthController()
        self.on_login = on_login

        self.title("Login")
        self.resizable(False,False)
        self.geometry("350x250")

        ttk.Label(self, text="Email").grid(row=0,column=0, padx=20, pady=10, sticky="w")
        self.email_entry = ttk.Entry(self, width=25)
        self.email_entry.grid(row=0,column=1, padx=10, pady=10)


        ttk.Label(self, text="Password").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.password_entry = ttk.Entry(self, width=25, show="*")
        self.password_entry.grid(row=1,column=1, padx=10, pady=10)
        self.password_entry.bind("<Return>", lambda e: self.login())

        ttk.Button(self, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=15)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        try:
            worker = self.auth_controller.login(email, password)
            if self.on_login:
                self.on_login(worker)
        except ValueError as e:
            messagebox.showerror("Login failed", str(e))