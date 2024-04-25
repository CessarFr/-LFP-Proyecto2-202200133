# lexico.py

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class AnalizadorLexico:
    def __init__(self):
        self.palabras_reservadas = {
            "$set", "CrearBD", "EliminarBD", "CrearColeccion", "EliminarColeccion",
            "InsertarUnico", "ActualizarUnico", "EliminarUnico",
            "BuscarTodo", "BuscarUnico",
            "nueva", "set"
        }

    def analizar_linea(self, linea):
        tokens = []
        palabra_actual = ""
        dentro_de_comillas = False

        for caracter in linea:
            if caracter == '"':
                dentro_de_comillas = not dentro_de_comillas

            if caracter.isspace() and not dentro_de_comillas:
                if palabra_actual:
                    tokens.append(self.obtener_token(palabra_actual))
                    palabra_actual = ""
            elif caracter in ':();,.{}$="´':
                if palabra_actual:
                    tokens.append(self.obtener_token(palabra_actual))
                    palabra_actual = ""
                if caracter == "(":
                    tokens.append(Token("PARENTESIS_ABIERTO", caracter))
                elif caracter == ")":
                    tokens.append(Token("PARENTESIS_CERRADO", caracter))
                elif caracter == "=":
                    tokens.append(Token("ASIGNACION", caracter))
                elif caracter == ",":
                    tokens.append(Token("COMA", caracter))
                elif caracter == '"':
                    tokens.append(Token("COMILLA", caracter))
                elif caracter == "{":
                    tokens.append(Token("CORCHETE_ABIERTO", caracter))
                elif caracter == "}":
                    tokens.append(Token("CORCHETE_CERRADO", caracter))
                elif caracter == ";":
                    tokens.append(Token("PUNTO_Y_COMA", caracter))
                elif caracter == ":":
                    tokens.append(Token("DOS_PUNTOS", caracter))
                elif caracter == ".":
                    tokens.append(Token("PUNTO", caracter))
                elif caracter == "$":
                    tokens.append(Token("DOLAR", caracter))
            elif caracter.isalnum():
                palabra_actual += caracter
            else:
                tokens.append(Token("ERROR_LEXICO", caracter))

        if palabra_actual:
            tokens.append(self.obtener_token(palabra_actual))

        return tokens
    
    def analizar_contenido(self, contenido):
        tokens_por_linea = []
        for linea in contenido.split('\n'):
            tokens_por_linea.append(self.analizar_linea(linea))
        return tokens_por_linea

    def obtener_token(self, palabra):
        if palabra in self.palabras_reservadas:
            return Token("PALABRA_RESERVADA", palabra)
        elif palabra.startswith('"') and palabra.endswith('"'):
            return Token("CADENA", palabra[1:-1])
        elif palabra:
            return Token("IDENTIFICADOR", palabra)
        else:
            return None 



