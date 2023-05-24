import decimal
import datetime
#Funções de validação de dados, como o pyhton não aceita todos os tipos de dados, temos que tratar se não da erro no Insert depois
def validacao_numero(valor):
    if valor is None:
        valor = "NULL"
    elif isinstance(valor,decimal.Decimal):
        valor = float(valor)        
    else:
        pass
    return valor

def validacao_caracter(valor):
    if valor is None:
        valor = ""
    else:
        pass
    return valor

def validacao_data(valor):
    if isinstance(valor, datetime.datetime):
        valor = valor.strftime("%Y-%m-%d %H:%M:%S")
    else:
        pass
    return valor

#Representação das colunas que precisamos usar da tabela
class c_ie_exam:
    def __init__(self,nidiface=None,nidexam=None,cexamlisexam=None,cexamequiexam=None,cdescexam=None,edesmembradoexam=None,nindexexam=None,cparametrosexam=None,cdiffroundexam=None):
        
        self.nidexam = validacao_numero(nidexam)
        self.nidiface = nidiface
        self.cexamlisexam = cexamlisexam
        self.cexamequiexam = cexamequiexam
        self.cdescexam = cdescexam
        self.edesmembradoexam = edesmembradoexam
        self.nindexexam = nindexexam
        self.tinc = "Now()"
        self.talt = "Now()"
        self.cparametrosexam = cparametrosexam
        self.cdiffroundexam = validacao_caracter(cdiffroundexam)

    def gravar_planilha_ieexam(self,lista,nindexexam,nidiface):
        self.nidiface = validacao_numero(nidiface)
        self.cexamlisexam = validacao_caracter(lista[0])
        self.cexamequiexam = validacao_caracter(lista[1])
        self.cdescexam = validacao_caracter(lista[2])
        self.nindexexam = validacao_numero(nindexexam)
        self.edesmembradoexam = "N"
        self.tinc = "now()"

        return f"({self.nidiface},'{self.cexamlisexam}','{self.cexamequiexam}','{self.cdescexam}','{self.edesmembradoexam}',{self.nindexexam},{self.tinc})"
    
    def gravar_modelopronto(self,lista,nidiface):
        self.nidiface = nidiface
        self.cexamequiexam = validacao_caracter(lista[0])
        self.cexamlisexam = validacao_caracter(lista[1])
        self.cdescexam = validacao_caracter(lista[2])
        self.edesmembradoexam = validacao_caracter(lista[3])
        self.nindexexam = validacao_numero(lista[4])
        if len(lista) == 6 :
            self.cdiffroundexam = validacao_caracter(lista[5])
        else:
            pass

        return f"({self.nidiface},'{self.cexamequiexam}','{self.cexamlisexam}','{self.cdescexam}','{self.edesmembradoexam}',{self.nindexexam},'{self.cdiffroundexam}',{self.tinc})"
     
    def gravar_copia(self,lista,nidiface,nindexexam):
        self.nidexam = lista[0]
        self.nidiface = validacao_numero(nidiface)
        self.cexamequiexam = validacao_caracter(lista[1])
        self.cexamlisexam = validacao_caracter(lista[2])
        self.cdescexam = validacao_caracter(lista[3])
        self.edesmembradoexam = validacao_caracter(lista[4])
        self.nindexexam = validacao_numero(nindexexam)
        self.cparametrosexam = validacao_caracter(lista[5])
        self.cdiffroundexam = validacao_caracter(lista[6])

        return f"({self.nidiface},'{self.cexamequiexam}','{self.cexamlisexam}','{self.cdescexam}',{self.tinc},'{self.edesmembradoexam}',{self.nindexexam},'{self.cparametrosexam}','{self.cdiffroundexam}')"

               
class c_ie_var:
    def __init__(self,nidvar=None,nidexam=None,cnomeequivar=None,cnomelisvar=None,nordemvar=None,cfatorvar=None,cexamequivar=None,nminimovar=None,ninferiorvar=None,nsuperiorvar=None,nmaximovar=None,cdecimaisvar=None,tinc=None,talt=None):
        self.nidvar = nidvar
        self.nidexam = nidexam
        self.cnomeequivar = cnomeequivar
        self.cnomelisvar = cnomelisvar
        self.nordemvar = nordemvar
        self.cfatorvar = cfatorvar
        self.tinc = "Now()"
        self.talt = "Now()"
        self.cexamequivar = cexamequivar
        self.nminimovar = nminimovar
        self.ninferiorvar = ninferiorvar
        self.nsuperiorvar = nsuperiorvar
        self.nmaximovar = nmaximovar
        self.cdecimaisvar = cdecimaisvar
    
    def copiar_exame(self,lista):
        self.cnomeequivar = validacao_caracter(lista[0])
        self.cnomelisvar = validacao_caracter(lista[1])
        self.nordemvar = validacao_numero(lista[2])
        self.cfatorvar = validacao_caracter(lista[3])
        self.cexamequivar = validacao_caracter(lista[4])
        self.nminimovar = validacao_numero(lista[5])
        self.ninferiorvar = validacao_numero(lista[6])
        self.nsuperiorvar = validacao_numero(lista[7])
        self.nmaximovar = validacao_numero(lista[8])
        self.cdecimaisvar = validacao_caracter(lista[9])
        
    def gravar_modelopronto(self,lista,nidexam):
        self.nidexam = nidexam
        self.cnomeequivar= validacao_caracter(lista[0])
        self.cnomelisvar = validacao_caracter(lista[1])
        self.nordemvar = validacao_numero(lista[2])
        self.cfatorvar = validacao_caracter(lista[3])
    

        return f"({self.nidexam},'{self.cnomeequivar}','{self.cnomelisvar}',{self.nordemvar},'{self.cfatorvar}',{self.tinc})"
        
    def gravar_copia(self,lista,nidexam):
        self.nidexam = validacao_numero(nidexam)
        self.cnomeequivar = validacao_caracter(lista[0])
        self.cnomelisvar = validacao_caracter(lista[1])
        self.nordemvar = validacao_numero(lista[2])
        self.cfatorvar = validacao_caracter(lista[3])
        self.cexamequivar = validacao_caracter(lista[4])
        self.nminimovar = validacao_numero(lista[5])
        self.ninferiorvar = validacao_numero(lista[6])
        self.nsuperiorvar = validacao_numero(lista[7])
        self.nmaximovar = validacao_numero(lista[8])
        self.cdecimaisvar = validacao_caracter(lista[9])

        return f"({self.nidexam},'{self.cnomeequivar}','{self.cnomelisvar}',{self.nordemvar},'{self.cfatorvar}',{self.tinc},'{self.cexamequivar}',{self.nminimovar},{self.ninferiorvar},{self.nsuperiorvar},{self.nmaximovar},'{self.cdecimaisvar}')"
        


