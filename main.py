# main.py
import tkinter as tk
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
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.html"), ("Todos los archivos", "*.*")])
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
  

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()
