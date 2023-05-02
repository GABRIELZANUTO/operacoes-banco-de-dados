import mysql.connector
from distutils.log import ERROR
import subprocess

#Função de conexão com o bacno
def getConection(user, senha, porta, tBanco):
  return mysql.connector.connect(
    host="localhost",
    user=str(user),
    passwd = str(senha),
    port = str(porta),
    database = "equipamento",
    charset = tBanco)

#Função de Inserção no banco
def insertToDatabase(insert_string, data, user,senha,porta, tBanco):
  conn = getConection(
    user,
    senha,
    porta,
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

#Função adaptavel de SELECT no banco
def selectToDatabase(select_string,user,senha,porta, tBanco , quantidade = 'one'):
  conn = getConection(
    user,
    senha,
    porta,
    tBanco
  )
  cursor = conn.cursor()
  try:
      cursor.execute(select_string)
      if quantidade == 'one':
        return cursor.fetchone()
      else:
        return cursor.fetchall()
  except ERROR as erro:
      print("Falha: {}".format(erro))
  finally:
      if (conn.is_connected()):
          conn.close()

#Função específica para SELECT quando usam a opção HEMCOMPLETO dos scripts prontos
def selectHemcompleto(select_string, user,senha,porta, tBanco):
  conn = getConection(
    user,
    senha,
    porta,
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

#teste de conexão para login no banco
def testeConexão(valores,tBanco):
    conn = getConection(
      valores['user'],
      valores['senha'],
      valores['porta'],
      tBanco
    )
  
def backup(user,senha,porta,tBanco,cliente):
  conn = getConection(
    user,
    senha,
    porta,
    tBanco
  )
  filename=f"{cliente}_ConfigIncial.sql"
  with open(filename, "w") as backup_file:
    subprocess.Popen(f"mysqldump -u{conn.user} -p{conn._password} -P{conn._port} {conn.database}", stdout=backup_file, shell=True).wait()
  conn.close()
  
