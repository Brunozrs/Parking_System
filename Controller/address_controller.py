from Service.address_Service import fetch_address_data

class AddressController:
    def get_address(self, CEP: str)->dict:
        # Retira erros de digitação do usuário
        CEP = CEP.replace("-", "").replace(" ", "").strip()

        if len(CEP) !=8 or not CEP.isdigit():
            raise ValueError("CEP must be 8 digits!")

        data = fetch_address_data(CEP)

        if data is None or "erro" in data:
            raise ValueError(f"CEP: {CEP} not found!")

        return {
            "cep": data.get("cep"),
            "street": data.get("logradouro"),
            "neighborhood": data.get("bairro"),
            "city": data.get("localidade"),
            "state": data.get("uf")
        }