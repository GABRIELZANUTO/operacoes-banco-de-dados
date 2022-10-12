import mysql.connector
from distutils.log import ERROR

#Abrindo conexão com o banco

def getConection():
  return mysql.connector.connect(
    host="",
    user="",
    passwd = "",
    database = ""
  )
#Função para inserir os dados

def insertToDatabase(insert_string, data):
  conn = getConection()
  cursor = conn.cursor()
  try:
      cursor.executemany(insert_string, data)
      conn.commit()

  except ERROR as erro:
      print("Falha: {}".format(erro))

#Fechando conexão com o Banco
  finally:
      if (conn.is_connected()):
          conn.close()
          print("Deu certo")