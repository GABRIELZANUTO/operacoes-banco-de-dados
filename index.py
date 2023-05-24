import pandas as pd
from PySimpleGUI import PySimpleGUI as sg
import database as db
from distutils.log import ERROR
from classes import *
import pickle

ie_exam = c_ie_exam()
ie_var = c_ie_var()
# -----------------------------------------------------------------------------BackEnd--------------------------------------------------------------------------------------------------
def inserir_planilha(host,user,passwd,port,nidiface):
    dataframe = pd.read_excel("Exames.xls")
    lista = dataframe.values.tolist()
    db.insert_planilha(host,user,passwd,port,nidiface,lista)

def insert_hem(host,user,passwd,port,nidiface):
    hem_ieexam = ('HEM', 'HEM', 'HEM', 'N', 1, 'SEGMENTADOS|BLASTOS|PROMIELOCITOS|MIELOCITOS|METAMIELOCITOS|BASTONETES|EOSINOFILOS|BASOFILOS|LINFOCITOS|MONOCITOS')
    hem_ieevar =  [('Hemacias', 'HEMACIA', 1, None), ('Hemoglobinas', 'HEMOGLOBINA', 2, None), ('Hematocritos', 'HEMATOCRITO', 3, None), ('RDW', 'RDW', 4, None), ('Leucocitos', 'LEUCOCITOS', 5, '*1000'), ('Blastos_P', 'BLASTOS', 6, None), ('PMielocitos_P', 'PROMIELOCITOS', 7, None), ('MIELOCITOS_P', 'MIELOCITOS', 8, None), ('MetaMielocitos_P', 'METAMIELOCITOS', 9, None), ('Bastoes_P', 'BASTONETES', 10, None), ('Segmentados_P', 'SEGMENTADOS', 11, None), ('LINFOCITOS_P', 'LINFOCITOS', 12, None), ('Monocitos_P', 'MONOCITOS', 13, None), ('Eosinofilos_P', 'EOSINOFILOS', 14, None), ('Basofilos_P', 'BASOFILOS', 15, None), ('Plaquetas', 'PLAQUETAS', 16, '*1000')]
    db.insert_modelpronto(host,user,passwd,port,nidiface,hem_ieexam,hem_ieevar)

def insert_gav(host,user,passwd,port,nidiface):
    gav_ieexam= ('GASOV', 'GASV', 'GASOMETRIA VENOSA', 'N', 1)
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
def criar_modelo(host,user,passwd,port,menmonico,interface,nome):
    select_ieexam = f"SELECT NIDEXAM,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM FROM ie_exam WHERE CEXAMLISEXAM ='{menmonico}' AND NIDIFACE={interface}" 
    dados_ieexam = db.select_database(host,user,passwd,port,select_ieexam)
    nidexam = dados_ieexam[0]
    select_ievar =f"SELECT CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR from ie_var WHERE NIDEXAM={nidexam}"
    dados_ievar = db.select_database(host,user,passwd,port,select_ievar,"ALL")
    modelo = [dados_ieexam,dados_ievar]
    with open(f'{nome}.exam','wb') as arquivo:
       pickle.dump(modelo,arquivo)

#Função para inserir modelo do exame
def inserir_modelo(host,user,passwd,port,interface_destino,caminho_modelo):
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
# -----------------------------------------------------------------------------FrontEnd--------------------------------------------------------------------------------------------------
def janela_Conectar():
  sg.theme('DarkGrey12')
  layout5= [
  [sg.Text('Conexão com o Banco', size=(30, 1), justification='center', font=("Helvetica", 13),
  relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
  [sg.Text('Host',size=8),sg.Input(key='host',size=(20,1))],
  [sg.Text('Usuario',size=8),sg.Input(key='user',size=(20,1))],
  [sg.Text('Senha  ',size=8),sg.Input(key='senha',size=(20,1),password_char='*')],
  [sg.Text('Porta  ',size=8),sg.Input(key='porta',size=(20,1))],
  [sg.Button('Conectar',size=8,button_color='green')]
  ]
  return sg.Window('Conexão', layout5,finalize=True)

def janela_Prontos():
  sg.theme('DarkGrey12')
  layout5= [
  [sg.Text('Escolha um script', size=(30, 1), justification='center', font=("Helvetica", 13),
  relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
  [sg.Combo(['HEM', 'GAS'],size =(37,1),key='escolhascript')],
  [sg.Text('Id Interface',size=8),sg.Input(key='numeroPlanilha',size =(20,1))],
  [sg.Button('Enviar',size=8,button_color='green'), sg.Button('Voltar',button_color='red') ]
  ]
  return sg.Window('Modelos Prontos', layout5,finalize=True)

def janela_Operacao():
  sg.theme('DarkGrey12')
  layout1= [
  [sg.Text('Escolha uma opção', size=(29, 1), justification='center', font=("Helvetica", 13),
  relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
  [sg.Button('Modelos Prontos',size=(15,1)),
    sg.Button('Inserir Planilha',size=(15,1))],
  [sg.Button('Extrair Config',size=(15,1)),
    sg.Button('Backup',size=(15,1))],
  [sg.Button('Copiar um Exame',size=(15,1)),
    sg.Button('Modelos',size=(15,1))]  
  ]
  return sg.Window('Decisão', layout1,finalize=True)

def janela_inserir():
  sg.theme('DarkGrey12')
  layout2= [
  [sg.Text('Id inter.', size=8),sg.Input(key='numeroPlanilha',size =(20,1))],
  [sg.Button('Enviar',button_color='green'), sg.Button('Voltar',button_color='red') ]
  ]
  return sg.Window('Inserir planilha', layout2,finalize=True)

def janela_extrair():
  sg.theme('DarkGrey12')
  layout6= [
  [sg.Text('Id interface', size=10),sg.Input(key='numeroPlanilha',size =(24,1))],
  [sg.Button('Gerar',button_color='green',size=(15,1)), sg.Button('Voltar',button_color='red',size=(15,1)) ]
  ]
  return sg.Window('Extrair Configurações', layout6,finalize=True)

def janela_backup():
  sg.theme('DarkGrey12')
  layout6= [
  [sg.Text('Adm do Cliente', size=15,font='Helvetica')],
  [sg.Input(key='cliente',size =(25,1))],
  [sg.Button('Gerar Backup',size=(10,1),button_color='green'), sg.Button('Voltar',size=(10,1),button_color='red') ]
  ]
  return sg.Window('Backup', layout6,finalize=True)

def janela_umexame():
  sg.theme('DarkGrey12')
  layout7= [
  [sg.Text('Mnemonico do exame', size=20,font='Helvetica'),sg.Input(key='mnemonico',size =(10,1))],
  [sg.Text('Id da interface original', size=20,font='Helvetica'),sg.Input(key='interfaceoriginal',size =(10,1))],
  [sg.Text('Id da interface destino', size=20,font='Helvetica'),sg.Input(key='interfacedestino',size =(10,1))],
  [sg.Button('Copiar',size=(10,1),button_color='green'), sg.Button('Voltar',size=(10,1),button_color='red') ]
  ]
  return sg.Window('Copiar exame', layout7,finalize=True)

def janela_modelos():
  sg.theme('DarkGrey12')
  layout8= [
  [sg.Text('Menu de Modelos', size=(30, 1), justification='center', font=("Helvetica", 13),
  relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
  [sg.Button('Criar Modelo',size=(15,2)),
    sg.Button('Inserir Modelo',size=(15,2))],
  [sg.Button('Voltar',size=(32,1),button_color='red') ]
  ]
  return sg.Window('Menu Modelos', layout8,finalize=True)

def janela_criarmodelos():
  sg.theme('DarkGrey12')
  layout9= [
  [sg.Text('Mnemonico do exame', size=20,font='Helvetica'),sg.Input(key='mnemonico',size =(10,1))],
  [sg.Text('Id da interface', size=20,font='Helvetica'),sg.Input(key='interface_criar',size =(10,1))],
  [sg.Text('Nome do Modelo', size=20,font='Helvetica'),sg.Input(key='nomemodelo',size =(10,1))],
  [sg.Button('Criar',size=(10,1),button_color='green'), sg.Button('Voltar',size=(10,1),button_color='red') ]
  ]
  return sg.Window('Criar Modelo',layout9,finalize=True)

def janela_inserirmodelos():
  sg.theme('DarkGrey12')
  layout10= [
  [sg.Text('Id da interface', size=15,font='Helvetica'),sg.Input(key='interface_inserir',size =(30,1))],
  [sg.Text('Selecione o Modelo', size=(40, 1), justification='center', font=("Helvetica", 13),
  relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
  [sg.Input(key='caminho_modelo'), sg.FileBrowse()],
  [sg.Button('Enviar',size=(20,1),button_color='green'), sg.Button('Voltar',size=(20,1),button_color='red') ]
  ]
  return sg.Window('Criar Modelo',layout10,finalize=True)

jConexao,jOperacao,jProntos,jInserir,jExtrair,JBackup,Jumexame,Jmodelos,Jcriarmodelos,jInserirmodelos = janela_Conectar(),None,None,None,None,None,None,None,None,None

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
              jOperacao=janela_Operacao()
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
          jProntos=janela_Prontos() 
      if eventos == "Inserir Planilha":
          jOperacao.hide()
          jInserir=janela_inserir()
      if eventos == "Extrair Config":
          jOperacao.hide()
          jExtrair=janela_extrair() 
      if eventos =='Backup':
          jOperacao.hide()
          JBackup=janela_backup()
      if eventos == 'Copiar um Exame':
          jOperacao.hide()
          Jumexame = janela_umexame()
      if eventos == 'Modelos':
          jOperacao.hide()
          Jmodelos = janela_modelos()
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
              print(e)
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
              print(e)
      if eventos == "Enviar" and valores['escolhascript'] == "GAS":
          try:
              insert_gav(host,user,senha,porta,valores['numeroPlanilha'])
              sg.popup("Gravado com sucesso !!!")
          except ERROR as e:
              sg.popup("Erro ao Gravar")
              print(e)
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
          try:
              db.backup(host,user,senha,porta,valores['cliente'])
              sg.popup('Backup Feito com Sucesso !!')
          except ERROR as e:
              sg.popup("Erro ao gerar backup")
              print(e)
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
              print(e)
  if window == Jmodelos:
    if eventos == sg.WIN_CLOSED:
      break
    if eventos == "Voltar":
      Jmodelos.hide()
      jOperacao.un_hide()
    if eventos =="Criar Modelo":
      Jmodelos.hide()
      Jcriarmodelos = janela_criarmodelos()
    if eventos =="Inserir Modelo":
      Jmodelos.hide()
      jInserirmodelos = janela_inserirmodelos()
  if window == Jcriarmodelos:
    if eventos == sg.WIN_CLOSED:
      break
    if eventos == "Voltar":
      Jcriarmodelos.hide()
      Jmodelos.un_hide()
    if eventos == "Criar":
      criar_modelo(host,user,senha,porta,valores['mnemonico'],valores["interface_criar"],valores['nomemodelo'])
      sg.popup("Arquivo criado com Sucesso !!!")
  if window == jInserirmodelos:
    if eventos == sg.WIN_CLOSED:
      break
    if eventos == "Voltar":
      jInserirmodelos.hide()
      Jmodelos.un_hide()
    if eventos == "Enviar":
        inserir_modelo(host,user,senha,porta,valores['interface_inserir'],valores['caminho_modelo'])
        sg.popup("Modelo inserido com Sucesso")    