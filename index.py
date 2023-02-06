from ast import Break
from email import charset
from logging import shutdown
from sqlite3 import connect
from PySimpleGUI import PySimpleGUI as sg
import xlrd
import mysql.connector
from distutils.log import ERROR
import database as db

#Back-End

#Usario

U=''
p=''
#script de Gasometria
def inserir_Gav(valores,user,senha,porta,tipo_conexao):
    NIDIFACE = (valores['numeroPlanilha'])

    db.insertToDatabase(
      "insert into ie_exam""(NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM,TINC) values ('"+NIDIFACE+"',%s,%s,%s,%s,%s,now())",
      [('GASOV', 'GASV', 'GASOMETRIA VENOSA', 'N', 1)],
      user,
      senha,
      porta,
      tipo_conexao
    )

    result_select = db.selectToDatabase(
      "SELECT NIDEXAM FROM ie_exam WHERE NIDIFACE = '"+NIDIFACE+"' ",
      user,
      senha,
      porta,
      tipo_conexao
    )

    db.insertToDatabase(
      "insert into ie_var""(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC) values ('"+str(result_select[0])+"',%s,%s,%s,%s,now())",
      [('pH', 'PH', 1, None), ('PO2', 'PO2', 2, None), ('PCO2', 'PCO2', 3, None), ('SO2', 'SO2', 4, None), ('cHCO3', 'HCO3', 5, None), ('BE', 'BE', 6, None), ('Na', 'SODIO', 7, None), ('K', 'POTASSIO', 8, None), ('Ca', 'CAIO', 9, None), ('Cl', 'CLORETO', 10, None), ('Glu', 'GLICOSE', 11, None), ('Lac', 'LACT', 12, None)],
      user,
      senha,
      porta,
      tipo_conexao
    )
    return sg.popup('Dados gravados com sucesso !!!!')

#Script de Hemograma
def inserir_hem(valores,user,senha,porta, tipo_conexao):
    NIDIFACE = (valores['numeroPlanilha'])

    db.insertToDatabase(
      "insert into ie_exam (NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM,CDIFFROUNDEXAM,TINC) values ('"+NIDIFACE+"',%s,%s,%s,%s,%s,%s,now())",
      [('HEM', 'HEM', 'HEM', 'N', 1, 'SEGMENTADOS|BLASTOS|PROMIELOCITOS|MIELOCITOS|METAMIELOCITOS|BASTONETES|EOSINOFILOS|BASOFILOS|LINFOCITOS|MONOCITOS')],
      user,
      senha,
      porta,
      tipo_conexao
    )

    result_sql = db.selectToDatabase(
      "SELECT NIDEXAM FROM ie_exam WHERE NIDIFACE = '"+NIDIFACE+"' ",
      user,
      senha,
      porta,
      tipo_conexao
    )

    db.insertToDatabase(
      "insert into ie_var""(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC) values ('"+str(result_sql[0])+"',%s,%s,%s,%s,now())",
      [('Hemacias', 'HEMACIA', 1, None), ('Hemoglobinas', 'HEMOGLOBINA', 2, None), ('Hematocritos', 'HEMATOCRITO', 3, None), ('RDW', 'RDW', 4, None), ('Leucocitos', 'LEUCOCITOS', 5, '*1000'), ('Blastos_P', 'BLASTOS', 6, None), ('PMielocitos_P', 'PROMIELOCITOS', 7, None), ('MIELOCITOS_P', 'MIELOCITOS', 8, None), ('MetaMielocitos_P', 'METAMIELOCITOS', 9, None), ('Bastoes_P', 'BASTONETES', 10, None), ('Segmentados_P', 'SEGMENTADOS', 11, None), ('LINFOCITOS_P', 'LINFOCITOS', 12, None), ('Monocitos_P', 'MONOCITOS', 13, None), ('Eosinofilos_P', 'EOSINOFILOS', 14, None), ('Basofilos_P', 'BASOFILOS', 15, None), ('Plaquetas', 'PLAQUETAS', 16, '*1000')],
      user,
      senha,
      porta,
      tipo_conexao
    )

    return sg.popup('Dados Gravados com Sucesso !!!!')

def inserir_hemCompleto(valores,user,senha,porta,tipo_conexao):
    NIDIFACE = (valores['numeroPlanilha'])

    db.insertToDatabase(
      "insert into ie_exam"" (NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM,TINC) values ('"+NIDIFACE+"',%s,%s,%s,%s,%s,now())",
     [( 'HEM', 'HEM', 'HEM', 'N', 1), ('HEM', 'PLA', 'PLAQUETAS', 'N', 2), ( 'HEM', 'HMG', 'HEMOGLOBINA', 'N', 3), ( 'HEM', 'HMT', 'HEMATOCRITO', 'N', 4), ( 'HEM', 'ERI', 'ERITROGRAMA', 'N', 5), ( 'HEM', 'LEU', 'LEUCOGRAMA', 'N', 6)],
      user,
      senha,
      porta,
      tipo_conexao
    )
    result_sql = db.selectHemcompleto(
      "SELECT NIDEXAM FROM ie_exam WHERE NIDIFACE = '"+NIDIFACE+"' ",
      user,
      senha,
      porta,
      tipo_conexao
    )
    

    db.insertToDatabase(
      "insert into ie_var""(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC) values('"+str(result_sql[0][0])+"',%s,%s,%s,%s,now())",
     [( 'Hemacias', 'HEMACIA', 1, None), ( 'Hemoglobinas', 'HEMOGLOBINA', 2, None), ( 'Hematocritos', 'HEMATOCRITO', 3, None), ('RDW', 'RDW', 4, None), ( 'Leucocitos', 'LEUCOCITOS', 5, '*1000'), ( 'Blastos_P', 'BLASTOS', 6, None), ( 'PMielocitos_P', 'PROMIELOCITOS', 7, None), ( 'MIELOCITOS_P', 'MIELOCITOS', 8, None), ( 'MetaMielocitos_P', 'METAMIELOCITOS', 9, None), ( 'Bastoes_P', 'BASTONETES', 10, None), ( 'Segmentados_P', 'SEGMENTADOS', 11, None), ( 'LINFOCITOS_P', 'LINFOCITOS', 12, None), ('Monocitos_P', 'MONOCITOS', 13, None), ('Eosinofilos_P', 'EOSINOFILOS', 14, None), ( 'Basofilos_P', 'BASOFILOS', 15, None), ( 'Plaquetas', 'PLAQUETAS', 16, '*1000')],
      user,
      senha,
      porta,
      tipo_conexao
    )
    db.insertToDatabase(
      "insert into ie_var""(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC) values('"+str(result_sql[1][0])+"',%s,%s,%s,%s,now())",
     [( 'Plaquetas', 'PLAQUETAS', 1, '*1000')],
      user,
      senha,
      porta,
      tipo_conexao
    )
    db.insertToDatabase(
      "insert into ie_var""(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC) values('"+str(result_sql[2][0])+"',%s,%s,%s,%s,now())",
     [( 'Hemoglobinas', 'HEMOGLOBINA', 1, None)],
      user,
      senha,
      porta,
      tipo_conexao
    )
    db.insertToDatabase(
      "insert into ie_var""(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC) values('"+str(result_sql[3][0])+"',%s,%s,%s,%s,now())",
     [( 'Hematocritos', 'HEMATOCRITO', 1, None)],
      user,
      senha,
      porta,
      tipo_conexao
    )
    db.insertToDatabase(
      "insert into ie_var""(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC) values('"+str(result_sql[4][0])+"',%s,%s,%s,%s,now())",
     [( 'Hemacias', 'HEMACIAS', 1, None), ( 'Hemoglobinas', 'HEMOGLOBINA', 2, None), ( 'Hematocritos', 'HEMATOCRITO', 3, None), ( 'RDW', 'RDW', 4, None)],
      user,
      senha,
      porta,
      tipo_conexao
    )
    db.insertToDatabase(
      "insert into ie_var""(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC) values('"+str(result_sql[5][0])+"',%s,%s,%s,%s,now())",
     [( 'Leucocitos', 'LEUCOCITOS', 1, '*1000'), ( 'Blastos_P', 'BLASTOS', 2, None), ( 'PMielocitos_P', 'PROMIELOCITOS', 3, None), ( 'MIELOCITOS_P', 'MIELOCITOS', 4, None), ( 'MetaMielocitos_P', 'METAMIELOCITOS', 5, None), ( 'Segmentados_P', 'NEUTROFILOS', 6, None), ( 'Eosinofilos_P', 'EOSINOFILOS', 7, None), ( 'Segmentados', 'SEGMENTADOS', 8, None), ( 'Bastoes_P', 'BASTONETES', 9, None), ( 'Basofilos_P', 'BASOFILOS', 10, None), ( 'LINFOCITOS_P', 'LINFOCITOS', 11, None), ( 'LinfocitosA_P', 'LINFOCITOSATIPICOS', 12, None), ( 'Monocitos_P', 'MONOCITOS', 13, None)],
      user,
      senha,
      porta,
      tipo_conexao
    )

    return sg.popup('Dados Gravados com Sucesso !!!!')
#Função de Select
def Buscar_Dados(user,senha,porta, tipo_conexao):
  result_sql = db.selectToDatabase(
    "SELECT NIDEXAM,CEXAMLISEXAM FROM ie_exam WHERE NIDIFACE = '"+valores['numeroPlanilha']+"' ",
    user,
    senha,
    porta,
    tipo_conexao,
    'all'
  )
    
  db.insertToDatabase(
    "insert into ie_var""(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,TINC) values (%s,'"+'Quantitativo'+"',%s,'"+'1'+"',now())",
    list(result_sql),
    user,
    senha,
    porta,
    tipo_conexao
  )

  return sg.popup('Dados Gravados com Sucesso !!!!')

#Função para inserir planilha 
def inserir_iexam(lista, user,senha,porta, tipo_conexao):
    db.insertToDatabase(
      "insert into ie_exam""(NIDIFACE,CEXAMLISEXAM,CEXAMEQUIEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM,TINC) values ('"+valores['numeroPlanilha']+"',%s,%s,%s,'"+str('N')+"',%s,now())",
      lista,
      user,
      senha,
      porta,
      tipo_conexao
    )

#Função para Ler planilha
def Ler_Planilha():
    loc= ("Exames.xlsx")
    lista= list()
    cursor = xlrd.open_workbook(loc)
    folha =cursor.sheet_by_index(0)
    folha.cell_value(0,0)
    for i in range(1,int(valores['qtLinhas'])):
        lista.append(tuple(folha.row_values(i)))
    return lista

#Fronte End

def janela_Login():
  sg.theme('DarkGrey12')
  layout1= [
      [sg.Text('         Bem Vindo !', size=(20, 1), justification='center', font=("Helvetica", 15))],
      [sg.Text('Usuario',size=(6, 1),font=("Arial", 12)),sg.Input(key='login',size=(20, 1))],
      [sg.Text('Senha',size=(6, 1),font=("Arial", 12)),sg.Input(key='senhal',password_char='*',size=(20, 1))],
      [sg.Button("Login",size=(30,1))]
    ]
  return sg.Window('Login', layout1,finalize=True)

def janela_Conectar():
    sg.theme('DarkGrey12')
    layout5= [
    [sg.Text('Conexão com o Banco', size=(30, 1), justification='center', font=("Helvetica", 13),
    relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
    [sg.Text('Usuario',size=8),sg.Input(key='user',size=(20,1))],
    [sg.Text('Senha  ',size=8),sg.Input(key='senha',size=(20,1),password_char='*')],
    [sg.Text('Porta  ',size=8),sg.Input(key='porta',size=(20,1))],
    [sg.Radio('MySQL50X32',"tipobanco", default=False,key='mysql'), sg.Radio('MariaDB',"tipobanco", default=False,key='mariadb')],
    [sg.Button('Conectar',size=8) ]
    ]
    return sg.Window('Conexão', layout5,finalize=True)


def janela_Prontos():
    sg.theme('DarkGrey12')
    layout5= [
    [sg.Text('Escolha um script', size=(30, 1), justification='center', font=("Helvetica", 13),
    relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
    [sg.Combo(['HEM', 'GAS','HEMCOMPLETO'],size =(37,1),key='escolhascript')],
    [sg.Text('Id Interface',size=8),sg.Input(key='numeroPlanilha',size =(20,1))],
    [sg.Button('Enviar',size=8), sg.Button('Voltar') ]
    ]
    return sg.Window('Modelos Prontos', layout5,finalize=True)

def janela_Operacao():
    sg.theme('DarkGrey12')
    layout1= [
    [sg.Text('Escolha uma opção', size=(30, 1), justification='center', font=("Helvetica", 13),
    relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
    [sg.Radio('Modelos Prontos','opcaoincial',default=False,key='mProntos'), sg.Radio('Inserir Planilha','opcaoincial',default=False,key='inserirP')],
    [sg.Button('Continuar')]
    ]
    return sg.Window('Decisão', layout1,finalize=True)

def janela_inserir():
    sg.theme('DarkGrey12')
    layout2= [
    [sg.Text('Linhas ', size=8),sg.Input(key='qtLinhas',size=(20,1)),],
    [sg.Text('Id inter.', size=8),sg.Input(key='numeroPlanilha',size =(20,1))],
    [sg.Button('Enviar'), sg.Button('Voltar') ]
    ]
    return sg.Window('Inserir planilha', layout2,finalize=True)

jLogin,jConexao,jOperacao,jProntos,jInserir = janela_Login(),None,None,None,None
while True:
    window,eventos,valores = sg.read_all_windows()
    if window == jLogin:
          if eventos == sg.WIN_CLOSED:
            break
          if eventos == 'Login':
            if valores['senhal'] == p and valores['login'] == U:
              jLogin.hide()
              jConexao = janela_Conectar()
            else:
              sg.popup('Usuario Incorreto')
              window.FindElement('login').Update('')
              window.FindElement('senhal').Update('')
    if window == jConexao:
      if eventos == sg.WIN_CLOSED:
            break
      if eventos == 'Conectar':
          try:
            if valores['mysql'] == True:
              tBanco = "utf8"
            if valores['mariadb'] == True:
              tBanco = "utf8mb4"
            db.testeConexão(valores,tBanco)
            user = valores['user']
            senha = valores['senha']
            porta = valores['porta']
            jConexao.hide()
            jOperacao=janela_Operacao()
          except:
            sg.popup('Dados Invalidos')
            window.FindElement('user').Update('')
            window.FindElement('senha').Update('')
            window.FindElement('porta').Update('')
    if window == jOperacao:
      if eventos == sg.WIN_CLOSED:
        break
      if eventos == "Continuar" and valores['mProntos'] == True:
        jOperacao.hide()
        jProntos=janela_Prontos() 
      if eventos == "Continuar" and valores['inserirP'] == True:
        jOperacao.hide()
        jInserir=janela_inserir()
        print(user)
    if window == jInserir:
      if eventos == sg.WIN_CLOSED:
        break
      if eventos == 'Voltar':
        jOperacao.un_hide()
        jInserir.hide()
      if eventos == 'Enviar':
        inserir_iexam(Ler_Planilha(),user,senha,porta,tBanco)
        Buscar_Dados(user,senha,porta, tBanco)
    if window == jProntos:
      if eventos == sg.WIN_CLOSED:
        break
      if eventos == "Voltar":
        jOperacao.un_hide()
        jProntos.hide()
      if eventos == "Enviar" and valores['escolhascript'] == "HEM":
        inserir_hem(valores,user,senha,porta,tBanco)
      if eventos == "Enviar" and valores['escolhascript'] == "GAS":
        inserir_Gav(valores,user,senha,porta,tBanco)
      if eventos == "Enviar" and valores['escolhascript'] == "HEMCOMPLETO":
        inserir_hemCompleto(valores,user,senha,porta,tBanco)