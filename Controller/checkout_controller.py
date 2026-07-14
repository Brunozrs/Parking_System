from Model.SizeEnum import Size
from Controller.parking_controller import ParkingSpaceController
from datetime import datetime


class CheckoutController:
    def __init__(self):
        self.parking_controller = ParkingSpaceController()

        # Tabela de Preços (R$ por hora)
        self.prices_per_hour = {
            Size.Moto: 5.00,  # Moto
            Size.Compacto:10.00,
            Size.Medio: 10.00,  # Carro Padrão
            Size.Grande: 15.00  # SUV / Caminhonete
        }

    def process_checkout(self, client, vehicle_size: Size, space_id: int) -> dict:
        """
        Processa a saída pegando o momento exato do encerramento.
        Retorna um dicionário com os dados do recibo.
        """
        if not client.arrival:
            raise ValueError("O cliente não possui data de entrada (Arrival) registrada.")

        self.parking_controller.free_space(space_id)
        # 1. Define a saída real como o EXATO MOMENTO do clique
        real_departure = datetime.now()

        # 2. Calcula a diferença de tempo (Duração)
        duration = real_departure - client.arrival
        hours = duration.total_seconds() / 3600.0

        # Opcional: Se ficou menos de 1 hora, cobra o valor mínimo de 1 hora integral
        if hours < 1.0:
            hours = 1.0

        # 3. Pega a tarifa correta baseada no tamanho do veículo
        hourly_rate = self.prices_per_hour.get(vehicle_size, 10.00)

        # 4. Calcula o total final
        total_to_pay = hours * hourly_rate

        # Retorna o "Recibo" formatado para a Interface Gráfica mostrar
        return {
            "arrival_str": client.arrival.strftime('%d/%m/%Y %H:%M'),
            "departure_str": real_departure.strftime('%d/%m/%Y %H:%M'),
            "hours_billed": round(hours, 2),
            "rate_applied": hourly_rate,
            "total_value": round(total_to_pay, 2),
            "real_departure_dt": real_departure  # Enviamos o objeto datetime para atualizar o banco se quiser
        }