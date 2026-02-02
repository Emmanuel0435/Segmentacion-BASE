import os

# Ruta donde Cellpose guarda sus modelos
ruta = os.path.expanduser(r"~\.cellpose\models")

# Crear la carpeta si no existe
os.makedirs(ruta, exist_ok=True)

# Lista completa de nombres de archivos que Cellpose intenta descargar
archivos = [
    "cyto_0", "cyto_1", "cyto_2", "cyto_3",
    "size_cyto_0.npy",
    "cytotorch_0", "cytotorch_1", "cytotorch_2", "cytotorch_3",
    "size_cytotorch_0.npy",
    "cyto2torch_0", "cyto2torch_1", "cyto2torch_2", "cyto2torch_3",
    "size_cyto2torch_0.npy",
    "nuclei_0", "nuclei_1", "nuclei_2", "nuclei_3",
    "size_nuclei_0.npy",
    "nucleitorch_0", "nucleitorch_1", "nucleitorch_2", "nucleitorch_3",
    "size_nucleitorch_0.npy"
]

for nombre in archivos:
    ruta_archivo = os.path.join(ruta, nombre)
    # Crear archivo vacío si no existe
    if not os.path.exists(ruta_archivo):
        with open(ruta_archivo, "wb") as f:
            pass

print("Todos los modelos fueron creados correctamente en:", ruta)