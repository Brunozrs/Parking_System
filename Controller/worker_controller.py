from Repository.worker_repo import WorkerRepo
from Model.Worker import Worker
from Service.auth_service import hash_password

class WorkerController:
    def __init__(self):
        self.repo = WorkerRepo()

    def create_worker(self, name, phone_number, email, document, address, salary, password, role):
        worker = Worker(
            name=name, phone_number=phone_number,
            email=email, document=document,
            address=address, salary=salary,
            password = hash_password(password), role = role
        )
        self.repo.save(worker)
        return worker

    def update_worker(self,worker_id, name, phone_number, email, document, address, salary,password,role):

        worker = self.repo.find_by_id(worker_id)
        worker.name = name
        worker.phonenumber = phone_number
        worker.email = email
        worker.document = document
        worker.address = address
        worker.salary = salary
        if password:
            worker.password = password
        if role:
            worker.role = role
        self.repo.update(worker)
        return worker

    def delete_worker(self, worker_id):
        self.repo.delete(worker_id)

    def list_workers(self):
        return self.repo.find_all()