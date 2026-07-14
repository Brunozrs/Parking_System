from Model.SizeEnum import Size
from database import get_connection
from Model.Vehicle import Vehicle

class VehicleRepo:

    def save(self, vehicle: Vehicle):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO vehicles (plate, color, size, client_id, image_b64,space_id) VALUES(?,?,?,?,?,?)",
                (vehicle.plate, vehicle.color, vehicle.size.value, vehicle.client_id, vehicle.image_b64, vehicle.space_id)
            )
            vehicle._id = cursor.lastrowid

    def find_by_id(self, vehicle_id: int) -> Vehicle:
        with get_connection() as conn:
            row= conn.execute(
                "SELECT * FROM vehicles WHERE id = ?", (vehicle_id,)
            ).fetchone()

        if row is None:
            raise ValueError(f"Vehicle {vehicle_id} not found")

        return Vehicle(
            id = row["id"],
            plate = row["plate"],
            color = row["color"],
            size = Size(row["size"]),
            client_id = row["client_id"], # só o id, não o objeto inteiro
            image_b64 = row["image_b64"],
            space_id = row["space_id"]
        )

    def find_all(self) -> list[Vehicle]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM vehicles").fetchall()

        vehicles = []
        for row in rows:
            # Pegamos do banco e transformamos no objeto Vehicle
            vehicles.append(Vehicle(
                id=row["id"],
                plate=row["plate"],
                color=row["color"],
                size=Size(row["size"]),
                client_id=row["client_id"],
                image_b64=row["image_b64"],
                space_id=row["space_id"]
            ))
        return vehicles

    def find_by_client(self, client_id: int) -> list[Vehicle]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM vehicles WHERE client_id = ?", (client_id,)
            ).fetchall()

        vehicles = []
        for row in rows:
            v = Vehicle(
                id=row["id"],
                plate=row["plate"],
                color=row["color"],
                size=Size(row["size"]),
                client_id=row["client_id"],
                image_b64=row["image_b64"],
                space_id=row["space_id"]
            )
            vehicles.append(v)
        return vehicles

    def update(self, vehicle:Vehicle):
        if vehicle.id is None:
            raise ValueError("Vehicle has no ID - Save before updating")
        with get_connection() as conn:
            conn.execute("""
                UPDATE vehicles
                SET plate=?, color=?, size=?, space_id=?
                WHERE id=?
                """,(vehicle.plate, vehicle.color, vehicle.size.value, vehicle.space_id, vehicle.id))

    def delete(self, vehicle_id: int):
        with get_connection() as conn:
            conn.execute("DELETE FROM vehicles WHERE id= ?", (vehicle_id,))