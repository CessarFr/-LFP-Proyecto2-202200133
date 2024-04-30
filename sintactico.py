class AnalizadorSintactico:
    def __init__(self):
        pass

    def analizar_linea(self, tokens):
        estructura_crearbd = [
            ("PALABRA_RESERVADA", "CrearBD"),
            ("CADENA", None),  
            ("ASIGNACION", "="),
            ("PALABRA_RESERVADA", "nueva"),
            ("PALABRA_RESERVADA", "CrearBD"),
            ("PARENTESIS_ABIERTO", "("),
            ("PARENTESIS_CERRADO", ")"),
            ("PUNTO_Y_COMA", ";")
        ]
        estructura_eliminardb = [
            ("PALABRA_RESERVADA", "EliminarBD"),
            ("CADENA", None),
            ("ASIGNACION", "="),
            ("PALABRA_RESERVADA", "nueva"),
            ("PALABRA_RESERVADA", "EliminarBD"),
            ("PARENTESIS_ABIERTO", "("),
            ("PARENTESIS_CERRADO", ")"),
            ("PUNTO_Y_COMA", ";")
        ]
               
        estructura_crearcoleccion = [
            ("PALABRA_RESERVADA", "CrearColeccion"),
            ("CADENA", None), 
            ("ASIGNACION", "="),
            ("PALABRA_RESERVADA", "nueva"),
            ("PALABRA_RESERVADA", "CrearColeccion"),
            ("PARENTESIS_ABIERTO", "("),
            ("IDENTIFICADOR", None),  
            ("PARENTESIS_CERRADO", ")"),
            ("PUNTO_Y_COMA", ";")
        ]
        
        estructura_eliminarcoleccion = [
            ("PALABRA_RESERVADA", "EliminarColeccion"),
            ("CADENA", None), 
            ("ASIGNACION", "="),
            ("PALABRA_RESERVADA", "nueva"),
            ("PALABRA_RESERVADA", "EliminarColeccion"),
            ("PARENTESIS_ABIERTO", "("),
            ("IDENTIFICADOR", None),  
            ("PARENTESIS_CERRADO", ")"),
            ("PUNTO_Y_COMA", ";")
        ]
        
        estructura_buscartodo = [
            ("PALABRA_RESERVADA", "BuscarTodo"),
            ("CADENA", None), 
            ("ASIGNACION", "="),
            ("PALABRA_RESERVADA", "nueva"),
            ("PALABRA_RESERVADA", "BuscarTodo"),
            ("PARENTESIS_ABIERTO", "("),
            ("IDENTIFICADOR", None),  
            ("PARENTESIS_CERRADO", ")"),
            ("PUNTO_Y_COMA", ";")
        ]
        
        estructura_buscarunico = [
            ("PALABRA_RESERVADA", "BuscarUnico"),
            ("CADENA", None), 
            ("ASIGNACION", "="),
            ("PALABRA_RESERVADA", "nueva"),
            ("PALABRA_RESERVADA", "BuscarUnico"),
            ("PARENTESIS_ABIERTO", "("),
            ("IDENTIFICADOR", None),  
            ("PARENTESIS_CERRADO", ")"),
            ("PUNTO_Y_COMA", ";")
        ]
        

        if (self.coincide_estructura(tokens, estructura_crearbd) or
            self.coincide_estructura(tokens, estructura_eliminardb) or
            self.coincide_estructura(tokens, estructura_crearcoleccion) or
            self.coincide_estructura(tokens, estructura_eliminarcoleccion) or
            self.coincide_estructura(tokens, estructura_buscartodo) or
            self.coincide_estructura(tokens, estructura_buscarunico)
            ):
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
            if not tokens:
                continue
            if not self.analizar_linea(tokens):  
                return False
        return True
