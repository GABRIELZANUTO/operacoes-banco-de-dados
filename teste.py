import requests
import pandas as pd
import math

class InserirPlainlha():
    def __init__(self):
        
        self.NOMEINTERFACE = None
        self.INTERFACE = None
        self.SETOR = None
        self.COMUNICACAO = None
        self.TIPO = None
        self.LISTAEXAMES = None

    def filtra_setor(self,value):
        if value =='Hematologia':
            return 'HEM'
        elif value =='Bioquímica':
            return 'BIO'
        elif value =='Gasometria':
            return 'GAS'
        elif value =='Imunologia':
            return 'IMU'
        elif value =='Coagulação':
            return 'COA ' 
        elif value =='Bioquímica':
            return 'BIO'
        elif value =='Urinálise':
            return 'URI'
        elif value =='Hemoglobina':
            return 'HMO'
        elif value =='Eletrosferase':
            return 'ELE '
        elif value =='Microbiologia':
            return 'MIC'
        elif value =='Triagem/Esteira':
            return 'TRI '
        elif value =='Imuno/Sorologia':
            return 'IMS'
        elif value =='Imuno/Bioquim.':
            return 'IMB'
        elif value == 'Todos':
            return 'TOD'
        
                         

    def filtra_tipo(self,value):
        if value == 'Request':
            return 'R'
        elif value == 'Worklist':
            return 'W'
        elif value == '----':
            return '-'
        else:
            return '-'

    def filtra_comunicacao(self,value):
        if value == 'Bi':
            return 'B'
        elif value == 'Uni':
            return 'U'
        elif value == 'Bi/Uni':
            return 'B'
        elif value == '--':
            return 'B'

    def filtra_conexao(self,value):
        if value == 'Socket':
            return 'SO'
        elif value == 'Serial':
            return 'SE'
        elif value == 'Arquivo':
            return 'AB'
        elif value == '--':
            return 'SO'
        elif value =='Arquivo/banco':
            return 'AB'

    def filtra_desenvolvido(self,value):
        if value == 'S':
            return 1
        else:
            return 0

    def filtra_protocolo(self,value):
        if value == 'HL7' :
            return 'H'
        elif value == 'ASTM':
            return 'A'
        else:
            return 'P'    

    def filtra_planilha(self,lista):
        lista_filtrada = []
        for  value in lista:
            if not (pd.isna(value[0]) or pd.isna(value[2]) or pd.isna(value[4]) or value[3] == 'N'):
                lista_filtrada.append(value)
        return lista_filtrada
    
    def filtraPlanilhaExam(self,lista):
        for value in lista:
            self.ID = value[0]
            self.NOME = value[1]
            self.SETOR = self.filtra_setor(value[2])
            self.COMUNICACAO= self.filtra_comunicacao(value[3])
            self.TIPO = self.filtra_tipo(value[4])
            self.CONEXAO = self.filtra_conexao(value[5])
            self.PROTOCOLO = self.filtra_protocolo(value[6])
            self.DENSENVOLVIDO = self.filtra_desenvolvido(value[7])

            print('----iniciou um exam ------')
            print(self.ID)
            print(self.NOME)
            print(self.SETOR)
            print(self.COMUNICACAO)
            print(self.TIPO)
            print(self.CONEXAO)
            print(self.PROTOCOLO)
            print(self.DENSENVOLVIDO)
            print('----Finalizou um exam ------')
           
           

        # print(lista)

            

    def ler_planilha(self,path):
        dataframe = pd.read_excel(path,skiprows=1)
        self.LISTAEXAMES = dataframe.values.tolist()
      
        self.LISTAEXAMES = self.filtraPlanilhaExam(self.LISTAEXAMES)




class HandlerApi(InserirPlainlha):
    def __init__(self):
        self.URL = "http://127.0.0.1:8000/equipamentos/pesquisa"
        self.HEADER = { 'Content-Type': 'application/json'}   
    def get(self):
        
        data = {
            'nome': 'Pentra',
            'setor': 'HEM'
        }
        try:
            response = requests.get(self.URL, headers=self.HEADER, json=data)
            response.raise_for_status()
            json = response.json()
            self.NOMEINTERFACE = json['nome']
            self.INTERFACE = json['id']
            self.SETOR = json['setor']
            self.COMUNICACAO = json['comunicacao']
            self.TIPO = json['tipo']
        except requests.exceptions.RequestException as e:
            print(f'Erro na requisição: {e}')


teste = HandlerApi()
# teste.get()
# print(teste.NOMEINTERFACE)
# print(teste.TIPO)
# print(teste.SETOR)
# print(teste.INTERFACE)
# print(teste.COMUNICACAO)
teste.ler_planilha('testelistaexam.xlsx')