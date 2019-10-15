import sys
import ply.yacc as yacc
import lexica
# from graphviz import Digraph
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

tokens =  lexica.tokens

id = 0
error = False

def p_programa(p):
    '''programa : lista_declaracoes'''
    global id
    p[0] = Node("< " + str(id) + " >" + " programa", children = [p[1]])
    id +=1

def p_lista_declaracoes(p):
    '''lista_declaracoes : lista_declaracoes declaracao
                        | declaracao'''
    global id
    if(len(p) == 3):
        p[0] = Node("< " + str(id) + " >" + " Lista_declaracoes", children = [p[1], p[2]])
    else:
        p[0] = Node("< " + str(id) + " >" + " Lista_declaracoes", children = [p[1]])
    id+=1

def p_declaracao(p):
    '''declaracao : declaracao_variaveis
            | inicializacao_variaveis
            | declaracao_funcao'''
    global id
    p[0] = Node("< " + str(id) + " >" + " declaracao", children = [p[1]])
    id+=1

def p_declaracao_variaveis(p):
    '''declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'''
    global id
    p[0] = Node("< " + str(id) + " >" + " " +str(p[2]), children = [p[1], p[3]])
    id+=1
def p_inicializacao_variaveis(p):
    '''inicializacao_variaveis : atribuicao'''
    global id
    p[0] = Node("< " + str(id) + " >" + " inicializacao_variaveis", children = [p[1]])
    id+=1
def p_lista_variaveis(p):
    '''lista_variaveis : lista_variaveis VIRGULA var 
                        | var'''
    global id
    if(len(p) == 4):
        p[0] = Node("< " + str(id) + " >" + " lista_variaveis", children = [p[1], p[3]])
    else:
        p[0] = Node("< " + str(id) + " >" + " variavel", children = [p[1]])
    id+=1
def p_var(p):
    '''var : ID
            | ID indice'''
    global id
    if(len(p) == 3):
        p[0] = Node("< " + str(id) + " >" + " Indice ID", children = [p[2]])
    else:
        p[0] = Node("< " + str(id) + " > " + p[1])
    id+=1

def p_indice(p):
    '''indice : indice ABRE_COLCHETE expressao FECHA_COLCHETE
            | ABRE_COLCHETE expressao FECHA_COLCHETE'''
    global id
    if(len(p) == 5):
        p[0] = Node("< " + str(id) + " >" + " indice" + str(p[2]) + "expressao" + str(p[4]), children = [p[1], p[3]])
    else:
        p[0] = Node("< " + str(id) + " >" + " " +str(p[1]) + "expressao" + str(p[3]), children = [p[2]])
    id+=1

def p_tipo(p):
    '''tipo : INTEIRO
            | FLUTUANTE'''
    global id
    p[0] = Node("< " + str(id) + " > " + p[1])
    id+=1

def p_declaracao_funcao(p):
    '''declaracao_funcao : tipo cabecalho 
                        | cabecalho'''
    global id
    if(len(p) == 3):
        p[0] = Node("< " + str(id) + " >" + " declaracao_funcao", children = [p[1], p[2]])
    else:
        p[0] = Node("< " + str(id) + " >" + " declaracao_funcao", children = [p[1]])
    id+=1

def p_cabecalho(p):
    '''cabecalho : ID ABRE_PARENTESES lista_parametros FECHA_PARENTESES corpo FIM'''
    global id
    p[0] = Node("< " + str(id) + " >" + " cabecalho", children = [p[3], p[5]])
    id+=1

def p_lista_parametros(p):
    '''lista_parametros : lista_parametros VIRGULA parametro
                        | parametro
                        | vazio'''
    global id
    if(len(p) == 4):
        p[0] = Node("< " + str(id) + " >" + " lista_parametros" + p[2] + "parametro", children = [p[1], p[3]])
    else:
        p[0] = Node("< " + str(id) + " >" + " lista_parametros", children = [p[1]])
    id+=1

def p_parametro(p):
    '''parametro : tipo DOIS_PONTOS ID
                |  parametro ABRE_COLCHETE FECHA_COLCHETE'''
    global id
    p[0] = Node("< " + str(id) + " >" + " tipo" + str(p[2]) + str(p[3]), children = [p[1]] )
    id+=1

def p_corpo(p):
    '''corpo : corpo acao 
            | vazio'''
    global id
    if(len(p) == 3):
        p[0] = Node("< " + str(id) + " >" + " corpo", children = [p[1], p[2]])
    else: 
        p[0] = Node("< " + str(id) + " >" + " vazio", children = [p[1]])
    id+=1

def p_acao(p):
    '''acao : expressao
            | declaracao_variaveis
            | se
            | repita
            | leia
            | escreva
            | retorna'''
    global id
    p[0] = Node("< " + str(id) + " >" + " acao", children = [p[1]])
    id+=1

def p_se(p):
    '''se : SE expressao ENTAO corpo FIM
        | SE expressao ENTAO corpo SENAO corpo FIM'''
    global id
    if(len(p) == 6):
        p[0] = Node("< " + str(id) + " >" + " se", children =[p[2], p[4]])
    else:
        p[0] = Node("< " + str(id) + " >" + " se", children =[p[2], p[4], p[6]])
    id+=1

def p_repita(p):
    '''repita : REPITA corpo ATE expressao'''
    global id
    p[0] = Node("< " + str(id) + " >" + " repita", children = [p[2], p[4]])
    id+=1
def p_atribuicao(p):
    '''atribuicao : var ATRIBUICAO expressao'''
    global id
    p[0] = Node("< " + str(id) + " >" + " :=", children = [p[1], p[3]])
    id+=1
def p_leia(p):
    '''leia : LEIA ABRE_PARENTESES var FECHA_PARENTESES'''
    global id
    p[0] = Node("< " + str(id) + " >" + " leia", children = [p[3]])
    id+=1
def p_escreva(p):
    '''escreva : ESCREVA ABRE_PARENTESES expressao FECHA_PARENTESES'''
    global id
    p[0] = Node("< " + str(id) + " >" + " escreva", children = [p[3]])
    id+=1
def p_retorna(p):
    '''retorna : RETORNA ABRE_PARENTESES expressao FECHA_PARENTESES'''
    global id
    p[0] = Node("< " + str(id) + " >" + " retorna", children = [p[3]])
    id+=1

def p_expressao(p):
    '''expressao : expressao_logica
                | atribuicao'''
    global id
    p[0] = Node("< " + str(id) + " >" + " expressao", children = [p[1]])
    id+=1

def p_expressao_logica(p):
    '''expressao_logica : expressao_simples
                        | expressao_logica operador_logico expressao_simples'''

    global id
    if(len(p) == 4):
        p[0] = Node("< " + str(id) + " >" + " expressao_logica", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node("< " + str(id) + " >" + " expressao_logica", children = [p[1]])
    id+=1

def p_expressao_simples(p):
    '''expressao_simples : expressao_aditiva
                        | expressao_simples operador_relacional expressao_aditiva'''
    global id
    if(len(p) == 4):
        p[0] = Node("< " + str(id) + " >" + " expressao_simples", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node("< " + str(id) + " >" + " expressao_simples", children = [p[1]])
    id+=1

def p_expressao_aditiva(p):
    '''expressao_aditiva : expressao_multiplicativa
                        | expressao_aditiva operador_soma expressao_multiplicativa'''
    global id
    if(len(p) == 4):
        p[0] = Node("< " + str(id) + " >" + " expressao_aditiva", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node("< " + str(id) + " >" + " expressao_aditiva", children = [p[1]])
    id+=1

def p_expressao_multiplicativa(p):
    '''expressao_multiplicativa : expressao_unaria
                                | expressao_multiplicativa operador_multiplicacao expressao_unaria'''
    global id
    if(len(p) == 4):
        p[0] = Node("< " + str(id) + " >" + " expressao_multiplicativa", children = [p[1], p[2], p[3]])
    else:
        p[0] = Node("< " + str(id) + " >" + " expressao_multiplicativa", children = [p[1]])
    id+=1

def p_expressao_unaria(p):
    '''expressao_unaria : fator
                        | operador_soma fator
                        | operador_negacao fator'''
    global id
    if(len(p) == 3):
        p[0] = Node("< " + str(id) + " >" + " expressao_unaria", children = [p[1], p[2]])
    else:
        p[0] = Node("< " + str(id) + " >" + " expressao_unaria", children = [p[1]])
    id+=1

def p_operador_relacional(p):
    '''operador_relacional : MENOR
                            | MAIOR 
                            | IGUALDADE 
                            | DIFERENTE 
                            | MENOR_IGUAL 
                            | MAIOR_IGUAL'''
    global id
    p[0] = Node("< " + str(id) + " > " + str(p[1]))
    id+=1

def p_operador_soma(p):
    '''operador_soma : SOMA
                    | SUBTRACAO'''
    global id
    p[0] = Node("< " + str(id) + " > " + str(p[1]))
    id+=1

def p_operador_logico(p):
    '''operador_logico : E_LOGICO
                        | OU_LOGICO'''
    global id
    p[0] = Node("< " + str(id) + " > " + str(p[1]))
    id+=1


def p_operador_negacao(p):
    '''operador_negacao : NEGACAO'''
    global id
    p[0] = Node("< " + str(id) + " > " + str(p[1]))
    id+=1

def p_operador_multiplicacao(p):
    '''operador_multiplicacao : MULTIPLICACAO
                            | DIVISAO'''
    global id
    p[0] = Node("< " + str(id) + " > " + str(p[1]))
    id+=1

def p_fator(p):
    '''fator : ABRE_PARENTESES expressao FECHA_PARENTESES
            | var
            | chamada_funcao
            | numero'''
    global id
    if(len(p) == 4):
        p[0] = Node("< " + str(id) + " >" + " fator", children = [p[2]])
    else:
        p[0] = Node("< " + str(id) + " >" + " fator", children = [p[1]])
    id+=1
    
def p_numero(p):
    '''numero : NUMERO_INTEIRO
            | NUMERO_FLUTUANTE
            | NOTACAO_CIENTIFICA'''
    global id
    p[0] = Node("< " + str(id) + " > " + str(p[1]))
    id+=1

def p_chamada_funcao(p):
    '''chamada_funcao : ID ABRE_PARENTESES lista_argumentos FECHA_PARENTESES'''
    global id
    p[0] = Node("< " + str(id) + " >" + " chamada_funcao", children = [p[3]])
    id+=1

def p_lista_argumentos(p):
    '''lista_argumentos : lista_argumentos VIRGULA expressao
                        | expressao
                        | vazio'''
    global id
    if(len(p) == 4):
        p[0] = Node("< " + str(id) + " >" + " lista_argumentos", children = [p[1], p[3]])
    else:
        p[0] = Node("< " + str(id) + " >" + " lista_argumentos", children = [p[1]])
    id+=1

def p_vazio(p):
    '''vazio : '''
    global id
    p[0] = Node("< " + str(id) + " >" + " None")
    id+=1

def find_column(token):
    input = token.lexer.lexdata
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def p_error(p):
    global error
    if p:
        print("Syntax error at token", p.type, "line: ", p.lineno, "column: ", find_column(p))
        # Just discard the token and tell the parser it's okay.
    else:
        print("Syntax error at EOF")
    error = True

yacc.yacc()

arquivo = open(sys.argv[1])
# lex.lex()

# lex.input(arquivo.read())
data = arquivo.read()
programa = yacc.parse(data)

if(not error):
    DotExporter(programa).to_picture("programa.png")