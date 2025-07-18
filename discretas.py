import re
#Esta clase se encarga de procesar y traducir el input a diferentes formatos para un analisis más practico, y de la entrega de los resultados en el formato deseado
class ReescritorLogico:
    def __init__(self, expresion: str):
        self.original = expresion
        #Diccionario de reescritura
        self.reescritura = {
            '\\land': '∧', '\\lor': '∨', '\\rightarrow': '→',
            '\\leftrightarrow': '↔', '\\neg': '¬'
        }
        self.devueltaAlatex = {v: k for k, v in self.reescritura.items()}
        #Formula lógica conseguida de aplicar el metodo de latex a formula
        self.formula = ""
        #formula logica transformada en una lista, con cada caracter siendo un elemento
        self.lista_formula = []
        #latex original recibido
        self.latex = ""
        #Esta variable es el objetivo del parser lógico, cada paso será almacenado en esta lista y operado por el siguiente (ex)
        self.nueva_lista = []
        self.nueva_formula = ""
        self.nuevo_latex = ""
#Aqui están todos los metodos que convierten el input en latex a su su versión formula lógica, lista y visceversa
    #el metodo de latex a formula, utiliza el diccionario reescritura para reemplazar las expresiones latex en sus equivalentes logicos (simbolos), además de retirar los $$, para ser agregados posteriormente en el proceso
    def de_latex_a_formula(self):
        expresion = self.original.replace('$', '')
        for clave, valor in self.reescritura.items():
            expresion = expresion.replace(clave, valor)
        self.formula = expresion
        return self.formula
    #El metodo de formula a lista, toma la formula logica y la convierte en una lista utilizando expresiones regulares para convertir cada caracter identificado en un elemento
    def de_formula_a_lista(self):
        if not self.formula:
            self.de_latex_a_formula()
        tokens = re.findall(r'(¬|∧|∨|→|↔|\(|\)|[a-zA-Z]+)', self.formula)
        self.lista_formula = tokens
        return self.lista_formula
    #El metodo de lista a formula, toma la lista en self.formula y la convierte en un string sin espacios
    def de_lista_a_formula(self):
        self.nueva_formula = ''.join(self.nueva_lista)
        return self.nueva_formula
    #El metodo de formula a latex, toma la formula logica y la convierte en una expresion latex
    def de_formula_a_latex(self):
        if not self.formula:
            self.de_latex_a_formula()
        expresion = self.nueva_formula
        for simbolo, latex in self.devueltaAlatex.items():
            expresion = expresion.replace(simbolo, latex)
        # Agregar espacio después de operadores de LaTeX
        expresion = re.sub(
            r'(\\neg|\\lor|\\land|\\rightarrow|\\leftrightarrow)(?![\s\(])',
            r'\1 ',
            expresion
        )
        self.nuevo_latex = f"${expresion}$"
        return self.nuevo_latex
    

    #Metodo utilizado para hacer pruebas del parcer, puede ser eliminado para el producto final 
    def procesar(self):
        print("Expresión original:", self.original)
        print("Expresión como fórmula lógica:", self.de_latex_a_formula())
        print("Lista de componentes:", self.de_formula_a_lista())
        print("Expresión arreglada como lista:",self.nueva_lista)
        print("Expresión arreglada como fórmula lógica:", self.de_lista_a_formula())
        print("Expresión arreglada en sintaxis de LaTeX:", self.de_formula_a_latex())
    def obtener_conversion(self):
        self.de_latex_a_formula()
        self.de_formula_a_lista()
        self.de_lista_a_formula()
        self.de_formula_a_latex()
        return {
            "vanilla": self.formula,
            "lista": self.lista_formula,
            "formula_bien_formada": self.nueva_formula,
            "latex_final": self.nuevo_latex
        }

#En esta clase se ejecuta toda la lógica de Inserción de parentesis para la construcción a una formula lógica bien formada, esto analizando cada elemento en la lista componentes con un for, y analizando los casos posibles
#en base a que elementos se encuentran adyacentes al elemento analizado
class ParserLogico:
    def __init__(self, reescritor : ReescritorLogico):
        self.componentes = reescritor.de_formula_a_lista()      
    #el metodo que separa cada caracter en un elemento individual en la lista, (se utiliza despues de cada uno de los pasos)
    def separador (self):
        listaSeparada= []
        for elemento in self.componentes:
            listaSeparada.extend(list(elemento))
        self.componentes = listaSeparada
        return
    #Estos son metodos auxiliares utlizados para analizar casos posibles utilizados para determinar que elementos se encuentran adyacentes al elemento analizado y como proseguir en base a eso
    # estos 4 metodos solo se usan en paso 2 y paso 3, el paso 1 tiene su propia lógica integrada, debido a que el operador not funciona diferente y no requiere tantas consideraciones
    def NoParentesisCerrado_Adyacente(self,i):
        if i >= 2 and i <= len(self.componentes)-3:
            if "(" in self.componentes[i-2] and ")" in self.componentes[i+2]:
                return True
            else:
                pass
        self.componentes[i-1] = "(" + self.componentes[i-1]
        return False
    def NoParentesisAbierto_Adyacente(self,i,contador_parentesisabiertos1,contador_parentesiscerrados1):
        #aqui si se encuentra un not adyacente, se busca  encerrar toda la expresion encerrada por el not, por ejemplo a → ¬(¬(a)∧¬(b)) se convierta en (a → ¬(¬(a)∧¬(b))), lo mismo con los and, or y si solo si
        #esto lo hace utilizando un for para contar los parentesis abiertos y cerrados hasta que se cierre toda una expresion, este en especifico se utiliza solo para agregar el parentesis cerrado y cerrar la expresión 
        if "¬" in self.componentes[i+1] :
            for j in range(i+2,len(self.componentes)):
                if "(" in self.componentes[j]:
                    contador_parentesisabiertos1 += self.componentes[j].count("(")
                if ")" in self.componentes[j]:
                    contador_parentesiscerrados1 += self.componentes[j].count(")")
                if contador_parentesisabiertos1 == contador_parentesiscerrados1:
                    self.componentes[j] = self.componentes[j] + ")"
                    contador_parentesisabiertos1 = 0
                    contador_parentesiscerrados1 = 0
                    break
        else:
            self.componentes[i+1] = self.componentes[i+1] + ")"
        return contador_parentesisabiertos1,contador_parentesiscerrados1 
    def ParentesisCerrado_adyacente(self,i):
        #logica para encerrar toda una expresion encerrada por parentesis adyacente a la izquierda del operador lógico 
        contador_parentesisabiertos2 = 0
        contador_parentesiscerrados2 = 0
        contador_parentesiscerrados2 += self.componentes[i-1].count(")")
        for h in range(i-2,-1,-1):
            if ")" in self.componentes[h] :
                contador_parentesiscerrados2 += self.componentes[h].count(")")
            if "(" in self.componentes[h]:
                contador_parentesisabiertos2 += self.componentes[h].count("(")
                if contador_parentesiscerrados2 == contador_parentesisabiertos2:
                    if self.componentes[h-1] == "¬":
                        self.componentes[h-1] = "(" + self.componentes[h-1]
                    else:
                            self.componentes[h] = "(" + self.componentes[h]
                            contador_parentesisabiertos2 = 0
                            contador_parentesiscerrados2 = 0
                    break
    def ParentesisAbierto_adyacente(self,i,contador_parentesisabiertos1,contador_parentesiscerrados1):
        #lógica para encerrar toda una expresion encerrada por parentesis adyacente a la derecha del operador lógico
        contador_parentesisabiertos1 += self.componentes[i+1].count("(")
        for h in range (i+2,len(self.componentes)):
            if "(" in self.componentes[h]:
                contador_parentesisabiertos1 += self.componentes[h].count("(")
            if ")" in self.componentes[h]:
                contador_parentesiscerrados1 += self.componentes[h].count(")")
                if contador_parentesisabiertos1 == contador_parentesiscerrados1:
                    self.componentes[h] = self.componentes[h] + ")"
                    contador_parentesisabiertos1 = 0
                    contador_parentesiscerrados1 = 0
                    break
        return contador_parentesisabiertos1, contador_parentesiscerrados1

#Aqui están los metodos que aplican los metodos que estan arriba, y que siguen la lógica de la jerarquia de operadores (primero el not, luego el and y el or y por ultimo si solo si y el entonces)
    #El paso 0 es el que hace las validaciones de si es una formula lógica que es posible pasar a bien formada,  
    def Paso0(self):
        Operadores = ['∧', '∨', '→', '↔']
        conteo_parentesis_Abiertos =  {comp: comp.count('(') for comp in self.componentes}
        conteo_parentesis_Cerrados =  {comp: comp.count(')') for comp in self.componentes}

        if "(" and ")" in self.componentes:
            if conteo_parentesis_Abiertos["("] != conteo_parentesis_Cerrados[")"]:
                return True
        if len(self.componentes) == 1 and self.componentes == [0] in Operadores:
            return True
        numeroOperadores = 0
        numeroVariables = 0
        primerOperador = True
        stackParentesis = []
        for i in range(len(self.componentes)):
            if self.componentes[i] == '(':
                stackParentesis.append('(')
                continue
            elif self.componentes[i] == ')':
                if len(stackParentesis) == 0:
                    return True
                else:
                    stackParentesis.pop()
                    continue
            elif self.componentes[i] == '¬' and i!=0:
                if self.componentes[i-1] not in Operadores and self.componentes[i]!='¬':
                    return True
            elif self.componentes[i] not in Operadores and self.componentes[i]!='¬':
                if len(self.componentes[i]) != 1 or not (97 < ord(self.componentes[i]) < 122):
                    return True
                numeroVariables += 1
                if primerOperador == True:
                    primerOperador = False
                if len(self.componentes[i])!=1:
                    return True
            elif self.componentes[i] in Operadores:
                numeroOperadores += 1
                if primerOperador == True:
                    return True
                elif (self.componentes[i-1] in Operadores) or (self.componentes[i-1] == '¬'):
                        return True
            else:
                continue
        for i in range(len(self.componentes)-1,-1,-1):
                if self.componentes[i] in Operadores and self.componentes[i]!= ')':
                    return True
                elif self.componentes[i] == '¬':
                    return True
                else:
                    break
        if numeroVariables==0:
            return True
        elif numeroOperadores == 0 and numeroVariables!=1:
            return True
        elif numeroVariables!=0:
            if numeroVariables <= numeroOperadores:
                return True
        
        if len(stackParentesis)!=0:
            return True
        ####################
        else:
            for i in range(len(self.componentes)):
                if self.componentes[i] == "ss":
                    return False
                if ((self.componentes[i]  in Operadores) and len(self.componentes ) == 1): 
                    return True
                elif ((self.componentes[i]  in Operadores) and (self.componentes[i+1] in Operadores)):
                    return True
                else:
                    return False
                
        
    #agregar los parentesis para los not
    def Paso1(self):
        contador_parentesis = 0         
        for i in range(len(self.componentes)-1):
            if "¬" in self.componentes[i]: 
                if "("  in self.componentes[i+1]:
                    pass
                elif "¬" in self.componentes[i+1]:
                    self.componentes[i+1] = "(" + self.componentes[i+1]
                    contador_parentesis +=1
                else:
                    if contador_parentesis > 0:
                        self.componentes[i+1] = self.componentes[i+1] + ")"*contador_parentesis
                    self.componentes[i+1] = "(" + self.componentes[i+1] + ")"

        self.separador()
        return self.componentes
    #agregar los parentesis para los and y or (tanto el paso 2 como el paso 3 utilizan la misma lógica)
    def paso2(self):
        contador_parentesisabiertos1 = 0 
        contador_parentesiscerrados1 = 0
        for i in range(len(self.componentes)-1):
            if self.componentes[i] == "∨" or self.componentes[i] == "∧":
                if not ")" in self.componentes[i-1]:
                    if self.NoParentesisCerrado_Adyacente(i) == True:
                        continue
                    else:
                        pass
                if not "(" in self.componentes[i+1] :
                    contador_parentesisabiertos1,contador_parentesiscerrados1 = self.NoParentesisAbierto_Adyacente(i,contador_parentesisabiertos1,contador_parentesiscerrados1)
                if "(" in self.componentes[i+1] :
                    contador_parentesisabiertos1,contador_parentesiscerrados1 = self.ParentesisAbierto_adyacente(i,contador_parentesisabiertos1,contador_parentesiscerrados1)

                if ")" in self.componentes[i-1] :
                    self.ParentesisCerrado_adyacente(i)

        self.separador()            
        return self.componentes
    #agregar los parentesis para los implica y si solo si  (tanto el paso 2 como el paso 3 utilizan la misma lógca)
    def paso3(self):
        contador_parentesisabiertos1 = 0 
        contador_parentesiscerrados1 = 0
        for i in range(len(self.componentes)-1):
            if self.componentes[i] == "→" or self.componentes[i] == "↔":
                if not ")" in self.componentes[i-1]:
                    if i >= 2 and i <= len(self.componentes)-3:
                        if "(" in self.componentes[i-2] and ")" in self.componentes[i+2]:
                            continue
                        else:
                            pass
                    self.componentes[i-1] = "(" + self.componentes[i-1]
                if not "(" in self.componentes[i+1]:
                    contador_parentesisabiertos1,contador_parentesiscerrados1 = self.NoParentesisAbierto_Adyacente(i,contador_parentesisabiertos1,contador_parentesiscerrados1)
                if "(" in self.componentes[i+1] :
                    contador_parentesisabiertos1,contador_parentesiscerrados1 = self.ParentesisAbierto_adyacente(i,contador_parentesisabiertos1,contador_parentesiscerrados1)
                if ")" in self.componentes[i-1] :
                    self.ParentesisCerrado_adyacente(i)
            

        self.separador()            
        return self.componentes

#esto solo es para probar como funciona, realmente en los demás archivos se implementa por aparte
if __name__ == "__main__":
    entrada = input("Ingrese la expresion: ")
    mi_reescritor = ReescritorLogico(entrada)
    mi_parser = ParserLogico(mi_reescritor)
    if mi_parser.Paso0() == True:
        print("Expresion no valida")
    else:
        mi_reescritor.nueva_lista = mi_parser.Paso1()
        mi_reescritor.nueva_lista = mi_parser.paso2()
        mi_reescritor.nueva_lista = mi_parser.paso3() 
        print(mi_reescritor.nueva_lista)
        mi_reescritor.procesar()
        print("Componentes para analizar:", mi_parser.componentes)
