from Controller.parking_controller import ParkingSpaceController
from Repository.vehicle_repo import VehicleRepo
from Model.Vehicle import Vehicle


class VehicleController:
    def __init__(self):
        self.parking_controller = ParkingSpaceController()
        self.repo = VehicleRepo()

    def create_vehicle(self, plate, color, size_enum, client_id, image_path):
        # O Model já cuida de ler o path e transformar em Base64 internamente!  
        try:
            # Puxa uma vaga livre compatível com o tamanho
            space = self.parking_controller.assign_space(vehicle_id=0, size=size_enum)
        except ValueError:
            # Se não tiver vaga, explode um erro antes mesmo de salvar o carro
            raise ValueError(f"Estacionamento LOTADO para veículos do tamanho {size_enum.name}!")
        
        vehicle = Vehicle(
            plate=plate,
            color=color,
            size=size_enum,
            client_id=client_id,
            path=image_path,
            space_id=space.id
        )
        self.repo.save(vehicle)
        return vehicle

    def create_vehicle_in_specific_space(self, plate, color, size_enum, client_id, space_id):
        # 1. Salva o veículo com uma imagem "vazia" (para não exigir foto no fluxo rápido)
        vehicle = Vehicle(
            plate=plate,
            color=color,
            size=size_enum,
            client_id=client_id,
            path=None,
            image_b64="",
            space_id=space_id
        )
        self.repo.save(vehicle)

        # 2. Muda o status da vaga clicada para OCUPADA (False)
        space = self.parking_controller.space_repo.find_by_id(space_id)
        space.available = False
        self.parking_controller.space_repo.update(space)

        return vehicle

    def update_vehicle(self, vehicle_id, plate, color, size_enum, client_id, space_id,image_path=None, image_b64=None):
        # Permite atualizar passando uma nova foto (path) ou mantendo a antiga (image_b64)
        vehicle = Vehicle(
            id=vehicle_id,
            plate=plate,
            color=color,
            size=size_enum,
            client_id=client_id,
            path=image_path,
            image_b64=image_b64,
            space_id=space_id
        )
        self.repo.update(vehicle)
        return vehicle

    def delete_vehicle(self, vehicle_id):
        self.repo.delete(vehicle_id)

    def get_vehicle(self, vehicle_id: int):
        return self.repo.find_by_id(vehicle_id)

    def list_client_vehicles(self, client_id):
        return self.repo.find_by_client(client_id)

    def list_all_vehicles(self):
        return self.repo.find_all()

    def allocate_existing_vehicle(self, vehicle_id, space_id):
        # 1. Puxa o veículo e atualiza a vaga dele
        vehicle = self.repo.find_by_id(vehicle_id)
        old_space_id = vehicle.space_id

        if old_space_id:
            self.parking_controller.free_space(old_space_id)

        # Como o update_vehicle precisa de muitos parâmetros, vamos
        # usar o repo direto aqui para ser mais eficiente
        vehicle.space_id = space_id
        self.repo.update(vehicle)

        # 2. Muda o status da vaga para OCUPADA (False)
        space = self.parking_controller.space_repo.find_by_id(space_id)
        space.available = False
        self.parking_controller.space_repo.update(space)