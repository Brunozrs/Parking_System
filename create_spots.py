from Model.SizeEnum import Size
from Model.ParkingSpace import ParkingSpace
from Repository.parking_space_repo import ParkingSpaceRepo
from database import init_db


def iniciar_vagas():
    init_db()
    repo = ParkingSpaceRepo()

    # Vamos criar um mix de tamanhos: 3 para Motos, 5 para Carros, 2 para Carrinhas/SUV
    vagas = [
        ParkingSpace(size=Size.Motorcycle, number=1),
        ParkingSpace(size=Size.Motorcycle, number=2),
        ParkingSpace(size=Size.Motorcycle, number=3),
        ParkingSpace(size=Size.Medium, number=4),
        ParkingSpace(size=Size.Medium, number=5),
        ParkingSpace(size=Size.Medium, number=6),
        ParkingSpace(size=Size.Medium, number=7),
        ParkingSpace(size=Size.Medium, number=8),
        ParkingSpace(size=Size.Large, number=9),
        ParkingSpace(size=Size.Large, number=10),
    ]

    print("A criar vagas no banco de dados...")

    for vaga in vagas:
        try:
            repo.save(vaga)
            print(f"Vaga {vaga.number} ({vaga.size.name}) criada com sucesso!")
        except Exception as e:
            print(f"Erro ao criar a vaga {vaga.number}: {e}")

    print("\nConcluído! Pode fechar este script e abrir o seu Dashboard.")


if __name__ == "__main__":
    iniciar_vagas()