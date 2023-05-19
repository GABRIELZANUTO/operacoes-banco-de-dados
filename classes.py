import decimal
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
    
#Representação das colunas que precisamos usar da tabela ie_exam
class c_ie_exam:
    def __init__(self,cexamlisexam=None,cexamequiexam=None,cdescexam=None,edesmembradoexam=None,nindexam=None,cparametrosexam=None,cdiffroundexam=None,tinc=None):

        self.cexamlisexam = cexamlisexam
        self.cexamequiexam = cexamequiexam
        self.cdescexam = cdescexam
        self.edesmembradoexam = edesmembradoexam
        self.nindexam = nindexam
        self.tinc = tinc
        self.cparametrosexam = validacao_caracter(cparametrosexam)
        self.cdiffroundexam = validacao_caracter(cdiffroundexam)

    def gravar_ieexam(self,lista):
        validador = len(lista)
        if validador == 3:
            self.cexamlisexam = validacao_caracter(lista[0])
            self.cexamequiexam = validacao_caracter(lista[1])
            self.cdescexam = validacao_caracter(lista[2])
            self.edesmembradoexam = "N"
            self.tinc = "now()"
        elif validador == 6:
            self.cexamequiexam = validacao_caracter(lista[0])
            self.cexamlisexam = validacao_caracter(lista[1])
            self.cdescexam = validacao_caracter(lista[2])
            self.edesmembradoexam = validacao_caracter(lista[3])
            self.nindexam = validacao_numero(lista[4])
            self.cdiffroundexam = validacao_numero(lista[5])
            self.tinc = "now()"
        elif validador == 5:
            self.cexamequiexam = validacao_caracter(lista[0])
            self.cexamlisexam = validacao_caracter(lista[1])
            self.cdescexam = validacao_caracter(lista[2])
            self.edesmembradoexam = validacao_caracter(lista[3])
            self.nindexam = validacao_numero(lista[4])
            self.cdiffroundexam = ""
            self.tinc = "now()"

#Representação das colunas que precisamos usar da tabela ie_var            
class c_ie_var:
    def __init__(self,nidexam=None,cnomeequivar=None,cnomelisvar=None,nordemvar=None,cfatorvar=None,cexamequivar=None,nminimovar=None,ninferiorvar=None,nsuperiorvar=None,nmaximovar=None,cdecimaisvar=None,tinc=None):
        
        self.nidexam = nidexam
        self.cnomeequivar = cnomeequivar
        self.cnomelisvar = cnomelisvar
        self.nordemvar = nordemvar
        self.cfatorvar = cfatorvar
        self.tinc = tinc
        self.cexamequivar = cexamequivar
        self.nminimovar = validacao_numero(nminimovar)
        self.ninferiorvar = validacao_numero(ninferiorvar)
        self.nsuperiorvar = validacao_numero(nsuperiorvar)
        self.nmaximovar = validacao_numero(nmaximovar)
        self.cdecimaisvar = cdecimaisvar
    
    def gravar_ievar(self,lista):
        validador = len(lista)
        if validador == 4:
            self.cnomeequivar = validacao_caracter(lista[0])
            self.cnomelisvar = validacao_caracter(lista[1])
            self.nordemvar = validacao_numero(lista[2])
            self.cfatorvar = validacao_caracter(lista[3])
            self.tinc = "now()"
        elif validador == 10:
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
            self.tinc = "now()"
            
    def __repr__(self):
        return f"{self.nidexam},{self.cnomeequivar},{self.cnomelisvar},{self.nordemvar},{self.cfatorvar},{self.tinc},{self.cexamequivar},{self.nminimovar},{self.ninferiorvar},{self.nsuperiorvar},{self.nmaximovar},{self.cdecimaisvar}"


