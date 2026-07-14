from Model import SizeEnum
from Model.SizeEnum import Size
from database import get_connection
from Model.ParkingSpace import ParkingSpace

class ParkingSpaceRepo:

    def save(self, parking_space: ParkingSpace):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO parking_spaces (number, size, available) VALUES (?, ?, ?)",
                (parking_space.number, parking_space.size.value, int(parking_space.available))
            )
            parking_space._id = cursor.lastrowid

    def find_by_id(self, parking_space_id: int) -> ParkingSpace:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM parking_spaces WHERE id = ?",(parking_space_id,)
            ).fetchone()
        if row is None:
            raise ValueError(f"Parking space {parking_space_id} not found")

        space= ParkingSpace(
            number=row["number"],
            size= Size(row["size"])
        )

        space._id = row["id"]

        return space


    def find_available(self, size: Size = None) -> list[ParkingSpace]:
        """find_available(size=Size.Moto) → only available spaces of that size
           find_available() → all available spaces, any size"""

        with get_connection() as conn:
            if size:
                rows = conn.execute("""
                    SELECT * FROM parking_spaces
                    WHERE available = 1 and size = ?
                """, (size.value,)).fetchall()
            else:
                rows = conn.execute("""
                SELECT * FROM parking_spaces WHERE available = 1
                """).fetchall()
        spaces=[]

        for row in rows:
            space = ParkingSpace(size=Size(row["size"]), number=row["number"])
            space._id = row["id"]
            space._available = bool(row["available"]) # Converte 0/1 para False/True
            spaces.append(space)
        return spaces

    def find_all(self) -> list[ParkingSpace]:
        with get_connection() as conn:
            # Ordena pelo número da vaga para o mapa ficar em ordem (1, 2, 3...)
            rows = conn.execute("SELECT * FROM parking_spaces ORDER BY number").fetchall()

        spaces = []
        for row in rows:
            space = ParkingSpace(size=Size(row["size"]), number=row["number"])
            space._id = row["id"]
            space._available = bool(row["available"])
            spaces.append(space)
        return spaces

    def update(self, parking_space:ParkingSpace):
        if parking_space.id is None:
            raise ValueError("Parking space has no ID - Save before updating")
        with get_connection() as conn:
            conn.execute("""
                UPDATE parking_spaces
                set number=?, size=?, available=?
                where id=?
            """, (parking_space.number,  parking_space.size.value, int(parking_space.available), parking_space.id))

    def delete(self, parking_space_id:int):
        with get_connection() as conn:
            conn.execute("DELETE FROM parking_spaces WHERE id= ?", (parking_space_id,))