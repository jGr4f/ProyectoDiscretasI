
Logicalc Calculadibar es una aplicación desarrollada como parte de un proyecto académico en el contexto de la carrera de Ingeniería de Sistemas y Computación. Su propósito es aplicar conceptos aprendidos en lógica proposicional y programación para crear una herramienta interactiva capaz de analizar y estructurar fórmulas lógicas.

El objetivo principal del programa es recibir una fórmula lógica ingresada por el usuario (ya sea mediante botones o escritura manual) y procesarla para obtener su versión bien formada (FBF), respetando la jerarquía de los operadores lógicos (¬, ∧, ∨, →, ↔). Esto incluye añadir los paréntesis necesarios para que la fórmula sea sintácticamente correcta y refleje adecuadamente la precedencia entre los conectivos.

Una vez estructurada correctamente, la herramienta también permite generar una representación en formato LaTeX, facilitando su uso en documentos académicos o presentaciones matemáticas. Esta funcionalidad está pensada especialmente para estudiantes y docentes que trabajan con lógica formal.

El sistema incluye una interfaz gráfica sencilla y funcional, desarrollada con Python y la biblioteca Tkinter, lo que permite un uso intuitivo tanto para usuarios con conocimientos básicos como avanzados en lógica proposicional.



MANUAL DE USUARIO

Al iniciar el programa el usuario tiene dos opciones:

<img width="353" height="248" alt="image" src="https://github.com/user-attachments/assets/ffc760af-3130-486b-9df5-13501e34bf94" />

Al iniciar con botonera: 

1. Se abrirá la calculadora con teclado dispuesto en pantalla. A través del cual el usuario puede escribir la fórmula lógica.
   
<img width="506" height="463" alt="image" src="https://github.com/user-attachments/assets/06cb7aad-6ef6-444c-bee6-1c8d05d001ee" />

2. Para añadir las variables, el usuario puede presionar el botón "var", lo que desplegará un teclado alfabético para añadir variables.

<img width="371" height="307" alt="image" src="https://github.com/user-attachments/assets/7006f53f-80d3-40fa-8153-a337c58c3457" />

3. El usuarió presionará el botón "enter" para que el programa se ejecute sobre la fórmula dada y así genere la fórmula bien formada en formato LaTeX.


Al iniciar con escritura manual: 

1. Se abrirá una ventana nueva con un campo de texto abierto para el usuario.

<img width="807" height="539" alt="image" src="https://github.com/user-attachments/assets/bf16470e-8b0a-41d3-bff2-a6088e895d5c" />

2. El usuario ingresará la fórmula mediante el campo de texto y presionará el botón "calcular" para así ejecutar el programa y generar la fórmula bien formada.

<img width="810" height="538" alt="image" src="https://github.com/user-attachments/assets/c8a13000-3ac9-4a83-b44e-dc23d0b8eef7" />

El programa es resistente a añadir textos distintos a fórmulas o fórmulas con errores.


