import tkinter as tk
from tkinter import ttk, messagebox
from Controller.client_controller import ClientController
from View.client_form_view import ClientFormView

class ClientListView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.controller = ClientController()

        self.title("Clients")
        self.geometry("600x400")

        columns = ("id", "name", "phone", "email", "Arrival", "Departure")
        self.tree = ttk.Treeview(self, columns = columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="New", command=self.new_client).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit", command=self.edit_client).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_client).pack(side="left", padx=5)

        self.clients = []
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        self.clients = self.controller.list_clients()
        for client in self.clients:
            self.tree.insert("", "end", iid=client.id, values=(client.id, client.name, client.phonenumber, client.email, client.arrival, client.departure))

    def get_selected_client(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No selection", "Select a client first")
            return None
        client_id = int(selection[0])
        return next(c for c in self.clients if c.id == client_id)

    def new_client(self):
        ClientFormView(self, on_saved=self.refresh)

    def edit_client(self):
        client = self.get_selected_client()
        if client:
            ClientFormView(self, on_saved=self.refresh, client=client)

    def delete_client(self):
        client = self.get_selected_client()
        if client and messagebox.askyesno("Confirm", f"Delete {client.name}?"):
            self.controller.delete_client(client.id)
            self.refresh()
