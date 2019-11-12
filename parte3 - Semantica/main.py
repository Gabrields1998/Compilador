import sys
import lexica
import sintatica
from tabelaSimbolos import TabelaSimbolos
from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter

vetError = []
vetTabela = []

def is_number(num):
     
    try:
        float(num)
        return True
    except:
        pass
    return False

def arvorePoda(no):
    for children in no.children:
        arvorePoda(children)

    if(no.name == "Lista_declaracoes"):
        if(no.parent.name != "programa"):
            no.parent.children = no.children + no.parent.children[1:]
    
    if(no.name == "declaracao_variaveis"):
        declaracoes = no.children[1]
        declaracoes.children = [no.children[0], no.children[2]]
        no.parent.children = [declaracoes]
            
    if(no.name == "tipo"):
        tipo = no.children[0]
        no.parent.children = [tipo] + list(no.parent.children[1:])
    
    if(no.name == "lista_parametros"):
        if(no.parent.name == "cabecalho"):
            no.children = tuple(children for children in no.children if (children.name != ","))

        if(no.parent.name == "lista_parametros"):
            i = 0
            tupla = []
            for i in range(0, len(no.parent.children)):
                if no.parent.children[i].name == no.name:
                    tupla = list(tupla) + list(no.children[0:])
                else:
                    tupla = list(tupla) + [no.parent.children[i]]
            no.parent.children = tupla

    if(no.name == "lista_argumentos"):
        if(no.parent.name != "lista_argumentos"):
            no.children = tuple(children for children in no.children if (children.name != ","))

        if(no.parent.name == "lista_argumentos"):
            i = 0
            tupla = []
            for i in range(0, len(no.parent.children)):
                if no.parent.children[i].name == no.name:
                    tupla = list(tupla) + list(no.children[0:])
                else:
                    tupla = list(tupla) + [no.parent.children[i]]
            no.parent.children = tupla

    if(no.name == "corpo"):
    
        if(no.parent.name == "corpo"):
            i = 0
            tupla = []
            for i in range(0, len(no.parent.children)):
                if no.parent.children[i].name == no.name:
                    tupla = list(tupla) + list(no.children[0:])
                else:
                    tupla = list(tupla) + [no.parent.children[i]]
            no.parent.children = tupla

    if(no.name == "parametro"):
        if(no.children[1].name == ":"):
            parametro = no.children[1]
            parametro.children = [no.children[0], no.children[2]]
            no.parent.children = list(no.parent.children[:-1]) + [parametro]
    
    if(no.name == "atribuicao"):
        if(no.children[1].name == ":="):
            parametro = no.children[1]
            parametro.children = [no.children[0], no.children[2]]
            
            i = 0
            tupla = []
            for i in range(0, len(no.parent.children)):
                if no.parent.children[i].name == no.name:
                    tupla = list(tupla) + list(no.children[0:])
                else:
                    tupla = list(tupla) + [no.parent.children[i]]
            no.parent.children = tupla

    if(no.name == "expressao_logica" or no.name == "expressao_simples" or no.name == "expressao_aditiva" or no.name == "expressao_multiplicativa" or no.name == "expressao_unaria" or no.name == "fator" or no.name == "numero" or no.name == "acao" or no.name == "vazio" or no.name == "None"):
        i = 0
        tupla = []
        for i in range(0, len(no.parent.children)):
            if no.parent.children[i].name == no.name:
                tupla = list(tupla) + list(no.children[0:])
            else:
                tupla = list(tupla) + [no.parent.children[i]]
        no.parent.children = tupla
    
    if(no.name == "expressao"):
        if(len(no.children) == 1):
            i = 0
            tupla = []
            for i in range(0, len(no.parent.children)):
                if no.parent.children[i].name == no.name:
                    tupla = list(tupla) + list(no.children[0:])
                else:
                    tupla = list(tupla) + [no.parent.children[i]]
            no.parent.children = tupla
        else:
            operador = no.children[1].children[0]
            tupla = [no.children[0]] + [no.children[2]]

            operador.children = list(tupla)

            i = 0
            tupla = []
            for i in range(0, len(no.parent.children)):
                if no.parent.children[i].name == no.name:
                    tupla = list(tupla) + [operador]
                else:
                    tupla = list(tupla) + [no.parent.children[i]]
            no.parent.children = tupla

    if(no.name == "lista_variaveis"):
        if(no.parent.name == "lista_variaveis"):
            no.parent.children = no.children + no.parent.children[1:]

        elif(no.parent.name != "lista_variaveis"):
            no.children = tuple(children for children in no.children if (children.name != ","))

    if(no.name == "leia"):
        if(no.parent.name == "leia"):
            no.parent.children = no.children + no.parent.children[1:]

    if(no.name == "repita"):
        if(no.parent.name == "repita"):
            no.parent.children = no.children + no.parent.children[1:]

    if(no.name == "retorna"):
        if(no.parent.name == "retorna"):
            no.parent.children = no.children + no.parent.children[1:]

    if(no.name == "escreva"):
        if(no.parent.name == "escreva"):
            no.parent.children = no.children + no.parent.children[1:]
    
    if(no.name == "se"):
        if(no.parent.name == "se"):
            no.parent.children = no.children + no.parent.children[1:]

def juntaFunc(arvore):
    error = {
        "erro": True,
        "tipo": "Erro:",
        "conteudo": "Função principal não declarada",
        "flag": True
    }
    pesquisaPrincipal(arvore, error)
    if(error["erro"]):
        vetError.append(error)

    chamadaPrincipal(arvore)

    chamadaRecursivaPrincipal(arvore)

def pesquisaRetorno(no, nome, error):
    if(no.name == "retorna"):
        if(error["flag"]):
            error["flag"] = False
            if(error["erro"]):
                error["erro"] = False
                error["conteudo"] = " "
                error["tipo"] = " "
            else:
                error["erro"] = True
                error["conteudo"] = "Função " + nome + " deveria retornar vazio, mas retorna inteiro!"
                error["tipo"] = "Erro:"
    
    for children in no.children:
        pesquisaRetorno(children, nome, error)

def pesquisaPrincipal(no, error):
    for children in no.children:
        pesquisaPrincipal(children, error)

    if(no.name == "cabecalho" and no.children[0].name == "principal"):
        error["erro"] = False
        error["conteudo"] = " "
        error["tipo"] = " "

def chamadaPrincipal(no):
    for children in no.children:
        chamadaPrincipal(children)

    if(no.name == "chamada_funcao" and no.children[0].name == "principal"):
        error = {
            "erro": True,
            "tipo": "Erro:",
            "conteudo": "Chamada para a função principal não permitida",
            "flag": True
        }
        vetError.append(error)

def chamadaUtilitariaRecursiva(no, error):
    for children in no.children:
        chamadaUtilitariaRecursiva(children, error)

    if(no.name == "chamada_funcao" and no.children[0].name == "principal"):
        error["erro"] = True
        error["tipo"] = "Warning:" 
        error["conteudo"] = "Chamada recursiva para principal."

def chamadaRecursivaPrincipal(no):
    for children in no.children:
        chamadaRecursivaPrincipal(children)

    if(no.name == "cabecalho" and no.children[0].name == "principal"):
        error = {
            "erro": False,
            "tipo": " ",
            "conteudo": " ",
            "flag": True
        }
        chamadaUtilitariaRecursiva(no, error)
        if(error["erro"]):
            vetError.append(error)

def pesquisaFuncao(no):
    if(no.name == "cabecalho"):
        if(len(no.parent.children) == 2):
            if(no.parent.children[0].name == "inteiro"):
                error = {
                    "erro": True,
                    "tipo": "Erro:",
                    "conteudo": "Função " + no.children[0].name + " deveria retornar inteiro, mas retorna vazio!",
                    "flag": True
                }
                pesquisaRetorno(no.children[4], no.children[0].name, error)
                if(error["erro"]):
                    vetError.append(error)
            else:
                error = {
                    "erro": True,
                    "tipo": "Erro:",
                    "conteudo": "Função " + no.children[0].name + " deve ser do tipo void ou inteiro!",
                    "flag": True
                }
                vetError.append(error)
        else:
            error = {
                "erro": False,
                "tipo": " ",
                "conteudo": " ",
                "flag": True
            }
            pesquisaRetorno(no.children[4], no.children[0].name, error)
            if(error["erro"]):
                vetError.append(error)
    for children in no.children:
        pesquisaFuncao(children)

def chamada_funcao(declaracao_funcao, no, error):
    for children in no.children:
        chamada_funcao(declaracao_funcao, children, error)

    if(no.name == "cabecalho" and no.children[0].name == declaracao_funcao.children[0].name):
        error["flag"] = True

    if(error["flag"]):

        if(no.name == "chamada_funcao" and no.children[0].name == declaracao_funcao.children[0].name):
            error["erro"] = False
            error["conteudo"] = " "
            error["tipo"] = " "
            if(len(no.children[2].children) != len(declaracao_funcao.children[2].children)):
                error["erro"] = True
                error["conteudo"] = "Chamada da função " + no.children[0].name + " com número de parâmetros diferente que o declarado"
                error["tipo"] = "Erro:"

def chamada_funcao2(chamada_funcao, no, error):
    for children in no.children:
        chamada_funcao2(chamada_funcao, children, error)

    if(no.name == "chamada_funcao" and no.children[0].name == chamada_funcao.children[0].name):
        error["flag"] = False

    if(error["flag"]):
        if(no.name == "cabecalho" and no.children[0].name == chamada_funcao.children[0].name):
            error["erro"] = False
            error["conteudo"] = " "
            error["tipo"] = " "
            if(len(no.children[2].children) != len(chamada_funcao.children[2].children)):
                error["erro"] = True
                error["conteudo"] = "Chamada da função " + no.children[0].name + " com número de parâmetros diferente que o declarado"
                error["tipo"] = "Erro:"

def declaracao_funcao(no, arvore):
    if(no.name == "chamada_funcao" and no.children[0].name != "principal"):
        error = {
            "erro": True,
            "tipo": "Erro:",
            "conteudo": "Chamada a funcao " + no.children[0].name + " mas nao declarada",
            "flag": True
        }
        chamada_funcao2(no, arvore, error)
        if(error["erro"]):
            vetError.append(error)

    if(no.name == "cabecalho" and no.children[0].name != "principal"):
        error = {
            "erro": True,
            "tipo": "Warning:",
            "conteudo": "Funcao " + no.children[0].name + " declarada mas nao utilizada",
            "flag": False
        }
        chamada_funcao(no, arvore, error)
        if(error["erro"]):
            vetError.append(error)
    
    for children in no.children:
        declaracao_funcao(children, arvore)

def criarTabela(no):
    if(no.name == ":"):
        if(no.children[1].name == "lista_variaveis"):
            for var in no.children[1].children:
                novaTabela = TabelaSimbolos()
                novaTabela.setTipo("variavel")
                novaTabela.setTipoValor(no.children[0].name)
                if(len(var.children) == 0):
                    novaTabela.setNome(var.name)
                else:
                    novaTabela.setNome(var.children[0].name)
                    if(var.children[1].children[0].name == "indice"):
                        novaTabela.setDimensoes([var.children[1].children[2].name,var.children[1].children[0].children[1].name])

                    else:
                        novaTabela.setDimensoes([var.children[1].children[1].name])
                
                pai = no
                breaker = True
                while(breaker):
                    pai = pai.parent
                    if(pai.name == "programa"):
                        novaTabela.setEscopo("global")
                        breaker = False
                    elif(pai.name == "cabecalho"):
                        novaTabela.setEscopo(pai.children[0].name)
                        breaker = False
                vetTabela.append(novaTabela)
        else:
            novaTabela = TabelaSimbolos()
            novaTabela.setTipo("variavel")
            novaTabela.setTipoValor(no.children[0].name)
            if(len(no.children[1].children) == 0):
                novaTabela.setNome(no.children[1].name)
            else:
                novaTabela.setNome(no.children[1].children[0].name)
                if(no.children[1].children[1].children[0].name == "indice"):
                    novaTabela.setDimensoes([int(no.children[1].children[1].children[2].name),int(no.children[1].children[1].children[0].children[1].name)])
                else:
                    novaTabela.setDimensoes([int(no.children[1].children[1].children[1].name)])
            
            pai = no
            breaker = True
            while(breaker):
                pai = pai.parent
                if(pai.name == "programa"):
                    novaTabela.setEscopo("global")
                    breaker = False
                elif(pai.name == "cabecalho"):
                    novaTabela.setEscopo(pai.children[0].name)
                    breaker = False
            vetTabela.append(novaTabela)
    elif(no.name == "cabecalho"):
        novaTabela = TabelaSimbolos()
        novaTabela.setTipo("Funcao")
        novaTabela.setTipoValor(no.parent.children[0].name)
        novaTabela.setNome(no.children[0].name)
        parametros = []
        for par in no.children[2].children:
            parametros.append([par.children[0].name, par.children[1].name])
        novaTabela.setParametros(parametros)
            
        pai = no
        breaker = True
        while(breaker):
            pai = pai.parent
            if(pai.name == "programa"):
                novaTabela.setEscopo("global")
                breaker = False
            elif(pai.name == "cabecalho"):
                novaTabela.setEscopo(pai.children[0].name)
                breaker = False
        vetTabela.append(novaTabela)
    for children in no.children:
        criarTabela(children)

def confereErro(no):
    if (no.name == ":=" or no.name == "leia" or no.name == "lista_parametros"):
        varTabela = None

        escopo = " "
        pai = no
        breaker = True
        while(breaker):
            pai = pai.parent
            if(pai.name == "programa"):
                escopo = "global"
                breaker = False
            elif(pai.name == "cabecalho"):
                escopo = pai.children[0].name
                breaker = False
        if(no.name == ":="):
            for tabela in vetTabela:
                if(no.children[0].name != "var"):
                    if(tabela.getNome() == no.children[0].name):
                        if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                            varTabela = tabela
                else:
                    if(tabela.getNome() == no.children[0].children[0].name):
                        if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                            varTabela = tabela
            if(varTabela != None):
                varTabela.setInicializada(True)
                varTabela.setUtilizada(True)
            elif(no.children[0].name != "chamada_funcao"):
                if(no.children[0].name != "var"):
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Variável " + no.children[0].name + " do escopo " + escopo + " nao declarada",
                        "flag": True
                    }
                else:
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Variável " + no.children[0].children[0].name + " do escopo " + escopo + " nao declarada",
                        "flag": True
                    }
                vetError.append(error)
        elif(no.name == "leia"):
            for tabela in vetTabela:
                if(no.children[1].name != "var"):
                    if(tabela.getNome() == no.children[1].name):
                        if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                            varTabela = tabela
                else:
                    
                    if(tabela.getNome() == no.children[1].children[0].name):
                        if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                            varTabela = tabela
            if(varTabela != None):
                varTabela.setInicializada(True)
            elif(no.children[0].name != "chamada_funcao"):
                if(no.children[1].name != "var"):
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Variável " + no.children[1].name + " do escopo " + escopo + " nao declarada",
                        "flag": True
                    }
                else:
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Variável " + no.children[1].children[0].name + " do escopo " + escopo + " nao declarada",
                        "flag": True
                    }
                vetError.append(error)
        elif(no.name == "lista_parametros"):
            for parametro in no.children:
                varTabela = None
                for tabela in vetTabela:
                    if(parametro.children[1].name != "var"):
                        if(tabela.getNome() == parametro.children[1].name):
                            if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                                varTabela = tabela
                    else:
                        if(tabela.getNome() == parametro.children[1].children[0].name):
                            if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                                varTabela = tabela
                if(varTabela != None):
                    varTabela.setInicializada(True)
                elif(no.children[0].name != "chamada_funcao"):
                    if(parametro.children[1].name != "var"):
                        error = {
                            "erro": True,
                            "tipo": "Erro:",
                            "conteudo": "Variável " + parametro.children[1].name + " do escopo " + escopo + " nao declarada",
                            "flag": True
                        }
                    else:
                        error = {
                            "erro": True,
                            "tipo": "Erro:",
                            "conteudo": "Variável " + parametro.children[1].children[0].name + " do escopo " + escopo + " nao declarada",
                            "flag": True
                        }
                    vetError.append(error)
    if(no.name == ":=" or no.name == "escreva" or no.name == "leia" or no.name == "repita" or no.name == "se"):
        if(no.name == ":="):
            escopo = " "
            pai = no
            breaker = True
            while(breaker):
                pai = pai.parent
                if(pai.name == "programa"):
                    escopo = "global"
                    breaker = False
                elif(pai.name == "cabecalho"):
                    escopo = pai.children[0].name
                    breaker = False
                    
            filho = no.children[1]
            varTabela = None
            if(filho.name != "*" and filho.name != "/" and filho.name != "+" and filho.name != "-"):
                for tabela in vetTabela:
                    if(filho.name != "var"):
                        if(tabela.getNome() == filho.name):
                            if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                                varTabela = tabela
                    else:
                        if(tabela.getNome() == filho.children[0].name):
                            if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                                varTabela = tabela
                if(varTabela != None):
                    varTabela.setUtilizada(True)
                else:
                    if(filho.name != "chamada_funcao"):
                        if(not is_number(filho.name)):
                            if(filho.name != "var"):
                                error = {
                                    "erro": True,
                                    "tipo": "Erro:",
                                    "conteudo": "Variável " + filho.name + " do escopo " + escopo + " nao declarada",
                                    "flag": True
                                }
                            else:
                                error = {
                                    "erro": True,
                                    "tipo": "Erro:",
                                    "conteudo": "Variável " + filho.children[0].name + " do escopo " + escopo + " nao declarada",
                                    "flag": True
                                }
                            vetError.append(error)
            else:
                for node in  filho.children:
                    for tabela in vetTabela:
                        if(node.name != "var"):
                            if(tabela.getNome() == node.name):
                                if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                                    varTabela = tabela
                        else:
                            if(tabela.getNome() == node.children[0].name):
                                if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                                    varTabela = tabela 
                    if(varTabela != None):
                        varTabela.setUtilizada(True)
                    else:
                        if(node.name != "chamada_funcao"):
                            if(not is_number(node.name)):
                                if(filho.name != "var"):
                                    error = {
                                        "erro": True,
                                        "tipo": "Erro:",
                                        "conteudo": "Variável " + node.name + " do escopo " + escopo + " nao declarada",
                                        "flag": True
                                    }
                                else:
                                    error = {
                                        "erro": True,
                                        "tipo": "Erro:",
                                        "conteudo": "Variável " + node.children[0].name + " do escopo " + escopo + " nao declarada",
                                        "flag": True
                                    }
                                vetError.append(error)
        if(no.name == "escreva" or no.name == "leia"):
            varTabela = None
            escopo = " "
            pai = no
            breaker = True
            while(breaker):
                pai = pai.parent
                if(pai.name == "programa"):
                    escopo = "global"
                    breaker = False
                elif(pai.name == "cabecalho"):
                    escopo = pai.children[0].name
                    breaker = False

            filho = no.children[1]
            for tabela in vetTabela:
                if(filho.name != "var"):
                    if(tabela.getNome() == filho.name):
                        if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                            varTabela = tabela
                else:
                    if(tabela.getNome() == no.children[0].name):
                        if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                            varTabela = tabela

            if(varTabela != None):
                varTabela.setUtilizada(True)
            else:
                if(not is_number(filho.name) and filho.name != "chamada_funcao"):
                    if(filho.name != "var"):
                        error = {
                            "erro": True,
                            "tipo": "Erro:",
                            "conteudo": "Variável " + filho.name + " do escopo " + escopo + " nao declarada",
                            "flag": True
                        }
                    else:
                        error = {
                            "erro": True,
                            "tipo": "Erro:",
                            "conteudo": "Variável " + filho.children[0].name + " do escopo " + escopo + " nao declarada",
                            "flag": True
                        }
                    vetError.append(error)
    if(no.name == "retorna"):
        varTabela1 = None
        varTabela2 = None
        escopo = " "
        pai = no
        breaker = True
        while(breaker):
            pai = pai.parent
            if(pai.name == "programa"):
                escopo = "global"
                breaker = False
            elif(pai.name == "cabecalho"):
                escopo = pai.children[0].name
                breaker = False
        if(len(no.children[1].children) == 2):
            for tabela in vetTabela:
                if(tabela.getNome() == no.children[1].children[0].name):
                    if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        varTabela1 = tabela

                if(tabela.getNome() == no.children[1].children[1].name):
                    if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        varTabela2 = tabela
            if(varTabela1 != None):
                varTabela1.setUtilizada(True)
            else:
                error = {
                    "erro": True,
                    "tipo": "Erro:",
                    "conteudo": "Variável " + no.children[1].children[0].name + " do escopo " + escopo + " não declarada",
                    "flag": True
                }
                vetError.append(error)
            if(varTabela2 != None):
                varTabela2.setUtilizada(True)
            else:
                error = {
                    "erro": True,
                    "tipo": "Erro:",
                    "conteudo": "Variável " + no.children[1].children[1].name + " do escopo " + escopo + " não declarada",
                    "flag": True
                }
                vetError.append(error)
        else:
            for tabela in vetTabela:
                if(tabela.getNome() == no.children[1].name):
                    if((escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        varTabela1 = tabela
            if(varTabela1 != None):
                varTabela1.setUtilizada(True)
            else:
                error = {
                    "erro": True,
                    "tipo": "Erro:",
                    "conteudo": "Variável " + no.children[1].name + " do escopo " + escopo + " não declarada",
                    "flag": True
                }
                vetError.append(error)
                
    for children in no.children:
        confereErro(children)

def atribuicaoDistinta(no):
    if(no.name == ":="):
        noAtributo = None
        if(no.children[0].name != "var"):
            noAtributo = no.children[0].name
        else:
            noAtributo = no.children[0].children[0].name
        noTipo = None   
        for tabela in vetTabela:
            if(noAtributo == tabela.getNome()):
                noTipo = tabela.getTipoValor()

        if(no.children[1].name == "+" or no.children[1].name == "-" or no.children[1].name == "*" or no.children[1].name == "/"):
            noOperando = []
            for filho in no.children[1].children:
                if(not is_number(filho.name)):
                    escopo = " "
                    pai = no
                    breaker = True
        
                    while(breaker):
                        pai = pai.parent
                        if(pai.name == "programa"):
                            escopo = "global"
                            breaker = False
                        elif(pai.name == "cabecalho"):
                            escopo = pai.children[0].name
                            breaker = False

                    for tabela in vetTabela:
                        if(filho.name == "var" or filho.name == "chamada_funcao"):
                            if(filho.children[0].name == tabela.getNome() and ((escopo == tabela.getEscopo() or tabela.getEscopo() == "global"))):
                                noOperando.append(tabela.getTipoValor())
                        else:
                            if(filho.name == tabela.getNome() and ((escopo == tabela.getEscopo() or tabela.getEscopo() == "global"))):
                                noOperando.append(tabela.getTipoValor())
                else:
                    if(filho.name.isdigit()):
                        noOperando.append("inteiro")
                    else:
                        noOperando.append("flutuante")

            if(noTipo == "inteiro" and (noOperando[0] == "flutuante" or noOperando[1] == "flutuante")):
                error = {
                    "erro": True,
                    "tipo": "Warning:",
                    "conteudo": "Coerção implícita do valor de " + noAtributo + ".",
                    "flag": True
                }
                vetError.append(error)

            if(noTipo == "inteiro" and (noTipo != noOperando[0] or noTipo != noOperando[1])):
                error = {
                    "erro": True,
                    "tipo": "Warning:",
                    "conteudo": "Atribuição de tipos distintos " + noAtributo + " de tipo " + noTipo + " difere da expressao passada",
                    "flag": True
                }
                vetError.append(error)
            elif(noTipo == "flutuante" and noOperando[0] == "inteiro" and noOperando[1] == "inteiro"):
                error = {
                    "erro": True,
                    "tipo": "Warning:",
                    "conteudo": "Atribuição de tipos distintos " + noAtributo + " de tipo " + noTipo + " difere da expressao passada",
                    "flag": True
                }
                vetError.append(error)
        else:
            noOperando = []
            filho = no.children[1]
            if(not is_number(filho.name)):
                escopo = " "
                pai = no
                breaker = True
    
                while(breaker):
                    pai = pai.parent
                    if(pai.name == "programa"):
                        escopo = "global"
                        breaker = False
                    elif(pai.name == "cabecalho"):
                        escopo = pai.children[0].name
                        breaker = False

                for tabela in vetTabela:
                    if(filho.name == "var" or filho.name == "chamada_funcao"):
                        if(filho.children[0].name == tabela.getNome() and ((escopo == tabela.getEscopo() or tabela.getEscopo() == "global"))):
                            noOperando.append(tabela.getTipoValor())
                    else:
                        if(filho.name == tabela.getNome() and ((escopo == tabela.getEscopo() or tabela.getEscopo() == "global"))):
                            noOperando.append(tabela.getTipoValor())
            else:
                if(filho.name.isdigit()):
                    noOperando.append("inteiro")
                else:
                    noOperando.append("flutuante")

        if(noTipo == "inteiro" and (noOperando[0] == "flutuante")):
            error = {
                "erro": True,
                "tipo": "Warning:",
                "conteudo": "Coerção implícita do valor de " + noAtributo + ".",
                "flag": True
            }
            vetError.append(error)

        if(noTipo != noOperando[0]):
            error = {
                "erro": True,
                "tipo": "Warning:",
                "conteudo": "Atribuição de tipos distintos " + noAtributo + " de tipo " + noTipo + " difere da expressao passada",
                "flag": True
            }
            vetError.append(error)

    for children in no.children:
        atribuicaoDistinta(children)

def verificaArray(no):
    if(no.name == "var"):
        if(no.children[1].children[0].name == "indice"):
            indice1 = no.children[1].children[2].name
            indice2 = no.children[1].children[0].children[1].name
            
            array = []
            escopo = " "
            pai = no
            breaker = True
            while(breaker):
                pai = pai.parent
                if(pai.name == "programa"):
                    escopo = "global"
                    breaker = False
                elif(pai.name == "cabecalho"):
                    escopo = pai.children[0].name
                    breaker = False
            tipo1 = None
            tipo2 = None
            if(not is_number(indice1) and not is_number(indice2)):
                for tabela in vetTabela:
                    if(no.children[0].name == tabela.getNome() and (escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        array = tabela.getDimensoes()

                    if(indice1 == tabela.getNome() and (escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        tipo1 = tabela.getTipoValor()

                    if(indice2 == tabela.getNome() and (escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        tipo2 = tabela.getTipoValor()
                
                if(tipo1 != "inteiro" or tipo2 != "inteiro"):
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Índice do array " + no.children[0].name + " não inteiro",
                        "flag": True
                    }
                    vetError.append(error)
            elif(not is_number(indice1) and is_number(indice2)):
                for tabela in vetTabela:
                    if(no.children[0].name == tabela.getNome() and (escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        array = tabela.getDimensoes()

                    if(indice1 == tabela.getNome() and (escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        tipo1 = tabela.getTipoValor()
                

                if(tipo1 != "inteiro" or not indice2.isdigit()):
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Índice do array " + no.children[0].name + " não inteiro",
                        "flag": True
                    }
                    vetError.append(error)
                elif (array[1].isdigit()):
                    if(int(indice2) > int(array[1])):
                        error = {
                            "erro": True,
                            "tipo": "Erro:",
                            "conteudo": "índice de array " + no.children[0].name + " fora do intervalo (out of range)",
                            "flag": True
                        }
                        vetError.append(error)      
            elif( is_number(indice1) and not is_number(indice2)):
                print("primeiro numero nao inteiro")
                for tabela in vetTabela:
                    if(no.children[0].name == tabela.getNome() and (escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        array = tabela.getDimensoes()

                    if(indice2 == tabela.getNome() and (escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        tipo2 = tabela.getTipoValor()
                        
                if(not indice1.isdigit() or tipo2 != "inteiro"):
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Índice do array " + no.children[0].name + " não inteiro",
                        "flag": True
                    }
                    vetError.append(error)
                elif (array[0].isdigit()):
                    if(int(indice1) > int(array[0])):
                        error = {
                            "erro": True,
                            "tipo": "Erro:",
                            "conteudo": "índice de array " + no.children[0].name + " fora do intervalo (out of range)",
                            "flag": True
                        }
                        vetError.append(error)
            elif( is_number(indice1) and  is_number(indice2)):
                for tabela in vetTabela:
                    if(no.children[0].name == tabela.getNome() and (escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        array = tabela.getDimensoes()

                if(not indice1.isdigit() or not indice2.isdigit()):
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Índice do array " + no.children[0].name + " não inteiro",
                        "flag": True
                    }
                    vetError.append(error)
                elif (array[0].isdigit()):
                    if(int(indice1) > int(array[0])):
                        error = {
                            "erro": True,
                            "tipo": "Erro:",
                            "conteudo": "índice de array " + no.children[0].name + " fora do intervalo (out of range)",
                            "flag": True
                        }
                        vetError.append(error)
                elif (array[1].isdigit()):
                    if(int(indice1) > int(array[1])):
                        error = {
                            "erro": True,
                            "tipo": "Erro:",
                            "conteudo": "índice de array " + no.children[0].name + " fora do intervalo (out of range)",
                            "flag": True
                        }
                        vetError.append(error)
        else:
            indice1 = no.children[1].children[1].name
            array = []
            escopo = " "
            pai = no
            breaker = True
            while(breaker):
                pai = pai.parent
                if(pai.name == "programa"):
                    escopo = "global"
                    breaker = False
                elif(pai.name == "cabecalho"):
                    escopo = pai.children[0].name
                    breaker = False
            tipo1 = None

            if(not is_number(indice1)):
                for tabela in vetTabela:
                    if(no.children[0].name == tabela.getNome() and (escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        array = tabela.getDimensoes()

                if(indice1 == tabela.getNome() and (escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                    tipo1 = tabela.getTipoValor()
            
                if(tipo1 != "inteiro"):
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Índice do array " + no.children[0].name + " não inteiro",
                        "flag": True
                    }
                vetError.append(error)
            elif( is_number(indice1)):
                for tabela in vetTabela:
                    if(no.children[0].name == tabela.getNome() and (escopo == tabela.getEscopo() or tabela.getEscopo() == "global")):
                        array = tabela.getDimensoes()

                if(not indice1.isdigit()):
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Índice do array " + no.children[0].name + " não inteiro",
                        "flag": True
                    }
                    vetError.append(error)
                elif (array[0].isdigit()):
                    if(int(indice1) > int(array[0])):
                        error = {
                            "erro": True,
                            "tipo": "Erro:",
                            "conteudo": "índice de array " + no.children[0].name + " fora do intervalo (out of range)",
                            "flag": True
                        }
                        vetError.append(error)
    for children in no.children:
        verificaArray(children)

def main():
    arvore = sintatica.generate(sys.argv[1])

    if(arvore):
        arvorePoda(arvore)
        criarTabela(arvore)
        confereErro(arvore)
        for tabela in vetTabela:
            if(tabela.getTipo() == "variavel"):
                count = 0
                for tabela2 in  vetTabela:
                    if(tabela.getNome() == tabela2.getNome() and tabela.getEscopo() == tabela2.getEscopo()):
                        count +=1
                if(count >= 2):
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Variável " + tabela.getNome() + " já declarada anteriormente",
                        "flag": True
                    }
                    vetError.append(error)
                if(tabela.getInicializada() == False):
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Variável " + tabela.getNome() + " declarada e não inicializada",
                        "flag": True
                    }
                    vetError.append(error)
                if(tabela.getUtilizada() == False):
                    error = {
                        "erro": True,
                        "tipo": "Erro:",
                        "conteudo": "Variável " + tabela.getNome() + " declarada e não utilizada",
                        "flag": True
                    }
                    vetError.append(error)

        atribuicaoDistinta(arvore)      
        juntaFunc(arvore)
        pesquisaFuncao(arvore)
        declaracao_funcao(arvore, arvore)
        verificaArray(arvore)
        # verificaTabela
        # for tabela in vetTabela:
        #     print("\n_______________________________________\n")
        #     print(" tipo: " , tabela.getTipo() 
        #     , "\n nome: " , tabela.getNome()
        #     , "\n tipoValor: " , tabela.getTipoValor()
        #     , "\n parametros: " , tabela.getParametros() 
        #     , "\n dimensoes: " , tabela.getDimensoes() 
        #     , "\n escopo: " , tabela.getEscopo() 
        #     , "\n declarada: " , tabela.getDeclarada() 
        #     , "\n inicializada: " , tabela.getInicializada() 
        #     , "\n utilizada: ", tabela.getUtilizada(), "\n" )

        if(len(vetError) != 0):
            for erro in vetError:
                print(erro["tipo"], erro["conteudo"])

        UniqueDotExporter(arvore).to_picture("programaPoda.png")


main()