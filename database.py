import mysql.connector
from distutils.log import ERROR

def getConection(user, senha, porta, charset='utf8'):
  return mysql.connector.connect(
    host="localhost",
    user=str(user),
    passwd = str(senha),
    port = str(porta),
    database = "equipamento",
    charset = charset)

def insertToDatabase(insert_string, data, valores, tipo_conexao = 'mysql'):
  charset = 'utf8'
  if tipo_conexao != 'mysql':
    charset = 'utf8mb4'

  conn = getConection(
    valores['user'],
    valores['senha'],
    valores['porta'],
    charset
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

def selectToDatabase(select_string, valores, tipo_conexao = 'mysql', quantidade = 'one'):
  charset = 'utf8'
  if tipo_conexao != 'mysql':
    charset = 'utf8mb4'

  conn = getConection(
    valores['user'],
    valores['senha'],
    valores['porta'],
    charset
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
