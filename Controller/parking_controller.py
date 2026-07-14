from Model.SizeEnum import Size

from Repository.parking_space_repo import ParkingSpaceRepo
from Repository.vehicle_repo import VehicleRepo


class ParkingSpaceController:
    def __init__(self):
        self.space_repo = ParkingSpaceRepo()
        self.vehicle_repo = VehicleRepo()

    def list_all_spaces(self):
        return self.space_repo.find_all()

    def assign_space(self, vehicle_id: int, size: Size):
        """ Econtra um espaço disponível de acordo com o tamanho do veículo"""
        available = self.space_repo.find_available(size=size)
        if not available:
                raise ValueError(f"No available space for size {size}")

        space = available[0]
        space.available = False
        self.space_repo.update(space)
        return space

    def free_space(self, space_id: int):
        space = self.space_repo.find_by_id(space_id)
        space.available = True
        self.space_repo.update(space)