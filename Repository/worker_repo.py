from database import get_connection
from Model.Worker import Worker

class WorkerRepo:


    def save(self, worker:Worker):
        with get_connection() as conn:
            cursor =  conn.execute(
            "INSERT INTO users ( name, phone_number, email, document, address, type) VALUES (?,?,?,?,?,?)",
                (worker.name, worker.phonenumber, worker.email, worker.document, worker.address, "worker")
            )
            user_id = cursor.lastrowid
            conn.execute(
                "INSERT INTO workers (id, salary, password, role) VALUES (?,?,?,?)",
                (user_id, worker.salary, worker.password, worker.role)
            )
            worker._id = user_id # atribui o id gerado de

    def find_all(self) ->list[Worker]:
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT u.id, u.name, u.phone_number, u.email, u.document, u.address, w.salary, w.password, w.role
                FROM users u JOIN workers w ON u.id = w.id
            """).fetchall()

        workers = []
        for row in rows:
            worker = Worker(
                name=row["name"], phone_number=row["phone_number"],
                email=row["email"], document=row["document"],
                address=row['address'], salary=row["salary"],
                password=row["password"], role=row["role"]
            )
            worker._id = row["id"]
            workers.append(worker)
        return workers

    def find_by_id(self, worker_id: int):
        with get_connection() as conn:
            row = conn.execute("""
                SELECT u.id, u.name, u.phone_number, u.email, u.document, u.address, w.salary, w.password, w.role
                FROM users u JOIN workers w ON u.id = w.id
                WHERE u.id=?
            """,(worker_id,)).fetchone()

        if row is None:
            raise ValueError(f"Worker {worker_id} not found")
            # Criamos o objeto Worker injetando os dados da linha do banco
        worker =  Worker(
            name=row['name'],  # ou row[1]
            phone_number=row['phone_number'],  # ou row[2]
            email=row['email'],  # ou row[3]
            document=row['document'],  # ou row[4]
            address=row['address'],# ou row[5]
            salary=row['salary'],  # ou row[6]
            password=row["password"],
            role=row["role"]
        )
        worker._id = row['id']
        return worker

    def find_by_email(self, email:str):
        with get_connection() as conn:
            row = conn.execute("""
                SELECT u.id, u.name, u.phone_number, u.email, u.document, u.address, w.salary, w.password, w.role
                FROM users u JOIN workers w ON u.id=w.id
                WHERE u.email=?
            """,(email,)).fetchone()

        if row is None:
            return None

        worker = Worker(
            name=row["name"], phone_number=row["phone_number"],
            email=row["email"], document=row["document"],
            address=row["address"], salary=row["salary"],
            password=row["password"], role=row["role"]
        )
        worker._id = row["id"]

        return worker

    def update(self, worker:Worker):
        if worker.id is None:
            raise ValueError("Worker has no ID - Save before Updating")
        with get_connection()as conn:
            conn.execute("""
                UPDATE users
                SET name=?, phone_number=?, email=?, document=?, address=?, password=?, role=?
                WHERE id=?
            """,(worker.name, worker.phonenumber, worker.email, worker.document, worker.address, worker.password, worker.role, worker.id))

            conn.execute("""
                UPDATE workers
                SET salary=?, password=?, role=?
                WHERE id=?
            """, (worker.salary, worker.password, worker.role, worker.id))

    def delete(self, worker_id: int):
        with get_connection() as conn:
            # deleta primeiro as linhas para respeitar chaves estrangeiras
            conn.execute("DELETE FROM workers WHERE id = ?", (worker_id,))
            conn.execute("DELETE FROM users WHERE id = ?", (worker_id,))