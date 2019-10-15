import sys
import ply.lex as lex

reserved = {
    'se': 'SE',
    'então': 'ENTAO',
    'senão': 'SENAO',
    'fim': 'FIM',
    'repita': 'REPITA',
    'flutuante': 'FLUTUANTE',
    'retorna': 'RETORNA',
    'até': 'ATE',
    'leia': 'LEIA',
    'escreva': 'ESCREVA',
    'inteiro': 'INTEIRO'
}

tokens = [
    'SOMA',
    'SUBTRACAO',
    'MULTIPLICACAO',
    'DIVISAO',
    'IGUALDADE',
    'VIRGULA',
    'ATRIBUICAO',
    'MENOR',
    'MAIOR',
    'MENOR_IGUAL',
    'MAIOR_IGUAL',
    'ABRE_PARENTESES',
    'FECHA_PARENTESES',
    'DOIS_PONTOS',
    'ABRE_COLCHETE',
    'FECHA_COLCHETE',
    'E_LOGICO',
    'OU_LOGICO',
    'NEGACAO',
    'DIFERENTE',
    'NOTACAO_CIENTIFICA',
    'ID',
    'NUMERO_INTEIRO',
    'NUMERO_FLUTUANTE'
] + list(reserved.values())

t_ignore = ' \t'
t_SOMA = r'\+'
t_SUBTRACAO = r'-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'/'
t_IGUALDADE = r'='
t_VIRGULA = r','
t_ATRIBUICAO = r':='
t_MENOR = r'<'
t_MAIOR = r'>'
t_MENOR_IGUAL = r'<='
t_MAIOR_IGUAL = r'>='
t_ABRE_PARENTESES = r'\('
t_FECHA_PARENTESES = r'\)'
t_DOIS_PONTOS = r':'
t_ABRE_COLCHETE = r'\['
t_FECHA_COLCHETE= r'\]'
t_E_LOGICO = r'&&'
t_OU_LOGICO = r'\|\|'
t_NEGACAO = r'!'
t_DIFERENTE = r'<>'
t_NOTACAO_CIENTIFICA = r'((\+|-)?[\d+]+\.?[\d+]*)(e|E)(\+|-)?[\d+]+'
t_NUMERO_FLUTUANTE = r'(\+|-)?[\d+]+\.[\d+]*'
t_NUMERO_INTEIRO = r'(-|\+)?\d+'

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    print('Illegal character: %s' % t.value[0])
    t.lexer.skip(1)

def t_COMMENT(t):
    r'\{((.|\n)*?)\}'
    t.lexer.lineno += len(t.value.split('\n')) - 1

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# arquivo = open(sys.argv[1])
lex.lex()

# lex.input(arquivo.read())
# while True:
#     tok =  lex.token()
#     if not tok: break
#     if(len(sys.argv) >= 3):
#         if(sys.argv[2] == "C"):
#             print(tok.type,",", tok.value)
#         elif(sys.argv[2] == "S"):
#             print(tok.type)
#     else:
#         print(tok.type,",", tok.value)