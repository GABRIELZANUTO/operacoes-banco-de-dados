import requests

class HanderSocket():
    URL = "http://127.0.0.1:8000/equipamentos/pesquisa"
    HEADER = { 'Content-Type': 'application/json'}
    INTERFACE = None
    SETOR = None
    COMUNICACAO = None
    TIPO = None
    

    def get(self):
        data = {
            'nome': 'Pentra',
            'setor': 'HEM'
        }

        try:
            response = requests.get(self.URL, headers=self.HEADER, json=data)
            response.raise_for_status()
            print(response)
            print(response.content)  # Exibe o conteúdo da resposta
            data = response.json()
            print(data)
        except requests.exceptions.RequestException as e:
            print(f'Erro na requisição: {e}')

teste = HanderSocket()
teste.get()