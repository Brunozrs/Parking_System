from Model.SizeEnum import Size
from Model.Client import Client
import base64

class Vehicle:
    def __init__(self, plate:str, color:str, size: Size, client: Client = None, client_id: int=None, path:str=None, image_b64: str=None, id: int=None, space_id: int=None):
        self._id = id
        self._plate = plate
        self._color = color
        self._size = size
        self._space_id=space_id


        #Client - accept object or just the id
        if client is not None:
            self._client = client
            self._client_id = client.id
        elif client_id is not None:
            self._client = None
            self._client_id = client_id
        else:
            raise ValueError("Provide either a Client object or a client_id")

        #Image - accept file path or pre-loaded base64
        if path is not None:
            with open(path, "rb") as f:
                self._image_b64 = base64.b64encode(f.read()).decode("utf-8")
            self._path = path
        elif image_b64 is not None:
            self._image_b64= image_b64
            self._path=None
        else:
            raise ValueError("Provide either an image path or image_b64")

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def plate(self):
        return self._plate
    @plate.setter
    def plate(self, plate):
        self._plate = plate

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, color):
        self._color = color

    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, size):
        self._size = size

    @property
    def space_id(self):
        return self._space_id

    @space_id.setter
    def space_id(self, value):
        self._space_id=value

    @property
    def client(self):
        return self._client

    @property
    def client_id(self):
        return self._client_id

    @property
    def image_b64(self):
        return self._image_b64
