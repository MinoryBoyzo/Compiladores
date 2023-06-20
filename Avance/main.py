import sys
import os


def convCadena(cadena):
    newPala = []
    for c in cadena:
        if c != "\"":
            newPala += c
    return "".join(newPala)


def compfloat(cadena):
    for c in cadena:
        if c == '.':
            return True
    return False


def reservadas(cadena):
    palabrasHM = {'for': 'FOR', 'fun': 'FUN', 'false': 'FALSE', 'if': 'IF', 'print': 'PRINT', 'return': 'RETURN',
                  'true': 'TRUE', 'var': 'VAR', 'else': 'ELSE', 'or': 'OR', 'null': 'NULL', 'try': 'TRY',
                  'not': 'NOT', 'break': 'BREAK', 'and': 'AND', 'identificador': 'ID', 'float': 'FLOAT',
                  'int': 'INT', 'string': 'STRING', '=': '=', 'while': 'WHILE',
                  '+': '+', '-': '-', '/': '/', '': '', '+=': '+=',
                  '<=': '<=', '>=': '>=', '==': '==', '!=': '!=', '<': '<', '>': '>',
                  '-=': '-=', '{': '{', '}': '}', '[': '[', ']': ']',
                  '(': '(', ')': ')', ';': ';', '.': '.', ',': ',',
                  'class': 'CLASS', 'this': 'THIS', 'super': 'SUPER'}
    if cadena in palabrasHM:
        return palabrasHM[cadena]
    else:
        return False


def palabraReservada(cadena):
    tokens = []
    for cad in cadena:
        if (reservadas(cad)) != False:
            tokens.append(reservadas(cad))
        elif (letras(cad[0])):
            tokens.append(reservadas('identificador'))
        elif (numeros(cad[0]) or cad[0] == '.'):
            if (compfloat(cad)):
                tokens.append(reservadas('float'))
            else:
                tokens.append(reservadas('int'))
        elif (comillas(cad[0])):
            if (len(cad) > 2):
                tokens.append(reservadas('string'))
            else:
                tokens.append(reservadas(cad))
        else:
            tokens.append(reservadas(cad))

    tokens.append('EOF')

    return tokens


def comillas(caracter):
    return caracter in "\""


def simbolicos(caracter):
    return caracter in "(){}[],.:;-+*/!=<>%&"


def espacios(caracter):
    return caracter in " \n\t"


def letras(caracter):
    return caracter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX_"


def numeros(caracter):
    return caracter in "1234567890"


def operadores(caracter):
    return caracter in ["!=", "==", "<=", ">="]


def operaciones(caracter):
    return caracter in "/=+-*"


def llaves(caracter):
    return caracter in "{[()]}"


def compnum(cadena):
    validar = True
    for n in cadena:
        if numeros(n) == False:
            validar = False
    return validar


def sepa(cadena):
    estado = 0
    tokens = []
    tokenaux = []
    listado = []
    for c in cadena:
        if letras(c) and estado == 0:
            estado = 1
            tokenaux += c
        elif numeros(c) and estado == 0:
            estado = 2
            tokenaux += c
        elif comillas(c) and estado == 0:
            estado = 3
            tokenaux += c
        elif simbolicos(c) and estado == 0:
            tokens += c
        elif espacios(c) and estado == 0:
            tokens += c
        elif (letras(c) or numeros(c)) and estado == 1:
            tokenaux += c
        elif comillas(c) and estado == 1:
            estado = 3
            tokens.append("".join(tokenaux))
            tokenaux.clear()
            tokenaux += c
        elif simbolicos(c) and estado == 1:
            estado = 0
            tokens.append("".join(tokenaux))
            tokens += c
            tokenaux.clear()
        elif espacios(c) and estado == 1:
            estado = 0
            tokens.append("".join(tokenaux))
            tokens += c
            tokenaux.clear()
        elif numeros(c) and estado == 2:
            tokenaux += c
        elif comillas(c) and estado == 2:
            estado = 3
            tokens.append("".join(tokenaux))
            tokenaux.clear()
            tokenaux += c
        elif simbolicos(c) and estado == 2:
            estado = 0
            tokens.append("".join(tokenaux))
            tokens += c
            tokenaux.clear()
        elif espacios(c) and estado == 2:
            estado = 0
            tokens.append("".join(tokenaux))
            tokens += c
            tokenaux.clear()
        elif letras(c) and estado == 2:
            estado = 1
            tokens.append("".join(tokenaux))
            tokenaux.clear()
            tokenaux += c
        elif not (comillas(c)) and estado == 3:
            tokenaux += c
        elif comillas(c) and estado == 3:
            estado = 0
            tokenaux += c
            tokens.append("".join(tokenaux))
            tokenaux.clear()
    if estado == 3:
        print("Cadena no terminanda")
        sys.exit(1)
    if estado == 2 or estado == 1:
        tokens.append("".join(tokenaux))
        tokenaux.clear()
    tokenaux.clear()

    for i in range(len(tokens)):
        try:
            if (tokens[i] in "!=+-<>") and tokens[i + 1] == "=":
                tokenaux += tokens[i]
                tokenaux += tokens[i + 1]
                tokens[i] = "".join(tokenaux)
                tokens[i + 1] = ""
                listado.append(i + 1)
                tokenaux.clear()
        except IndexError:
            pass
    tokenaux.clear()

    compru = 0
    for i in range(len(tokens)):
        try:
            if compru != 0:
                compru -= 1
            elif compnum(tokens[i]) and tokens[i + 1] == "." and compnum(tokens[i + 2]):
                tokenaux += tokens[i]
                tokenaux += tokens[i + 1]
                tokenaux += tokens[i + 2]
                tokens[i] = "".join(tokenaux)
                tokens[i + 1] = ""
                tokens[i + 2] = ""
                listado.append(i + 1)
                listado.append(i + 2)
                compru = 2
                tokenaux.clear()
            elif tokens[i] == "." and compnum(tokens[i + 1]):
                tokenaux += tokens[i]
                tokenaux += tokens[i + 1]
                tokens[i] = "".join(tokenaux)
                tokens[i + 1] = ""
                listado.append(i + 1)
                compru = 1
                tokenaux.clear()
            elif compnum(tokens[i]) and tokens[i + 1] == '.':
                tokenaux += tokens[i]
                tokenaux += tokens[i + 1]
                tokens[i] = "".join(tokenaux)
                tokens[i + 1] = ""
                listado.append(i + 1)
                compru = 1
                tokenaux.clear()

        except IndexError:
            if (i + 2) > len(tokens):
                compru = 0
            elif tokens[i] == "." and compnum(tokens[i + 1]):
                tokenaux += tokens[i]
                tokenaux += tokens[i + 1]
                tokens[i] = "".join(tokenaux)
                tokens[i + 1] = ""
                listado.append(i + 1)
                compru = 1
                tokenaux.clear()
            elif compnum(tokens[i]) and tokens[i + 1] == '.':
                tokenaux += tokens[i]
                tokenaux += tokens[i + 1]
                tokens[i] = "".join(tokenaux)
                tokens[i + 1] = ""
                listado.append(i + 1)
                compru = 1
                tokenaux.clear()

    tokenaux.clear()
    listado.sort()
    cont = 0
    for num in listado:
        num -= cont
        tokens.pop(num)
        cont += 1

    cont = 0
    for i in range(len(tokens)):
        if tokens[i] == ' ':
            cont += 1
    for j in range(cont):
        tokens.remove(' ')

    cont = 0
    for i in range(len(tokens)):
        if tokens[i] == '\t':
            cont += 1
    for j in range(cont):
        tokens.remove(' \t')

    cont = 0
    for i in range(len(tokens)):
        if tokens[i] == '\n':
            cont += 1
    for j in range(cont):
        tokens.remove('\n')

    return tokens


def remove(cadena):
    estado = 0
    cad = []
    for c in cadena:
        # estado 0
        if estado == 0 and c == '/':
            estado = 1
            cad += c
        elif estado == 0 and c != '/':
            cad += c
        # estado 1
        elif estado == 1 and c == '/':
            estado = 2
            cad.pop()
        elif estado == 1 and c == '*':
            estado = 3
            cad.pop()
        elif estado == 1 and c != '/':
            estado = 0
            cad += c
        # estado 2
        elif estado == 2 and c == '\n':
            estado = 0
        # estado 3
        elif estado == 3 and c == '*':
            estado = 4
        # estado 4
        elif estado == 4 and c == '*':
            estado = 4
        elif estado == 4 and c == '/':
            estado = 0
        elif estado == 4 and c != '/':
            estado = 3
    return cad


estancia = 0


def error():
    print("Error sintactico ")
    print(tokenActual[estancia])
    sys.exit(1)


def program():
    global estancia
    declaration()
    if tokenActual[estancia] == 'EOF':
        print("cadena aceptada")
    else:
        print("Error de cadena")


# parserDeclaration
def declaration():
    if class_decl():
        declaration()
    elif fun_decl():
        declaration()
    elif var_decl():
        declaration()
    elif statement():
        declaration()
    else:
        pass


def class_decl():
    global estancia
    if tokenActual[estancia] == 'CLASS':
        estancia += 1
        if tokenActual[estancia] == 'ID':
            estancia += 1
            if class_inher():
                if tokenActual[estancia] == '{':
                    estancia += 1
                    if functions():
                        if tokenActual[estancia] == '}':
                            estancia += 1
                            return True
                        else:
                            error()
                    else:
                        error()
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        return False


def class_inher():
    global estancia
    if tokenActual[estancia] == '<':
        estancia += 1
        if tokenActual[estancia] == 'ID':
            estancia += 1
            return True
        else:
            error()
    else:
        return True


def fun_decl():
    global estancia
    if tokenActual[estancia] == 'FUN':
        estancia += 1
        if funct(): return True
    else:
        return False


def var_decl():
    global estancia
    if tokenActual[estancia] == 'VAR':
        estancia += 1
        if tokenActual[estancia] == 'ID':
            estancia += 1
            if var_init():
                if tokenActual[estancia] == ';':
                    estancia += 1
                    return True
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        return False


def var_init():
    global estancia
    if tokenActual[estancia] == '=':
        estancia += 1
        if expression():
            return True
    else:
        return True


# parsesStatement
def statement():
    global estancia
    if expr_stmt():
        return True
    elif for_stmt():
        return True
    elif if_stmt():
        return True
    elif print_stmt():
        return True
    elif return_stmt():
        return True
    elif while_stmt():
        return True
    elif block():
        return True
    else:
        return False


def expr_stmt():
    global estancia
    if expression():
        if tokenActual[estancia] == ';':
            estancia += 1
            return True
        else:
            error()
    else:
        return False


def for_stmt():
    global estancia
    if tokenActual[estancia] == 'FOR':
        estancia += 1
        if tokenActual[estancia] == '(':
            estancia += 1
            if for_stmt_1():
                if for_stmt_2():
                    if for_stmt_3():
                        if tokenActual[estancia] == ')':
                            estancia += 1
                            if statement():
                                return True
                            else:
                                error()
                        else:
                            error()
                    else:
                        error()
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        return False


def for_stmt_1():
    global estancia
    if var_decl():
        return True
    elif expr_stmt():
        return True
    elif tokenActual[estancia] == ';':
        estancia += 1
        return True
    else:
        return False


def for_stmt_2():
    global estancia
    if expression():
        if tokenActual[estancia] == ';':
            estancia += 1
            return True
        else:
            error()
    elif tokenActual[estancia] == ';':
        estancia += 1
        return True
    else:
        return False


def for_stmt_3():
    global estancia
    if expression():
        return True
    else:
        return True


def if_stmt():
    global estancia
    if tokenActual[estancia] == 'IF':
        estancia += 1
        if tokenActual[estancia] == '(':
            estancia += 1
            if expression():
                if tokenActual[estancia] == ')':
                    estancia += 1
                    if statement():
                        if else_statement():
                            return True
                        else:
                            error()
                    else:
                        error()
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        return False


def else_statement():
    global estancia
    if tokenActual[estancia] == 'ELSE':
        estancia += 1
        if statement():
            return True
        else:
            error()
    else:
        return True


def print_stmt():
    global estancia
    if tokenActual[estancia] == 'PRINT':
        estancia += 1
        if expression():
            if tokenActual[estancia] == ';':
                estancia += 1
                return True
            else:
                error()
        else:
            error()
    else:
        return False


def return_stmt():
    global estancia
    if tokenActual[estancia] == 'RETURN':
        estancia += 1
        if return_exp_opc():
            if tokenActual[estancia] == ';':
                estancia += 1
                return True
            else:
                error()
        else:
            error()
    else:
        return False


def return_exp_opc():
    global estancia
    if expression():
        return True
    else:
        return True


def while_stmt():
    global estancia
    if tokenActual[estancia] == 'WHILE':
        estancia += 1
        if tokenActual[estancia] == '(':
            estancia += 1
            if expression():
                if tokenActual[estancia] == ')':
                    estancia += 1
                    if statement():
                        return True
                    else:
                        error()
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        return False


def block():
    global estancia
    if tokenActual[estancia] == '{':
        estancia += 1
        if block_decl():
            if tokenActual[estancia] == '}':
                estancia += 1
                return True
            else:
                error()
        else:
            error()
    else:
        return False


def block_decl():
    global estancia
    if declaration():
        if block_decl():
            return True
        else:
            error()
    else:
        return True


# EXPRESSION
def expression():
    global estancia
    if assignment():
        return True
    else:
        return False


def assignment():
    global estancia
    if logic_or():
        if assignment_opc():
            return True
        else:
            error()
    else:
        return False


def assignment_opc():
    global estancia
    if tokenActual[estancia] == '=':
        estancia += 1
        if expression():
            return True
        else:
            error()
    else:
        return True


def logic_or():
    global estancia
    if logic_and():
        if logic_or_2():
            return True
        else:
            error()
    else:
        return False


def logic_or_2():
    global estancia
    if tokenActual[estancia] == 'OR':
        estancia += 1
        if logic_and():
            if logic_or_2():
                return True
            else:
                error()
        else:
            error()
    else:
        return True


def logic_and():
    global estancia
    if equality():
        if logic_and_2():
            return True
        else:
            error()
    else:
        return False


def logic_and_2():
    global estancia
    if tokenActual[estancia] == 'AND':
        estancia += 1
        if equality():
            if logic_and_2():
                return True
            else:
                error()
        else:
            error()
    else:
        return True


def equality():
    global estancia
    if comparison():
        if equality_2():
            return True
        else:
            error()
    else:
        return False


def equality_2():
    global estancia
    if tokenActual[estancia] == '!=':
        estancia += 1
        if comparison():
            if equality_2():
                return True
            else:
                error()
        else:
            error()
    elif tokenActual[estancia] == '==':
        estancia += 1
        if comparison():
            if equality_2():
                return True
            else:
                error()
        else:
            error()
    else:
        return True


def comparison():
    global estancia
    if term():
        if comparison_2():
            return True
        else:
            error()
    else:
        return False


def comparison_2():
    global estancia
    if tokenActual[estancia] == '>':
        estancia += 1
        if term():
            if comparison_2():
                return True
            else:
                error()
        else:
            error()
    elif tokenActual[estancia] == '>=':
        estancia += 1
        if term():
            if comparison_2():
                return True
            else:
                error()
        else:
            error()
    elif tokenActual[estancia] == '<':
        estancia += 1
        if term():
            if comparison_2():
                return True
            else:
                error()
        else:
            error()
    elif tokenActual[estancia] == '<=':
        estancia += 1
        if term():
            if comparison_2():
                return True
            else:
                error()
        else:
            error()
    else:
        return True


def term():
    global estancia
    if factor():
        if term_2():
            return True
        else:
            error()
    else:
        return False


def term_2():
    global estancia
    if tokenActual[estancia] == '-':
        estancia += 1
        if factor():
            if term_2():
                return True
            else:
                error()
        else:
            error()
    elif tokenActual[estancia] == '+':
        estancia += 1
        if factor():
            if term_2():
                return True
            else:
                error()
        else:
            error()
    else:
        return True


def factor():
    global estancia
    if unary():
        if factor_2():
            return True
        else:
            error()
    else:
        return False


def factor_2():
    global estancia
    if tokenActual[estancia] == '/':
        estancia += 1
        if unary():
            if factor_2():
                return True
            else:
                error()
        else:
            error()
    elif tokenActual[estancia] == '*':
        estancia += 1
        if unary():
            if factor_2():
                return True
            else:
                error()
        else:
            error()
    else:
        return True


def unary():
    global estancia
    if tokenActual[estancia] == '!':
        estancia += 1
        if unary():
            return True
        else:
            error()
    elif tokenActual[estancia] == '-':
        estancia += 1
        if unary():
            return True
        else:
            error()
    elif call():
        return True
    else:
        return False


def call():
    global estancia
    if primary():
        if call_2():
            return True
        else:
            error()
    else:
        return False


def call_2():
    global estancia
    if tokenActual[estancia] == '(':
        estancia += 1
        if arguments_opc():
            if tokenActual[estancia] == ')':
                estancia += 1
                if call_2():
                    return True
                else:
                    error()
            else:
                error()
        else:
            error()
    elif tokenActual[estancia] == '.':
        estancia += 1
        if tokenActual[estancia] == 'ID':
            estancia += 1
            if call_2():
                return True
            else:
                error()
        else:
            error()
    else:
        return True


def call_opc():
    global estancia


def primary():
    global estancia
    if tokenActual[estancia] == 'TRUE':
        estancia += 1
        return True
    elif tokenActual[estancia] == 'FALSE':
        estancia += 1
        return True
    elif tokenActual[estancia] == 'NULL':
        estancia += 1
        return True
    elif tokenActual[estancia] == 'THIS':
        estancia += 1
        return True
    elif tokenActual[estancia] == 'INT':
        estancia += 1
        return True
    elif tokenActual[estancia] == 'FLOAT':
        estancia += 1
        return True
    elif tokenActual[estancia] == 'STRING':
        estancia += 1
        return True
    elif tokenActual[estancia] == 'ID':
        estancia += 1
        return True
    elif tokenActual[estancia] == '(':
        estancia += 1
        if expression():
            if tokenActual[estancia] == ')':
                estancia += 1
                return True
            else:
                error()
        else:
            error()
    elif tokenActual[estancia] == 'SUPER':
        estancia += 1
        if tokenActual[estancia] == '.':
            estancia += 1
            if tokenActual[estancia] == 'ID':
                estancia += 1
                return True
            else:
                error()
        else:
            error()
    else:
        return False


# Otras----------------------------------------------------
def funct():
    global estancia
    if tokenActual[estancia] == 'ID':
        estancia += 1
        if tokenActual[estancia] == '(':
            estancia += 1
            if parameters_opc():
                if tokenActual[estancia] == ')':
                    estancia += 1
                    if block():
                        return True
                    else:
                        error()
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        return False


def functions():
    global estancia
    if funct():
        if functions():
            return True
        else:
            error()
    else:
        return True


def parameters_opc():
    global estancia
    if parameters():
        return True
    else:
        return True


def parameters():
    global estancia
    if tokenActual[estancia] == 'ID':
        estancia += 1
        if parameters_2():
            return True
        else:
            error()
    else:
        False


def parameters_2():
    global estancia
    if tokenActual[estancia] == ',':
        estancia += 1
        if tokenActual[estancia] == 'ID':
            estancia += 1
            if parameters_2():
                return True
            else:
                error()
        else:
            error()
    else:
        return True


def arguments_opc():
    global estancia
    if arguments():
        return True
    else:
        return True


def arguments():
    global estancia
    if expression():
        if arguments_2():
            return True
        else:
            error()
    else:
        False


def arguments_2():
    global estancia
    if tokenActual[estancia] == ',':
        estancia += 1
        if expression():
            if arguments_2():
                return True
            else:
                error()
        else:
            error()
    else:
        return True


def lexico(cadena):
    cad = remove(cadena)
    global globalLex
    globalLex = sepa(cad)
    global tokenActual
    tokenActual = palabraReservada(globalLex)

    program()


def transforma(archivo):
    if not os.path.exists(archivo):
        return False
    arch = open(archivo, "r")
    cadena = []
    for linea in arch:
        for c in linea:
            cadena += c
    arch.close()
    return cadena


if len(sys.argv) == 2:
    cadena = transforma(sys.argv[1])
    if (not cadena):
        print("Error al leer el archivo.")
    else:
        lexico(cadena)
elif len(sys.argv) == 1:
    print("Seleccione la opción deseada \n1.Leer archivo txt\n2.Ingresar manualmente la cadena")
    varOpcion = input('Opción: ')
    cadena = []
    if varOpcion == '1':
        archivo = open("archivo.txt", "r")
        texto = archivo.read()
        cadena = texto
    else:
        print("Para terminar esciba 'ok'")
        while True:
            escrito = input('>>')
            if escrito != 'ok':
                cadena += escrito + '\n'
            else:
                break
    lexico(cadena)

else:
    print("Error de ejecución")
