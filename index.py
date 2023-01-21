from ast import Break
from email import charset
from logging import shutdown
from sqlite3 import connect
from PySimpleGUI import PySimpleGUI as sg
import xlrd
import mysql.connector
from distutils.log import ERROR
import database as db
from database import teste_conection as testeConexão

#Back-End
#script de Gasometria
def inserir_Gav(valores, tipo_conexao):
    NIDIFACE = (valores['numeroPlanilha'])

    db.insertToDatabase(
      "insert into ie_exam""(NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM,TINC) values ('"+NIDIFACE+"',%s,%s,%s,%s,%s,now())",
      [('GASOV', 'GASV', 'GASOMETRIA VENOSA', 'N', 1)],
      valores,
      tipo_conexao
    )

    result_select = db.selectToDatabase(
      "SELECT NIDEXAM FROM ie_exam WHERE NIDIFACE = '"+NIDIFACE+"' ",
      valores,
      tipo_conexao
    )

    db.insertToDatabase(
      "insert into ie_var""(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC) values ('"+str(result_select[0])+"',%s,%s,%s,%s,now())",
      [('pH', 'PH', 1, None), ('PO2', 'PO2', 2, None), ('PCO2', 'PCO2', 3, None), ('SO2', 'SO2', 4, None), ('cHCO3', 'HCO3', 5, None), ('BE', 'BE', 6, None), ('Na', 'SODIO', 7, None), ('K', 'POTASSIO', 8, None), ('Ca', 'CAIO', 9, None), ('Cl', 'CLORETO', 10, None), ('Glu', 'GLICOSE', 11, None), ('Lac', 'LACT', 12, None)],
      valores,
      tipo_conexao
    )

    return sg.popup('Dados gravados com sucesso !!!!')

#Script de Hemograma
def inserir_hem(valores, tipo_conexao):
    NIDIFACE = (valores['numeroPlanilha'])

    db.insertToDatabase(
      "insert into ie_exam""(NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM,CDIFFROUNDEXAM,TINC) values ('"+NIDIFACE+"',%s,%s,%s,%s,%s,%s,now())",
      [('HEM', 'HEM', 'HEM', 'N', 1, 'SEGMENTADOS|BLASTOS|PROMIELOCITOS|MIELOCITOS|METAMIELOCITOS|BASTONETES|EOSINOFILOS|BASOFILOS|LINFOCITOS|MONOCITOS')],
      valores,
      tipo_conexao
    )

    result_sql = db.selectToDatabase(
      "SELECT NIDEXAM FROM ie_exam WHERE NIDIFACE = '"+NIDIFACE+"' ",
      valores,
      tipo_conexao
    )

    db.insertToDatabase(
      "insert into ie_var""(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC) values ('"+str(result_sql[0])+"',%s,%s,%s,%s,now())",
      [('Hemacias', 'HEMACIA', 1, None), ('Hemoglobinas', 'HEMOGLOBINA', 2, None), ('Hematocritos', 'HEMATOCRITO', 3, None), ('RDW', 'RDW', 4, None), ('Leucocitos', 'LEUCOCITOS', 5, '*1000'), ('Blastos_P', 'BLASTOS', 6, None), ('PMielocitos_P', 'PROMIELOCITOS', 7, None), ('MIELOCITOS_P', 'MIELOCITOS', 8, None), ('MetaMielocitos_P', 'METAMIELOCITOS', 9, None), ('Bastoes_P', 'BASTONETES', 10, None), ('Segmentados_P', 'SEGMENTADOS', 11, None), ('LINFOCITOS_P', 'LINFOCITOS', 12, None), ('Monocitos_P', 'MONOCITOS', 13, None), ('Eosinofilos_P', 'EOSINOFILOS', 14, None), ('Basofilos_P', 'BASOFILOS', 15, None), ('Plaquetas', 'PLAQUETAS', 16, '*1000')],
      valores,
      tipo_conexao
    )

    return sg.popup('Dados Gravados com Sucesso !!!!')

#Função de Select
def Buscar_Dados(valores, tipo_conexao):
  result_sql = db.selectToDatabase(
    "SELECT NIDEXAM,CEXAMLISEXAM FROM ie_exam WHERE NIDIFACE = '"+valores['numeroPlanilha']+"' ",
    valores,
    tipo_conexao,
    'all'
  )
    
  db.insertToDatabase(
    "insert into ie_var""(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,TINC) values (%s,'"+'Quantitativo'+"',%s,'"+'1'+"',now())",
    list(result_sql),
    valores,
    tipo_conexao
  )

  return sg.popup('Dados Gravados com Sucesso !!!!')

#Função para inserir planilha 
def inserir_iexam(lista, conexao, tipo_conexao):
    db.insertToDatabase(
      "insert into ie_exam""(NIDIFACE,CEXAMLISEXAM,CEXAMEQUIEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM,TINC) values ('"+valores['numeroPlanilha']+"',%s,%s,%s,'"+str('N')+"',%s,now())",
      lista,
      conexao,
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
 
def janela_inserirPlanilha():
    sg.theme('DarkGrey12')
    layout5= [
    [sg.Text('Escolha um script', size=(30, 1), justification='center', font=("Helvetica", 13),
    relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
    [sg.Combo(['HEM', 'GAS'],size =(37,1),key='escolhascript')],
    [sg.Text('Id Interface',size=8),sg.Input(key='numeroPlanilha',size =(20,1))],
    [sg.Button('Enviar',size=8), sg.Button('Voltar') ]
    ]
    return sg.Window('Inserir Prontos', layout5,finalize=True)

def janela_inicial():
    sg.theme('DarkGrey12')
    layout6 = [
    [sg.Text('Conexão com o Banco', size=(30, 1), justification='center', font=("Helvetica", 13),
    relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
    [sg.Text('Usuario',size=8),sg.Input(key='user',size=(20,1))],
    [sg.Text('Senha  ',size=8),sg.Input(key='senha',size=(20,1),password_char='*')],
    [sg.Text('Porta  ',size=8),sg.Input(key='porta',size=(20,1))],
    [sg.Radio('MySQL50X32',"tipobanco", default=False,key='mysql'), sg.Radio('MariaDB',"tipobanco", default=False,key='mariadb')],
    [sg.Button('Continuar')]
    ]
    return sg.Window('Inicial', layout6,finalize=True)

def janela_2():
    sg.theme('DarkGrey12')
    layout1= [
    [sg.Text('Bem vindo', size=(30, 1), justification='center', font=("Helvetica", 13),
    relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
    [sg.Radio('Modelos Prontos','opcaoincial',default=False,key='mProntos'), sg.Radio('Inserir Planilha','opcaoincial',default=False,key='inserirP')],
    [sg.Button('Continuar')]
    ]
    return sg.Window('Janela Incial', layout1,finalize=True)

def janela_inserir():
    sg.theme('DarkGrey12')
    layout2= [
    [sg.Text('Digite as informações do banco', size=(30, 1), justification='center', font=("Helvetica", 13),)],
    [sg.Radio('MySQL50X32','tipobanco',default=False,key='mysql'), sg.Radio('MariaDB','tipobanco',default=False,key='mariadb')],
    [sg.Text('Linhas ', size=8),sg.Input(key='qtLinhas',size=(20,1)),],
    [sg.Text('Id inter.', size=8),sg.Input(key='numeroPlanilha',size =(20,1))],
    [sg.Button('Enviar'), sg.Button('Voltar') ]
    ]
    return sg.Window('Inserir planilha', layout2,finalize=True)

janela1,janela2,janela3,janela4,janela5 = janela_inicial(),None,None,None,None
while True:
    window,eventos,valores = sg.read_all_windows()

    if window == janela1:
      if eventos == sg.WIN_CLOSED:
        break
      if eventos == 'Continuar':
        testeConexão(valores['user'],valores['senha'],valores['porta'])
        janela2 = janela_2()
        janela1.hide()

    if window == janela2:
      if eventos == sg.WIN_CLOSED:
        break
      if eventos == 'Voltar':
        janela2.hide()
        janela1.un_hide()
      if  window == janela2 and  eventos == 'mProntos':
        janela3 == janela_inserir()
        janela2.hide()
        
        if valores['mysql'] == True:
          inserir_iexam(Ler_Planilha(), valores, 'mysql')
          Buscar_Dados(valores, 'mysql')
        if valores['mariadb'] == True:
          inserir_iexam(Ler_Planilha(), valores, 'mariadb')
          Buscar_Dados(valores, 'mariadb')
    if window == janela3:
      if eventos == sg.WIN_CLOSED:
        break
      if eventos == 'Voltar':
        janela3.hide()
        janela1.un_hide()
      
      if eventos == 'Enviar':
        if valores['escolhascript'] == 'HEM':
          if valores['mysql'] == True:
            inserir_hem(valores, 'mysql')
          elif valores['mariadb'] == True:
            inserir_hem(valores, 'mariadb')

        if valores['escolhascript'] == 'GAS':
          if valores['mysql'] == True:
            inserir_Gav(valores, 'mysql')
          elif valores['mariadb'] == True:
            inserir_Gav(valores, 'mariadb')