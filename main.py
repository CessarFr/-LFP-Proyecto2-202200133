import tkinter as tk
from tkinter import ttk
from graphviz import Digraph
from tkinter import filedialog, messagebox
from lexico import AnalizadorLexico
from sintactico import AnalizadorSintactico

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Código")

        self.archivo_actual = None

        self.crear_menu()
        self.crear_areas()

    def crear_menu(self):
        menubar = tk.Menu(self.root)

        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Nuevo", command=self.nuevo_archivo)
        archivo_menu.add_command(label="Abrir", command=self.abrir_archivo)
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        archivo_menu.add_command(label="Guardar Como", command=self.guardar_como_archivo)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.salir)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        
        traducir_menu = tk.Menu(menubar, tearoff=0)
        traducir_menu.add_command(label="Traducir", command=self.traducir_archivo)
        menubar.add_cascade(label="Traducir", menu=traducir_menu)
        
        herramientas_menu = tk.Menu(menubar, tearoff=0)
        herramientas_menu.add_command(label="Tokens", command=self.mostrar_tokens)
        menubar.add_cascade(label="Herramientas", menu=herramientas_menu)
        herramientas_menu.add_command(label="Errores", command=self.mostrar_errores)


        self.root.config(menu=menubar)

    def crear_areas(self):
        self.codigo_texto = tk.Text(self.root, wrap="word")
        self.codigo_texto.pack(fill="both", expand=True)


    def nuevo_archivo(self):
        if self.codigo_texto.get("1.0", "end-1c") != "":
            respuesta = messagebox.askyesnocancel("Nuevo Archivo", "¿Desea guardar los cambios antes de crear un nuevo archivo?")
            if respuesta is True:
                self.guardar_archivo()
            elif respuesta is None:
                return  

        self.codigo_texto.delete("1.0", "end")
        self.archivo_actual = None

    def abrir_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if archivo:
            with open(archivo, "r", encoding="utf-8") as f:  
                contenido = f.read()
            self.codigo_texto.delete("1.0", "end")
            self.codigo_texto.insert("1.0", contenido)
            self.analizar_lexico(contenido)
            self.analizar_sintactico(contenido)


    def guardar_archivo(self):
        if self.archivo_actual:
            with open(self.archivo_actual, "w") as f:
                f.write(self.codigo_texto.get("1.0", "end-1c"))
        else:
            self.guardar_como_archivo()

    def guardar_como_archivo(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            with open(archivo, "w") as f:
                f.write(self.codigo_texto.get("1.0", "end-1c"))
            self.archivo_actual = archivo

    def salir(self):
        self.root.quit()


    def analizar_lexico(self, contenido):
        analizador = AnalizadorLexico()
        lineas = contenido.split("\n")
        tokens_validos = []
        errores_lexicos = []

        for num_linea, linea in enumerate(lineas, start=1):
            tokens = analizador.analizar_linea(linea)
            for token in tokens:
                if token.tipo != "ERROR_LEXICO":
                    tokens_validos.append((num_linea, token))
                else:
                    errores_lexicos.append((num_linea, token))

        for num_linea, token in tokens_validos:
            print(f"Línea {num_linea}: {token.tipo}, {token.valor}")

        for num_linea, token in errores_lexicos:
            print(f"Línea {num_linea}: ERROR LÉXICO, {token.valor}")
            

    def analizar_sintactico(self, contenido):
        analizador_lexico = AnalizadorLexico()
        analizador_sintactico = AnalizadorSintactico()

        tokens_por_linea = analizador_lexico.analizar_contenido(contenido)
        estructuras_validas = []

        for num_linea, tokens in enumerate(tokens_por_linea, start=1):
            if analizador_sintactico.analizar_linea(tokens):
                estructuras_validas.append(num_linea)

        for num_linea, tokens in enumerate(tokens_por_linea, start=1):
            if num_linea in estructuras_validas:
                print(f"Línea {num_linea}: SINTACTICO, ESTRUCTURA VALIDA")
            else:
                print(f"Línea {num_linea}: ERROR_SINTACTICO, ESTRUCTURA NO VALIDA")
  
    def traducir_archivo(self):
        contenido = self.codigo_texto.get("1.0", "end-1c")
        
        analizador_lexico = AnalizadorLexico()

        tokens_por_linea = analizador_lexico.analizar_contenido(contenido)
      
        traduccion = self.traducir_contenido(tokens_por_linea)

        ventana_traduccion = tk.Toplevel(self.root)
        ventana_traduccion.title("Traducción a MongoDB")

        cuadro_traduccion = tk.Text(ventana_traduccion, wrap="word")
        cuadro_traduccion.pack(fill="both", expand=True)
        cuadro_traduccion.insert("1.0", traduccion)

    def traducir_contenido(self, tokens_por_linea):
        traduccion = ""
        for tokens in tokens_por_linea:
            if len(tokens) == 0:
                continue
            primer_token = tokens[0]
            if primer_token.tipo == "PALABRA_RESERVADA":
                if primer_token.valor == "CrearBD":
                    traduccion += f"use('{tokens[1].valor}');\n"
                elif primer_token.valor == "EliminarBD":
                    traduccion += "db.dropDatabase();\n"
                elif primer_token.valor == "CrearColeccion":
                    traduccion += f"db.createCollection('{tokens[1].valor}');\n"
                elif primer_token.valor == "EliminarColeccion":
                    traduccion += f"db.{tokens[1].valor}.drop();\n"
                elif primer_token.valor == "BuscarTodo":
                    traduccion += f"db.{tokens[1].valor}.find();\n"
                elif primer_token.valor == "BuscarUnico":
                    traduccion += f"db.{tokens[1].valor}.findOne();\n"
        return traduccion
    
    def mostrar_tokens(self):
        contenido = self.codigo_texto.get("1.0", "end-1c")
        
        analizador_lexico = AnalizadorLexico()
        tokens_por_linea = analizador_lexico.analizar_contenido(contenido)

        ventana_tokens = tk.Toplevel(self.root)
        ventana_tokens.title("Tokens")

        tabla_tokens = ttk.Treeview(ventana_tokens, columns=("Línea", "Tipo", "Valor"))
        tabla_tokens.heading("#0", text="Índice")
        tabla_tokens.heading("Línea", text="Línea")
        tabla_tokens.heading("Tipo", text="Tipo")
        tabla_tokens.heading("Valor", text="Valor")

        for num_linea, tokens in enumerate(tokens_por_linea, start=1):
            for indice, token in enumerate(tokens, start=1):
                if token.tipo != "ERROR_LEXICO" and token.tipo != "ERROR_SINTACTICO":
                    tabla_tokens.insert("", "end", text=str(indice), values=(num_linea, token.tipo, token.valor))

        tabla_tokens.pack(expand=True, fill="both")
        
        
    def mostrar_errores(self):
        errores_lexicos = []
        errores_sintacticos = []

        analizador_lexico = AnalizadorLexico()
        analizador_sintactico = AnalizadorSintactico()

        contenido = self.codigo_texto.get("1.0", "end-1c")
        tokens_por_linea = analizador_lexico.analizar_contenido(contenido)

        for num_linea, tokens in enumerate(tokens_por_linea, start=1):
            if not analizador_sintactico.analizar_linea(tokens):
                errores_sintacticos.append((num_linea, "Error sintáctico en la estructura"))

            for token in tokens:
                if token.tipo == "ERROR_LEXICO":
                    errores_lexicos.append((num_linea, token))

        if errores_lexicos or errores_sintacticos:
            ventana_errores = tk.Toplevel(self.root)
            ventana_errores.title("Errores")
            
            frame = tk.Frame(ventana_errores)
            frame.pack(fill="both", expand=True)

            lexico_label = tk.Label(frame, text="Errores Léxicos")
            lexico_label.pack()
            lexico_table = ttk.Treeview(frame, columns=("Línea", "Error"), show="headings")
            lexico_table.heading("Línea", text="Línea")
            lexico_table.heading("Error", text="Error")
            lexico_table.pack(fill="both", expand=True)

            for linea, error in errores_lexicos:
                lexico_table.insert("", "end", values=(linea, error.valor))

            sintactico_label = tk.Label(frame, text="Errores Sintácticos")
            sintactico_label.pack()
            sintactico_table = ttk.Treeview(frame, columns=("Línea", "Error"), show="headings")
            sintactico_table.heading("Línea", text="Línea")
            sintactico_table.heading("Error", text="Error")
            sintactico_table.pack(fill="both", expand=True)

            for linea, error in errores_sintacticos:
                sintactico_table.insert("", "end", values=(linea, error))
        else:
            messagebox.showinfo("Sin Errores", "No se encontraron errores léxicos ni sintácticos en el archivo.")

grafo = Digraph()

grafo.node("Interfaz", label="Interfaz")
grafo.node("TextoEntrada", label="Texto de Entrada")
grafo.node("AnalizadorLexico", label="Analizador Léxico")
grafo.node("Tokens", label="Tokens válidos")
grafo.node("AnalizadorSintactico", label="Analizador Sintáctico")
grafo.node("EstructurasValidas", label="Estructuras Válidas")
grafo.node("TraduccionMongoDB", label="Traducción a MongoDB")
grafo.node("TablaTokens", label="Tabla de Tokens")
grafo.node("TablaErrores", label="Tabla de Errores")

grafo.edge("Interfaz", "TextoEntrada", label="Entrada de texto")
grafo.edge("TextoEntrada", "AnalizadorLexico", label="Texto sin procesar")
grafo.edge("AnalizadorLexico", "Tokens", label="Lista de Tokens válidos")
grafo.edge("Tokens", "AnalizadorSintactico", label="Lista de Tokens válidos")
grafo.edge("AnalizadorSintactico", "EstructurasValidas", label="Estructuras válidas")
grafo.edge("EstructurasValidas", "TraduccionMongoDB", label="Estructuras válidas")
grafo.edge("AnalizadorLexico", "TablaTokens", label="Tabla de Tokens")
grafo.edge("AnalizadorSintactico", "TablaErrores", label="Tabla de Errores")

grafo.node("PalabrasReservadas", label="Palabras Reservadas")
grafo.node("CaracteresEspeciales", label="Caracteres Especiales")
grafo.node("Identificadores", label="Identificadores")
grafo.node("Cadenas", label="Cadenas")
grafo.edge("AnalizadorLexico", "PalabrasReservadas", label="Palabras Reservadas")
grafo.edge("AnalizadorLexico", "CaracteresEspeciales", label="Caracteres Especiales")
grafo.edge("AnalizadorLexico", "Identificadores", label="Identificadores")
grafo.edge("AnalizadorLexico", "Cadenas", label="Cadenas")

grafo.node("EstructuraCrearBD", label="CrearBD")
grafo.node("EstructuraEliminarBD", label="EliminarBD")
grafo.node("EstructuraCrearColeccion", label="CrearColeccion")
grafo.node("EstructuraEliminarColeccion", label="EliminarColeccion")
grafo.node("EstructuraBuscarTodo", label="BuscarTodo")
grafo.node("EstructuraBuscarUnico", label="BuscarUnico")
grafo.edge("AnalizadorSintactico", "EstructuraCrearBD", label="CrearBD")
grafo.edge("AnalizadorSintactico", "EstructuraEliminarBD", label="EliminarBD")
grafo.edge("AnalizadorSintactico", "EstructuraCrearColeccion", label="CrearColeccion")
grafo.edge("AnalizadorSintactico", "EstructuraEliminarColeccion", label="EliminarColeccion")
grafo.edge("AnalizadorSintactico", "EstructuraBuscarTodo", label="BuscarTodo")
grafo.edge("AnalizadorSintactico", "EstructuraBuscarUnico", label="BuscarUnico")

grafo.render("grafo_programa_actualizado", format="png", cleanup=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()
