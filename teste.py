import mysql.connector

con = mysql.connector.connect(
    host ="localhost",
    user="UNIWARE",
    port=3309,
    passwd="DBUCFGS",
    database="equipamento",
    charset="utf8"
)

cur = con.cursor()
exame ="LDG"
interface ="1"
cur.execute(f"SELECT NIDEXAM,CEXAMEQUIEXAM,CEXAMLISEXAM,CDESCEXAM,EDESMEMBRADOEXAM,CPARAMETROSEXAM,CDIFFROUNDEXAM FROM ie_exam WHERE CEXAMLISEXAM = {exame} AND NIDIFACE= {interface}" )
ie_exam =cur.fetchone()
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
    nova_lista(tuple(i2))
print(type(nova_lista))

    