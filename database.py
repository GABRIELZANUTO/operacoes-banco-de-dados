import mysql.connector
from distutils.log import ERROR
import decimal
import datetime

#função para formatar possiveis retronos da query que o SQL nos desvolve, como None,Decimal e Datetime
def formatacao(insert):
    insert = insert
    traducao =[]
    for i in range(len(insert)):
        if insert[i] is None:
            insert[i] = "NULL"
    for result in insert:
        if isinstance(result, datetime.datetime):
            result = result.strftime("%Y-%m-%d %H:%M:%S")
            traducao.append(result)
        elif isinstance(result,decimal.Decimal):
            result = float(result)
            traducao.append(result)
        else:
            traducao.append(result)
    return traducao

#Função de conexão com o bacno
def getConection(user, senha, porta, tBanco):
  return mysql.connector.connect(
    host="localhost",
    user=str(user),
    passwd = str(senha),
    port = str(porta),
    database = "equipamento",
    charset = tBanco
    )

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
def testeconexao(valores,tBanco):
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
    cursor = conn.cursor()
    try:
      cursor.execute("SHOW TABLES")
      retorno = cursor.fetchall()
      tables = len(retorno)
      with open(f'Bakcup_{cliente}.sql','w',encoding="utf-8") as f:
          f.write("USE equipamento;\n")
          for i in range(tables):
              table = str(retorno[i])
              table = table.replace("(", "").replace(")", "").replace("'", "")
              table2 = table.replace(",", "")
              cursor.execute(f"SHOW CREATE TABLE {table2}")
              create= cursor.fetchone()
              cursor.execute(f"SELECT * FROM {table2}")
              insert= cursor.fetchall()
              create2 = create[1]
              f.write(f"DROP TABLE IF EXISTS `{table2}`;\n")
              f.write(f"{create2};\n")
              for i in range(len(insert)):
                  formatado = formatacao(list(insert[i]))
                  formatado2 = str(formatado)
                  formatado2 = formatado2.replace("[","(").replace("]",")").replace("'NULL'","NULL")
                  f.write(f"INSERT INTO {table2} VALUES {formatado2};\n")
    except ERROR as erro:
      print("Falha: {}".format(erro))
    finally:
      if (conn.is_connected()):
          conn.close()