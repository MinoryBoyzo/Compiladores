import os

_NOMBRE_ARCHIVO = os.getcwd() + "/ProgramaEnC.c"
tabla_de_simbolos = []
palabras_reservadas = [
    'PRINTF',
    'WHILE',
    'DEFINE',
    'SCANF',
    'SWITCH',
    'IF',
    'ELSE',
    'CASE',
    'INT',
    'FLOAT',
    'CHAR',
    'DOUBLE',
    'TRY',
    'CATCH',
    'MAIN',
    'VOID',
    'GETS',
    'DO',
    'FOR',
    'BREAK',
    'SYSTEM',
    'RETURN',
    'PAUSE',
]
simb = ['(', ')', '{', '}', '[', ']', '"', ',']
for i in palabras_reservadas:
    tabla_de_simbolos.append(['PALABRA RESERVADA', i])

operadores_relacionales = ['>', '<', '=', '!']
operadores = ['+', '*', '/', '-', '%']

with open(_NOMBRE_ARCHIVO, 'r') as file:
    cont = file.read() + " \0"



    def sigToken():
        estado = 0
        contador = -1
        c = None
        pal = ''
        ascii = 0
        linea = 1

        while contador < len(cont) - 1:
            if contador >= len(cont) - 2:
                print("Fin del archivo")
                return

            contador += 1
            c = cont[contador]
            ascii = ord(c.upper())
            if ascii == 13:
                linea += 1
            if estado == 0:
                if c in operadores_relacionales:
                    if c == '<':
                        estado = 1
                    elif c == '=':
                        estado = 5
                    elif c == '>':
                        estado = 6
                    elif c == '!':
                        estado = 40
                    contador -= 1
                    pal += c
                elif ascii > 64 and ascii < 91:
                    pal += c
                    estado = 10
                elif c.isdigit():
                    pal += c
                    estado = 13
                    contador -=1
                elif c in simb:
                    estado = 22
                    contador -= 1
                elif c in operadores:
                    estado = 23
                    contador-=1
                elif c == ';':
                    estado = 41
                    contador -= 1
                else:
                    if 8 <= ord(c) <= 15 or ord(c) == 32:
                        estado = 0
                    else:
                        print( f"error en la linea ----> {linea} {ord(c)}")
                        estado = 0
                        exit(1)
            elif estado == 1:
                c = cont[contador + 1]
                ascii = ord(c.upper())
                if c == '>':
                    pal += c
                    estado = 3
                    contador += 1
                elif c == '=':
                    pal += c
                    estado = 2
                    contador += 1
                else:
                    estado = 4
                    pass
            elif estado == 2:
                pal = ''
                estado = 0
                print( "(MENOR_O_IGUAL, <=)")
                estado = 0
                pass
            elif estado == 3:
                pal = ''
                estado = 0
                print( "(DISTINTO, <>)")
                estado = 0
                pass
            elif estado == 4:
                pal = ''
                estado = 0
                print( "(MENOR, <)")
                estado = 0
                pass
            elif estado == 5:
                pal = ''
                estado = 0
                print( "(IGUAL, =)")
                estado = 0
                pass
            elif estado == 40:
                pal = ''
                print( "(DISTINTO, !)")
                estado = 0
                contador -= 1
                pass
            elif estado == 6:
                if c == '=':
                    pal += c
                    estado = 7
                else:
                    estado = 8
                pass
            elif estado == 7:
                pal = ''
                print( "(MAYOR_O_IGUAL, >=)")
                estado = 0
                contador = contador - 1
                pass
            elif estado == 8:
                pal = ''
                print( "(MAYOR, >)")
                estado = 0
                pass
            elif estado == 9:
                pass
            elif estado == 10:
                ascii = ord(c.upper())
                if (ascii > 64 and ascii < 91) or (ascii > 47 and ascii < 58):
                    pal += c
                    estado = 10
                else:
                    contador -= 1
                    estado = 11
                pass
            elif estado == 11:
                con = pal
                pal = ''
                if con.upper() in palabras_reservadas:
                    print( "(PALABRA DE C, " + con + ")")
                    estado = 0
                    contador -= 1
                else:
                    tabla_de_simbolos.append(['id', con])
                    print("(ID, " + con + ")")
                    estado = 0

                pass
            elif estado == 12:
                pass
            elif estado == 13:
                if c.isdigit():
                    print(f"(NUMERO, {pal})")
                    estado = 0
                    pal = ''
                elif c == '.':
                    pal += c
                    estado = 14
                elif c == 'E' or c == 'e':
                    pal += c
                    estado = 16
                elif c == ' ':
                    estado = 20
                elif ord(c) == 13:
                    linea += 1
                    estado = 20
                else:
                    contador -= 1
                    estado = 20
                pass
            elif estado == 14:
                if c.isdigit():
                    pal += c
                    estado = 15
                elif c == 'E' or c == 'e':
                    pal += c
                    estado = 16
                else:
                    print( f"ERROR EN: {linea}", ord(c))
                    estado = 0
                    exit(-1)
                pass
            elif estado == 15:
                if c.isdigit():
                    pal += c
                elif c == 'E' or c == 'e':
                    pal += c
                    estado = 16
                elif c == ' ':
                    estado = 21
                elif ord(c) == 13:
                    linea += 1
                    estado = 21
                else:
                    contador -= 1
                    estado = 20
                pass
            elif estado == 16:
                if c == '+' or c == '-':
                    pal += c
                    estado = 17
                elif c.isdigit():
                    pal += c
                    estado = 18
                pass
            elif estado == 17:
                if c.isdigit():
                    pal += c
                    estado = 18
                else:
                    print( f"ERROR EN: {linea}")
                    estado = 0
                    exit(-1)
                pass
            elif estado == 18:
                if c.isdigit():
                    pal += c
                elif ord(c) == 13:
                    linea += 1
                    estado = 19
                else:
                    estado = 20
                    contador -= 1
                pass
            elif estado == 19 or estado == 20 or estado == 21:
                send = pal
                pal = ''
                print( f"(TEXTO, {send})")
                contador -= 1
                estado = 0
                pass
            elif estado == 22:
                estado = 0
                if c == '(':
                    print( "(INICIO PARENTESIS,'" + c + "')")
                    estado = 0
                elif c == ')':
                    print(  "(FIN PARENTESIS,'" + c + "')")
                    estado = 0
                elif c == '}':
                    print( "(INICIO LLAVE,'" + c + "')")
                    estado = 0
                elif c == '{':
                    print(  "(FIN LLAVE,'" + c + "')")
                    estado = 0
                elif c == '[':
                    print( "(INICIO CORCHETE,'" + c + "')")
                    estado = 0
                elif c == ']':
                    print(  "(FIN CORCHETE,'" + c + "')")
                    estado = 0
                elif c == '"':
                    estado = 24
                    pal += c
                elif c == ',':
                    print(  "(COMA,'" + c + "')")
                    estado = 0
                pass
            elif estado == 23:
                estado = 0
                if c == '*':
                    print(  "(MULTIPLICACIÓN,'" + c + "')")
                    estado = 0
                elif c == '+':
                    print( "(SUMA,'" + c + "')")
                    estado = 0
                elif c == '-':
                    print(  "(RESTA,'" + c + "')")
                    estado = 0
                elif c == '/':
                    print(  "(DIVISIÓN,'" + c + "')")
                    estado = 0
                elif c == '%':
                    print(  "(PORCENTAJE,'" + c + "')")
                    estado = 0
                pass
            elif estado == 24:
                    pal += c
                    if c != '"':
                        estado = 24
                    else:
                        estado = 0
                        pal2 = pal
                        pal = ''
                        print(  "(TEXTO,'" + pal2 + "')")
                        estado = 0
                    pass
            elif estado == 41:
                send = ";"
                pal = ''
                print( f"(FIN DE LINEA, {send})")
                estado = 0
                pass
            else:
                 contador += 1
                 c = cont[contador]

sigToken()