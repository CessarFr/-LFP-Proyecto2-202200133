class AnalizadorSintactico:
    def __init__(self):
        pass

    def analizar_linea(self, tokens):
        estructura_deseada = [
            ("PALABRA_RESERVADA", "CrearBD"),
            ("IDENTIFICADOR", None),  
            ("ASIGNACION", "="),
            ("PALABRA_RESERVADA", "nueva"),
            ("PALABRA_RESERVADA", "CrearBD"),
            ("PARENTESIS_ABIERTO", "("),
            ("PARENTESIS_CERRADO", ")"),
            ("PUNTO_Y_COMA", ";")
        ]

        if self.coincide_estructura(tokens, estructura_deseada):   
            return True
        else:  
            return False

    def coincide_estructura(self, tokens, estructura_deseada):
        
        if len(tokens) != len(estructura_deseada):
            return False
        for token, (tipo_esperado, valor_esperado) in zip(tokens, estructura_deseada):
            if tipo_esperado is not None and token.tipo != tipo_esperado:
                return False
            if valor_esperado is not None and token.valor != valor_esperado:
                return False

        return True

    def analizar_contenido(self, tokens_por_linea): 
        for tokens in tokens_por_linea:
            if not self.analizar_linea(tokens):  
                return False
        return True
