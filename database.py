import mysql.connector
from distutils.log import ERROR

def getConection(user, senha, porta, tBanco):
  return mysql.connector.connect(
    host="localhost",
    user=str(user),
    passwd = str(senha),
    port = str(porta),
    database = "equipamento",
    charset = tBanco)

def insertToDatabase(insert_string, data, valores, tBanco):


  conn = getConection(
    valores['user'],
    valores['senha'],
    valores['porta'],
    tBanco
  )

  cursor = conn.cursor()
  try:
      cursor.executemany(insert_string, data)
      conn.commit()
  except ERROR as erro:
      print("Falha: {}".format(erro))
  finally:
      if (conn.is_connected()):
          conn.close()

def selectToDatabase(select_string, valores, tBanco , quantidade = 'one'):

  conn = getConection(
    valores['user'],
    valores['senha'],
    valores['porta'],
    tBanco
  )
  cursor = conn.cursor()
  try:
      cursor.execute(select_string)
      if quantidade == 'one':
        return cursor.fetchone()
      
      return cursor.fetchall()
  except ERROR as erro:
      print("Falha: {}".format(erro))
  finally:
      if (conn.is_connected()):
          conn.close()

def selectHemcompleto(select_string, valores, tBanco):
  conn = getConection(
    valores['user'],
    valores['senha'],
    valores['porta'],
    tBanco
  )
  cursor = conn.cursor()
  try:
      cursor.execute(select_string)
      return cursor.fetchall()
  except ERROR as erro:
      print("Falha: {}".format(erro))
  finally:
      if (conn.is_connected()):
          conn.close()

def testeConexão(valores,tBanco):
  
  conn = getConection(
    valores['user'],
    valores['senha'],
    valores['porta'],
    tBanco
  )
  
