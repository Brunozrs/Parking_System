import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Controller.vehicle_controller import VehicleController
from Model.SizeEnum import Size


class VehicleFormView(tk.Toplevel):
    def __init__(self, master, client_id, on_saved=None, vehicle=None):
        super().__init__(master)
        self.controller = VehicleController()

        self.client_id = client_id
        self.vehicle = vehicle
        self.on_saved = on_saved
        self.image_path = None

        self.title("Edit Vehicle" if vehicle else "New Vehicle")
        self.geometry("400x320")  # Aumentei um pouquinho para caber os botões
        self.resizable(False, False)

        # --- Campos do Formulário ---
        ttk.Label(self, text="License Plate:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.plate_entry = ttk.Entry(self, width=30)
        self.plate_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self, text="Color:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.color_entry = ttk.Entry(self, width=30)
        self.color_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self, text="Size:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.size_var = tk.StringVar()
        self.size_combo = ttk.Combobox(self, textvariable=self.size_var, state="readonly", width=27)
        self.size_combo['values'] = [e.name for e in Size]
        self.size_combo.grid(row=2, column=1, padx=10, pady=10)

        # --- Seção de Fotos ---
        ttk.Label(self, text="Picture:").grid(row=3, column=0, padx=10, pady=10, sticky="w")

        img_frame = ttk.Frame(self)
        img_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Agrupando os botões lado a lado
        btn_frame = ttk.Frame(img_frame)
        btn_frame.pack(anchor="w")
        ttk.Button(btn_frame, text="Search File", command=self.choose_image).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="📸 Take Picture", command=self.take_photo).pack(side=tk.LEFT)

        self.lbl_img_name = ttk.Label(img_frame, text="No picture selected", foreground="gray")
        self.lbl_img_name.pack(anchor="w", pady=(5, 0))

        # --- Preenchimento se for Edição ---
        if vehicle:
            self.plate_entry.insert(0, vehicle.plate)
            self.color_entry.insert(0, vehicle.color)
            self.size_combo.set(vehicle.size.name)
            if vehicle.image_b64:
                self.lbl_img_name.config(text="Image saved (Choose another one to switch)")

        ttk.Button(self, text="Save Vehicle", command=self.save).grid(row=4, column=0, columnspan=2, pady=20)

    def choose_image(self):
        file_path = filedialog.askopenfilename(
            title="Select vehicle picture",
            filetypes=[("Image", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            self.image_path = file_path
            file_name = file_path.split("/")[-1]
            self.lbl_img_name.config(text=file_name, foreground="black")

    def take_photo(self):
        # Importa o cv2 apenas quando o botão for clicado, para não quebrar a tela se a biblioteca não estiver instalada
        try:
            import cv2
        except ImportError:
            messagebox.showerror("Error",
                                 "A biblioteca OpenCV não está instalada.\nRode no terminal: pip install opencv-python")
            return

        # Abre a câmera (0 é geralmente a webcam padrão)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            messagebox.showerror("Erro", "Cannot access computer webcam.")
            return

        messagebox.showinfo("Instructions",
                            "Webcam will open.\n\n- Press SPACE to take picture.\n- Press ESC ti cancel.")

        while True:
            # Lê o frame da câmera
            ret, frame = cap.read()
            if not ret:
                break

            # Mostra a imagem na tela
            cv2.imshow("Vehicle Capture - SPACE to take picture", frame)

            # Espera uma tecla ser pressionada (1 milissegundo de delay para atualizar a imagem)
            key = cv2.waitKey(1)

            if key % 256 == 27:  # Tecla ESCressionada
                break
            elif key % 256 == 32:  # Tecla ESPAÇO pressionada
                # Salva o frame temporariamente na pasta do projeto
                temp_filename = "temp_webcam_capture.jpg"
                cv2.imwrite(temp_filename, frame)

                # Seta o caminho para o método save() poder usar
                self.image_path = temp_filename
                self.lbl_img_name.config(text="Picture taken with success!", foreground="green")
                break

        # Libera a câmera e fecha a janela do OpenCV
        cap.release()
        cv2.destroyAllWindows()

    def save(self):
        plate = self.plate_entry.get().strip()
        color = self.color_entry.get().strip()
        size_name = self.size_var.get()

        if not plate or not color or not size_name:
            messagebox.showerror("Error", "Fill all entrys!")
            return

        if not self.vehicle and not self.image_path:
            messagebox.showerror("Error", "Must choose or take picture for register!")
            return

        size_enum = Size[size_name]

        try:
            if self.vehicle:
                self.controller.update_vehicle(
                    self.vehicle.id, plate, color, size_enum,
                    self.client_id, self.image_path, self.vehicle.image_b64
                )
            else:
                self.controller.create_vehicle(
                    plate, color, size_enum, self.client_id, self.image_path
                )

            if self.on_saved:
                self.on_saved()
            self.destroy()

        except Exception as e:
            messagebox.showerror("Save error", str(e))