import pandas as pd
from PySimpleGUI import PySimpleGUI as sg
import database as db
from distutils.log import ERROR
from classes import *
import pickle
import templates as temp

ie_exam = c_ie_exam()
ie_var = c_ie_var()
ie_iface = c_ie_face()
# -----------------------------------------------------------------------------BackEnd--------------------------------------------------------------------------------------------------
def inserir_planilha(host,user,passwd,port,nidiface):
    dataframe = pd.read_excel("Exames.xls")
    lista = dataframe.values.tolist()
    db.insert_planilha(host,user,passwd,port,nidiface,lista)

def insert_hem(host,user,passwd,port,nidiface):
    hem_ieexam = ('HEM', 'HEM', 'HEM', 'N', 'SEGMENTADOS|BLASTOS|PROMIELOCITOS|MIELOCITOS|METAMIELOCITOS|BASTONETES|EOSINOFILOS|BASOFILOS|LINFOCITOS|MONOCITOS')
    hem_ieevar =  [('Hemacias', 'HEMACIA', 1, None), ('Hemoglobinas', 'HEMOGLOBINA', 2, None), ('Hematocritos', 'HEMATOCRITO', 3, None), ('RDW', 'RDW', 4, None), ('Leucocitos', 'LEUCOCITOS', 5, '*1000'), ('Blastos_P', 'BLASTOS', 6, None), ('PMielocitos_P', 'PROMIELOCITOS', 7, None), ('MIELOCITOS_P', 'MIELOCITOS', 8, None), ('MetaMielocitos_P', 'METAMIELOCITOS', 9, None), ('Bastoes_P', 'BASTONETES', 10, None), ('Segmentados_P', 'SEGMENTADOS', 11, None), ('LINFOCITOS_P', 'LINFOCITOS', 12, None), ('Monocitos_P', 'MONOCITOS', 13, None), ('Eosinofilos_P', 'EOSINOFILOS', 14, None), ('Basofilos_P', 'BASOFILOS', 15, None), ('Plaquetas', 'PLAQUETAS', 16, '*1000')]
    db.insert_modelpronto(host,user,passwd,port,nidiface,hem_ieexam,hem_ieevar)

def insert_gav(host,user,passwd,port,nidiface):
    gav_ieexam= ('GASOV', 'GASV', 'GASOMETRIA VENOSA', 'N')
    gav_ieevar = [('pH', 'PH', 1, None), ('PO2', 'PO2', 2, None), ('PCO2', 'PCO2', 3, None), ('SO2', 'SO2', 4, None), ('cHCO3', 'HCO3', 5, None), ('BE', 'BE', 6, None), ('Na', 'SODIO', 7, None), ('K', 'POTASSIO', 8, None), ('Ca', 'CAIO', 9, None), ('Cl', 'CLORETO', 10, None), ('Glu', 'GLICOSE', 11, None), ('Lac', 'LACT', 12, None)]
    db.insert_modelpronto(host,user,passwd,port,nidiface,gav_ieexam,gav_ieevar)

def extrair_config(host,user,passwd,port,planilha):
  comando = f"SELECT ie_exam.CEXAMLISEXAM,ie_exam.CEXAMEQUIEXAM,ie_exam.CDESCEXAM,ie_var.CNOMELISVAR FROM ie_exam  INNER JOIN ie_var ON ie_exam.NIDEXAM = ie_var.NIDEXAM WHERE ie_exam.NIDIFACE ={planilha}"
  retorno = db.select_database(host,user,passwd,port,comando,modo="ALL")
  dic = {}
  mnemonico = []
  cod_equi = []
  nome = []
  lis = []
  #separação das lista que retono do select em colunas
  for i in retorno:
    mnemonico.append(i[0])
    cod_equi.append(i[1])
    nome.append(i[2])
    lis.append(i[3])
  dic['mnemonico'] = mnemonico
  dic['codigo_equp'] = cod_equi
  dic['nome'] = nome
  dic['lis'] =lis
  dados= pd.DataFrame.from_dict(dic, orient='index')
  dados = dados.transpose()
  dados.to_excel("dados_interface="+str(planilha)+".xlsx",index=False)

#Função para cirar modelo do exame
def criar_modeloexam(host,user,passwd,port,menmonico,interface,nome):
    select_ieexam = f"SELECT NIDEXAM,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM FROM ie_exam WHERE CEXAMLISEXAM ='{menmonico}' AND NIDIFACE={interface}" 
    dados_ieexam = db.select_database(host,user,passwd,port,select_ieexam)
    nidexam = dados_ieexam[0]
    select_ievar =f"SELECT CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR from ie_var WHERE NIDEXAM={nidexam}"
    dados_ievar = db.select_database(host,user,passwd,port,select_ievar,"ALL")
    modelo = [dados_ieexam,dados_ievar]
    with open(f'{nome}.exam','wb') as arquivo:
       pickle.dump(modelo,arquivo)

#Função para inserir modelo do exame
def inserir_modeloexam(host,user,passwd,port,interface_destino,caminho_modelo):
    comando_nindexexam = f"SELECT MAX(NINDEXEXAM) FROM ie_exam WHERE NIDIFACE= {interface_destino}"
    comando_nidexam = "SELECT MAX(NIDEXAM) FROM ie_exam"
    nindexexam = db.select_database(host,user,passwd,port,comando_nindexexam)
    with open(caminho_modelo,"rb") as arquivo:
      lista_recuperada = pickle.load(arquivo)
    retorno_ieexam = lista_recuperada.pop(0)
    nindexexam = nindexexam[0]
    if nindexexam is None:
      nindexexam=1
    else:
      nindexexam =nindexexam+1
    dados_ieexam = ie_exam.gravar_copia(retorno_ieexam,interface_destino,nindexexam)
    insert_ieexam= f"INSERT INTO ie_exam(NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,TINC,EDESMEMBRADOEXAM,NINDEXEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM) values " +dados_ieexam
    db.insert(host,user,passwd,port,insert_ieexam)
    nidexam = db.select_database(host,user,passwd,port,comando_nidexam)
    for i in lista_recuperada:
       for j in i:
          dados_ievar = ie_var.gravar_copia(j,nidexam[0])
          insert_ievar = f"INSERT INTO ie_var(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR) values" + dados_ievar
          db.insert(host,user,passwd,port,insert_ievar) 

def criar_modeloface(host,user,passwd,port,interface,nome):
  select_ieexam = f"SELECT NIDEXAM,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM FROM ie_exam WHERE NIDIFACE={interface}"
  select_ieiface = f"SELECT NIDEQUI, NIDSETOR, CNOMEIFACE, ETIPOENVIFACE, ETIPOCOMIFACE, NPORTAIFACE, NBAUDIFACE, NBITSDADOSIFACE, NBITSPARADAIFACE, NPARIDADEIFACE, CBUFFERENTRADAIFACE, CBUFFERSAIDAIFACE, NTCPPORTIFACE, NTCPPORT2IFACE, CPATHPEDIFACE, CPATHRESIFACE, EATIVOIFACE,NRACKIFACE, NPOSRACKIFACE, EREVISARIFACE, ECONFIRMANORMAISIFACE, EENVIAPARIFACE, EWLAUTOIFACE, NQTDWLAUTOIFACE, EUSAPROT2IFACE, EUSARTSIFACE, CTCPHOSTIFACE, CPATHIMAGEMIFACE, ETROCASEPARADORIFACE, NTCPPORT3IFACE, NTCPPORT4IFACE, CWSHOSTIFACE, CLOGINIFACE, CSENHAIFACE, EIMPORTRESUIMAGEMIFACE FROM ie_iface WHERE NIDIFACE= {interface}"
  retorno_ieexam = db.select_database(host,user,passwd,port,select_ieexam,"ALL")
  retorno_ieiface = db.select_database(host,user,passwd,port,select_ieiface)
  dados_ievar = []
  for i in retorno_ieexam:
    select_ievar =f"SELECT CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR from ie_var WHERE NIDEXAM={i[0]}"
    retorno_ievar = db.select_database(host,user,passwd,port,select_ievar,"ALL")
    dados_ievar.append(retorno_ievar)
  modelo = [retorno_ieiface,retorno_ieexam,dados_ievar]
  with open(f'{nome}.face','wb') as arquivo:
    pickle.dump(modelo,arquivo)
    
def inserir_modeloface(host,user,passwd,port,caminho_modelo):
  comando_nidiface = "SELECT MAX(NIDIFACE) FROM ie_iface"
  with open(caminho_modelo,"rb") as arquivo:
    lista_recuperada = pickle.load(arquivo)
  dados_ieiface = ie_iface.gravar_modeloface(lista_recuperada[0])
  insert_ieiface =" INSERT INTO ie_iface (NIDEQUI, NIDSETOR, CNOMEIFACE, ETIPOENVIFACE, ETIPOCOMIFACE, NPORTAIFACE, NBAUDIFACE, NBITSDADOSIFACE, NBITSPARADAIFACE, NPARIDADEIFACE, CBUFFERENTRADAIFACE, CBUFFERSAIDAIFACE, NTCPPORTIFACE, NTCPPORT2IFACE, CPATHPEDIFACE, CPATHRESIFACE, EATIVOIFACE,TINC,NRACKIFACE, NPOSRACKIFACE, EREVISARIFACE, ECONFIRMANORMAISIFACE, EENVIAPARIFACE, EWLAUTOIFACE, NQTDWLAUTOIFACE, EUSAPROT2IFACE, EUSARTSIFACE, CTCPHOSTIFACE, CPATHIMAGEMIFACE, ETROCASEPARADORIFACE, NTCPPORT3IFACE, NTCPPORT4IFACE, CWSHOSTIFACE, CLOGINIFACE, CSENHAIFACE, EIMPORTRESUIMAGEMIFACE) values" + dados_ieiface
  db.insert(host,user,passwd,port,insert_ieiface)
  nidiface = db.select_database(host,user,passwd,port,comando_nidiface)
  for i in lista_recuperada[1]:
    dados_iexam = ie_exam.gravar_copia(i,nidiface[0])
    insert_ieexam = f"INSERT INTO ie_exam(NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,TINC,EDESMEMBRADOEXAM,NINDEXEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM) VALUES " +dados_iexam
    db.insert(host,user,passwd,port,insert_ieexam)
  comando_nidexam = f"SELECT NIDEXAM FROM ie_exam WHERE NIDIFACE = {nidiface[0]}"
  retorno_nidexam = db.select_database(host,user,passwd,port,comando_nidexam,"ALL")
  contador= 0
  for i in lista_recuperada[2]:
    for j in i:
      dados_ievar = ie_var.gravar_copia(j,retorno_nidexam[contador][0])
      insert_ievar = f"INSERT INTO ie_var(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR) values" + dados_ievar
      db.insert(host,user,passwd,port,insert_ievar)
    contador=contador+1

def trocar_codexame(host='',user='',passwd='',port=''):
   comando = f"SELECT NIDAMOSTRA FROM ie_amostra WHERE CEXAMLISEXAM = 'CHDL' and CEXAMEQUIEXAM = 'HDL-LABT' "
   result = db.select_database(host,user,passwd,port,comando,modo='MORE')
   print(result)
   

jReenviarExames,jOperacao,jProntos,jInserir,jExtrair,JBackup,Jumexame,Jmodelos,Jcriarmodelos,jInserirmodelos,Jinserirface,Jcriarface,jConexao = temp.janela_reenviarexames(),None,None,None,None,None,None,None,None,None,None,None,None

#Inicio das operações nas telas da interface
while True:
  window,eventos,valores = sg.read_all_windows()
  if window == jConexao:
      if eventos == sg.WIN_CLOSED:
          break
      if eventos == 'Conectar':
          try:
              host = valores['host']
              user = valores['user']
              senha = valores['senha']
              porta = valores['porta']
              db.getConection(host,user, senha, porta)
              jConexao.hide()
              jOperacao=temp.janela_Operacao()
          except Exception as e:
              sg.popup('Dados Invalidos')
              window.FindElement('user').Update('')
              window.FindElement('senha').Update('')
              window.FindElement('porta').Update('')
  if window == jOperacao:
      if eventos == sg.WIN_CLOSED:
          break
      if eventos == "Modelos Prontos":
          jOperacao.hide()
          jProntos=temp.janela_Prontos() 
      if eventos == "Inserir Planilha":
          jOperacao.hide()
          jInserir=temp.janela_inserir()
      if eventos == "Extrair Config":
          jOperacao.hide()
          jExtrair=temp.janela_extrair() 
      if eventos =='Backup':
          jOperacao.hide()
          JBackup=temp.janela_backup()
      if eventos == 'Copiar um Exame':
          jOperacao.hide()
          Jumexame = temp.janela_umexame()
      if eventos == 'Modelos':
          jOperacao.hide()
          Jmodelos = temp.janela_modelos()
      if eventos == 'Reenviar Exames':
          jOperacao.hide()
          jReenviarExames = temp.janela_reenviarexames()    
  if window == jInserir:
      if eventos == sg.WIN_CLOSED:
          break
      if eventos == 'Voltar':
          jOperacao.un_hide()
          jInserir.hide()
      if eventos == 'Enviar':
          try:
              inserir_planilha(host,user,senha,porta,valores['numeroPlanilha'])
              sg.popup("Dados gravados com Sucesso !!!")
          except ERROR as e:
              sg.popup("Erro ao gravar dados")
    
  if window == jProntos:
      if eventos == sg.WIN_CLOSED:
          break
      if eventos == "Voltar":
          jOperacao.un_hide()
          jProntos.hide()
      if eventos == "Enviar" and valores['escolhascript'] == "HEM":
          try:
              insert_hem(host,user,senha,porta,valores['numeroPlanilha'])
              sg.popup("Gravado com sucesso !!!")
          except ERROR as e:
              sg.popup("Erro ao Gravar")
    
      if eventos == "Enviar" and valores['escolhascript'] == "GAS":
          try:
              insert_gav(host,user,senha,porta,valores['numeroPlanilha'])
              sg.popup("Gravado com sucesso !!!")
          except ERROR as e:
              sg.popup("Erro ao Gravar")
    
  if window == jExtrair:
      if eventos == sg.WIN_CLOSED:
          break
      if eventos == "Voltar":
          jOperacao.un_hide()
          jExtrair.hide()
      if eventos == "Gerar":
          extrair_config(host,user,senha,porta,valores['numeroPlanilha'])
          sg.popup("Planilha Gerada !!!")
  if window == JBackup:
      if eventos == sg.WIN_CLOSED:
          break
      if eventos == "Voltar":
          jOperacao.un_hide()
          JBackup.hide()
      if eventos == "Gerar Backup":
        file_path =db.backup(host,user,senha,porta,valores['adm_backup'],valores['unidade_backup'],valores['cliente'])
        result =db.manda_api(file_path,str(valores['cliente']))
        if result == True:
           sg.popup('Backup Enviado com sucesso')
        else:
           sg.popup('Erro ao mandar backup')
  if window == Jumexame:
      if eventos == sg.WIN_CLOSED:
          break
      if eventos == "Voltar":
          jOperacao.un_hide()
          Jumexame.hide()
      if eventos == "Copiar":
          try:
              db.inserirum_exame(host,user,senha,porta,valores['mnemonico'],valores['interfaceoriginal'],valores['interfacedestino'])
              sg.popup("Exame Copiado com sucesso !!!")
          except ERROR as e:
              sg.popup("Erro ao Copiar !!!") 
    
  if window == Jmodelos:
    if eventos == sg.WIN_CLOSED:
      break
    if eventos == "Voltar":
      Jmodelos.hide()
      jOperacao.un_hide()
    if eventos =="Criar Modelo Exam":
      Jmodelos.hide()
      Jcriarmodelos = temp.janela_criarmodelos()
    if eventos =="Inserir Modelo Exam":
      Jmodelos.hide()
      jInserirmodelos = temp.janela_inserirmodelos()
    if eventos == "Criar Modelo Face":
       Jmodelos.hide()
       Jcriarface = temp.janela_criarmodelosface()
    if eventos == "Inserir Modelo Face":
       Jmodelos.hide()
       Jinserirface = temp.janela_inserirmodelosface()
  if window == Jcriarmodelos:
    if eventos == sg.WIN_CLOSED:
      break
    if eventos == "Voltar":
      Jcriarmodelos.hide()
      Jmodelos.un_hide()
    if eventos == "Criar":
      criar_modeloexam(host,user,senha,porta,valores['mnemonico'],valores["interface_criar"],valores['nomemodelo'])
      sg.popup("Arquivo criado com Sucesso !!!")
  if window == jInserirmodelos:
    if eventos == sg.WIN_CLOSED:
      break
    if eventos == "Voltar":
      jInserirmodelos.hide()
      Jmodelos.un_hide()
    if eventos == "Enviar":
        inserir_modeloexam(host,user,senha,porta,valores['interface_inserir'],valores['caminho_modelo'])
        sg.popup("Modelo inserido com Sucesso !!!")
  if window == Jcriarface:
    if eventos == sg.WIN_CLOSED:
      break
    if eventos == "Voltar":
      Jcriarface.hide()
      Jmodelos.un_hide()
    if eventos == "Criar":
      criar_modeloface(host,user,senha,porta,valores['id_face'],valores['nomemodelo'])
      sg.popup("Modelo criado com sucesso !!!")
  if window == Jinserirface:
    if eventos == sg.WIN_CLOSED:
      break
    if eventos == "Voltar":
      Jinserirface.hide()
      Jmodelos.un_hide()
    if eventos == "Enviar":
      inserir_modeloface(host,user,senha,porta,valores['caminho_modelo'])
      sg.popup("Interface inserida com sucesso !!!")
  if window == jReenviarExames:
      if eventos == sg.WIN_CLOSED:
        break
      if eventos == "Voltar":
           jReenviarExames.hide()
           jOperacao.un_hide()
      if eventos == "Trocar":
         trocar_codexame()
      
                   