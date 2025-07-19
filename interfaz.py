from tkinter import *
from tkinter import messagebox
import discretas
from functools import partial
import os
#Esta interfaz cuenta con dos pestañas, una una calculadora donde la formula lógica se inserta con botonera y se hace todo con los botones, y otra donde se hace el input de la formula lógica escrbiendola directamente
class LogiCalcApp:
    def __init__(self, master, r_callback = None):
        self.master = master
        self.r_callback = r_callback
        self.master.title("LogiCalc Calculadibar")
        self.master.geometry("500x420")
        self.master.config(background="#2f2d3d")
        try:
            ruta_icono = os.path.join(os.path.dirname(__file__), "icono.ico")
            self.master.iconbitmap(ruta_icono)
        except Exception as e:
            print(f"Advertencia: no se pudo cargar el icono. {e}")
        self.boton_sc = None
        self.modo_latex = False
        self.original_expr = ""
        self.var_latex = ""

        self.pantalla_var = StringVar()

        self.crear_widgets()

    def crear_widgets(self):
        Label(self.master, text="Kadio ®", font=('Eurostile-Black', 20),
              bg="#2f2d3d", fg="#ffffff").place(x=5, y=5)

        pantalla = Entry(self.master, textvariable=self.pantalla_var, font=('Consolas', 20),
                         bg="#ffffff", fg="#000000", justify='right',
                         state='readonly', readonlybackground='white', bd=4, relief='sunken')
        pantalla.pack(fill='x', padx=10, pady=50, ipady=10)

        botonera = Frame(self.master, bg="#2f2d3d")
        botonera.pack(padx=10, fill='both', expand=True)

        botones = [
            [("¬",), ("(",), (")",), ("⌫", self.borrar_ultimo), ("C", self.borrar_todo)],
            [("∧",), ("∨",), ("→",), ("↔",), ("↵", self.enter)],  # ↵ aún sin funcionalidad
            [("var", self.tecladovar), ("LaTeX", self.cambio_sc), ("",), ("",), ("",)]
        ]

        for fila_idx, fila in enumerate(botones):
            for col_idx, btn_info in enumerate(fila):
                texto = btn_info[0]
                if texto == "":
                    continue
                funcion = btn_info[1] if len(btn_info) > 1 else lambda t=texto: self.actualizar_pantalla(t)
                boton = Button(botonera, text=texto, command=funcion,
                               bg='#a09ea8', fg='#ffffff', font=('Arial', 14))
                boton.grid(row=fila_idx, column=col_idx, sticky='nsew', padx=2, pady=2)
                if texto == "LaTeX":
                    self.boton_sc = boton

        for i in range(5):
            botonera.columnconfigure(i, weight=1)
        for i in range(len(botones)):
            botonera.rowconfigure(i, weight=1)
            
        Button(self.master, text= "Atras", command=self.main_return, bg='#9e4b4b', fg='white').pack(pady=10)

    def actualizar_pantalla(self, caracter):
        texto_actual = self.pantalla_var.get()
        self.pantalla_var.set(texto_actual + caracter)

    def borrar_ultimo(self):
        texto_actual = self.pantalla_var.get()
        self.pantalla_var.set(texto_actual[:-1])

    def borrar_todo(self):
        self.pantalla_var.set("")
    
    def main_return(self):
        self.master.destroy()
        if self.r_callback:
            self.r_callback()

    def tecladovar(self):
        self.master.update_idletasks()
        x = self.master.winfo_rootx()
        y = self.master.winfo_rooty()
        w = self.master.winfo_width()
        teclado = Toplevel(self.master)
        teclado.title("Seleccionar variable")
        teclado.geometry(f"365x270+{x + w + 10}+{y}")
        teclado.resizable(False, False)
        teclado.config(bg="#2f2d3d")

        letras = "abcdefghijklmnopqrstuv"
        filas = 4
        columnas = 7

        def insertar_letra(letra):
            self.actualizar_pantalla(letra)
            teclado.destroy()

        for idx, letra in enumerate(letras):
            fila = idx // columnas
            col = idx % columnas
            btn = Button(teclado, text=letra, width=4, height=2,
                         command=lambda l=letra: insertar_letra(l),
                         bg='#a09ea8', fg='#ffffff', font=('Arial', 12))
            btn.grid(row=fila, column=col, padx=3, pady=3)

        Button(teclado, text="Cerrar", command=teclado.destroy,
               bg='#9e4b4b', fg='white').grid(row=filas+1, columnspan=columnas, pady=10)

    def conv_latex(self):
        self.original_expr = self.pantalla_var.get()
        reemplazos = {
            "¬": r" \lnot",
            "∧": r" \land",
            "∨": r" \lor",
            "→": r" \rightarrow",
            "↔": r" \leftrightarrow",
        }
        self.var_latex = ''.join(reemplazos.get(c, c) for c in self.original_expr)
        if not "$" in str(self.var_latex):
            self.var_latex = "$" + self.var_latex + "$"
            return
    def de_latex_a_simbolos(self):
        reemplazos_inversos = {
            r"\lnot": "¬",
            r"\land": "∧",
            r"\lor": "∨",
            r"\rightarrow": "→",
            r"\leftrightarrow": "↔",
        }
        resultado = self.original_expr
        for latex, simbolo in reemplazos_inversos.items():
            resultado = resultado.replace(latex, simbolo)

        self.var_latex = resultado.replace("$", "")  # opcional, puedes usar otra variable si quieres
        self.pantalla_var.set(resultado.replace("$", ""))
        return

    def cambio_sc(self):
        if self.modo_latex:
            self.de_latex_a_simbolos()
            self.boton_sc.config(bg='#4b9e4b')  # verde
            self.modo_latex = False
        else:
            self.conv_latex()
            self.pantalla_var.set(self.var_latex)
            self.boton_sc.config(bg='#9e4b4b')  # rojo
            self.modo_latex = True
    def enter(self):
        from discretas import ReescritorLogico
        
        texto = str(self.pantalla_var.get())

        if texto != "" : 
            from discretas import ParserLogico
            reescritor = ReescritorLogico(texto)
            reescritor.de_latex_a_formula()
            reescritor.de_formula_a_lista()

            parser =ParserLogico(reescritor)
            if parser.Paso0():
                messagebox.showerror("Error", "La fórmula no es bien formada")
                return
            else:
                reescritor.nueva_lista = parser.Paso1()
                reescritor.nueva_lista = parser.paso2()
                reescritor.nueva_lista = parser.paso3()
                conversion = reescritor.obtener_conversion()
                self.pantalla_var.set(conversion["latex_final"])

                return


                



class RecibeLatex:

    def __init__(self, master, r_callback= None):
        self.master = master
        self.master.title("LogiCalc Calculadibar")
        self.master.geometry("800x500")
        self.master.config(background="#2f2d3d")
        self.master.resizable(False, False)
        try:
            ruta_icono = os.path.join(os.path.dirname(__file__), "icono.ico")
            self.master.iconbitmap(ruta_icono)
        except Exception as e:
            print(f"Advertencia: no se pudo cargar el icono. {e}")
        self.r_callback = r_callback

        self.placeholder_entry = "Ingrese su fórmula en LaTeX"
        self.placeholder_vanilla = "Aquí aparecerá su formula en LaTeX en forma de fórmula lógica"
        self.placeholder_bienformada = "Aquí aparecerá su fórmula lógica bien formada"
        self.placeholder_latex_final = "Aquí aparecerá el resultado final en LaTeX"

        self.centrar_ventana(800, 500)
        self.crear_widgets()

    def centrar_ventana(self, ancho, alto):
        pantalla_ancho = self.master.winfo_screenwidth()
        pantalla_alto = self.master.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.master.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_widgets(self):
        Label(self.master, text="Kadio ®", font=('Eurostile-Black', 20),
          bg="#2f2d3d", fg="#ffffff").pack(pady=(10, 10))

        frame = Frame(self.master, bg="#2f2d3d")
        frame.pack(fill='both', expand=True, padx=50)
        frame.columnconfigure(0, weight=1)

        #entrada usuario
        self.entry = Entry(frame, font=('Consolas', 10),
                       bg="#ffffff", fg="gray", justify='center', bd=4, relief='sunken')
        self.entry.insert(0, self.placeholder_entry)
        self.entry.grid(row=0, column=0, pady=10, ipadx=10, ipady=10, sticky='ew')
        self.entry.bind("<FocusIn>", partial(self.al_entrar, widget=self.entry, placeholder=self.placeholder_entry))
        self.entry.bind("<FocusOut>", partial(self.al_salir, widget=self.entry, placeholder=self.placeholder_entry))

        #labels salida
        self.formulavanilla = Label(frame, text=self.placeholder_vanilla, font=('Consolas', 10),
                                bg="#ffffff", fg="gray", bd=4, relief='sunken', anchor='center')
        self.formulavanilla.grid(row=1, column=0, pady=10, ipadx=10, ipady=10, sticky='ew')

        self.formulabienformada = Label(frame, text=self.placeholder_bienformada, font=('Consolas', 12),
                                    bg="#ffffff", fg="gray", bd=4, relief='sunken', anchor='center')
        self.formulabienformada.grid(row=2, column=0, pady=10, ipadx=10, ipady=10, sticky='ew')

        self.latexfinal = Label(frame, text=self.placeholder_latex_final, font=('Consolas', 10),
                            bg="#ffffff", fg="gray", bd=4, relief='sunken', anchor='center')
        self.latexfinal.grid(row=3, column=0, pady=10, ipadx=10, ipady=10, sticky='ew')

        #botoness
        # frame para los botones 
        boton_frame = Frame(self.master, bg="#2f2d3d")
        boton_frame.pack(pady=(0, 10))


        Button(boton_frame, text="Calcular", font=('Arial', 12),
        bg='#a09ea8', fg='#ffffff', command=self.calcular,
        width=12, height=2).grid(row=0, column=0, padx=10)


        Button(boton_frame, text="Limpiar", font=('Arial', 12),
        bg='#6c6c6c', fg='#ffffff', command=self.limpiar_resultados,
        width=12, height=2).grid(row=0, column=1, padx=10)


        Button(boton_frame, text="Atrás", font=('Arial', 12),
        command=self.main_return, bg='#9e4b4b', fg='white',
        width=12, height=2).grid(row=0, column=2, padx=10)


        
        



    def al_entrar(self, event, widget, placeholder):
        if widget.get() == placeholder:
            widget.delete(0, 'end')
            widget.config(fg="black")

    def al_salir(self, event, widget, placeholder):
        if widget.get() == "":
            widget.insert(0, placeholder)
            widget.config(fg="gray")
            
    def limpiar_resultados(self):
        self.formulavanilla.config(text=self.placeholder_vanilla, fg="gray")
        self.formulabienformada.config(text=self.placeholder_bienformada, fg="gray")
        self.latexfinal.config(text=self.placeholder_latex_final, fg="gray")
    def calcular(self):
        from discretas import ReescritorLogico
        texto = self.entry.get()
        if texto != self.placeholder_entry and texto.strip() != "":
            reescritor = ReescritorLogico(texto)
            reescritor.de_latex_a_formula()
            reescritor.de_formula_a_lista()

            from discretas import ParserLogico 

            parser = ParserLogico(reescritor)
            if parser.Paso0():
                self.formulavanilla.config(text="Fórmula no válida", fg="red")
                self.formulabienformada.config(text="", fg="gray")
                self.latexfinal.config(text="", fg="gray")
                return

            reescritor.nueva_lista = parser.Paso1()
            reescritor.nueva_lista = parser.paso2()
            reescritor.nueva_lista = parser.paso3()

            conversion = reescritor.obtener_conversion()

            self.formulavanilla.config(text=conversion["vanilla"], fg="black")
            self.formulabienformada.config(text=conversion["formula_bien_formada"], fg="black")
            self.latexfinal.config(text=conversion["latex_final"], fg="black")
        else:
            self.formulavanilla.config(text="No se ingresó fórmula", fg="red")

            
    def main_return(self):
        self.master.destroy()
        if self.r_callback:
            self.r_callback()