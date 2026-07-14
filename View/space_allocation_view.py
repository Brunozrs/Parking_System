import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

from Controller.client_controller import ClientController
from Controller.vehicle_controller import VehicleController


class SpaceAllocationView(tk.Toplevel):
    def __init__(self, master, space, on_saved):
        super().__init__(master)
        self.space = space
        self.on_saved = on_saved

        self.client_ctrl = ClientController()
        self.vehicle_ctrl = VehicleController()

        self.title(f"Allocate Parking space {space.number}")
        self.geometry("380x420")
        self.resizable(False, False)

        ttk.Label(self, text=f"Parking space {space.number} ({space.size.name})", font=("Arial", 14, "bold")).pack(pady=10)

        # ==========================================
        # OPÇÃO 1: VEÍCULO JÁ CADASTRADO
        # ==========================================
        frame_existente = ttk.LabelFrame(self, text="Option 1: Client/Vehicle registered")
        frame_existente.pack(fill="x", padx=15, pady=5)

        # Puxa os veículos, mas FILTRA para mostrar apenas os veículos do tamanho exato da vaga!
        all_vehicles = self.vehicle_ctrl.list_all_vehicles()
        valid_vehicles = [v for v in all_vehicles if v.size == space.size]

        self.combo_var = tk.StringVar()
        self.combo = ttk.Combobox(frame_existente, textvariable=self.combo_var, state="readonly")

        if valid_vehicles:
            # Formata a lista para o Combobox aparecer bonito: "[ID] Placa"
            self.combo['values'] = [f"[{v.id}] License Plate: {v.plate}" for v in valid_vehicles]
        else:
            self.combo['values'] = ["No compatible vehicle"]
            self.combo.set("No compatible vehicle")
            self.combo.config(state="disabled")

        self.combo.pack(padx=10, pady=10, fill="x")

        ttk.Button(frame_existente, text="🚗 Allocate Selected Vehicle", command=self.allocate_existing).pack(pady=5)

        ttk.Label(self, text="OR", font=("Arial", 10, "bold"), foreground="gray").pack(pady=2)

        # ==========================================
        # OPÇÃO 2: AVULSO / CHECK-IN RÁPIDO
        # ==========================================
        frame_avulso = ttk.LabelFrame(self, text="Option 2: Quick Check-in (Individual)")
        frame_avulso.pack(fill="x", padx=15, pady=5)

        f_grid = ttk.Frame(frame_avulso)
        f_grid.pack(padx=10, pady=5)

        ttk.Label(f_grid, text="License Plate:").grid(row=0, column=0, sticky="w", pady=2)
        self.plate_entry = ttk.Entry(f_grid, width=15)
        self.plate_entry.grid(row=0, column=1, sticky="w", pady=2)

        ttk.Label(f_grid, text="Color:").grid(row=1, column=0, sticky="w", pady=2)
        self.color_entry = ttk.Entry(f_grid, width=15)
        self.color_entry.grid(row=1, column=1, sticky="w", pady=2)

        self.duration_var = tk.IntVar(value=30)
        ttk.Radiobutton(f_grid, text="30 min", variable=self.duration_var, value=30).grid(row=2, column=0, pady=5)
        ttk.Radiobutton(f_grid, text="1 Hour", variable=self.duration_var, value=60).grid(row=2, column=1, pady=5)

        ttk.Button(frame_avulso, text="⚡ Confirm Quick Check-in", command=self.save_quick).pack(pady=10)

    # Função do botão 1
    def allocate_existing(self):
        selected = self.combo_var.get()
        if not selected or selected == "No compatible vehicle":
            messagebox.showwarning("Warning", "Select a valid vehicle on list!")
            return

        # Pega a string "[15] Placa: ABC1234", divide pelo "]", remove o "[" e converte o 15 para inteiro
        v_id = int(selected.split("]")[0].replace("[", ""))

        try:
            self.vehicle_ctrl.allocate_existing_vehicle(v_id, self.space.id)
            messagebox.showinfo("Success", f"Vehicle allocated on Parking Space {self.space.number}!")
            if self.on_saved:
                self.on_saved()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Função do botão 2
    def save_quick(self):
        plate = self.plate_entry.get().strip()
        color = self.color_entry.get().strip()
        if not plate:
            messagebox.showerror("Error", "Must have License Plate!")
            return

        arrival_dt = datetime.now()
        departure_dt = arrival_dt + timedelta(minutes=self.duration_var.get())

        try:
            client = self.client_ctrl.create_client(f"Individual - {plate}", "", "", "", arrival_dt, departure_dt)
            self.vehicle_ctrl.create_vehicle_in_specific_space(plate, color, self.space.size, client.id, self.space.id)

            messagebox.showinfo("Success", f"Vehicle {plate} allocated with success!")
            if self.on_saved:
                self.on_saved()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))