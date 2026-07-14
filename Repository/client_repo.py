from datetime import datetime

from database import get_connection
from Model.Client import Client

class ClientRepo:

    def save(self, client: Client):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users (name, phone_number, email, document, address, type) VALUES (?,?,?,?,?,?)",
                (client.name, client.phonenumber, client.email, client.document, client.address, "client")
            )
            user_id = cursor.lastrowid
            conn.execute(
                "INSERT INTO clients (id, arrival, departure) VALUES (?,?,?)",
                (user_id, client.arrival, client.departure)
            )
            client.id = user_id  # atribui o id gerado de volta

    def find_by_id(self, client_id: int) -> Client:
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT u.id, u.name, u.phone_number, u.email, u.document, u.address, c.arrival, c.departure
                FROM users u JOIN clients c ON u.id = c.id
                WHERE u.id=?
            """,(client_id,))
        row = cursor.fetchone()

        if row:
            arrival_val = row["arrival"]
            departure_val = row["departure"]

            # Verificação de segurança (Inline if)
            arrival_dt = datetime.fromisoformat(arrival_val) if isinstance(arrival_val, str) else arrival_val
            departure_dt = datetime.fromisoformat(departure_val) if isinstance(departure_val, str) else departure_val

            return Client(
                id=row['id'],  # ou row[0]
                name=row['name'],  # ou row[1]
                phone_number=row['phone_number'],  # ou row[2]
                email=row['email'],  # ou row[3]
                document=row['document'], # ou row[4]
                address=row['address'],
                arrival=arrival_dt,
                departure=departure_dt
            )


    def update(self, client:Client):
        if client.id is None:
            raise ValueError("Client has no ID - Save before updating")
        with get_connection()as conn:
            conn.execute("""
                UPDATE users
                SET name=?, phone_number=?, email=?, document=?, address=?
                WHERE id=?
            """,(client.name, client.phonenumber, client.email, client.document, client.address, client.id))

            conn.execute("""
                UPDATE clients
                SET arrival=?, departure=?
                WHERE id=?
            """, (client.arrival, client.departure, client.id))

    def find_all(self) ->list[Client]:
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT u.id, u.name, u.phone_number, u.email, u.document, u.address, c.arrival, c.departure
                FROM users u JOIN clients c ON u.id = c.id
            """).fetchall()

        clients = []
        for row in rows:
            arrival_val = row["arrival"]
            departure_val = row["departure"]

            arrival_dt = datetime.fromisoformat(arrival_val) if isinstance(arrival_val, str) else arrival_val
            departure_dt = datetime.fromisoformat(departure_val) if isinstance(departure_val, str) else departure_val

            client = Client(
                name=row["name"], phone_number=row["phone_number"],
                email=row["email"], document=row["document"], address=row['address'],
                arrival=arrival_dt, departure=departure_dt
            )
            client._id = row["id"]
            clients.append(client)

        return clients

    def delete(self, client_id:int):
        with get_connection() as conn:
            #deleta primeiro as linhas para respeitar chaves estrangeiras
            conn.execute("DELETE FROM vehicles WHERE client_id = ?", (client_id,))
            conn.execute("DELETE FROM clients WHERE id = ?", (client_id,))
            conn.execute("DELETE FROM users WHERE id = ?", (client_id,))

