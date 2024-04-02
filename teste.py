
import mysql.connector

def getConection(host='localhost',user='UNIWARE', senha='DBUCFGS', porta='3309'):
  return mysql.connector.connect(
    host=str(host),
    user=str(user),
    passwd = str(senha),
    port = int(porta),
    database = "equipamento",
    charset = 'utf8'
    )

def execute():
  conn = getConection()
  cursor = conn.cursor()
  nidexansSelect = 'SELECT NIDEXAM,CEXAMEQUIEXAM FROM ie_exam WHERE NIDIFACE="1"'
  cursor.execute(nidexansSelect)
  nidexans = cursor.fetchall()
  print(nidexans)
  for nidexam in nidexans:
    if nidexam[1] != 'Desmembrado':
        nordemvarSelect = F'SELECT MAX(NORDEMVAR) FROM ie_var WHERE NIDEXAM = {nidexam[0]}'
        cursor.execute(nordemvarSelect)
        nordemvar = cursor.fetchone()
        nordemvar1 = int(nordemvar[0]) + 1
        nordemvar2 =nordemvar1 + 1
        nordemvar3 = nordemvar2 + 1
        insert= f"INSERT INTO ie_var(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,TINC) values({nidexam[0]},'OBS','OBS1',{nordemvar1},now()),({nidexam[0]},'OBS2','OBS2',{nordemvar2},now()),({nidexam[0]},'OBS3','OBS3',{nordemvar3},now())"
        try:
            cursor.execute(insert)
            conn.commit()
            print('comitou')
        except Exception as e:
            print(e)
    else:
       print('entrou no else')
       print(nidexam[0])
       desmemSelect = f'SELECT CEXAMEQUIVAR FROM ie_var WHERE NIDEXAM =  {nidexam[0]}'
       cursor.execute(desmemSelect)
       retorno = cursor.fetchall()
       for i in retorno:
           opa = f'SELECT MAX(NORDEMVAR) FROM ie_var WHERE NIDEXAM = {nidexam}'
           cursor.execute(opa)
           opa2 = cursor.fetchone()
           nordemvar1 = int(opa2[0]) + 1
           nordemvar2 =nordemvar1 + 1
           nordemvar3 = nordemvar2 + 1
           nidexamSelect = 'SELECT NIDEXAM FROM ie_var where CEXAMEQUIVAR'
           insert2= f"INSERT INTO ie_var(NIDEXAM,CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,TINC,CEXAMEQUIVAR) values({nidexam[0]},'OBS','OBS1',{nordemvar1},now(),'{i[0]}'),({nidexam[0]},'OBS2','OBS2',{nordemvar2},now(),'{i[0]}'),({nidexam[0]},'OBS3','OBS3',{nordemvar3},now(),'{i[0]}')"
           try:
                cursor.execute(insert2)
                conn.commit()
                print('comitou')
           except Exception as e:
                print(e)
             


execute()