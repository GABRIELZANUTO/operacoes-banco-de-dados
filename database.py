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
def getConection(host,user, senha, porta, tBanco):
  return mysql.connector.connect(
    host=str(host),
    user=str(user),
    passwd = str(senha),
    port = str(porta),
    database = "equipamento",
    charset = tBanco
    )

#Função de Inserção no banco
def insertToDatabase(insert_string, data,host,user,senha,porta, tBanco):
  conn = getConection(
    host,
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
def selectToDatabase(select_string,host,user,senha,porta, tBanco , quantidade = 'one'):
  conn = getConection(
    host,
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
def selectHemcompleto(select_string,host,user,senha,porta, tBanco):
  conn = getConection(
    host,
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
      valores['host'],
      valores['user'],
      valores['senha'],
      valores['porta'],
      tBanco
    )
#Função de backup imitando o comando mysqldump
def backup(host,user,senha,porta,tBanco,cliente):
    conn = getConection(
    host,
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
      with open(f'{cliente}.ulb','w',encoding="utf-8") as f:
          f.write("/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;\n")
          f.write("/*!40101 SET NAMES utf8 */;\n")
          f.write("/*!50503 SET NAMES utf8mb4 */;\n")
          f.write("/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;\n")
          f.write("/*!40103 SET TIME_ZONE='+00:00' */;\n")
          f.write("/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;\n")
          f.write("/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;\n")
          f.write("/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;\n")
          f.write("\n")
          f.write("\n")
          f.write("USE equipamento;\n")
          for i in range(tables):
              table = str(retorno[i])
              table = table.replace("(", "").replace(")", "").replace("'", "")
              table2 = table.replace(",", "")
              cursor.execute(f"SHOW CREATE TABLE {table2}")
              create= cursor.fetchone()
              if table2 == "ie_amostra" or table2 == "ie_amostra_hist" or table2 =="ie_amostra_resu":
                pass     
              else:    
                cursor.execute(f"SELECT * FROM {table2}")
                insert= cursor.fetchall()
              create2 = create[1]
              f.write(f"DROP TABLE IF EXISTS `{table2}`;\n")
              f.write(f"{create2};\n")
              if table2 == "ie_amostra" or table2 == "ie_amostra_hist" or table2 =="ie_amostra_resu":
                pass
              else:
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

#Função para copiar um exame de uma interface e mandar pra outra
def inserirum_exame(host,user,senha,porta,tBanco,exame,interface_antiga,interface_nova):
  exame = str(exame)
  interface_antiga = int(interface_antiga)
  interface_nova = int(interface_nova)
  conn = getConection(
    host,
    user,
    senha,
    porta,
    tBanco
  )
  cur = conn.cursor()
  cur.execute(f"SELECT NIDEXAM,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM FROM ie_exam WHERE CEXAMLISEXAM ='{exame}' AND NIDIFACE={interface_antiga}" )
  ie_exam =cur.fetchone()
  cur.execute(f'SELECT MAX(NINDEXEXAM) FROM ie_exam WHERE NIDIFACE ={interface_nova}')
  nindexexam =cur.fetchone()
  nindexexam = int(nindexexam[0]+1)
  nidiface =ie_exam[0]
  cur.execute(f"SELECT CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR from ie_var WHERE NIDEXAM={nidiface}")
  ie_var = cur.fetchall()
  #Formatação do retorno da Select do Ie_var, no retorno vem uma lista de tuplas, essa função acessa o valor verifica se é None, se for ele modifica pra Null para fazermos o Insert  posteriormente
  nova_lista = []
  for i in ie_var:
    i_lista = []
    for j in range(len(i)):
      if i[j] is None:
        i_lista.append("NULL")
      elif isinstance(i[j],decimal.Decimal):
            t = float(i[j])
            i_lista.append(t)
      else:
        i_lista.append(i[j])
    nova_lista.append(list(i_lista))
  ie = list(ie_exam)
  ie = formatacao(ie)
  validador_parametro = len(ie[6])
  try:
    if validador_parametro == 4:
      cur.execute(f"INSERT INTO ie_exam(NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM,TINC,NINDEXEXAM) values({interface_nova},'{ie[1]}','{ie[2]}','{ie[3]}','{ie[4]}',{ie[5]},'{ie[6]}',now(),{nindexexam})")
      conn.commit()
    else:
      cur.execute(f"INSERT INTO ie_exam(NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM,TINC,NINDEXEXAM) values({interface_nova},'{ie[1]}','{ie[2]}','{ie[3]}','{ie[4]}','{ie[5]}','{ie[6]}',now(),{nindexexam})")
      conn.commit()     
  except ERROR as error:
     print(error)
  cur.execute("SELECT MAX(NIDEXAM) FROM ie_exam ")
  nidexam = cur.fetchone()
  for item in nova_lista:
    insert = str(item)
    insert = insert.replace("'NULL'","NULL").replace("[","(").replace("]",")").replace("(","").replace(")","")
    try:
      cur.execute(f"INSERT into ie_var(CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR,NIDEXAM,TINC) VALUES({insert},{nidexam[0]},now())")
      conn.commit()
    except ERROR as error:
      print(error)
