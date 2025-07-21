from tkinter import *
from interfaz import RecibeLatex, LogiCalcApp
import os


class VentanaInicio:
    def __init__(self, master):
        self.master = master

        # Intentar cargar el ícono
        try:
            ruta_icono = os.path.join(os.path.dirname(__file__), "icono.ico")
            self.master.iconbitmap(ruta_icono)
        except Exception as e:
            print(f"Advertencia: no se pudo cargar el icono. {e}")
        
        self.master.title("Logicalc Calculadibar")
        self.master.geometry("300x200")
        self.master.config(bg="#2f2d3d")
        
        Label(master, text="Selecciona una opción", font=('Arial', 14), bg="#2f2d3d", fg="white").pack(pady=20)
        Button(master, text="Escritura con botonera", font=('Arial', 12), command=self.abrir_logicalc).pack(pady=10)
        Button(master, text="Escritura Manual", font=('Arial', 12), command=self.abrir_otra_opcion).pack(pady=10)
        
        self.centrar_ventana(300, 200)

    def centrar_ventana(self, ancho, alto):
        pantalla_ancho = self.master.winfo_screenwidth()
        pantalla_alto = self.master.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.master.geometry(f"{ancho}x{alto}+{x}+{y}")

    def abrir_logicalc(self):
        self.master.destroy()
        nueva_ventana = Tk()
        LogiCalcApp(nueva_ventana, self.main_return)

    def abrir_otra_opcion(self):
        self.master.destroy()
        nueva_ventana = Tk()
        RecibeLatex(nueva_ventana, self.main_return)

    def main_return(self):  # pa volver al mm uwu
        nueva_ventana = Tk()
        VentanaInicio(nueva_ventana)


if __name__ == "__main__":
    root = Tk()
    VentanaInicio(root)
    root.mainloop()
