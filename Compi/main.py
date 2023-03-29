import os

_NOMBRE_ARCHIVO = os.getcwd() + "/Prueba.c"

tipos_variables = [
    'INT',
    'FLOAT',
    'CHAR'
]
tipos_bucles = [
    'DO',
    'WHILE',
    'FOR',
    'SWITCH',
    'CASE',
    'IF',
    'ELSE',
    'BREAK',
]
tipos_acciones= [
    'PRINTF',
    'SCANF',
    'MAIN',
    'RETURN',
]
simb = [
    '(',
    ')',
    '{',
    '}',
    '[',
    ']',
    '"',
    ','
]
relaciones = [
    '>',
    '<',
    '=',
    '!',
    ';'
]
operaciones = [
    '+',
    '*',
    '/',
    '-',
    '%'
]
tokens = []
with open(_NOMBRE_ARCHIVO, 'r') as file:
    cont = file.read() + " \0"

    def sigToken():
        etapa = 0
        contador = -1
        c = None
        pal = ''
        ascii = 0
        linea = 1

        if contador >= len(cont) - 2:
            tokens.append("(Fin del archivo, EOF)")

        while contador < len(cont) - 1:

            contador += 1
            c = cont[contador]
            ascii = ord(c.upper())
            if ascii == 13:
                linea += 1
            if etapa == 0:
                if c in relaciones:
                    if c == '<':
                        etapa = 1
                    elif c == '=':
                        etapa = 5
                    elif c == '>':
                        etapa = 6
                    elif c == '!':
                        etapa = 40
                    elif c == ';':
                        etapa = 41
                    pal += c
                elif ascii > 64 and ascii < 91:
                    pal += c
                    etapa = 10
                elif c.isdigit():
                    pal += c
                    etapa = 13
                elif c in simb:
                    etapa = 22
                    contador -= 1
                elif c in operaciones:
                    etapa = 23
                    contador-=1
                else:
                    if 8 <= ord(c) <= 15 or ord(c) == 32:
                        etapa = 0
                    else:
                        etapa = 0
            elif etapa == 1:
                c = cont[contador + 1]
                ascii = ord(c.upper())
                if c == '>':
                    pal += c
                    etapa = 3
                    contador += 1
                elif c == '=':
                    pal += c
                    etapa = 2
                    contador += 1
                else:
                    etapa = 4
                    pass
            elif etapa == 2:
                pal = ''
                tokens.append( "(MENOR_O_IGUAL, <=)")
                etapa = 0
                pass
            elif etapa == 3:
                pal = ''
                tokens.append( "(DIFERENTE, <>)")
                etapa = 0
                pass
            elif etapa == 4:
                pal = ''
                tokens.append( "(MENOR, <)")
                etapa = 0
                pass
            elif etapa == 5:
                pal = ''
                tokens.append( "(IGUAL, =)")
                etapa = 0
                pass
            elif etapa == 40:
                pal = ''
                tokens.append( "(DIFERENTE, !)")
                etapa = 0
                pass
            elif etapa == 41:
                pal = ''
                tokens.append("(FIN DE LINEA, ;)")
                etapa = 0
                pass
            elif etapa == 6:
                if c == '=':
                    pal += c
                    etapa = 7
                else:
                    etapa = 8
                pass
            elif etapa == 7:
                pal = ''
                tokens.append( "(MAYOR_O_IGUAL, >=)")
                etapa = 0
                pass
            elif etapa == 8:
                pal = ''
                tokens.append( "(MAYOR, >)")
                etapa = 0
                pass
            elif etapa == 9:
                pass
            elif etapa == 10:
                ascii = ord(c.upper())
                if (ascii > 64 and ascii < 91) or (ascii > 47 and ascii < 58):
                    pal += c
                    etapa = 10
                else:
                    contador -= 1
                    etapa = 11
                pass
            elif etapa == 11:
                con = pal
                pal = ''
                if con.upper() in tipos_variables:
                    tokens.append( "(TIPO DE VARIABLE, " + con + ")")
                    etapa = 0
                    contador -= 1
                elif con.upper() in tipos_bucles:
                    tokens.append( "(PALABRA BUCLE, " + con + ")")
                    etapa = 0
                    contador -= 1
                elif con.upper() in tipos_acciones:
                    tokens.append( "(ACCION RESERVADA, " + con + ")")
                    etapa = 0
                    contador -= 1
                else:
                    tokens.append("(NOMBRE_VARIABLE, " + con + ")")
                    etapa = 0
                    contador -= 1

                pass
            elif etapa == 12:
                pass
            elif etapa == 13:
                if c.isdigit():
                    pal += c
                elif c == '.':
                    pal += c
                    etapa = 14
                elif c == ' ':
                    etapa = 20
                elif ord(c) == 13:
                    linea += 1
                    etapa = 20
                else:
                    contador -= 1
                    etapa = 20
                contador -= 1
                pass
            elif etapa == 14:
                if c.isdigit():
                    pal += c
                    etapa = 15
                else:
                    etapa = 0
                pass
            elif etapa == 15:
                if c.isdigit():
                    pal += c
                elif c == ' ':
                    etapa = 21
                elif ord(c) == 13:
                    linea += 1
                    etapa = 21
                else:
                    contador -= 1
                    etapa = 20
                pass
            elif etapa == 16:
                if c == '+' or c == '-':
                    pal += c
                    etapa = 17
                elif c.isdigit():
                    pal += c
                    etapa = 18
                pass
            elif etapa == 17:
                if c.isdigit():
                    pal += c
                    etapa = 18
                else:
                    etapa = 0
                pass
            elif etapa == 18:
                if c.isdigit():
                    pal += c
                elif ord(c) == 13:
                    linea += 1
                    etapa = 19
                else:
                    etapa = 20
                    contador -= 1
                pass
            elif etapa == 19 or etapa == 20 or etapa == 21:
                send = pal
                pal = ''
                tokens.append(f"(VALOR, {send})")
                etapa = 0
                pass
            elif etapa == 22:
                etapa = 0
                if c == '(':
                    tokens.append("(APERTURA PARENTESIS,'" + c + "')")
                    etapa = 0
                elif c == ')':
                    tokens.append("(CERRADURA PARENTESIS,'" + c + "')")
                    etapa = 0
                elif c == '}':
                    tokens.append("(CERRADURA LLAVE,'" + c + "')")
                    etapa = 0
                elif c == '{':
                    tokens.append("(APERTURA LLAVE,'" + c + "')")
                    etapa = 0
                elif c == '[':
                    tokens.append("(APERTURA CORCHETE,'" + c + "')")
                    etapa = 0
                elif c == ']':
                    tokens.append("(CERRADURA CORCHETE,'" + c + "')")
                    etapa = 0
                elif c == '"':
                    etapa = 24
                    pal += c
                elif c == ',':
                    tokens.append("(COMA,'" + c + "')")
                    etapa = 0
                pass
            elif etapa == 23:
                etapa = 0
                if c == '*':
                    tokens.append("(MULTIPLICACIÓN,'" + c + "')")
                    etapa = 0
                elif c == '+':
                    tokens.append( "(SUMA,'" + c + "')")
                    etapa = 0
                elif c == '-':
                    tokens.append(  "(RESTA,'" + c + "')")
                    etapa = 0
                elif c == '/':
                    tokens.append(  "(DIVISION,'" + c + "')")
                    etapa = 0
                elif c == '%':
                    tokens.append(  "(PORCENTAJE,'" + c + "')")
                    etapa = 0
                pass
            elif etapa == 24:
                    pal += c
                    if c != '"':
                        etapa = 24
                    else:
                        pal2 = pal
                        pal = ''
                        tokens.append("(VALOR,'" + pal2 + "')")
                        etapa = 0
                    pass
            else:
                 contador += 1
                 c = cont[contador]
        return tokens
print(sigToken())
