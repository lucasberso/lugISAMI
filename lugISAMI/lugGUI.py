#
# Authors:
# Pablo Arcediano,
# Lucas Bernacer Soriano,
# Ángela Blazquez,
# Héctor Dionisio,
# Javier Vela
#
# Copyright (c) 2021, Capgemini Engineering
#

import tkinter as tk
from tkinter import filedialog
from functools import partial
from lugReader import lugHTML
from lugWriter import lugInput
import os

class run_GUI:
    """
    Clase desarrollada para proporcionar una interfaz gráfica a la herramienta de orejetas.

    """
    def __init__(self, master):
        """
        Inicializa la interfaz y establece la organización de objetos.

        """
        self.master = master
        self.master.title("ISAMI LUG V1.0") # Título a mostrar en la ventana de la interfaz.
        self.master.resizable(False, False) # No permite modificar el tamaño de la ventana.
        self.master.update() # Actualiza la visualización.

        # Botones de selección caso.
        self.case= tk.IntVar()
        self.case_create = tk.Radiobutton(self.master, text='Create ISAMI input', variable=self.case, value=1)
        self.case_create.grid(row = 0, column = 0, padx = 10, pady = (10,0), sticky=tk.W)
        self.case_read = tk.Radiobutton(self.master, text='Read HTML or CZM', variable=self.case, value=2)
        self.case_read.grid(row=1, column=0, padx = 10, pady = 0, sticky=tk.W)

        # Boton de ayuda.
        self.help = tk.Button(self.master, text="HELP", command=self.open_help)
        self.help.grid(row=1, column=1, padx=10, pady = 10)

        # Bloques de entrada.
        self.label_dic, self.button_dic, self.entry_dic  = {}, {}, {}
        self.count = 0
        self.create_block('input_file','file', 'Input file:', 2, 0)
        self.create_block('output_folder','folder', 'Output folder:', 3, 0)
        self.create_block('output_name','entry', 'Output filename:', 4, 0)

        # Botón de generar.
        self.generate_button = tk.Button(self.master, text='Generate', command=self.generate)
        self.generate_button.grid(row=5, column=0, columnspan = 2, sticky = tk.W+tk.E, padx = (10,0), pady = (10,10))

        # Texto de salida y barra.
        self.scrollbar = tk.Scrollbar(orient="vertical")
        self.output_print = tk.Text(self.master, yscrollcommand=self.scrollbar.set,  height=3, width = 10)
        self.output_print.configure(state='disabled')
        self.output_print.grid(row=6, column=0, columnspan=2, sticky=tk.W + tk.E, padx = 10, pady = (10,20))
        self.scrollbar.config(command=self.output_print.yview)
        self.scrollbar.grid(row=6, column=2, sticky=tk.N + tk.S + tk.W, padx = 10)

        self.label_version = tk.Label(self.master, text="© Capgemini Engineering")
        self.label_version.grid(row=7, column=0)

    def askfilename(self, entry):
        """
        Función que almacena el nombre del archivo de entrada y actualiza el texto mostrado en la barra.

        entry: identificador de la barra de texto a actualizar.

        """
        file_name = filedialog.askopenfilename()
        self.entry_dic[entry].configure(state=tk.NORMAL)
        self.entry_dic[entry].delete(0, "end")
        self.entry_dic[entry].insert(0, file_name)
        self.entry_dic[entry].configure(state=tk.DISABLED)

    def askdirectory(self, entry):
        """
        Función que almacena el directorio de salida y actualiza el texto mostrado en la barra.

        entry: identificador de la barra de texto a actualizar.

        """
        dir_path = filedialog.askdirectory()
        self.entry_dic[entry].configure(state=tk.NORMAL)
        self.entry_dic[entry].delete(0, "end")
        self.entry_dic[entry].insert(0, dir_path)
        self.entry_dic[entry].configure(state=tk.DISABLED)

    def create_block(self, id, type, label_text, row, column):
        """
        Crea el conjunto de bloques compuesto por un label, entry y botón.

        id: Identificador del bloque.
        type: Tipo del bloque.
        label_text: Texto a mostrar en la etiqueta.
        row: Fila inicial.
        column: Columna inicia.

        """
        label = tk.Label(self.master, text= label_text)
        label.grid(row=row, column=column, sticky=tk.W, padx = 10)
        self.label_dic.update({id:label})
        if type == 'file':
            button = tk.Button(self.master, text="...", command=partial(self.askfilename, entry=id))
            button.grid(row=row, column=column + 2, sticky=tk.W, padx = 10)
            self.button_dic.update({id:button})
        elif type == 'folder':
            button = tk.Button(self.master, text="...", command=partial(self.askdirectory, entry=id))
            button.grid(row=row, column=column + 2, sticky=tk.W, padx = 10)
            self.button_dic.update({id:button})
        if type == 'entry':
            entry = tk.Entry(self.master)
        else:
            entry = tk.Entry(self.master, state="disabled")
        entry.grid(row=row, column=column+1, sticky=tk.W)
        self.entry_dic.update({id:entry})
        self.count = self.count +1

    def generate(self):
        """
        Activador del botón "generar" que desencadena la acción del programa llamando a la librería lugISAMI.

        """
        self.warning_print = ""
        self.output_print.configure(state='normal')
        self.output_print.delete(1.0, tk.END)

        for i in self.entry_dic.keys(): # Recoge la existencia de warnings en caso de entradas incorrectas o vacías.
            warning = self.check_empty(self.entry_dic[i], i)
            if warning:
                self.warning_print = self.warning_print + warning + "\n"

        self.write_in_txt(self.warning_print, self.output_print) # Escritura de los warnings.

        file_name = self.entry_dic['input_file'].get()
        dir_path = self.entry_dic['output_folder'].get()
        output_name = self.entry_dic['output_name'].get()

        if self.warning_print == "": # Activa el programa en caso de que no haya errores.
            if self.case.get() == 1: # Genera el archivo de entrada a ISAMI.
                try:
                    ISAMI = lugInput(input_file=file_name)
                    ISAMI.write_output(output_path=dir_path, output_filename=output_name)
                    ISAMI.write_bach(output_path=dir_path, output_filename=output_name)
                    self.write_in_txt("The ISAMI file has been generated.", self.output_print)
                except: # Si la librería falla muestra un error.
                    self.write_in_txt("Error: ISAMI input file not compatible.", self.output_print)

            elif self.case.get() == 2: # Genera el archivo de salida a partir de un HTML o CZM.
                try:
                    HTML = lugHTML(input_file=file_name)
                    HTML.write_output(output_path=dir_path, output_filename=output_name)
                    self.write_in_txt("The HTML file has been read: Kt has been extracted.",self.output_print)
                except: # Si la librería falla muestra un error.
                    self.write_in_txt("Error: HTML or CZM file not compatible.", self.output_print)
            else: # Situación sin selección de caso de estudio.
                self.write_in_txt("Error: Select one of the program options.", self.output_print)

        self.warning_print = "" # Reinicia la búsqueda de errores al pulsar el botón.

    def open_help(self):
        """
        Acción del botón de ayuda.

        """
        try: # Abre el archivo de ayuda "LugISAMI_Help.pdf" en caso de encontrarse en el mismo directorio.
            os.system("LugISAMI_Help.pdf")
        except: # Muestra un error en caso de no encontrar el archivo.
            self.write_in_txt("Error: Couldn't open the README file.", self.output_print)

    def write_in_txt(self, txt, object):
        """
        Escribe la cadena de texto de entrada en el objeto suministrado.

        txt: Texto deseado a escribir.
        bject: Objeto de destino. Debe ser una entrada tk.TEXT.

        """
        object.configure(state='normal')
        object.delete(1.0, tk.END)
        object.insert(tk.END, txt)
        object.configure(state='disabled')

    def check_empty(self, input, field):
        """
        Comprobación de errores y escritura de los mismos.

        input: Objeto a comprobar si está vacío.
        field: Identificador del objeto introducido.

        """
        warning = ""
        if not input.get():
            warning = "Error: %s has not been selected." % (field.replace("_"," "))
        return warning

if __name__ == '__main__':

    root = tk.Tk()
    app = run_GUI(root)
    root.mainloop() # Bucle principal del programa.