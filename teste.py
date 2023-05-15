import mysql.connector
import datetime
import decimal

con = mysql.connector.connect(
    host ="localhost",
    user="root",
    port=3306,
    passwd="1012",
    database="equipamento",
    charset="utf8"
)
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

cur = con.cursor()
def inserirum_exame(exame,interface_antiga,interface_nova):
    cur.execute(f"SELECT NIDEXAM,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM FROM ie_exam WHERE CEXAMLISEXAM ='{exame}' AND NIDIFACE={interface_antiga}" )
    ie_exam =cur.fetchone()
    cur.execute(f'SELECT MAX(NINDEXEXAM) FROM ie_exam WHERE NIDIFACE ={interface_antiga}')
    nindexexam =cur.fetchone()
    nindexexam = int(nindexexam[0]+1)
    nidiface =ie_exam[0]
    cur.execute(f"SELECT CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR from ie_var WHERE NIDEXAM={nidiface}")
    ie_var = cur.fetchall()
    nova_lista = []
    for i in ie_var:
        i_lista = []
        for j in range(len(i)):
            if i[j] is None:
                i_lista.append("NULL")
            else:
                i_lista.append(i[j])
        nova_lista.append(list(i_lista))
    ie = list(ie_exam)
    print(ie)
    cur.execute(f"INSERT INTO ie_exam(NIDIFACE,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM,TINC,NINDEXEXAM) values({interface_nova},'{ie[1]}','{ie[2]}','{ie[3]}','{ie[4]}',{ie[5]},'{ie[6]}',now(),{nindexexam})")
    con.commit()
    cur.execute("SELECT MAX(NIDEXAM) FROM ie_exam ")
    nidexam = cur.fetchone()
    for item in nova_lista:
        insert = str(i)
        insert = insert.replace("'NULL'","NULL").replace("[","(").replace("]",")").replace("(","").replace(")","")
        cur.execute(f"INSERT into ie_var(CNOMEEQUIVAR,CNOMELISVAR,NORDEMVAR,CFATORVAR,CEXAMEQUIVAR,NMINIMOVAR,NINFERIORVAR,NSUPERIORVAR,NMAXIMOVAR,CDECIMAISVAR,NIDEXAM,TINC) VALUES({insert},{nidexam[0]},now())")
        con.commit()