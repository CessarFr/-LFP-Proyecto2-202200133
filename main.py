import tkinter as tk
from tkinter import filedialog, messagebox

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
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if archivo:
            with open(archivo, "r") as f:
                contenido = f.read()
            self.codigo_texto.delete("1.0", "end")
            self.codigo_texto.insert("1.0", contenido)
            self.archivo_actual = archivo

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

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()
