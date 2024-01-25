import decimal
import datetime
import requests
import pandas as pd
from traducoes import INTERFACEOPTION
import database as db
#Funções de validação de dados, como o pyhton não aceita todos os tipos de dados, temos que tratar se não da erro no Insert depois
def validacao_numero(valor):
    if valor is None:
        valor = "NULL"
    elif isinstance(valor,decimal.Decimal):
        valor = float(valor)        
    else:
        pass
    return valor

def validacao_caracter(valor):
    if valor is None:
        valor = ""
    else:
        pass
    return valor

def validacao_data(valor):
    if isinstance(valor, datetime.datetime):
        valor = valor.strftime("%Y-%m-%d %H:%M:%S")
    else:
        pass
    return valor

#Representação das colunas que precisamos usar da tabela
class c_ie_exam:
    def __init__(self,nidiface=None,nidexam=None,cexamlisexam=None,cexamequiexam=None,cdescexam=None,edesmembradoexam=None,nindexexam=None,cparametrosexam=None,cdiffroundexam=None):
        
        self.nidexam = validacao_numero(nidexam)
        self.nidiface = nidiface
        self.cexamlisexam = cexamlisexam
        self.cexamequiexam = cexamequiexam
        self.cdescexam = cdescexam
        self.edesmembradoexam = edesmembradoexam
        self.nindexexam = nindexexam
        self.tinc = "Now()"
        self.talt = "Now()"
        self.cparametrosexam = cparametrosexam
        self.cdiffroundexam = validacao_caracter(cdiffroundexam)

    def gravar_planilha_ieexam(self,lista,nindexexam,nidiface):
        self.nidiface = validacao_numero(nidiface)
        self.cexamlisexam = validacao_caracter(lista[0])
        self.cexamequiexam = validacao_caracter(lista[1])
        self.cdescexam = validacao_caracter(lista[2])
        self.nindexexam = validacao_numero(nindexexam)
        self.edesmembradoexam = "N"
        self.tinc = "now()"

        return f"({self.nidiface},'{self.cexamlisexam}','{self.cexamequiexam}','{self.cdescexam}','{self.edesmembradoexam}',{self.nindexexam},{self.tinc})"
    
    def gravar_modelopronto(self,lista,nidiface,nindexexam):
        self.nidiface = nidiface
        self.cexamequiexam = validacao_caracter(lista[0])
        self.cexamlisexam = validacao_caracter(lista[1])
        self.cdescexam = validacao_caracter(lista[2])
        self.edesmembradoexam = validacao_caracter(lista[3])
        self.nindexexam = nindexexam
        if len(lista) == 5 :
            self.cdiffroundexam = validacao_caracter(lista[4])
        else:
            pass

        return f"({self.nidiface},'{self.cexamequiexam}','{self.cexamlisexam}','{self.cdescexam}','{self.edesmembradoexam}',{self.nindexexam},'{self.cdiffroundexam}',{self.tinc})"
     
    def gravar_copia(self,lista,nidiface,nindexexam=None):
        self.nidexam = lista[0]
        self.nidiface = validacao_numero(nidiface)
        self.cexamequiexam = validacao_caracter(lista[1])
        self.cexamlisexam = validacao_caracter(lista[2])
        self.cdescexam = validacao_caracter(lista[3])
        self.edesmembradoexam = validacao_caracter(lista[4])
        if len(lista) == 8:
            self.nindexexam = validacao_numero(lista[5])
            self.cparametrosexam = validacao_caracter(lista[6])
            self.cdiffroundexam = validacao_caracter(lista[7])
        else:
            self.nindexexam = validacao_numero(nindexexam)
            self.cparametrosexam = validacao_caracter(lista[5])
            self.cdiffroundexam = validacao_caracter(lista[6])


        return f"({self.nidiface},'{self.cexamequiexam}','{self.cexamlisexam}','{self.cdescexam}',{self.tinc},'{self.edesmembradoexam}',{self.nindexexam},'{self.cparametrosexam}','{self.cdiffroundexam}')"

               
class c_ie_var:
    def __init__(self,nidvar=None,nidexam=None,cnomeequivar=None,cnomelisvar=None,nordemvar=None,cfatorvar=None,cexamequivar=None,nminimovar=None,ninferiorvar=None,nsuperiorvar=None,nmaximovar=None,cdecimaisvar=None,tinc=None,talt=None):
        self.nidvar = nidvar
        self.nidexam = nidexam
        self.cnomeequivar = cnomeequivar
        self.cnomelisvar = cnomelisvar
        self.nordemvar = nordemvar
        self.cfatorvar = cfatorvar
        self.tinc = "Now()"
        self.talt = "Now()"
        self.cexamequivar = cexamequivar
        self.nminimovar = nminimovar
        self.ninferiorvar = ninferiorvar
        self.nsuperiorvar = nsuperiorvar
        self.nmaximovar = nmaximovar
        self.cdecimaisvar = cdecimaisvar
    
    def copiar_exame(self,lista):
        self.cnomeequivar = validacao_caracter(lista[0])
        self.cnomelisvar = validacao_caracter(lista[1])
        self.nordemvar = validacao_numero(lista[2])
        self.cfatorvar = validacao_caracter(lista[3])
        self.cexamequivar = validacao_caracter(lista[4])
        self.nminimovar = validacao_numero(lista[5])
        self.ninferiorvar = validacao_numero(lista[6])
        self.nsuperiorvar = validacao_numero(lista[7])
        self.nmaximovar = validacao_numero(lista[8])
        self.cdecimaisvar = validacao_caracter(lista[9])
        
    def gravar_modelopronto(self,lista,nidexam):
        self.nidexam = nidexam
        self.cnomeequivar= validacao_caracter(lista[0])
        self.cnomelisvar = validacao_caracter(lista[1])
        self.nordemvar = validacao_numero(lista[2])
        self.cfatorvar = validacao_caracter(lista[3])
    

        return f"({self.nidexam},'{self.cnomeequivar}','{self.cnomelisvar}',{self.nordemvar},'{self.cfatorvar}',{self.tinc})"
        
    def gravar_copia(self,lista,nidexam):
        self.nidexam = validacao_numero(nidexam)
        self.cnomeequivar = validacao_caracter(lista[0])
        self.cnomelisvar = validacao_caracter(lista[1])
        self.nordemvar = validacao_numero(lista[2])
        self.cfatorvar = validacao_caracter(lista[3])
        self.cexamequivar = validacao_caracter(lista[4])
        self.nminimovar = validacao_numero(lista[5])
        self.ninferiorvar = validacao_numero(lista[6])
        self.nsuperiorvar = validacao_numero(lista[7])
        self.nmaximovar = validacao_numero(lista[8])
        self.cdecimaisvar = validacao_caracter(lista[9])

        return f"({self.nidexam},'{self.cnomeequivar}','{self.cnomelisvar}',{self.nordemvar},'{self.cfatorvar}',{self.tinc},'{self.cexamequivar}',{self.nminimovar},{self.ninferiorvar},{self.nsuperiorvar},{self.nmaximovar},'{self.cdecimaisvar}')"
        
class c_ie_face():
    def __init__(self,nidiface = None, nidequi = None, nidsetor = None, cnomeiface = None, etipoenviface = None, etipocomiface = None, nportaiface = None, nbaudiface = None, nbitsdadosiface = None, nbitsparadaiface = None, nparidadeiface = None, cbufferentradaiface = None, cbuffersaidaiface = None, ntcpportiface = None, ntcpport2iface = None, cpathpediface = None, cpathresiface = None, eativoiface = None, nrackiface = None, nposrackiface = None, erevisariface = None, econfirmanormaisiface = None, eenviapariface = None, ewlautoiface = None, nqtdwlautoiface = None, eusaprot2iface = None, eusartsiface = None, ctcphostiface = None, cpathimagemiface = None, etrocaseparadoriface = None, ntcpport3iface = None, ntcpport4iface = None, cwshostiface = None, cloginiface = None, csenhaiface = None, eimportresuimagemiface = None):
        self.nidiface = nidiface
        self.nidequi = nidequi
        self.nidsetor = nidsetor
        self.cnomeiface = cnomeiface
        self.etipoenviface = etipoenviface
        self.etipocomiface = etipocomiface
        self.nportaiface = nportaiface
        self.nbaudiface = nbaudiface
        self.nbitsdadosiface = nbitsdadosiface
        self.nbitsparadaiface = nbitsparadaiface
        self.nparidadeiface = nparidadeiface
        self.cbufferentradaiface = cbufferentradaiface
        self.cbuffersaidaiface = cbufferentradaiface
        self.ntcpportiface = ntcpportiface
        self.ntcpport2iface = ntcpport2iface
        self.cpathpediface = cpathpediface
        self.cpathresiface = cpathresiface
        self.eativoiface = eativoiface
        self.tinc = "Now()"
        self.talt = "Now()"
        self.nrackiface = nrackiface
        self.nposrackiface = nrackiface
        self.erevisariface = nrackiface
        self.econfirmanormaisiface = econfirmanormaisiface
        self.eenviapariface = eenviapariface
        self.ewlautoiface = ewlautoiface
        self.nqtdwlautoiface = nqtdwlautoiface
        self.eusaprot2iface = eusaprot2iface
        self.eusartsiface = eusartsiface
        self.ctcphostiface = ctcphostiface
        self.cpathimagemiface = cpathimagemiface
        self.etrocaseparadoriface = etrocaseparadoriface
        self.ntcpport3iface = ntcpport3iface
        self.ntcpport4iface = ntcpport4iface
        self.cwshostiface = cwshostiface
        self.cloginiface = cloginiface
        self.csenhaiface = csenhaiface
        self.eimportresuimagemiface=eimportresuimagemiface
    
    def gravar_modeloface(self,lista):
        self.nidequi = validacao_numero(lista[0])
        self.nidsetor = validacao_numero(lista[1])
        self.cnomeiface = validacao_caracter(lista[2])
        self.etipoenviface = validacao_caracter(lista[3])
        self.etipocomiface = validacao_caracter(lista[4])
        self.nportaiface = validacao_numero(lista[5])
        self.nbaudiface = validacao_numero(lista[6])
        self.nbitsdadosiface = validacao_numero(lista[7])
        self.nbitsparadaiface = validacao_numero(lista[8])
        self.nparidadeiface = validacao_numero(lista[9])
        self.cbufferentradaiface = validacao_caracter(lista[10])
        self.cbuffersaidaiface = validacao_caracter(lista[11])
        self.ntcpportiface = validacao_numero(lista[12])
        self.ntcpport2iface = validacao_numero(lista[13])
        self.cpathpediface = validacao_caracter(lista[14])
        self.cpathresiface = validacao_caracter(lista[15])
        self.eativoiface = validacao_caracter(lista[16])
        self.nrackiface = validacao_numero(lista[17])
        self.nposrackiface = validacao_numero(lista[18])
        self.erevisariface = validacao_caracter(lista[19])
        self.econfirmanormaisiface = validacao_caracter(lista[20])
        self.eenviapariface = validacao_caracter(lista[21])
        self.ewlautoiface = validacao_caracter(lista[22])
        self.nqtdwlautoiface = validacao_numero(lista[23])
        self.eusaprot2iface = validacao_caracter(lista[24])
        self.eusartsiface = validacao_caracter(lista[25])
        self.ctcphostiface = validacao_caracter(lista[26])
        self.cpathimagemiface = validacao_caracter(lista[27])
        self.etrocaseparadoriface = validacao_caracter(lista[28])
        self.ntcpport3iface = validacao_numero(lista[29])
        self.ntcpport4iface = validacao_numero(lista[30])
        self.cwshostiface = validacao_caracter(lista[31])
        self.cloginiface = validacao_caracter(lista[32])
        self.csenhaiface = validacao_caracter(lista[33])
        self.eimportresuimagemiface=validacao_caracter(lista[34])

        return f"({self.nidequi},{self.nidsetor},'{self.cnomeiface}','{self.etipoenviface}','{self.etipocomiface}',{self.nportaiface},{self.nbaudiface},{self.nbitsdadosiface},{self.nbitsparadaiface},{self.nparidadeiface},'{self.cbufferentradaiface}','{self.cbuffersaidaiface}',{self.ntcpportiface},{self.ntcpport2iface},'{self.cpathpediface}','{self.cpathresiface}','{self.eativoiface}',{self.tinc},{self.nrackiface},{self.nposrackiface},'{self.erevisariface}','{self.econfirmanormaisiface}','{self.eenviapariface}','{self.ewlautoiface}',{self.nqtdwlautoiface},'{self.eusaprot2iface}','{self.eusartsiface}','{self.ctcphostiface}','{self.cpathimagemiface}','{self.etrocaseparadoriface}',{self.ntcpport3iface},{self.ntcpport4iface},'{self.cwshostiface}','{self.cloginiface}','{self.csenhaiface}','{self.eimportresuimagemiface}')"






class HandlerApi():
    URL = "https://backup.gszanuto.com.br//equipamentos/pesquisa"

    def get_tokens(self):
        url_tokens = 'https://backup.gszanuto.com.br//token/'
        data ={
            "username":"z",
            "password":"z",
            'unit_id':''
        }

        headers = {
        "Content-Type": "application/json"
        }   

        try:
            response = requests.post(url_tokens, json=data,headers=headers)
        except Exception as e:
            print(('Erro ao conectar com credenciais',f'{e}'))
        if response.status_code == 200:
            token_data = response.json()
            self.acessToken = token_data.get("access")
            self.refreshToken = token_data.get("refresh")
            self.HEADER = { 
                'Authorization': f'Bearer {self.acessToken}',
                'Content-Type': 'application/json',
        
            }
            if self.acessToken == None or self.refreshToken == None:
                raise ValueError('Não conseguiu pegar credenciais, verifique usuário, senha e token !!')
        else:
            raise ValueError('Não conseguiu pegar credenciais, verifique usuário, senha e token !!')     
        
    def post(self,data):
        try:
            response = requests.post(self.URL, headers=self.HEADER, json=data)
            response.raise_for_status()
            if response.status_code == 201:
                print('salvou')
            else:
                print('nao salvou')
        except requests.exceptions.RequestException as e:
            print(f'Erro na requisição: {e}')
    
    def get(self,data):
        try:
            response = requests.get(self.URL, headers=self.HEADER, json=data)
            if response.status_code == 200:
                json = response.json()
                return json
            elif response.status_code == 400:
                raise ValueError('Não achei esse equipamento')
            else:
                raise ValueError(f'Erro na requisisção {response.status_code}')
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Erro na requisisção {e}')
  
class HandlerPlanilha(HandlerApi):
    def __init__(self):
        self.NOMEINTERFACE = None
        self.INTERFACE = None
        self.SETOR = None
        self.COMUNICACAO = None
        self.TIPO = None
        self.LISTAEXAMES = None
        self.POSFIXO = None
        self.HOST = None
        self.USER = None
        self.SENHA = None
        self.PORTA = None


    def traduzir(self,palavra):
        return INTERFACEOPTION.get(palavra,palavra)
    def valida_comunicacao(self):
        if self.DADOSINTERFACE['comunicacao'] == 'B' and self.DADOSINTERFACE['tipo'] == 'R':
            self.DADOSINTERFACE['comunicacao'] = 'R'
        elif self.DADOSINTERFACE['comunicacao'] == 'B' and self.DADOSINTERFACE['tipo'] == 'W':
            self.DADOSINTERFACE['comunicacao'] = 'W'
        else:
            self.DADOSINTERFACE['comunicacao'] = 'U'
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
        else:
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
        else:
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
        else:
            return 'SO'

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
        separados_por_ultimo_elemento = {}
        for  value in lista:
            if not (pd.isna(value[0]) or pd.isna(value[2]) or pd.isna(value[4]) or value[3] == 'N'):
                lista_filtrada.append(value)
        
        for sublist in  lista_filtrada:
            ultimo_elemento = sublist[-1]
            if ultimo_elemento not in separados_por_ultimo_elemento:
                separados_por_ultimo_elemento[ultimo_elemento] = [sublist]
            else:
                separados_por_ultimo_elemento[ultimo_elemento].append(sublist)
        return separados_por_ultimo_elemento
        
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
           
    def ler_planilha(self,path):
        dataframe = pd.read_excel(path,skiprows=3)
        self.LISTAEXAMES = dataframe.values.tolist()
        self.LISTAEXAMES = self.filtra_planilha(self.LISTAEXAMES)
        self.criaInterface()
       
    def criaInterface(self):
        for chave, value in self.LISTAEXAMES.items():
            chave = chave.strip()
            try:
                data = {
                    'nome':F'{chave}'
                }
                self.DADOSINTERFACE = self.get(data)
                self.valida_comunicacao()
                self.DADOSINTERFACE['setor'] = self.traduzir(self.DADOSINTERFACE['setor'])
                self.DADOSINTERFACE['conexao'] = self.traduzir(self.DADOSINTERFACE['conexao'])
                comand_iface = f" INSERT INTO ie_iface (NIDEQUI,NIDSETOR,CNOMEIFACE,ETIPOENVIFACE,ETIPOCOMIFACE,NPORTAIFACE,NBAUDIFACE,NBITSDADOSIFACE,NBITSPARADAIFACE,NPARIDADEIFACE,CBUFFERENTRADAIFACE,CBUFFERSAIDAIFACE,EATIVOIFACE,TINC,EREVISARIFACE,ECONFIRMANORMAISIFACE,EENVIAPARIFACE,EWLAUTOIFACE,NQTDWLAUTOIFACE,EUSAPROT2IFACE,EUSARTSIFACE,ETROCASEPARADORIFACE,EIMPORTRESUIMAGEMIFACE,NTCPPORTIFACE,NTCPPORT2IFACE,NTCPPORT3IFACE,NTCPPORT4IFACE) values ({self.DADOSINTERFACE['id']},{self.DADOSINTERFACE['setor']},'{self.DADOSINTERFACE['nome']}','{self.DADOSINTERFACE['comunicacao']}','{self.DADOSINTERFACE['conexao']}',2,7,3,0,0,'3000','3000','S',now(),'N','N','N','N',0,'N','N','N','N',NULL,NULL,NULL,NULL) "
                db.insert(host=self.HOST,user=self.USER,port=self.PORTA,passwd=self.SENHA,comando=comand_iface)
                nidiface = db.select_database(host=self.HOST,user=self.USER,port=self.PORTA,passwd=self.SENHA,comando='SELECT MAX(NIDIFACE) FROM IE_IFACE ')
                nidiface = nidiface[0]
            except Exception or ValueError as e:
                print(e)
            db.insert_planilha(host=self.HOST,user=self.USER,passwd=self.SENHA,port=self.PORTA,nidiface=nidiface,conteudo=value,posfixo=self.POSFIXO)
        
