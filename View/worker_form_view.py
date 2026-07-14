import re
import tkinter as tk
from tkinter import ttk, messagebox

from Controller.worker_controller import WorkerController
from Controller.address_controller import AddressController



class WorkerFormView(tk.Toplevel):
    def __init__(self, master, on_saved=None, worker=None):
        super().__init__(master)
        self.controller = WorkerController()
        self.address_controller = AddressController()
        self.worker = worker #None = criar, Worker= editar
        self.on_saved = on_saved

        self.title("Edit worker" if worker else "New worker")
        self.resizable(False, False)

        fields = ["Name", "Phone number", "Email", "Document", "Salary", "Password", "Role"]
        self.entries= {}
        self.entries["Password"].bind("<KeyRelease>", lambda e: self.check_password())


        for i, field in enumerate(fields):
            ttk.Label(self, text=field).grid(row=i, column=0, padx=10,pady=6,sticky="w")
            entry = ttk.Entry(self, width=30)
            entry.grid(row=i, column=1, padx=10,pady=6)
            self.entries[field] = entry

            self.checks = {}
            checks_def = [
                ("length", "At least 8 characters"),
                ("upper", "At least 1 uppercase letter"),
                ("lower", "At least 1 lowercase letter"),
                ("digit", "At least 1 number"),
                ("special", "At least 1 special character (!@#$...)"),
            ]

            check_frame = ttk.LabelFrame(self, text="Password strength")
            check_frame.grid(row=i, column=0, columnspan=3, padx=10, pady=4, sticky="ew")
            i += 1

            for key, text in checks_def:
                lbl = ttk.Label(check_frame, text=f"✗  {text}", foreground="red")
                lbl.pack(anchor="w", padx=8, pady=1)
                self.checks[key] = lbl

            if field == "Role":
                combo = ttk.Combobox(self, values=["worker", "admin"], width=27, state="readonly")
                combo.set("worker")
                combo.grid(row=i, column=1, padx=10, pady=6)
                self.entries[field] = combo

        #address section
        row = len(fields)
        ttk.Separator(self, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=8
        )
        row+=1

        ttk.Label(self, text="CEP").grid(row=row, column=0, padx=10, pady=6, sticky="ew")
        self.entries["CEP"] = ttk.Entry(self, width=15)
        self.entries["CEP"].grid(row=row, column=1, padx=10, pady=6, sticky="w")
        self.entries["CEP"].bind("<Return>", lambda event: self.fetch_address())
        ttk.Button(self, text="Search", command=self.fetch_address).grid(
            row=row, column=2, padx=5
        )
        row += 1

        # Preenchido pela API, pode ser modificado se necessário
        for field in ["Street", "Neighborhood", "City", "State"]:
            ttk.Label(self, text=field).grid(row=row, column=0, padx=10, pady=6, sticky="w")
            entry = ttk.Entry(self, width=30)
            entry.grid(row=row, column=1, padx=10, pady=6)
            self.entries[field] = entry
            row += 1

        # Numero escrito manualmente
        ttk.Label(self, text="Number").grid(row=row, column=0, padx=10, pady=6, sticky="w")
        self.entries["Number"] = ttk.Entry(self, width=10)
        self.entries["Number"].grid(row=row, column=1, padx=10, pady=6, sticky="w")
        row += 1

        if worker:
            self.entries["Name"].insert(0, worker.name)
            self.entries["Phone number"].insert(0, worker.phonenumber)
            self.entries["Email"].insert(0, worker.email)
            self.entries["Document"].insert(0, worker.document)
            self.entries["Salary"].insert(0, str(worker.salary))
            if worker.address:
                # Endereço guardado como uma unica linha, dividido em partes
                parts = worker.address.split(", ")
                if len(parts) == 5:
                    self.entries["Street"].insert(0, parts[0])
                    self.entries["Number"].insert(0, parts[1])
                    self.entries["Neighborhood"].insert(0, parts[2])
                    self.entries["City"].insert(0, parts[3])
                    self.entries["State"].insert(0, parts[4])

        ttk.Button(self, text="Save", command=self.save).grid(
            row=row, column=0, columnspan=2, pady=12
        )

    def check_password(self):
        pwd = self.entries["Password"].get()

        rules = {
            "length": len(pwd) >= 8,
            "upper": bool(re.search(r"[A-Z]", pwd)),
            "lower": bool(re.search(r"[a-z]", pwd)),
            "digit": bool(re.search(r"\d", pwd)),
            "special": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd)),
        }

        for key, passed in rules.items():
            label = self.checks[key]
            if passed:
                label.config(text=f"✓  {label.cget('text')[3:]}", foreground="green")
            else:
                label.config(text=f"✗  {label.cget('text')[3:]}", foreground="red")

        return all(rules.values())  # True if password is strong

    def fetch_address(self):
        cep = self.entries["CEP"].get()
        try:
            data = self.address_controller.get_address(cep)
            # limpa e preenche os campos do endereço
            for field, key in [("Street", "street"), ("Neighborhood", "neighborhood"),
                               ("City", "city"), ("State", "state")]:
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, data[key])
            # Foca o campo do número para o usuário preencher
            self.entries["Number"].focus()
        except ValueError as e:
            messagebox.showerror("CEP Error", str(e))

    def save(self):
        try:
            name = self.entries["Name"].get()
            phone = self.entries["Phone number"].get()
            email = self.entries["Email"].get()
            document = self.entries["Document"].get()
            salary = float(self.entries["Salary"].get().replace(",", "."))
            password = self.entries["Password"].get()
            if not self.check_password():
                messagebox.showwarning("Weak password", "Password does not meet all requirements")
                return
            role = self.entries["role"].get() or "worker"
            # Constrói um endereço em uma unica linha
            street = self.entries["Street"].get()
            number = self.entries["Number"].get()
            neighborhood = self.entries["Neighborhood"].get()
            city = self.entries["City"].get()
            state = self.entries["State"].get()
            address = f"{street}, {number}, {neighborhood}, {city}, {state}"

            if self.worker:
                self.controller.update_worker(self.worker.id, name, phone, email, document, address,salary,password, role)
            else:
                self.controller.create_worker(name,phone,email,document,address,salary, password, role)

            if self.on_saved:
                self.on_saved()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            print(e)