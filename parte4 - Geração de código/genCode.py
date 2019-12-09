from llvmlite import ir
from llvmlite import binding as llvm
from semantica import *

llvm.initialize()
llvm.initialize_all_targets()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

module = ir.Module('meu_modulo.bc')

module.triple = llvm.get_default_triple()

target = llvm.Target.from_triple(module.triple)
target_machine = target.create_target_machine()

llvm.load_library_permanently('./io.so')
module.data_layout = target_machine.target_data

escrevaInteiro = ir.Function(module,ir.FunctionType(ir.VoidType(), [ir.IntType(32)]),name="escrevaInteiro")
escrevaFlutuante = ir.Function(module,ir.FunctionType(ir.VoidType(),[ir.FloatType()]),name="escrevaFlutuante")
leiaInteiro = ir.Function(module,ir.FunctionType(ir.IntType(32),[]),name="leiaInteiro")
leiaFlutuante = ir.Function(module,ir.FunctionType(ir.FloatType(),[]),name="leiaFlutuante")


vetTabela = []
# funcNow = {
#     "nome": None,
#     "escopo": "global",
#     "type": None,
#     "funcCabecalho": None,
#     "entryBlock": None,
#     "endBasicBlock": None,
#     "builder": None,
#     "retorno": None
# }

escopoVec = []

# varVec = {
#     "nome": "",
#     "tipo": "",
#     "escopo": "",
#     "conteudo": {}
# }

varVec = []

iftrue = []
iffalse = []
ifend = []

LacoBegin = []
LacoEnd = []
LacoFora = []

retornoFunc = False

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

def criaVariavel(node, flag):
    variables = []
    funcNow = []
    if(getEscopo(node) != "global"):
        funcNow = escopoVec[-1]
    if(node.children[1].name == "lista_variaveis"):
        for children in node.children[1].children:
            variables.append(children)
    else:
        variables.append(node.children[1])

    for variable in variables:
        tipo = None
        if(node.children[0].name == "inteiro"):
            tipo = "inteiro"
            if(getEscopo(variable) == "global"):
                var = ir.GlobalVariable(module, ir.IntType(32), variable.name)
                var.initializer =  ir.Constant(ir.IntType(32), 0)
                var.linkage = "common"
            else:
                var = funcNow["builder"].alloca(ir.IntType(32), name=variable.name)
        else:
            tipo = "flutuante"
            if(getEscopo(variable) == "global"):
                var = ir.GlobalVariable(module, ir.FloatType(), variable.name)
                var.initializer =  ir.Constant(ir.FloatType(), 0.0)
                var.linkage = "common"
            else:
                var = funcNow["builder"].alloca(ir.FloatType(), name=variable.name)
        var.align = 4

        if(flag == "lista_parametros"):
            i = 0
            for parametro in node.parent.children:
                if(parametro.children[1].name == variable.name):
                    funcNow["builder"].store(funcNow["funcCabecalho"].args[i], var)
                i+=1

        varVec.append({
            "nome": variable.name,
            "tipo": tipo,
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
    funcNow = {
        "nome": node.children[0].name,
        "parametros": [],
        "escopo": "global",
        "type": None,
        "funcCabecalho": None,
        "entryBlock": None,
        "endBasicBlock": None,
        "builder": None,
        "retorno": None
    }

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

    funcNow["type"] = tipoRet
    funcNow["escopo"] = getEscopo(node)

    if(node.children[0].name == "principal"):
        funcNow["funcCabecalho"] = ir.Function(module, funcTipo, name="main")
    else:
        funcNow["funcCabecalho"] = ir.Function(module, funcTipo, name=node.children[0].name)

    funcNow["entryBlock"] = funcNow["funcCabecalho"].append_basic_block('entry')
    funcNow["builder"] = ir.IRBuilder(funcNow["entryBlock"])

    funcNow["retorno"] = funcNow["builder"].alloca(funcNow["type"], name='retorno')
    escopoVec.append(funcNow)

def fechaFuncao():
    global retornoFunc
    funcNow =  escopoVec[-1]
    funcNow["endBasicBlock"] = funcNow["funcCabecalho"].append_basic_block('exit')

    funcNow["builder"].branch(funcNow["endBasicBlock"])
    funcNow["builder"].position_at_end(funcNow["endBasicBlock"])
    funcNow["builder"].store(ir.Constant(ir.FloatType(), 0.0), funcNow["builder"].alloca(ir.FloatType(), name='finsterson'))

    # funcNow["retorno"] = funcNow["builder"].alloca(funcNow["type"], name='retorno')
    # funcNow["builder"].store(retornoFunc, funcNow["retorno"])
    funcNow["builder"].ret(funcNow["builder"].load(funcNow["retorno"], "retorno"))

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

def getCallConteudo(node):
    if(node.name == "chamada_funcao"):
        function = None
        for func in escopoVec:
            if(node.children[0].name == func["nome"]):
                function = func
        parans = []

        for parametro in node.children[2].children:
            if(getVarConteudo(parametro)):
                parans.append(escopoVec[-1]["builder"].load(getVarConteudo(parametro)["conteudo"], getVarConteudo(parametro)["nome"]))
            else:
                var = escopoVec[-1]["builder"].alloca(getCallConteudo(parametro)["tipo"], name="funcVar")
                
                escopoVec[-1]["builder"].store(getCallConteudo(parametro)["conteudo"], var)

                parans.append(escopoVec[-1]["builder"].load(var, getCallConteudo(parametro)["nome"]))
        funcRes = {
            "nome": node.children[0].name,
            "escopo": getEscopo(node),
            "tipo": function["type"],
            "conteudo": escopoVec[-1]["builder"].call(function["funcCabecalho"], parans)
        }

        return funcRes
    return False

def utilizaVariavel(node, flag):
    funcNow = escopoVec[-1]
    if(flag == "atribuicao"):
        varRes = getVarConteudo(node.children[0])
    filhos = pegaFilhosDireita(node.children[1], [])

    funcNow = escopoVec[-1]
    global retornoFunc

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
            if(filhos[1].name == "chamada_funcao"):
                num1 = getCallConteudo(filhos[1])["conteudo"]
            else:
                num1 = funcNow["builder"].load(getVarConteudo(filhos[1])["conteudo"], getVarConteudo(filhos[1])["nome"])
        
        if(is_number(filhos[2].name)):
            if(filhos[2].name.isdigit()):
                num2 = ir.Constant(ir.IntType(32), int(filhos[2].name))
            else:
                num2 = ir.Constant(ir.FloatType(), float(filhos[2].name))
        else:
            if(filhos[2].name == "chamada_funcao"):
                num2 = getCallConteudo(filhos[2])["conteudo"]
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

        if(flag == "atribuicao"):
            funcNow["builder"].store(temp, varRes["conteudo"])
        elif(flag == "retorno"):
            retornoFunc = temp
            funcNow["builder"].store(retornoFunc, funcNow["retorno"])

    elif(is_number(filhos[0].name)):
        if(filhos[0].name.isdigit()):
            num1 = ir.Constant(ir.IntType(32), int(filhos[0].name))
        else:
            num1 = ir.Constant(ir.FloatType(), float(filhos[0].name))
        
        if(flag == "atribuicao"):
            funcNow["builder"].store(num1, varRes["conteudo"])
        elif(flag == "retorno"):
            retornoFunc = num1
            funcNow["builder"].store(retornoFunc, funcNow["retorno"])
    else:
        if(filhos[0].name == "chamada_funcao"):
            num1 = getCallConteudo(filhos[0])["conteudo"]
        else:
            num1 = funcNow["builder"].load(getVarConteudo(filhos[0])["conteudo"], getVarConteudo(filhos[0])["nome"])

        if(flag == "atribuicao"):
            funcNow["builder"].store(num1, varRes["conteudo"])
        elif(flag == "retorno"):
            retornoFunc = num1
            funcNow["builder"].store(retornoFunc, funcNow["retorno"])

def pegaExpressao(node, expressao):
    
    expressao.append(node)

    for children in node.children:
        pegaExpressao(children, expressao)

    return expressao

def populaVariavel(number):
    funcNow = escopoVec[-1]
    if(is_number(number.name)):
        if(number.name.isdigit()):
            return ir.Constant(ir.IntType(32), int(number.name))
        else:
            return ir.Constant(ir.FloatType(), float(number.name))
    else:
        return funcNow["builder"].load(getVarConteudo(number)["conteudo"], getVarConteudo(number)["nome"])

def criaBlocoTrue(node):
    funcNow = escopoVec[-1]
    global iftrue
    global iffalse
    global ifend
    iftrue.append(funcNow["funcCabecalho"].append_basic_block('iftrue'))
    iffalse.append(funcNow["funcCabecalho"].append_basic_block('iffalse'))
    ifend.append(funcNow["funcCabecalho"].append_basic_block('ifend'))

    expressao = pegaExpressao(node.children[0], [])
    
    operador = expressao[0].name
    var1 = populaVariavel(expressao[1])
    var2 = populaVariavel(expressao[2])
    
    If = funcNow["builder"].icmp_signed(operador, var1, var2, name='if_test')

    funcNow["builder"].cbranch(If, iftrue[-1], iffalse[-1])
    funcNow["builder"].position_at_end(iftrue[-1])

def criaBlocoFalse(node):
    iftrue.pop()
    funcNow = escopoVec[-1]
    funcNow["builder"].branch(ifend[-1])
    funcNow["builder"].position_at_end(iffalse[-1])

def fechaBlocoIf(node):
    iffalse.pop()
    funcNow = escopoVec[-1]
    funcNow["builder"].branch(ifend[-1])
    funcNow["builder"].position_at_end(ifend[-1])
    funcNow["builder"].alloca(ir.IntType(32), name="finsterson")
    ifend.pop()

def criaLaco(node):
    funcNow = escopoVec[-1]
    global LacoBegin
    global LacoEnd
    global LacoFora
    LacoBegin.append(funcNow["funcCabecalho"].append_basic_block('LacoBegin'))
    LacoEnd.append(funcNow["funcCabecalho"].append_basic_block('LacoEnd'))
    LacoFora.append(funcNow["funcCabecalho"].append_basic_block('LacoFora'))


    funcNow["builder"].branch(LacoBegin[-1])
    funcNow["builder"].position_at_end(LacoBegin[-1])

def fechaLaco(node):

    funcNow = escopoVec[-1]
    funcNow["builder"].branch(LacoEnd[-1])
    funcNow["builder"].position_at_end(LacoEnd[-1])

    expressao = pegaExpressao(node, [])
    operador = expressao[0].name

    if(operador == "="):
        operador = "=="

    var1 = populaVariavel(expressao[1])
    var2 = populaVariavel(expressao[2])
    If = funcNow["builder"].icmp_signed(operador, var1, var2, name='if_test')

    funcNow["builder"].cbranch(If, LacoFora[-1], LacoBegin[-1])
    funcNow["builder"].position_at_end(LacoFora[-1])
    funcNow["builder"].alloca(ir.IntType(32), name="finsterson")
    LacoFora.pop()

def escrevaFunc(variavel):
    parans = []
    if(variavel.name == "chamada_funcao"):
        var = getCallConteudo(variavel)
    else:
        var = getVarConteudo(variavel)

    if(var):
        parans.append(escopoVec[-1]["builder"].load(var["conteudo"], var["nome"]))

        if(var["tipo"] == "inteiro" or var["tipo"] == ir.IntType(32)):
            escopoVec[-1]["builder"].call(escrevaInteiro, parans)
        else:
            escopoVec[-1]["builder"].call(escrevaFlutuante, parans)
    else:
        if(is_number(variavel.name)):
            if(variavel.name.isdigit()):
                escopoVec[-1]["builder"].call(escrevaInteiro, [ir.Constant(ir.IntType(32), int(variavel.name))])
            else:
                escopoVec[-1]["builder"].call(escrevaFlutuante, [ir.Constant(ir.FloatType(), float(variavel.name))])

def leiaFunc(variavel):
    parans = []
    if(variavel.name == "chamada_funcao"):
        var = getCallConteudo(variavel)
    else:
        var = getVarConteudo(variavel)

    if(var):
        if(var["tipo"] == "inteiro" or var["tipo"] == ir.IntType(32)):
            escopoVec[-1]["builder"].store(escopoVec[-1]["builder"].call(leiaInteiro, parans), var["conteudo"])
        else:
            escopoVec[-1]["builder"].store(escopoVec[-1]["builder"].call(leiaFlutuante, parans), var["conteudo"])

def percorreArvore(node):

    if(node.name == ":"):
        if(node.parent.name != "lista_parametros"):
            criaVariavel(node, "")
        else:
            criaVariavel(node, "lista_parametros")

    if(node.name == "cabecalho"):
        criaFuncao(node)

    if(node.name == "fim"):
        fechaFuncao()

    if(node.name == "se"):
        criaBlocoTrue(node)
    
    if(node.name == "senão"):
        criaBlocoFalse(node)
    
    if(node.name == "seFim"):
        fechaBlocoIf(node)

    if(node.name == "repita"):
        criaLaco(node)

    if(node.name == "até"):
        fechaLaco(node.parent.children[2])

    if(node.name == ":="):
        utilizaVariavel(node, "atribuicao")
    
    if(node.name == "escreva"):
        escrevaFunc(node.children[1])
    
    if(node.name == "leia"):
        leiaFunc(node.children[1])

    if(node.name == "retorna"):
        utilizaVariavel(node, "retorno")

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

    llvm.shutdown()

def genCode():
    global vetTabela

    resultadoSemantica = semantica(sys.argv[1])

    if(not isError(resultadoSemantica[2])):
        vetTabela = resultadoSemantica[0]
        geraLLVM(resultadoSemantica[1])

genCode()