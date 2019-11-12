import sys
import ply.yacc as yacc
import lexica
# from graphviz import Digraph
from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter

tokens =  lexica.tokens

error = False

def p_programa(p):
    '''programa : lista_declaracoes'''
    
    p[0] = Node("programa", children = [p[1]])

def p_lista_declaracoes(p):
    '''lista_declaracoes : lista_declaracoes declaracao
                        | declaracao'''
    
    if(len(p) == 3):
        p[0] = Node("Lista_declaracoes", children = [p[1], p[2]])
    else:
        p[0] = Node("Lista_declaracoes", children = [p[1]])

def p_declaracao(p):
    '''declaracao : declaracao_variaveis
            | inicializacao_variaveis
            | declaracao_funcao'''
    
    p[0] = Node("declaracao", children = [p[1]])

def p_declaracao_variaveis(p):
    '''declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'''
    
    doispontos = Node(p[2])
    p[0] = Node("declaracao_variaveis", children = [p[1], doispontos, p[3]])

def p_inicializacao_variaveis(p):
    '''inicializacao_variaveis : atribuicao'''
    
    p[0] = Node("inicializacao_variaveis", children = [p[1]])

def p_lista_variaveis(p):
    '''lista_variaveis : lista_variaveis VIRGULA var 
                        | var'''
    

    if(len(p) == 4):
        virgula = Node(p[2])


        p[0] = Node("lista_variaveis", children = [p[1], virgula, p[3]])
    else:
        p[0] = Node("lista_variaveis", children = [p[1]])

def p_var(p):
    '''var : ID
            | ID indice'''
    
    
    if(len(p) == 3):
        ident = Node(p[1])

        p[0] = Node("var", children = [ident, p[2]])
    else:
        p[0] = Node(p[1])

def p_indice(p):
    '''indice : indice ABRE_COLCHETE expressao FECHA_COLCHETE
            | ABRE_COLCHETE expressao FECHA_COLCHETE'''

    
    
    if(len(p) == 5):
        abreColchete = Node(str(p[2]))

        fechaColchete = Node(str(p[4]))

        p[0] = Node("indice", children = [p[1], abreColchete, p[3], fechaColchete])
    else:
        abreColchete = Node(str(p[1]))

        fechaColchete = Node(str(p[3]))

        p[0] = Node("indice", children = [abreColchete, p[2], fechaColchete])

def p_tipo(p):
    '''tipo : INTEIRO
            | FLUTUANTE'''
    
    
    tipo = Node(p[1])

    p[0] = Node("tipo", children = [tipo])

def p_declaracao_funcao(p):
    '''declaracao_funcao : tipo cabecalho 
                        | cabecalho'''
    
    if(len(p) == 3):
        p[0] = Node("declaracao_funcao", children = [p[1], p[2]])
    else:
        p[0] = Node("declaracao_funcao", children = [p[1]])

def p_cabecalho(p):
    '''cabecalho : ID ABRE_PARENTESES lista_parametros FECHA_PARENTESES corpo FIM'''
    
    ident = Node(str(p[1]))
    abreColchete = Node(str(p[2]))
    fechaColchete = Node(str(p[4]))
    fim = Node(str(p[6]))

    p[0] = Node("cabecalho", children = [ident, abreColchete, p[3], fechaColchete, p[5], fim])

def p_lista_parametros(p):
    '''lista_parametros : lista_parametros VIRGULA parametro
                        | parametro
                        | vazio'''
    

    if(len(p) == 4):
        virgula = Node(str(p[2]))


        p[0] = Node("lista_parametros", children = [p[1], virgula, p[3]])
    else:
        p[0] = Node("lista_parametros", children = [p[1]])

def p_parametro(p):
    '''parametro : tipo DOIS_PONTOS ID
                |  parametro ABRE_COLCHETE FECHA_COLCHETE'''
    
    var2 = Node(str(p[2]))
    var3 = Node(str(p[3]))
    p[0] = Node("parametro", children = [p[1], var2, var3] )

def p_corpo(p):
    '''corpo : corpo acao 
            | vazio'''
    
    if(len(p) == 3):
        p[0] = Node("corpo", children = [p[1], p[2]])
    else: 
        p[0] = Node("corpo", children = [p[1]])

def p_acao(p):
    '''acao : expressao
            | declaracao_variaveis
            | se
            | repita
            | leia
            | escreva
            | retorna'''
    
    p[0] = Node("acao", children = [p[1]])

def p_se(p):
    '''se : SE expressao ENTAO corpo FIM
        | SE expressao ENTAO corpo SENAO corpo FIM'''
    

    se = Node(str(p[1]))
    entao = Node(str(p[3]))

    if(len(p) == 6):
        fim = Node(str(p[5]))

        p[0] = Node("se", children =[se, p[2], entao, p[4], fim])
    else:

        senao = Node(str(p[5]))

        fim = Node(str(p[7]))


        p[0] = Node( "se", children =[se, p[2], entao, p[4], senao, p[6], fim])

def p_repita(p):
    '''repita : REPITA corpo ATE expressao'''

    repita = Node(str(p[1]))
    ate = Node(str(p[3]))

    p[0] = Node("repita", children = [repita, p[2], ate, p[4]])

def p_atribuicao(p):
    '''atribuicao : var ATRIBUICAO expressao'''
    
    atribuicao = Node(str(p[2]))

    p[0] = Node("atribuicao", children = [p[1], atribuicao, p[3]])

def p_leia(p):
    '''leia : LEIA ABRE_PARENTESES var FECHA_PARENTESES'''
    
    leia = Node(str(p[1]))
    abreparenteses = Node(str(p[2]))
    fechaparenteses = Node(str(p[4]))
    p[0] = Node("leia", children = [leia, abreparenteses, p[3], fechaparenteses])

def p_escreva(p):
    '''escreva : ESCREVA ABRE_PARENTESES expressao FECHA_PARENTESES'''
    
    escreva = Node(str(p[1]))
    abreparenteses = Node(str(p[2]))
    fechaparenteses = Node(str(p[4]))
    
    p[0] = Node("escreva", children = [escreva, abreparenteses, p[3], fechaparenteses])

def p_retorna(p):
    '''retorna : RETORNA ABRE_PARENTESES expressao FECHA_PARENTESES'''
    
    retorna = Node(str(p[1]))
    abreparenteses = Node(str(p[2]))
    fechaparenteses = Node(str(p[4]))

    p[0] = Node("retorna", children = [retorna, abreparenteses, p[3], fechaparenteses])

def p_expressao(p):
    '''expressao : expressao_logica
                | atribuicao'''
    
    p[0] = Node("expressao", children = [p[1]])

def p_expressao_logica(p):
    '''expressao_logica : expressao_simples
                        | expressao_logica operador_logico expressao_simples'''

    
    if(len(p) == 4):
        p[0] = Node("expressao_logica", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node("expressao_logica", children = [p[1]])

def p_expressao_simples(p):
    '''expressao_simples : expressao_aditiva
                        | expressao_simples operador_relacional expressao_aditiva'''
    
    if(len(p) == 4):
        p[0] = Node("expressao_simples", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node("expressao_simples", children = [p[1]])

def p_expressao_aditiva(p):
    '''expressao_aditiva : expressao_multiplicativa
                        | expressao_aditiva operador_soma expressao_multiplicativa'''
    
    if(len(p) == 4):
        p[0] = Node("expressao_aditiva", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node("expressao_aditiva", children = [p[1]])

def p_expressao_multiplicativa(p):
    '''expressao_multiplicativa : expressao_unaria
                                | expressao_multiplicativa operador_multiplicacao expressao_unaria'''
    
    if(len(p) == 4):
        p[0] = Node("expressao_multiplicativa", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node("expressao_multiplicativa", children = [p[1]])

def p_expressao_unaria(p):
    '''expressao_unaria : fator
                        | operador_soma fator
                        | operador_negacao fator'''
    
    if(len(p) == 3):
        p[0] = Node("expressao_unaria", children = [p[1], p[2]])
    else:
        p[0] = Node("expressao_unaria", children = [p[1]])

def p_operador_relacional(p):
    '''operador_relacional : MENOR
                            | MAIOR 
                            | IGUALDADE 
                            | DIFERENTE 
                            | MENOR_IGUAL 
                            | MAIOR_IGUAL'''
    
    operador = Node(str(p[1]))

    p[0] = Node("operador_relacional", children = [operador])

def p_operador_soma(p):
    '''operador_soma : SOMA
                    | SUBTRACAO'''
    
    operador = Node(str(p[1]))

    p[0] = Node("operador_soma", children = [operador])

def p_operador_logico(p):
    '''operador_logico : E_LOGICO
                        | OU_LOGICO'''
    
    operador = Node(str(p[1]))

    p[0] = Node("operador_logico", children = [operador])

def p_operador_negacao(p):
    '''operador_negacao : NEGACAO'''
    
    operador = Node(str(p[1]))

    p[0] = Node("operador_negacao", children = [operador])

def p_operador_multiplicacao(p):
    '''operador_multiplicacao : MULTIPLICACAO
                            | DIVISAO'''
    
    operador = Node(str(p[1]))

    p[0] = Node("operador_multiplicacao", children = [operador])

def p_fator(p):
    '''fator : ABRE_PARENTESES expressao FECHA_PARENTESES
            | var
            | chamada_funcao
            | numero'''
    
    if(len(p) == 4):

        abreparenteses = Node(str(p[1]))
        fechaparenteses = Node(str(p[3]))

        p[0] = Node("fator", children = [abreparenteses, p[2], fechaparenteses])
    else:
        p[0] = Node("fator", children = [p[1]])
    
def p_numero(p):
    '''numero : NUMERO_INTEIRO
            | NUMERO_FLUTUANTE
            | NOTACAO_CIENTIFICA'''
    
    numeracao = Node(str(p[1]))

    p[0] = Node("numero", children = [numeracao])

def p_chamada_funcao(p):
    '''chamada_funcao : ID ABRE_PARENTESES lista_argumentos FECHA_PARENTESES'''
    
    ident = Node(str(p[1]))
    abreparenteses = Node(str(p[2]))
    fechaparenteses = Node(str(p[4]))

    p[0] = Node("chamada_funcao", children = [ident, abreparenteses, p[3], fechaparenteses])

def p_lista_argumentos(p):
    '''lista_argumentos : lista_argumentos VIRGULA expressao
                        | expressao
                        | vazio'''
    
    if(len(p) == 4):

        virgula = Node(str(p[2]))

        p[0] = Node("lista_argumentos", children = [p[1], virgula, p[3]])
    else:
        p[0] = Node("lista_argumentos", children = [p[1]])

def p_vazio(p):
    '''vazio : '''
    
    vazio = Node("None")

    p[0] = Node("vazio", children = [vazio])

def find_column(token):
    input = token.lexer.lexdata
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def p_error(p):
    global error
    if p:
        print("Syntax error at token", p.type, "line: ", p.lineno, "column: ", find_column(p))
    else:
        print("Syntax error at EOF")
    error = True

def generate(arquivoRead):
    yacc.yacc()

    arquivo = open(arquivoRead)
    data = arquivo.read()
    programa = yacc.parse(data)

    if(not error):
        UniqueDotExporter(programa).to_picture("programa.png")
        return programa

    return False