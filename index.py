from distutils.log import ERROR
from logging import root
from xmlrpc.server import XMLRPCDocGenerator
import xlrd         
from database import insertToDatabase

#Transformando a tebela do Excel em uma tupla 

def getSheetData(local_file):
  local = ("local da arquivo xlsx")
  listReturn = list()
  sheetData = xlrd.open_workbook(local)
  sheet = sheetData.sheet_by_index(0)
  sheet.cell_value(0,0)

  for i in range(1,38):   #Quantidade incial e final de linhas de tabela 
    listReturn.append(tuple(sheet.row_values(i)))
  
  return listReturn

sheetData = getSheetData("local do arquivo xlsx")

#inserindo dados no banco

insertToDatabase(
  "insert into ie_exam(NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,NINDEXEXAM) values (%s,%s,%s,%s,%s,%s)", #tabelas a serem gravadas
  sheetData
)
