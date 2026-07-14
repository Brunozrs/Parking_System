import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime,timedelta

from Controller.vehicle_controller import VehicleController
from Controller.client_controller import ClientController
from Controller.checkout_controller import CheckoutController
from Controller.address_controller import AddressController

from View.vehicle_form_view import VehicleFormView


class ClientFormView(tk.Toplevel):
    def __init__(self, master, on_saved=None, client=None):
        super().__init__(master)
        self.controller = ClientController()
        self.address_controller = AddressController()
        self.client = client #None = criar, Client= editar
        self.on_saved = on_saved

        self.title("Edit client" if client else "New client")
        self.resizable(False, False)

        fields = ["Name", "Phone number", "Email", "Document", "Arrival", "Duration"]
        self.entries= {}

        self.duration_var = tk.IntVar(value=30)

        for i, field in enumerate(fields):
            ttk.Label(self, text=field).grid(row=i, column=0, padx=10,pady=6,stick="w")

            if field == "Arrival":
                frame = ttk.Frame(self)
                frame.grid(row=i, column=1, padx=10, pady=6, sticky="w")

                date_entry = DateEntry(frame, width=27, bg='darkblue',fg="white",borderwidth=2,date_pattern='dd/mm/yyyy')
                date_entry.pack(side="left", padx=(0,5))

                time_entry = ttk.Entry(frame, width=8)
                time_entry.insert(0, datetime.now().strftime("%H:%M"))
                time_entry.pack(side="left")

                time_entry.bind("<KeyRelease>", lambda e: self.update_preview())

                #guarda data/hora como tupla no dicionário
                self.entries[field] = (date_entry, time_entry)

            elif field == "Duration":
                frame = ttk.Frame(self)
                frame.grid(row=i, column=1, padx=10, pady=6, sticky="w")

                # Radio Buttons para as opções pré-pagas
                ttk.Radiobutton(frame, text="15 min", variable=self.duration_var, value=15,
                                command=self.update_preview).pack(side="left", padx=5)
                ttk.Radiobutton(frame, text="30 min", variable=self.duration_var, value=30,
                                command=self.update_preview).pack(side="left", padx=5)
                ttk.Radiobutton(frame, text="1 Hora", variable=self.duration_var, value=60,
                                command=self.update_preview).pack(side="left", padx=5)
                ttk.Radiobutton(frame, text="2 Horas", variable=self.duration_var, value=120,
                                command=self.update_preview).pack(side="left", padx=5)

                # Label Interativo para mostrar a saída calculada visualmente
                self.preview_label = ttk.Label(self, text="Saída prevista: --:--", foreground="gray")
                self.preview_label.grid(row=i + 1, column=1, sticky="w", padx=10)
            else:
                entry = ttk.Entry(self, width=30)
                entry.grid(row=i, column=1, padx=10,pady=6)
                self.entries[field] = entry

        self.update_preview()

        # address section
        row = len(fields) + 2
        ttk.Separator(self, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=8
        )
        row += 1

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

        if client:
            self.entries["Name"].insert(0, client.name)
            self.entries["Phone number"].insert(0, client.phonenumber)
            self.entries["Email"].insert(0, client.email)
            self.entries["Document"].insert(0, client.document)
            if client.arrival:
                self.entries["Arrival"][0].set_date(client.arrival)  # [0] é o calendário
                self.entries["Arrival"][1].delete(0, tk.END)  # [1] é a hora
                self.entries["Arrival"][1].insert(0, client.arrival.strftime("%H:%M"))

            if client.address:
                # Endereço guardado como uma unica linha, dividido em partes
                parts = client.address.split(", ")
                if len(parts) == 5:
                    self.entries["Street"].insert(0, parts[0])
                    self.entries["Number"].insert(0, parts[1])
                    self.entries["Neighborhood"].insert(0, parts[2])
                    self.entries["City"].insert(0, parts[3])
                    self.entries["State"].insert(0, parts[4])

        ttk.Button(self, text="Save", command=self.save).grid(
            row=row, column=0, columnspan=2, pady=12)
        row+=1
        self.checkout_controller = CheckoutController()

        checkout_btn = tk.Button(self, text="💰 FINALIZAR ESTADIA (CHECKOUT)", bg="green", fg="white",
                                 font=("Arial", 10, "bold"), command=self.do_checkout)
        # Aumentamos o len(fields) + 3 para ele ficar logo abaixo da tabela de carros
        checkout_btn.grid(row=row, column=0, columnspan=2, pady=15, sticky="ew", padx=10)
        row+=1

        # ==========================================
        # INÍCIO DA SESSÃO DE VEÍCULOS (MESTRE-DETALHE)
        # ==========================================

        # Aumentamos a janela na edição para caber a tabela
        if client:
            self.geometry("600x800")
            self.v_controller = VehicleController()

            # Cria uma "caixa" visual para organizar os carros
            v_frame = ttk.LabelFrame(self, text="Client Vehicles")
            v_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
            row+=1
            # Tabela (Treeview)
            self.v_tree = ttk.Treeview(v_frame, columns=("ID", "Plate", "Color", "Size"), show="headings", height=4)
            self.v_tree.heading("ID", text="ID")
            self.v_tree.heading("Plate", text="Plate")
            self.v_tree.heading("Color", text="Color")
            self.v_tree.heading("Size", text="Size")

            self.v_tree.column("ID", width=30, anchor="center")
            self.v_tree.column("Plate", width=100, anchor="center")
            self.v_tree.column("Color", width=100, anchor="center")
            self.v_tree.column("Size", width=80, anchor="center")
            self.v_tree.pack(fill="x", padx=10, pady=5)

            # Botões de ação do veículo
            btn_frame = ttk.Frame(v_frame)
            btn_frame.pack(fill="x", padx=10, pady=5)

            ttk.Button(btn_frame, text="New Vehicle", command=self.add_vehicle).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Edit", command=self.edit_vehicle).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Delete", command=self.delete_vehicle).pack(side="left", padx=5)

            # Preenche a tabela a primeira vez
            self.refresh_vehicles()

        else:
            self.geometry("550x600")
            ttk.Label(self, text="* Save client first to show vehicle register",
                      foreground="gray").grid(
                row=row, column=0, columnspan=2, pady=5
            )
            row+=1
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


    def update_preview(self):
        try:
            date_widget, time_widget = self.entries["Arrival"]
            arrival_date = date_widget.get_date()
            arrival_time = datetime.strptime(time_widget.get(), "%H:%M").time()
            arrival_dt = datetime.combine(arrival_date, arrival_time)

            # Pega os minutos do RadioButton e soma
            duration = self.duration_var.get()
            departure_dt = arrival_dt + timedelta(minutes=duration)

            self.preview_label.config(text=f"Preview Departure: {departure_dt.strftime('%d/%m/%Y %H:%M')}")
        except ValueError:
            self.preview_label.config(text="Preview Departure: Hour error")

    def save(self):
        try:
            name = self.entries["Name"].get()
            phone = self.entries["Phone number"].get()
            email = self.entries["Email"].get()
            document = self.entries["Document"].get()

            # Constrói um endereço em uma unica linha
            street = self.entries["Street"].get()
            number = self.entries["Number"].get()
            neighborhood = self.entries["Neighborhood"].get()
            city = self.entries["City"].get()
            state = self.entries["State"].get()
            address = f"{street}, {number}, {neighborhood}, {city}, {state}"

            date_widget, time_widget = self.entries["Arrival"]
            arrival_date = date_widget.get_date()
            arrival_time = datetime.strptime(time_widget.get(), "%H:%M").time()
            arrival_dt = datetime.combine(arrival_date, arrival_time)

            # Pega apenas os minutos selecionados!
            duration_minutes = self.duration_var.get()
            departure_dt = arrival_dt + timedelta(minutes=duration_minutes)

            if self.client:
                self.controller.update_client(self.client.id, name, phone, email, document, address, arrival_dt,departure_dt)
            else:
                self.controller.create_client(name,phone,email,document,address,arrival_dt,departure_dt)

            if self.on_saved:
                self.on_saved()
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            print(e)

    def refresh_vehicles(self):
        # Limpa a tabela
        for item in self.v_tree.get_children():
            self.v_tree.delete(item)

        # Busca os carros do cliente no banco
        vehicles = self.v_controller.list_client_vehicles(self.client.id)

        # Insere na tabela
        for v in vehicles:
            self.v_tree.insert("", "end", values=(v.id, v.plate, v.color, v.size.name))

    def add_vehicle(self):
        # Chama a tela de veículo passando o ID do cliente atual!
        VehicleFormView(self, client_id=self.client.id, on_saved=self.refresh_vehicles)

    def edit_vehicle(self):
        selected = self.v_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select vehicle to edit.")
            return

        # Pega o ID da primeira coluna da linha selecionada
        item = self.v_tree.item(selected[0])
        vehicle_id = item['values'][0]

        # Busca o objeto completo para edição e abre a tela
        try:
            vehicle = self.v_controller.get_vehicle(int(vehicle_id))
            VehicleFormView(self, client_id=self.client.id, on_saved=self.refresh_vehicles, vehicle=vehicle)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_vehicle(self):
        selected = self.v_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select vehicle to delete.")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this vehicle?"):
            item = self.v_tree.item(selected[0])
            vehicle_id = item['values'][0]

            self.v_controller.delete_vehicle(vehicle_id)
            self.refresh_vehicles()

    def do_checkout(self):
        # 1. Verifica se o cliente tem veículos para saber a vaga e o tamanho
        vehicles = self.v_controller.list_client_vehicles(self.client.id)
        if not vehicles:
            messagebox.showwarning("Warning", "Client has no vehicles registered. Cannot do checkout.")
            return

        vehicle = vehicles[0]  # Pega o veículo principal do cliente

        # 2. Pede confirmação
        if not messagebox.askyesno("Checkout", f"Do you want to end client stay {self.client.name} now?"):
            return

        try:
            # 3. Roda a regra de Checkout (passando o space_id do veículo para liberar a vaga!)
            receipt = self.checkout_controller.process_checkout(self.client, vehicle.size, vehicle.space_id)

            # 4. Monta o recibo
            msg = (
                f"🧾 PARKING RECEIPT\n"
                f"---------------------------------------\n"
                f"Client: {self.client.name}\n"
                f"Vehicle: {vehicle.plate} (Vaga {vehicle.space_id})\n"
                f"Arrival: {receipt['arrival_str']}\n"
                f"Departure: {receipt['departure_str']}\n"
                f"Billable time: {receipt['hours_billed']} horas\n"
                f"Base fare: R$ {receipt['rate_applied']:.2f}/h\n"
                f"---------------------------------------\n"
                f"TOTAL VALUE: R$ {receipt['total_value']:.2f}"
            )

            messagebox.showinfo("Checkout Complete", msg)

            # Atualiza o cliente no banco com a data oficial de saída
            self.controller.update_client(
                self.client.id, self.client.name, self.client.phonenumber,
                self.client.email, self.client.document, self.client.address,
                self.client.arrival, receipt['real_departure_dt']
            )

            if self.on_saved:
                self.on_saved()
            self.destroy()

        except Exception as e:
            messagebox.showerror("Erro no Checkout", str(e))