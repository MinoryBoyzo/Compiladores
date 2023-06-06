import ply.lex as lex

reservadas = {
    'for': 'pFor',
    'and': 'pAnd',
    'switch': 'pSwitch',
    'or': 'pOr',
    'false': 'pFalse',
    'true': 'pTrue',
    'return': 'pReturn',
    'super': 'pSuper',
    'else': 'pElse',
    'if': 'pIf',
    'NULL': 'pNull',
    'priny': 'pPrint',
    'fun': 'pFun',
    'number': 'pNumber',
    'this': 'pThis',
    'string': 'pString',
    'while': 'pWhile',
    'class': 'pClass',
    # 'ademas' :'pAdemas',
    'var': 'pVar'
}

tokens = [
             'coma',
             'punto',
             'dosPuntos',
             'llaveA',
             'llaveC',
             'parentesisA',
             'parentesisC',
             'menos',
             'mas',
             'multiplicacion',
             'division',
             'admiracion',
             'diferenteDe',
             'igualA',
             'igualQue',
             'menorQue',
             'mayorQue',
             'menorIgualQue',
             'mayorIgualQue',
             'puntoYComa',
             'id',
             'entero',
         ] + list(reservadas.values())

t_coma = r','
t_punto = r'\.'
t_dosPuntos = r':'
t_llaveA = r'\{'
t_llaveC = r'\}'
t_parentesisA = r'\('
t_parentesisC = r'\)'
t_puntoYComa = r';'
t_menos = r'-'
t_mas = r'\+'
t_multiplicacion = r'\*'
t_division = r'/'
t_admiracion = r'!'
t_diferenteDe = r'!='
t_igualA = r'='
t_igualQue = r'=='
t_menorQue = r'<'
t_mayorQue = r'>'
t_menorIgualQue = r'<='
t_mayorIgualQue = r'>='

t_ignore = " \t"


def t_nuevaLinea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_comentario(t):
    r'//.*'
    pass


def t_id(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'id')
    return t


def t_decimal(t):
    r'(\d*\.\d+)|(\d+\.\d*)'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d" % t.value)
        t.value = 0
    return t


def t_entero(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Interger value too large %d" % t.value)
        t.value = 0
    return t


def t_cadena(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t


def t_error(t):
    print("caracter invalido '%s'" % t.value[0])
    t.lexer.skip(1)


analizador = lex.lex()
archivo = open("archivo.txt", "r")
texto = archivo.read()

analizador.input(texto)

lista_tokens = []
for token in analizador:
    lista_tokens.append(token.type)

archivo.close()

# print(lista_tokens)

# analizador sintáctico:

nLinea = 0
estancia = -1
tokenActual = lista_tokens[estancia]


def match(token_esperado):
    global tokenActual
    global estancia
    if tokenActual == token_esperado:
        estancia += 1
    else:
        error()


def error():
    global nLinea
    print(f"error en linea {nLinea}\n")


# ----------------------------ini prod expression-------------------------------
def EXPRESSION():
    global estancia
    estancia += 1
    ASSIGMENT()


def LOGIC_OR_2():
    global estancia
    if tokenActual == "pOr":
        estancia += 1
        LOGIC_AND()
        LOGIC_OR_2()
    pass


def LOGIC_AND():
    EQUALITY()
    LOGIC_AND_2()


def LOGIC_AND_2():
    global estancia
    if tokenActual == "pAnd":
        estancia += 1
        EQUALITY()
        LOGIC_AND_2()
    pass


def EQUALITY():
    COMPARISON()
    EQUALITY_2()


def EQUALITY_2():
    global estancia
    if tokenActual == "equalEqual" or tokenActual == "notEqual":
        estancia += 1
        COMPARISON()
        EQUALITY_2()
    pass


def COMPARISON_2():
    global estancia
    if tokenActual == "greaterThan" or tokenActual == "lessThan" or tokenActual == "greaterEqual" or tokenActual == "lessEqual":
        estancia += 1
        TERM()
        COMPARISON_2()
    pass


def TERM():
    FACTOR()
    TERM_2()


def TERM_2():
    global estancia
    if tokenActual == "minus" or tokenActual == "plus":
        estancia += 1
        FACTOR()
        TERM_2()
    pass


def FACTOR_2():
    global estancia
    if tokenActual == "divide" or tokenActual == "multiply":
        estancia += 1
        UNARY()
        FACTOR_2()


def UNARY():
    global estancia
    if tokenActual == "exclamation" or tokenActual == "minus":
        estancia += 1
        UNARY()
        FACTOR()
    pass


def CALL():
    PRIMARY()
    CALL_2()


def CALL_2():
    global estancia
    if tokenActual == "lparen":
        estancia += 1
        ARGUMENTS_OPC()
        match("rparen")
        CALL_2()
    elif tokenActual == "dot":
        estancia += 1
        match("id")
        CALL_2()
    pass


def PRIMARY():
    global estancia
    if tokenActual == "pTrue" or tokenActual == "pFalse" or tokenActual == "id" or tokenActual == "integer" or tokenActual == "decimal" or tokenActual == "pSuper" or tokenActual == "pNull" or tokenActual == "pThis":
        estancia += 1
    elif tokenActual == "lparen":
        estancia += 1
        EXPRESSION()
        match("rparen")
    else:
        error()


def FACTOR():
    UNARY()
    FACTOR_2()


def COMPARISON():
    TERM()
    COMPARISON_2()


def LOGIC_OR():
    LOGIC_AND()
    LOGIC_OR_2()


def ASSIGMENT():
    LOGIC_OR()
    ASSIGMENT_OPC()


def ASSIGMENT_OPC():
    global estancia
    if tokenActual == "equal":
        estancia += 1
        EXPRESSION()
    pass


# ----------------------------fin prod expression-------------------------------
# --------------------------ini prod declaration--------------------
def CLASS_INHER():
    global estancia
    global nLinea
    nLinea += 1
    if tokenActual == "lessThan":
        estancia += 1
        if tokenActual == "id":
            estancia += 1
            print(f"linea {nLinea} aceptada\n")
            parse_DECLARATION()
        else:
            error()


def CLAS_DECL():
    global estancia
    if tokenActual == "id":
        estancia += 1
        CLASS_INHER()


def VAR_INIT():
    EXPRESSION()


def parse_DECLARATION():
    global estancia
    if tokenActual == "pClass":
        estancia += 1
        CLAS_DECL()
        estancia += 1
    elif tokenActual == "fun":
        estancia += 1
        FUNCTION()
    elif tokenActual == "pVar":
        estancia += 1
        VAR_DECL()
    else:
        parse_STATEMENT()


def VAR_DECL():
    global estancia
    if tokenActual == "id":
        estancia += 1
        VAR_INIT()


# -------------------------fin prod declaration-------------------
# ----------------------------ini prod statement------------------
def parse_STATEMENT():
    global estancia
    global nLinea
    if tokenActual == "pFor":
        estancia += 1
        nLinea += 1
        FOR_STMT()
    elif tokenActual == "pTrue" or tokenActual == "pFalse" or tokenActual == "id" or tokenActual == "lparen" or tokenActual == "integer" or tokenActual == "decimal" or tokenActual == "pSuper" or tokenActual == "pNull" or tokenActual == "pThis":
        estancia += 1
        nLinea += 1
        EXPR_STMT()
    elif tokenActual == "pIf":
        estancia += 1
        nLinea += 1
        IF_STMT()
    elif tokenActual == "pPrint":
        estancia += 1
        nLinea += 1
        PRINT_STMT()
    elif tokenActual == "pReturn":
        estancia += 1
        nLinea += 1
        RETURN_STMT()
    elif tokenActual == "pWhile":
        estancia += 1
        nLinea += 1
        WHILE_STMT()
    elif tokenActual == "lbrace":
        estancia += 1
        nLinea += 1
        BLOCK()
    else:
        EXPRESSION()


def PRINT_STMT():
    EXPRESSION()
    match("semicolon")


def RETURN_STMT():
    RETURN_EXP_OPC()
    match("semicolon")


def RETURN_EXP_OPC():
    EXPRESSION()


def WHILE_STMT():
    global estancia
    if tokenActual == "lparen":
        estancia += 1
        EXPRESSION()
        match("rparen")
        parse_STATEMENT()
    else:
        error()


def ELSE_STATEMENT():
    global estancia
    if tokenActual == "pElse":
        estancia += 1
        parse_STATEMENT()
    pass


def IF_STMT():
    global estancia
    if tokenActual == "lparen":
        estancia += 1
        EXPRESSION()
        match("rparen")
        parse_STATEMENT()
        ELSE_STATEMENT()
    else:
        error()


def EXPR_STMT():
    EXPRESSION()
    match("semicolon")


def BLOCK():
    BLOCK_DECL()
    match("rbrace")


def BLOCK_DECL():
    parse_STATEMENT()


def FOR_STMT():
    if tokenActual == "lparen":
        global estancia
        estancia += 1
        FOR_STMT_1()
        FOR_STMT_2()
        FOR_STMT_3()
        if tokenActual == "rparen":
            parse_STATEMENT()
        else:
            error()
    else:
        error()


def FOR_STMT_1():
    global estancia
    if tokenActual == "pVar":
        estancia += 1
        VAR_DECL()
    elif tokenActual == "equal":
        estancia += 1
        VAR_INIT()
    elif tokenActual == "semicolon":
        print("linea aceptada")


def FOR_STMT_2():
    if tokenActual != "semicolon":
        EXPRESSION()
        match("semicolon")


def FOR_STMT_3():
    EXPRESSION()


# -------------------------------------ini prod otras----------------------------------------
def FUNCTION():
    if tokenActual == "id":
        global estancia
        estancia += 1
        if tokenActual == "lparen":
            estancia += 1
            PARAMETERS_OPC()
            match("rparen")
            BLOCK()


def FUNCTIONS():
    FUNCTION()
    FUNCTIONS()


def PARAMETERS_OPC():
    PARAMETERS()


def PARAMETERS():
    if tokenActual == "id":
        global estancia
        estancia += 1
        PARAMETERS_2()
    else:
        error()


def PARAMETERS_2():
    if tokenActual == "comma":
        match("id")
        PARAMETERS_2()
    pass


def ARGUMENTS_OPC():
    ARGUMENTS()


def ARGUMENTS():
    EXPRESSION()
    ARGUMENTS_2()


def ARGUMENTS_2():
    if tokenActual == "comma":
        EXPRESSION()
        ARGUMENTS_2()
    pass


# ---------------------------inicio---------------------------
parse_DECLARATION()
if(parse_DECLARATION()== -1):
    print("hay errores sintacticos")
else:
    print("archivo aceptado")