import mysql.connector
from classes import *
from distutils.log import ERROR
import decimal
import datetime

host ="localhost"
user = "UNIWARE"
passwd = "DBUCFGS"
port = 3309
exame = "URIG"
interface_antiga = 1
interface_nova = 2
ie_exam = c_ie_exam()
ie_var = c_ie_var()

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

def getConection(host,user, senha, porta):
  return mysql.connector.connect(
    host=str(host),
    user=str(user),
    passwd = str(senha),
    port = int(porta),
    database = "equipamento",
    charset = 'utf8'
    )

def insert_planilha(host,user,passwd,port,nidiface,conteudo):
  conn =getConection(host,user,passwd,port)
  conn.autocommit = False
  contador = 1
  try:
    conn.start_transaction()
    cur = conn.cursor()
    for i in conteudo:
      ie_exam.gravar_ieexam(i)
      cur.execute(f"INSERT INTO ie_exam(NIDIFACE,CEXAMLISEXAM,CEXAMEQUIEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM,TINC) VALUES({nidiface},'{ie_exam.cexamlisexam}','{ie_exam.cexamequiexam}','{ie_exam.cdescexam}','{ie_exam.edesmembradoexam}',{contador},{ie_exam.tinc})")
      cur.execute("SELECT MAX(NIDEXAM) FROM ie_exam")
      nidexam = cur.fetchone()
      cur.execute(f"INSERT INTO ie_var(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,TINC) values({nidexam[0]},'Quantitativo','{ie_exam.cexamlisexam}',1,{ie_exam.tinc})")
      conn.commit()
      contador = contador+1 
  except:
    conn.rollback()
  finally:
    cur.close()
    conn.close()
  
def insert_modelpronto(host,user,passwd,port,nidiface,conteudo_ieexam,conteudo_ievar):
  conn =getConection(host,user,passwd,port)
  conn.autocommit = False
  try:
    conn.start_transaction()
    cur = conn.cursor()
    ie_exam.gravar_ieexam(conteudo_ieexam)
    cur.execute(f"INSERT INTO ie_exam (NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM,CDIFFROUNDEXAM,TINC) VALUES({nidiface},'{ie_exam.cexamequiexam}','{ie_exam.cexamlisexam}','{ie_exam.cdescexam}','{ie_exam.edesmembradoexam}',{ie_exam.nindexam},'{ie_exam.cdiffroundexam}',{ie_exam.tinc})")
    cur.execute("SELECT MAX(NIDEXAM) FROM ie_exam")
    nidexam = cur.fetchone()
    for indice in conteudo_ievar:
      ie_var.gravar_ievar(indice)
      cur.execute(f"insert into ie_var(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC) values ({nidexam[0]},'{ie_var.cnomeequivar}','{ie_var.cnomelisvar}',{ie_var.nordemvar},'{ie_var.cfatorvar}',{ie_var.tinc})")
      conn.commit()
  except ERROR as error:
    conn.rollback()
    print(f"erro {error}")
  finally:
    cur.close()
    conn.close()

def select_database(host,user,passwd,port,comando,modo="ONE"):
  conn =getConection(host,user,passwd,port)
  conn.autocommit = False
  cur = conn.cursor()
  if modo == "ONE":
    cur.execute(comando)
    return cur.fetchone()
  else:
    cur.execute(comando)
    return cur.fetchall()
  
def backup(host,user,senha,porta,cliente):
  conn = getConection(host,user,senha,porta)
  cursor = conn.cursor()
  try:
    cursor.execute("SHOW TABLES")
    retorno = cursor.fetchall()
    tables = len(retorno)
    with open(f'{cliente}.ulb','w',encoding="utf-8") as f:
        f.write("/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;\n")
        f.write("/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;\n")
        f.write("/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;\n")
        f.write("/*!40101 SET NAMES utf8 */;\n")
        f.write("/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;\n")
        f.write("/*!40103 SET TIME_ZONE='+00:00' */;\n")
        f.write("/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;")
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
            f.write("/*!40101 SET @saved_cs_client     = @@character_set_client */;\n")
            f.write("/*!40101 SET character_set_client = utf8 */;\n")
            f.write("\n")
            f.write(f"{create2};\n")
            f.write(f"/*!40101 SET character_set_client = @saved_cs_client */;\n")
            if table2 == "ie_amostra" or table2 == "ie_amostra_hist" or table2 =="ie_amostra_resu":
              pass
            else:
              f.write("\n")
              f.write(f"LOCK TABLES `{table2}` WRITE;\n")
              f.write(f"/*!40000 ALTER TABLE `{table2}` DISABLE KEYS */;\n")
              for i in range(len(insert)):
                  formatado = formatacao(list(insert[i]))
                  formatado2 = str(formatado)
                  formatado2 = formatado2.replace("[","(").replace("]",")").replace("'NULL'","NULL")
                  f.write(f"INSERT INTO {table2} VALUES {formatado2};\n")
              f.write(f"/*!40000 ALTER TABLE `{table2}` ENABLE KEYS */;\n")
              f.write("UNLOCK TABLES;\n")
              f.write("\n")
        f.write("/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;\n")
        f.write("/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;\n")
        f.write("/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;\n")
        f.write("/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;\n")
        f.write("/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;\n")
        f.write("/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;\n")
        f.write("/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;\n")
        f.write("/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;\n")
  except ERROR as erro:
    print("Falha: {}".format(erro))
  finally:
    if (conn.is_connected()):
        conn.close()

def inserirum_exame(host,user,passwd,port,exame,interface_antiga,interface_nova):

  exame = str(exame)
  interface_antiga = int(interface_antiga)
  interface_nova = int(interface_nova)
  comando_ieexam = f"SELECT NIDEXAM,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM FROM ie_exam WHERE CEXAMLISEXAM ='{exame}' AND NIDIFACE={interface_antiga}" 
  comando_nindexam = f'SELECT MAX(NINDEXEXAM) FROM ie_exam WHERE NIDIFACE ={interface_nova}'
  comando_nidexam = f"SELECT MAX(NIDEXAM) FROM ie_exam"

  conn = getConection(host,user,passwd,port)
  cur = conn.cursor()
  ie_exam_retorno = list(select_database(host,user,passwd,port,comando_ieexam))
  nindexexam = select_database(host,user,passwd,port,comando_nindexam)
  nindexexam = int(nindexexam[0]+1)
  nidiface =ie_exam_retorno.pop(0)
  comando_ievar = f"SELECT CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR from ie_var WHERE NIDEXAM={nidiface}"
  ie_var_retorno = select_database(host,user,passwd,port,comando_ievar,"ALL")
  ie_exam.gravar_ieexam(ie_exam_retorno)
  try:
    # conn.start_transaction()
    cur.execute(f"INSERT INTO ie_exam(NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM,TINC,NINDEXEXAM) values({interface_nova},'{ie_exam.cexamequiexam}','{ie_exam.cexamlisexam}','{ie_exam.cdescexam}','{ie_exam.edesmembradoexam}','{ie_exam.cparametrosexam}','{ie_exam.cdiffroundexam}',now(),{nindexexam})")
    conn.commit()
    nidexam = select_database(host,user,passwd,port,comando_nidexam)
    for i in ie_var_retorno:
      ie_var.gravar_ievar(i)
      cur.execute(f"INSERT into ie_var(CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR,NIDEXAM,TINC) VALUES('{ie_var.cnomeequivar}','{ie_var.cnomelisvar}','{ie_var.nordemvar}','{ie_var.cfatorvar}','{ie_var.cexamequivar}',{ie_var.nminimovar},{ie_var.ninferiorvar},{ie_var.nsuperiorvar},{ie_var.nmaximovar},'{ie_var.cdecimaisvar}','{nidexam[0]}',now())")      
    conn.commit()
  except ERROR as e:
    conn.rollback()
    print(e)
  finally:
    cur.close()
    conn.close()