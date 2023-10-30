from PySimpleGUI import PySimpleGUI as sg

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
    sg.Button('Modelos',size=(15,1))],
  [sg.Button('Reenviar Exames',size=(15,1))]    
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
  [sg.Text('Token do Cliente', size=15,font='Helvetica')],
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
  [sg.Button('Criar Modelo Exam',size=(15,1)),
    sg.Button('Inserir Modelo Exam',size=(15,1))],
  [sg.Button('Criar Modelo Face',size=(15,1)),
    sg.Button('Inserir Modelo Face',size=(15,1))],
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
  return sg.Window('Inseir Modelo Exam',layout10,finalize=True)

def janela_criarmodelosface():
  sg.theme('DarkGrey12')
  layout11= [
  [sg.Text('ID da interface', size=20,font='Helvetica'),sg.Input(key='id_face',size =(10,1))],
  [sg.Text('Nome do Modelo', size=20,font='Helvetica'),sg.Input(key='nomemodelo',size =(10,1))],
  [sg.Button('Criar',size=(10,1),button_color='green'), sg.Button('Voltar',size=(10,1),button_color='red') ]
  ]
  return sg.Window('Criar Modelo Face',layout11,finalize=True)

def janela_inserirmodelosface():
  sg.theme('DarkGrey12')
  layout12= [
  [sg.Text('Selecione o Modelo', size=(40, 1), justification='center', font=("Helvetica", 13),
  relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)],
  [sg.Input(key='caminho_modelo'), sg.FileBrowse()],
  [sg.Button('Enviar',size=(20,1),button_color='green'), sg.Button('Voltar',size=(20,1),button_color='red') ]
  ]
  return sg.Window('Inserir Modelo Face',layout12,finalize=True)