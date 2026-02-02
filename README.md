Este es un código base para poder moverle como queramos al main y basicamente cualquier experimento que queramos hacer
Igual pueden leer el archivo "Analisis_Completo_CellAnalizer.docx" para entender un poquito más a fondo el contenido

EXPLICACIÓN DE LAS CARPETAS:
    - Cellpose
        Contiene las funciones y todas las bases para la segmentación

    - Imágenes
        Aqui pueden subir cuantas fotos de celulas que quieran para hacer las pruebas

    - model
        Carpeta de la que se asiste cellpose para obtener los modelos entrenados de IA (o eso entendí jaja)

    - crear_modelos
        Este fue el que creó Erick a inicios de cuando descargamos CellAnalyzer

    - membranas_500_125
        NO TOCAR ESTE ARCHIVO
        NO TOCAR ESTE ARCHIVO
        NO TOCAR ESTE ARCHIVO
        NO TOCAR ESTE ARCHIVO
        NO TOCAR ESTE ARCHIVO

        ES EL ARCHIVO DE REENTRENAMIENTO
    
    - estructura.txt 
        Es tal cual el arbol de como se estructura el proyecto, por si les sirve y quieren pasarselo a una IA

    - main.py
        Este como tal es una base, pero pueden borrarlo y experimentar cuanto quieran
        Este main al ejecutarlo creará una carpeta llamada "masks" donde hará una mascara en un archivo .npy
        Para que no se me asusten