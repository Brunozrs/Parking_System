from Model.SizeEnum import Size


class ParkingSpace:
    def __init__(self, size:Size, number: int):
        self._id = None
        self._available = True
        self._size = size
        self._number = number

    @property
    def id(self):
        return self._id

    @property
    def available(self):
        return self._available
    @available.setter
    def available(self, available: bool):
        self._available = available

    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, size: int):
        self._size = size

    @property
    def number(self):
        return self._number
    @number.setter
    def number(self,number: int):
        self._number = number