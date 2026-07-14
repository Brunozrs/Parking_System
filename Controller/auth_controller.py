from Service.auth_service import verify_password
from Repository.worker_repo import WorkerRepo

class AuthController:
    def __init__(self):
        self.repo = WorkerRepo()

    def login(self, email:str, password:str):
        worker = self.repo.find_by_email(email)

        if worker is None:
            raise ValueError("Email not found")

        if not verify_password(password, worker.password):
            raise ValueError("Invalid password")

        return worker #retorna o trabalhador logado com a role atribuída