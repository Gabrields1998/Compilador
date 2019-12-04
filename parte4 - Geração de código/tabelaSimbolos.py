class TabelaSimbolos:
    def __init__(self):
        self.__tipo = None
        self.__nome = None
        self.__tipoValor = None
        self.__parametros = []
        self.__dimensoes = []
        self.__escopo = None
        self.__declarada = True
        self.__inicializada = False
        self.__utilizada = False

    def setTipo(self, tipo):
        self.__tipo = tipo

    def getTipo(self):
        return self.__tipo

    def setNome(self, nome):
        self.__nome = nome

    def getNome(self):
        return self.__nome
    
    def setTipoValor(self, tipoValor):
        self.__tipoValor = tipoValor

    def getTipoValor(self):
        return self.__tipoValor

    def setParametros(self, parametros):
        self.__parametros = parametros

    def getParametros(self):
        return self.__parametros
    
    def setDimensoes(self, dimensoes):
        self.__dimensoes = dimensoes

    def getDimensoes(self):
        return self.__dimensoes

    def setEscopo(self, escopo):
        self.__escopo = escopo

    def getEscopo(self):
        return self.__escopo

    def setDeclarada(self, declarada):
        self.__declarada = declarada

    def getDeclarada(self):
        return self.__declarada
    
    def setInicializada(self, inicializada):
        self.__inicializada = inicializada
    
    def getInicializada(self):
        return self.__inicializada

    def setUtilizada(self, utilizada):
        self.__utilizada = utilizada
    
    def getUtilizada(self):
        return self.__utilizada
    