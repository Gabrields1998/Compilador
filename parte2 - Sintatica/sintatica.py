import sys
import ply.yacc as yacc
import lexica
tokens =  lexica.tokens


def p_programa(p):
    '''programa : lista_declaracoes'''

def p_lista_declaracoes(p):
    '''lista_declaracoes : lista_declaracoes declaracao
                        | declaracao'''

def p_declaracao(p):
    '''declaracao : declaracao_variaveis
            | inicializacao_variaveis
            | declaracao_funcao'''

def p_declaracao_variaveis(p):
    '''declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'''

def p_inicializacao_variaveis(p):
    '''inicializacao_variaveis : atribuicao'''

def p_lista_variaveis(p):
    '''lista_variaveis : lista_variaveis VIRGULA var 
                        | var'''

def p_var(p):
    '''var : ID
            | ID indice'''

def p_indice(p):
    '''indice : indice ABRE_COLCHETE expressao FECHA_COLCHETE
            | ABRE_COLCHETE expressao FECHA_COLCHETE'''

def p_tipo(p):
    '''tipo : INTEIRO
            | FLUTUANTE'''

def p_declaracao_funcao(p):
    '''declaracao_funcao : tipo cabecalho 
                        | cabecalho'''

def p_cabecalho(p):
    '''cabecalho : ID ABRE_PARENTESES lista_parametros FECHA_PARENTESES corpo FIM'''

def p_lista_parametros(p):
    '''lista_parametros : lista_parametros VIRGULA parametro
                        | parametro
                        | vazio'''

def p_parametro(p):
    '''parametro : tipo DOIS_PONTOS ID
                |  parametro ABRE_COLCHETE FECHA_COLCHETE'''

def p_corpo(p):
    '''corpo : corpo acao 
            | vazio'''

def p_acao(p):
    '''acao : expressao
            | declaracao_variaveis
            | se
            | repita
            | leia
            | escreva
            | retorna
            | erro'''

def p_se(p):
    '''se : SE expressao ENTAO corpo FIM
        | SE expressao ENTAO corpo SENAO corpo FIM'''

def p_repita(p):
    '''repita : REPITA corpo ATE expressao'''

def p_atribuicao(p):
    '''atribuicao : var ATRIBUICAO expressao'''

def p_leia(p):
    '''leia : LEIA ABRE_PARENTESES var FECHA_PARENTESES'''

def p_escreva(p):
    '''escreva : ESCREVA ABRE_PARENTESES expressao FECHA_PARENTESES'''

def p_retorna(p):
    '''retorna : RETORNA ABRE_PARENTESES expressao FECHA_PARENTESES'''

def p_expressao(p):
    '''expressao : expressao_logica
                | atribuicao'''

def p_expressao_logica(p):
    '''expressao_logica : expressao_simples
                        | expressao_logica operador_logico expressao_simples'''

def p_expressao_simples(p):
    '''expressao_simples : expressao_aditiva
                        | expressao_simples operador_relacional expressao_aditiva'''

def p_expressao_aditiva(p):
    '''expressao_aditiva : expressao_multiplicativa
                        | expressao_aditiva operador_soma expressao_multiplicativa'''

def p_expressao_multiplicativa(p):
    '''expressao_multiplicativa : expressao_unaria
                                | expressao_multiplicativa operador_multiplicacao expressao_unaria'''

def p_expressao_unaria(p):
    '''expressao_unaria : fator
                        | operador_soma fator
                        | operador_negacao fator'''

def p_operador_relacional(p):
    '''operador_relacional : MENOR
                            | MAIOR 
                            | IGUALDADE 
                            | DIFERENTE 
                            | MENOR_IGUAL 
                            | MAIOR_IGUAL'''

def p_operador_soma(p):
    '''operador_soma : SOMA
                    | SUBTRACAO'''

def p_operador_logico(p):
    '''operador_logico : E_LOGICO
                        | OU_LOGICO'''

def p_operador_negacao(p):
    '''operador_negacao : NEGACAO'''

def p_operador_multiplicacao(p):
    '''operador_multiplicacao : MULTIPLICACAO
                            | DIVISAO'''

def p_fator(p):
    '''fator : ABRE_PARENTESES expressao FECHA_PARENTESES
            | var
            | chamada_funcao
            | numero'''

def p_numero(p):
    '''numero : NUMERO_INTEIRO
            | NUMERO_FLUTUANTE
            | NOTACAO_CIENTIFICA'''

def p_chamada_funcao(p):
    '''chamada_funcao : ID ABRE_PARENTESES lista_argumentos FECHA_PARENTESES'''

def p_lista_argumentos(p):
    '''lista_argumentos : lista_argumentos VIRGULA expressao
                        | expressao
                        | vazio'''

yacc.yacc()
data = "variavel"
yacc.parse(data)