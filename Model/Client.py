from datetime import datetime,timedelta
from Model.User import User


class Client(User):
    def __init__(self, arrival: datetime, departure: datetime,**kwargs):
        super().__init__(**kwargs)
        self._vehicles = []
        self._arrival = arrival
        self.departure = departure

    @property
    def vehicles(self):
        return self._vehicles
    def add_vehicle(self, vehicle):
        self._vehicles.append(vehicle)

    @property
    def arrival(self):
        return self._arrival
    @arrival.setter
    def arrival(self, arrival):
        self._arrival = arrival

    @property
    def departure(self):
        return self._departure
    @departure.setter
    def departure(self, departure):
        self._departure = departure

