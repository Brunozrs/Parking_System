import tkinter as tk
from tkinter import ttk, messagebox
from Controller.worker_controller import WorkerController
from View.worker_form_view import WorkerFormView

class WorkerListView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.controller = WorkerController()

        self.title("Workers")
        self.geometry("600x400")

        columns = ("id", "name", "phone", "email", "salary")
        self.tree = ttk.Treeview(self, columns = columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="New", command=self.new_worker).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit", command=self.edit_worker).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_worker).pack(side="left", padx=5)

        self.workers = []
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        self.workers = self.controller.list_workers()
        for worker in self.workers:
            self.tree.insert("", "end", iid=worker.id, values=(worker.id, worker.name, worker.phonenumber, worker.email, worker.salary))

    def get_selected_worker(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No selection", "Select a worker first")
            return None
        worker_id = int(selection[0])
        return next(w for w in self.workers if w.id == worker_id)

    def new_worker(self):
        WorkerFormView(self, on_saved=self.refresh)

    def edit_worker(self):
        worker = self.get_selected_worker()
        if worker:
            WorkerFormView(self, on_saved=self.refresh, worker=worker)

    def delete_worker(self):
        worker = self.get_selected_worker()
        if worker and messagebox.askyesno("Confirm", f"Delete {worker.name}?"):
            self.controller.delete_worker(worker.id)
            self.refresh()
