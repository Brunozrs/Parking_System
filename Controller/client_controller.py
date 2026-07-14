from Repository.client_repo import ClientRepo
from Model.Client import Client


class ClientController:
    def __init__(self):
        self.repo = ClientRepo()

    def create_client(self, name, phone_number, email, document, address,arrival, departure):
        client = Client(
            name=name, phone_number=phone_number,
            email=email, document=document, address=address,
            arrival=arrival, departure=departure
        )
        self.repo.save(client)
        return client

    def update_client(self,client_id, name, phone_number, email, document, address, arrival, departure):

        client = self.repo.find_by_id(client_id)
        client.name = name
        client.phonenumber = phone_number
        client.email = email
        client.document = document
        client.address = address
        client.arrival = arrival
        client.departure = departure
        self.repo.update(client)
        return client

    def delete_client(self, client_id):
        self.repo.delete(client_id)

    def list_clients(self):
        return self.repo.find_all()