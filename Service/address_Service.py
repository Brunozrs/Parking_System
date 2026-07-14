import requests

def fetch_address_data(cep):
    # Pega a url e verifica se o codigo de status é 200(OK)

    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    return None