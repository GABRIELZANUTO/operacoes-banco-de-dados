import mysql.connector
from classes import *
import os
from distutils.log import ERROR
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload
import decimal
import datetime

CRE = {
}
ie_exam = c_ie_exam()
ie_var = c_ie_var()
comando_nidexam = "SELECT MAX(NIDEXAM) FROM ie_exam"

def upload_file_to_folder(file_path):
    folder_id = '19ix3eNhsyC4sKq4zy7G3gp4LUqSF-Lrk'
    credentials = Credentials.from_service_account_info(
        CRE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    drive_service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }

    media = MediaFileUpload(file_path, resumable=True)

    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

def get_file_id_by_initials(file_initials):
    credentials = Credentials.from_service_account_info(
        CRE,
        scopes=['https://www.googleapis.com/auth/drive'])
    drive_service = build('drive', 'v3', credentials=credentials)
    query = f"name contains '{file_initials}' and '19ix3eNhsyC4sKq4zy7G3gp4LUqSF-Lrk' in parents"
    fields = 'files(id, name)'
    results = drive_service.files().list(q=query, fields=fields).execute()
    files = results.get('files', [])
    if len(files) >0 and len(files) < 5:
      return files
    else:
      return False
    
def exclui_drive(arquivo_id):
  pasta_id = "19ix3eNhsyC4sKq4zy7G3gp4LUqSF-Lrk"
   # Caminho para o arquivo de credenciais baixado anteriormente
  credenciais_path = Credentials.from_service_account_info(
  CRE,
  scopes=['https://www.googleapis.com/auth/drive']
    )
  service = build('drive', 'v3', credentials=credenciais_path)
  service.files().update(fileId=arquivo_id, removeParents=pasta_id).execute()

#Função para formatar os dados que vem na Select na função de Bakcup
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
#Função de conexão do banco
def getConection(host,user, senha, porta):
  return mysql.connector.connect(
    host=str(host),
    user=str(user),
    passwd = str(senha),
    port = int(porta),
    database = "equipamento",
    charset = 'utf8'
    )
#Função de select para otimizar as querys
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
#Função usada para todos os inserts
def insert(host,user,passwd,port,comando):
  conn = getConection(host,user,passwd,port)
  conn.autocommit = False
  try:
     cur = conn.cursor()
     cur.execute(comando)
     conn.commit()
  except ERROR as e:
     conn.rollback()
     print(e)
  finally:
    cur.close()
    conn.close() 
#Função Backend para inserir os dados da planilha no banco ie_exam e ie_var
def insert_planilha(host,user,passwd,port,nidiface,conteudo): 
  comando_nindexexam = f"SELECT MAX(NINDEXEXAM) FROM ie_exam WHERE NIDIFACE={nidiface}"
  nindexexam = select_database(host,user,passwd,port,comando_nindexexam)
  if nindexexam[0] is None:
    nindexexam = 1
  else:
    nindexexam = nindexexam[0]+1
  for i in conteudo:
    dados_ieexam =ie_exam.gravar_planilha_ieexam(i,nindexexam,nidiface)
    comando_ieexam = "INSERT INTO ie_exam(NIDIFACE,CEXAMLISEXAM,CEXAMEQUIEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM,TINC) VALUES "+dados_ieexam
    insert(host,user,passwd,port,comando_ieexam)
    nidexam = select_database(host,user,passwd,port,comando_nidexam)
    comando_ieevar = f"INSERT INTO ie_var(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,TINC) values({nidexam[0]},'Quantitativo','{ie_exam.cexamlisexam}',1,{ie_exam.tinc})"
    insert(host,user,passwd,port,comando_ieevar)
    nindexexam=nindexexam+1
#Função de inserir scripts prontos que estão no código, como HEM e GASOV
def insert_modelpronto(host,user,passwd,port,nidiface,conteudo_ieexam,conteudo_ievar):
  comando_nidexexam = f"SELECT MAX(NINDEXEXAM) FROM ie_exam WHERE NIDIFACE ={nidiface}"
  nindexexam = select_database(host,user,passwd,port,comando_nidexexam)
  if nindexexam[0] is None:
     nindexexam = 1
  else:
     nindexexam = nindexexam[0]+1
  dados = ie_exam.gravar_modelopronto(conteudo_ieexam,nidiface,nindexexam)
  comando_ieexam = "INSERT INTO ie_exam (NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM,CDIFFROUNDEXAM,TINC) VALUES"+dados
  insert(host,user,passwd,port,comando_ieexam)
  nidexam = select_database(host,user,passwd,port,comando_nidexam)
  for indice in conteudo_ievar:
    dados = ie_var.gravar_modelopronto(indice,nidexam[0])
    comando_ievar = "insert into ie_var(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC) values"+dados
    insert(host,user,passwd,port,comando_ievar)
#Função para montar o arquivo .ulb de backup
def backup(host,user,senha,porta,cliente):
  conn = getConection(host,user,senha,porta)
  cursor = conn.cursor()
  data_atual = datetime.datetime.now().strftime("%Y%m%d")
  cliente = str(cliente)
  nome_arquivo = cliente+"_"+data_atual
  try:
    cursor.execute("SHOW TABLES")
    retorno = cursor.fetchall()
    tables = len(retorno)
    with open(f'{nome_arquivo}.ulb','w',encoding="utf-8") as f:
        name = f'{nome_arquivo}.ulb'
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
    return name,cliente
  except ERROR as erro:
    print("Falha: {}".format(erro))
  finally:
    if (conn.is_connected()):
        conn.close()
#Função para copiar um exame de uma interface para outra
def inserirum_exame(host,user,passwd,port,exame,interface_antiga,interface_nova):
  #Comandos SQL
  select_ieexam = f"SELECT NIDEXAM,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM FROM ie_exam WHERE CEXAMLISEXAM ='{exame}' AND NIDIFACE={interface_antiga}" 
  select_nindexexam = f'SELECT MAX(NINDEXEXAM) FROM ie_exam WHERE NIDIFACE ={interface_nova}'
  #Chamadas das Selects
  retorno_ieexam = select_database(host,user,passwd,port,select_ieexam)
  retorno_nindexexam =select_database(host,user,passwd,port,select_nindexexam)
  nindexexam = retorno_nindexexam[0] + 1
  dados_iexam = ie_exam.gravar_copia(retorno_ieexam,interface_nova,nindexexam)
  #comando para reconhecer dados do IE_var de acordo com o exame
  select_ievar = f"SELECT CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR from ie_var WHERE NIDEXAM={ie_exam.nidexam}"
  retorno_ievar = select_database(host,user,passwd,port,select_ievar,"ALL")
  #Comando insert do ie_Exam
  insert_iexam = f"INSERT INTO ie_exam(NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,TINC,EDESMEMBRADOEXAM,NINDEXEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM) values " + dados_iexam
  insert(host,user,passwd,port,insert_iexam)
  retorno_nidexam = select_database(host,user,passwd,port,comando_nidexam)
  ie_exam.nidexam = retorno_nidexam[0]
  for i in retorno_ievar:
    dados_ievar = ie_var.gravar_copia(i,ie_exam.nidexam)
    #Comando insert do ie_var
    insert_ievar = f"INSERT INTO ie_var(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,TINC,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR) values " + dados_ievar
    insert(host,user,passwd,port,insert_ievar)

