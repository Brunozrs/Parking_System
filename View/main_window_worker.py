import tkinter as tk
from tkinter import ttk, messagebox
from Controller.parking_controller import ParkingSpaceController


class MainWindowWorker(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        self.title("Parking System - Dashboard")
        self.geometry("800x600")

        # Inicia o Controller das vagas
        self.parking_controller = ParkingSpaceController()

        # ==========================================
        # 1. MENU SUPERIOR (Onde você já deve ter Clientes e Trabalhadores)
        # ==========================================
        menu_frame = ttk.Frame(self)
        menu_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Button(menu_frame, text="👥 Manage Clients", command=self.open_clients).pack(side=tk.LEFT, padx=5)
        ttk.Button(menu_frame, text="🔄 Refresh Map", command=self.refresh_dashboard).pack(side=tk.RIGHT, padx=5)

        # ==========================================
        # 2. ÁREA DO MAPA DE VAGAS (Visualização Dinâmica)
        # ==========================================
        # Criamos um frame principal para conter o mapa
        self.map_frame = ttk.LabelFrame(self, text="Parking Status (Parking Space Map)")
        self.map_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Chama a função para desenhar as vagas pela primeira vez
        self.refresh_dashboard()

    def open_clients(self):
        # Importamos aqui dentro para evitar problemas de dependência circular
        from View.client_list_view import ClientListView
        ClientListView(self)

    def open_workers(self):
        # Importamos aqui dentro para evitar problemas de dependência circular
        from View.worker_list_view import WorkerListView
        WorkerListView(self)

    # ==========================================
    # A MÁGICA DO MAPA DINÂMICO ACONTECE AQUI
    # ==========================================
    def refresh_dashboard(self):
        """Limpa o mapa atual e desenha os blocos com as cores atualizadas"""

        # 1. Destrói os blocos antigos (limpa a tela para não sobrepor)
        for widget in self.map_frame.winfo_children():
            widget.destroy()

        try:
            # 2. Busca as vagas no banco de dados
            spaces = self.parking_controller.list_all_spaces()

            if not spaces:
                ttk.Label(self.map_frame, text="No spaces registered in the system yet.", font=("Arial", 12)).pack(
                    pady=50)
                return

            # 3. Desenha a grade
            columns = 5  # Quantas vagas por linha você quer que apareça

            for index, space in enumerate(spaces):
                row = index // columns
                col = index % columns

                # Define as cores baseadas no status da vaga
                if space.available:
                    bg_color = "#28a745"  # Verde (Livre)
                    status_text = "FREE"
                else:
                    bg_color = "#dc3545"  # Vermelho (Ocupada)
                    status_text = "BUSY"

                # Cria um "Quadrado" visual usando o tk.Button
                # O botão é ótimo para isso porque já tem efeito visual e permite clicar
                btn = tk.Button(
                    self.map_frame,
                    text=f"Parking space {space.number}\n({space.size.name})\n\n{status_text}",
                    bg=bg_color,
                    fg="white",
                    font=("Arial", 10, "bold"),
                    width=12,
                    height=5,
                    relief="raised",
                    command=lambda s=space: self.on_space_click(s)  # Ação ao clicar na vaga
                )

                # Posiciona o quadrado na grade
                btn.grid(row=row, column=col, padx=15, pady=15)

        except Exception as e:
            messagebox.showerror("Error", f"Fail to load Map: {e}")

    def on_space_click(self, space):
        """O que acontece quando o operador clica em um quadrado"""
        if space.available:
            # Importa a janela de Check-in Rápido
            from View.space_allocation_view import SpaceAllocationView

            # Abre a janela passando a vaga clicada e o comando para atualizar o mapa!
            SpaceAllocationView(self, space, on_saved=self.refresh_dashboard)
        else:
            # Futuramente, clicou na vaga vermelha? Poderá abrir direto o Checkout!
            messagebox.showinfo("Occupied Space", f"Space {space.number} is occupied at the moment.")

