import re

# Función que lee el archivo de la gramática y la convierte en un diccionario de reglas
def leer_gramatica(archivo_gramatica):
    gramatica = {}
    with open(archivo_gramatica) as archivo:
        for regla in archivo:
            izquierda, derecha = regla.strip().split(' -> ')
            derecha = derecha.split(' | ')
            gramatica[izquierda] = derecha
    return gramatica

# Función que tokeniza un código fuente en C
def analizar_lexico(codigo_fuente):
    tokens = []
    # Expresiones regulares para los tokens
    regex = {
        'LOOP_IF': r'if',
        'LOOP_ELSE': r'else',
        'LOOP_ELIF': r'elif',
        'LOOP_DOWHILE': r'do while',
        'LOOP_DO': r'do',
        'LOOP_WHILE' : r'while',
        'IMPRIMIR' : r'printf',
        'ESCANEAR' : r'scanf',
        'REGRESO' : r'return',
        'INICIO_MAIN' : r'main',
        'TIPO_INT': r'int',
        'TIPO_FLOAT': r'float',
        'TIPO_DOUBLE': r'double',
        'TIPO_CHAR': r'char',
        'LOGICO_AND': r'AND',
        'LOGICO_OR': r'OR',
        'LOGICO_NOT': r'NOT',
        'ID': r'[a-zA-Z_]\w*',
        'NUMERO': r'\d+',
        'CHAR': r"'.'",
        'STRING': r'"[^"]*"',
        'OPERACION': r'[+\-*/%&|<>=!~^?]',
        'FIN_DE_LINEA' : r';',
        'PARENTESIS': r'[()]',
        'LLAVE': r'[{}\[\]]'
    }

    # Patrón global de todas las expresiones regulares
    patron = '|'.join('(?P<%s>%s)' % par for par in regex.items())
    # Tokenización
    for linea in codigo_fuente:
        for match in re.finditer(patron, linea):
            for nombre, valor in match.groupdict().items():
                if valor and nombre != 'WS':
                    tokens.append((nombre, valor))

    return tokens

# Prueba del analizador léxico
if __name__ == '__main__':

    entrada = input("Ingrese el código en C : ")
    codigo_fuente = [entrada]
    tokens = analizar_lexico(codigo_fuente)
    print(tokens);