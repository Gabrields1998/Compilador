from llvmlite import ir
from semantica import *

vetTabela = []

module = ir.Module('meu_modulo.bc')

funcNow = {
    "escopo": "global",
    "funcCabecalho": None,
    "entryBlock": None,
    "endBasicBlock": None,
    "builder": None,
    "retorno": None
}

# varVec = {
#     "nome": "",
#     "escopo": "",
#     "conteudo": {}
# }

varVec = []
cd
def is_number(num):
     
    try:
        float(num)
        return True
    except:
        pass
    return False

def getEscopo(node):
    escopo = " "
    pai = node
    breaker = True
    while(breaker):
        pai = pai.parent
        if(pai.name == "programa"):
            escopo = "global"
            breaker = False
        elif(pai.name == "cabecalho"):
            escopo = pai.children[0].name
            breaker = False
    return escopo

def criaVariavel(node):
    variables = []
    if(node.children[1].name == "lista_variaveis"):
        for children in node.children[1].children:
            variables.append(children)
    else:
        variables.append(node.children[1])

    for variable in variables:
        if(node.children[0].name == "inteiro"):
            if(getEscopo(variable) == "global"):
                var = ir.GlobalVariable(module, ir.IntType(32), variable.name)
                var.linkage = "common"
            else:
                var = funcNow["builder"].alloca(ir.IntType(32), name=variable.name)
        else:
            if(getEscopo(variable) == "global"):
                var = ir.GlobalVariable(module, ir.FloatType(), variable.name)
                var.linkage = "common"
            else:
                var = funcNow["builder"].alloca(ir.FloatType(), name=variable.name)
        var.align = 4

        varVec.append({
            "nome": variable.name,
            "escopo": getEscopo(variable),
            "conteudo": var 
        })

def getParametrosFuncao(nome):
    global vetTabela
    tipoParametros = []
    for tupla in vetTabela:
        if(tupla.getNome() == nome):
            for parametros in tupla.getParametros():
                tipoParametros.append(parametros[0])
    return tipoParametros

def criaFuncao(node):
    funcTipo = None
    tipoRet = None
    valRet = None
    tupla = getParametrosFuncao(node.children[0].name)
    parans = []
    for tipo in tupla:
        if(tipo == "inteiro"):
            parans.append(ir.IntType(32))
        else:
            parans.append(ir.FloatType())
    if(node.parent.children[0].name == "inteiro"):
        funcTipo = ir.FunctionType(ir.IntType(32), parans)
        tipoRet = ir.IntType(32)
        valRet = ir.Constant(ir.IntType(32), 0)
    else:
        funcTipo = ir.FunctionType(ir.FloatType(), parans)
        tipoRet = ir.FloatType()
        valRet = ir.Constant(ir.FloatType(), 0.0)

    funcNow["escopo"] = getEscopo(node)
    if(node.children[0].name == "principal"):
        funcNow["funcCabecalho"] = ir.Function(module, funcTipo, name="main")
    else:
        funcNow["funcCabecalho"] = ir.Function(module, funcTipo, name=node.children[0].name)
    funcNow["entryBlock"] = funcNow["funcCabecalho"].append_basic_block('entry')
    funcNow["endBasicBlock"] = funcNow["funcCabecalho"].append_basic_block('exit')
    funcNow["builder"] = ir.IRBuilder(funcNow["entryBlock"])

    funcNow["retorno"] = funcNow["builder"].alloca(tipoRet, name='retorno')
    funcNow["builder"].store(valRet, funcNow["retorno"])

def pegaFilhosDireita(node, filhos):

    if(node.name != ":="):
        filhos.append(node)

    for children in node.children:
        pegaFilhosDireita(children, filhos)
    return filhos

def getVarConteudo(node):
    for var in varVec:
        if((var["nome"] == node.name and var["escopo"] == getEscopo(node)) or (var["nome"] == node.name and var["escopo"] == "global")):
            return var
    return False

def utilizaVariavel(node):
    varRes = getVarConteudo(node.children[0])
    filhos = pegaFilhosDireita(node.children[1], [])

    num1 = None
    num2 = None
    temp = None

    if(filhos[0].name == "+" or filhos[0].name == "-" or filhos[0].name == "*" or filhos[0].name == "/"):
        if(is_number(filhos[1].name)):
            if(filhos[1].name.isdigit()):
                num1 = ir.Constant(ir.IntType(32), int(filhos[1].name))
            else:
                num1 = ir.Constant(ir.FloatType(), float(filhos[1].name))
        else:
            num1 = funcNow["builder"].load(getVarConteudo(filhos[1])["conteudo"], getVarConteudo(filhos[1])["nome"])
        
        if(is_number(filhos[2].name)):
            if(filhos[2].name.isdigit()):
                num2 = ir.Constant(ir.IntType(32), int(filhos[2].name))
            else:
                num2 = ir.Constant(ir.FloatType(), float(filhos[2].name))
        else:
            num2 = funcNow["builder"].load(getVarConteudo(filhos[2])["conteudo"], getVarConteudo(filhos[2])["nome"])

        if(filhos[0].name == "+"):
            temp = funcNow["builder"].add(num1, num2, name='soma')
        elif(filhos[0].name == "-"):
            temp = funcNow["builder"].sub(num1, num2, name='subtracao')
        elif(filhos[0].name == "*"):
            temp = funcNow["builder"].mul(num1, num2, name='multiplicacao')
        elif(filhos[0].name == "/"):
            temp = funcNow["builder"].mul(num1, num2, name='divisao')

        funcNow["builder"].store(temp, varRes["conteudo"])
    elif(is_number(filhos[0].name)):
        if(filhos[0].name.isdigit()):
            num1 = ir.Constant(ir.IntType(32), int(filhos[0].name))
        else:
            num1 = ir.Constant(ir.FloatType(), float(filhos[0].name))
        funcNow["builder"].store(num1, varRes["conteudo"])
    else:
        num1 = funcNow["builder"].load(getVarConteudo(filhos[0])["conteudo"], getVarConteudo(filhos[0])["nome"])
        funcNow["builder"].store(num1, varRes["conteudo"])

def pegaExpressao(node, expressao):
    
    expressao.append(node)

    for children in node.children:
        pegaExpressao(children, expressao)

    return expressao

def populaVariavel(number):
    if(is_number(number.name)):
        if(number.name.isdigit()):
            return ir.Constant(ir.IntType(32), int(number.name))
        else:
            return ir.Constant(ir.FloatType(), float(number.name))
    else:
        return funcNow["builder"].load(getVarConteudo(number)["conteudo"], getVarConteudo(number)["nome"])

def criaBlocoDeDecisao(node):
    # iftrue = funcNow["funcCabecalho"].append_basic_block('iftrue')
    # iffalse = funcNow["funcCabecalho"].append_basic_block('iffalse')
    # ifend = funcNow["funcCabecalho"].append_basic_block('ifend')

    expressao = pegaExpressao(node.children[0], [])
    
    operador = expressao[0].name
    var1 = populaVariavel(expressao[1])
    var2 = populaVariavel(expressao[2])
    
    If = funcNow["builder"].icmp_signed(operador, var1, var2, name='if_test')
    # funcNow["builder"].cbranch(If, iftrue, iffalse)

    # funcNow["builder"].position_at_end(iftrue)
    # funcNow["builder"].branch(ifend)

    # funcNow["builder"].position_at_end(iffalse)
    # funcNow["builder"].branch(ifend)

    # funcNow["builder"].position_at_end(ifend)

def percorreArvore(node):

    if(node.name == ":"):
        criaVariavel(node)

    if(node.name == "cabecalho"):
        criaFuncao(node)

    if(node.name == "se"):
        criaBlocoDeDecisao(node)

    if(node.name == ":="):
        utilizaVariavel(node)

    for children in node.children:
        percorreArvore(children)

def isError(vetError):
    erros = False
    if(len(vetError) != 0):
        for erro in vetError:
            print(erro["tipo"], erro["conteudo"])
            if(erro["tipo"] == "Erro:"):
                erros = True
    return erros

def geraLLVM(arvore):
    percorreArvore(arvore)
    arquivo = open('vars.ll', 'w')
    arquivo.write(str(module))
    arquivo.close()
    print(module)

def genCode():
    global vetTabela

    resultadoSemantica = semantica(sys.argv[1])

    if(not isError(resultadoSemantica[2])):
        vetTabela = resultadoSemantica[0]
        geraLLVM(resultadoSemantica[1])

genCode()