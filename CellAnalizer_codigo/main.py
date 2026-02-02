#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
CellAnalyzer - Pipeline Completo de Segmentación y Análisis
Procesa imágenes microscópicas y calcula índices de citotoxicidad/genotoxicidad
"""

import os
import sys
import numpy as np
from cellpose import models, io as cellpose_io
from model.folder import Folder
from model.image import Image

def segment_images(image_folder, model_path='./membranas_500_125', 
                   diameter=30, channels=[0,0]):
    """
    Segmenta imágenes usando Cellpose
    
    Args:
        image_folder: Ruta de carpeta con imágenes
        model_path: Ruta del modelo entrenado
        diameter: Diámetro esperado de células
        channels: Canales a usar [0,0] = escala de grises
    
    Returns:
        folder: Objeto Folder con imágenes procesadas
    """
    # Cargar modelo de Cellpose
    print(f"Cargando modelo: {model_path}")
    model = models.CellposeModel(gpu=False, pretrained_model=model_path)
    
    # Crear objeto Folder
    folder = Folder(image_folder)
    folder.upload_images(formats=('.jpg', '.png', '.tif', '.tiff'))
    print(f"Imágenes cargadas: {len(folder)}")
    
    # Procesar cada imagen
    for i, img in enumerate(folder.images):
        print(f"Procesando [{i+1}/{len(folder)}]: {img.name}")
        
        # Segmentar con Cellpose
        # CORREGIDO: Algunas versiones devuelven 3 valores en lugar de 4
        result = model.eval(
            img.data, 
            diameter=diameter, 
            channels=channels
        )
        
        # Manejar ambos casos (3 o 4 valores de retorno)
        if len(result) == 4:
            masks, flows, styles, diams = result
        else:  # len(result) == 3
            masks, flows, styles = result
            diams = diameter  # Usar el diámetro especificado
        
        # Guardar máscaras (ejemplo para citoplasma)
        # En tu caso real, necesitarías 3 segmentaciones separadas:
        # - Una para citoplasmas
        # - Una para núcleos
        # - Una para micronúcleos
        
        mask_path = f"./masks/{img.name}_cytoplasm.npy"
        os.makedirs("./masks", exist_ok=True)
        np.save(mask_path, {'masks': masks})
        
        # Cargar máscara en el objeto Image
        img.upload_mask_cytoplasm(mask_path)
    
    return folder

def analyze_folder(folder):
    """
    Analiza imágenes ya segmentadas y calcula índices
    
    Args:
        folder: Objeto Folder con máscaras cargadas
    
    Returns:
        dict con resultados
    """
    # Procesar máscaras
    for img in folder.images:
        # Agregar elementos desde las máscaras
        img.mask_cytoplasm.add_elements()
        img.mask_nucleus.add_elements(cytoplasms=img.mask_cytoplasm.elements)
        img.mask_micronucleus.add_elements(cytoplasms=img.mask_cytoplasm.elements)
        
        # Filtrar elementos válidos
        img.mask_cytoplasm.select_elements(shape=img.data.shape)
        img.mask_nucleus.select_elements(img=img.data, 
                                        cytoplasms=img.mask_cytoplasm.elements)
        img.mask_micronucleus.select_elements(img=img.data,
                                             cytoplasms=img.mask_cytoplasm.elements)
    
    # Calcular índices
    cytotoxicity, genotoxicity = folder.calculate_indices()
    
    return {
        'cytotoxicity_index': cytotoxicity,
        'genotoxicity_index': genotoxicity,
        'total_images': len(folder),
        'total_cytoplasms': sum(len(img.mask_cytoplasm.elements) for img in folder.images),
        'total_nuclei': sum(img.mask_nucleus.total_elements for img in folder.images),
        'total_binucleate': sum(img.mask_nucleus.total_binucleate for img in folder.images),
        'total_trinucleate': sum(img.mask_nucleus.total_trinucleate for img in folder.images),
        'total_micronuclei': sum(img.mask_micronucleus.total_micronucleus for img in folder.images)
    }

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <carpeta_imagenes> [opciones]")
        print("\nOpciones:")
        print("  --segment    : Ejecutar segmentación con Cellpose")
        print("  --analyze    : Solo analizar máscaras existentes")
        print("  --model PATH : Ruta del modelo (default: ./membranas_500_125)")
        print("  --diameter N : Diámetro esperado (default: 30)")
        print("\nEjemplos:")
        print("  python main.py ./imagenes/ --segment")
        print("  python main.py ./imagenes/ --analyze")
        print("  python main.py ./imagenes/ --segment --model ./mi_modelo --diameter 40")
        sys.exit(1)
    
    image_folder = sys.argv[1]
    do_segment = '--segment' in sys.argv
    do_analyze = '--analyze' in sys.argv or not do_segment
    
    # Obtener parámetros opcionales
    model_path = './membranas_500_125'
    diameter = 30
    
    if '--model' in sys.argv:
        idx = sys.argv.index('--model')
        if idx + 1 < len(sys.argv):
            model_path = sys.argv[idx + 1]
    
    if '--diameter' in sys.argv:
        idx = sys.argv.index('--diameter')
        if idx + 1 < len(sys.argv):
            diameter = int(sys.argv[idx + 1])
    
    # Si no especifica, hacer ambos
    if not do_segment and not do_analyze:
        do_segment = True
        do_analyze = True
    
    # Segmentación
    if do_segment:
        print("\n=== FASE 1: SEGMENTACIÓN ===")
        folder = segment_images(image_folder, model_path=model_path, diameter=diameter)
    else:
        # Solo cargar imágenes y máscaras existentes
        folder = Folder(image_folder)
        folder.upload_images()
        # TODO: Cargar máscaras desde archivos
    
    # Análisis
    if do_analyze:
        print("\n=== FASE 2: ANÁLISIS ===")
        results = analyze_folder(folder)
        
        print("\n=== RESULTADOS ===")
        print(f"Total de imágenes:        {results['total_images']}")
        print(f"Total de citoplasmas:     {results['total_cytoplasms']}")
        print(f"Total de núcleos:         {results['total_nuclei']}")
        print(f"  - Binucleadas:          {results['total_binucleate']}")
        print(f"  - Trinucleadas:         {results['total_trinucleate']}")
        print(f"Total de micronúcleos:    {results['total_micronuclei']}")
        print(f"\nÍndice de Citotoxicidad:  {results['cytotoxicity_index']:.4f}")
        print(f"Índice de Genotoxicidad:  {results['genotoxicity_index']:.4f}")
        
        # Guardar resultados visuales
        output_path = os.path.join(image_folder, "resultados")
        os.makedirs(output_path, exist_ok=True)
        folder.save_images(output_path, flag_mask=0b1111)
        print(f"\nResultados guardados en: {output_path}")

if __name__ == "__main__":
    main()