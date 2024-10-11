import streamlit as st
import os
import pythoncom
import PyPDF2
from docx2pdf import convert
from pdf2docx import Converter

def generador_nombre_unico(carpeta, nombre_base):
    """
    Genera un nombre único para un archivo PDF para evitar sobreescritura.
    
    Parámetros:
    carpeta (str): Ruta de la carpeta donde se guardará el archivo.
    nombre_base (str): Nombre base del archivo sin extensión.
    
    Retorna:
    str: Ruta completa del archivo con un nombre único.
    """
    contador = 0 
    nombre_archivo = f'{nombre_base}.pdf'
    ruta_archivo = os.path.join(carpeta, nombre_archivo)
    while os.path.exists(ruta_archivo):
        contador += 1
        nombre_archivo = f'{nombre_base}_{contador}.pdf'
        ruta_archivo = os.path.join(carpeta, nombre_archivo)
    return ruta_archivo

def convertidor_archivos(carpeta_origen, carpeta_destino, archivos_docx_individuales=None):
    """
    Convierte archivos .docx a PDF y los guarda en la carpeta destino.
    
    Parámetros:
    carpeta_origen (str): Carpeta que contiene archivos .docx.
    carpeta_destino (str): Carpeta donde se guardarán los archivos PDF.
    archivos_docx_individuales (list): Lista de archivos .docx individuales a convertir.
    """
    # Inicializar COM
    pythoncom.CoInitialize()

    # Si se proporcionan archivos .docx individuales
    if archivos_docx_individuales:
        temp_folder = "temp"
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
        for archivo in archivos_docx_individuales:
            # Guardar el archivo subido en una ruta temporal
            archivo_temp = os.path.join('temp', archivo.name)
            with open(archivo_temp, 'wb') as f:
                f.write(archivo.getbuffer())
            
            # Convertir el archivo temporal a PDF y guardarlo en la carpeta de destino
            convert(archivo_temp, carpeta_destino)
            
            # Eliminar el archivo temporal después de la conversión
            os.remove(archivo_temp)
            
        st.success('¡Conversión realizada con éxito!')
        
    # Si se proporciona una carpeta de origen con archivos .docx
    elif os.path.isdir(carpeta_origen):
        archivos_docx = [archivo for archivo in os.listdir(carpeta_origen) if archivo.endswith('.docx')]
        for archivo in archivos_docx:
            convert(os.path.join(carpeta_origen, archivo), carpeta_destino)
            st.write(f'* El archivo --{archivo}-- ha sido convertido con éxito a PDF. \nEl mismo ha sido guardado en la ruta --{carpeta_destino}--.')
    
        st.success('¡Conversión realizada con éxito!')
    
    else:
        st.write('ERROR: No se encontró la carpeta y/o el archivo.')
    
    # Desinicializar COM
    pythoncom.CoUninitialize()

def unir_pdfs(lista_archivos_pdf, carpeta_destino_pdf, nombre_base='pdfs_unidos'):
    """
    Une múltiples archivos PDF en uno solo y lo guarda en la carpeta destino.
    
    Parámetros:
    lista_archivos_pdf (list): Lista de archivos PDF a unir.
    carpeta_destino_pdf (str): Carpeta donde se guardará el archivo PDF unido.
    nombre_base (str): Nombre base del archivo PDF unido.
    """
    # Crear un objeto PdfWriter
    pdf_writer = PyPDF2.PdfWriter()
    
    # Iterar a través de los archivos PDF
    if lista_archivos_pdf:
        for archivo in lista_archivos_pdf:
            pdf_reader = PyPDF2.PdfReader(archivo)
            for pagina in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[pagina])
        
        archivo_salida = generador_nombre_unico(carpeta_destino_pdf, nombre_base)
      
        with open(archivo_salida, 'wb') as salida:
            pdf_writer.write(salida)
        
        st.success('¡Unión realizada con éxito!')
    else:
        st.write(f"La ruta {lista_archivos_pdf} no es válida.")

def convertir_pdf_word(pdf, nombre_salida):
    """
    Convierte un archivo PDF a Word y lo guarda con el nombre especificado.
    
    Parámetros:
    pdf (UploadedFile): Archivo PDF subido.
    nombre_salida (str): Nombre del archivo de salida .docx.
    """
    # Guarda el archivo PDF subido en una ubicación temporal
    with open(pdf.name, "wb") as f:
        f.write(pdf.getbuffer())
    
    # Crea un convertidor para el archivo PDF subido
    cv = Converter(pdf.name)
    cv.convert(nombre_salida, start=0, end=None)
    cv.close()

def main():
    st.sidebar.title('Navegación')
    app_mode = st.sidebar.selectbox('Elige una opción', ['Convertidor Word a PDF', 'Convertidor PDF a Word', 'Unir PDFs'])
    
    if app_mode == 'Convertidor Word a PDF':
        st.title('Convertidor Word a PDF')
        # Input del usuario para seleccionar archivos ".docx"
        archivos_docx_individuales = st.file_uploader('Seleccione archivos Word', type='docx', accept_multiple_files=True)

        # Inputs del usuario para seleccionar carpeta_origen y carpeta_destino
        carpeta_origen = st.text_input('En caso de desear convertir varios archivos de una sola carpeta, ingrese dicha carpeta.') 
        carpeta_destino = st.text_input('Ingrese la carpeta destino donde se guardarán los archivos PDF.')     
            
        # Botón para iniciar la conversión
        if st.button('Convertir'):
            if not archivos_docx_individuales and not carpeta_origen:
                st.error('Por favor, seleccione un archivo Word o una carpeta que contenga archivos Word.')
            elif not carpeta_destino:
                st.error('Por favor, ingrese la ruta con la carpeta de destino donde se guardarán los archivos PDF.')
            else:
                convertidor_archivos(carpeta_origen, carpeta_destino, archivos_docx_individuales)
    
    if app_mode == 'Convertidor PDF a Word':
        st.title('Convertidor PDF a Word')
        
        lista_archivos_word = st.file_uploader('Seleccione los archivos PDF para convertir:', type='pdf', accept_multiple_files=True)
            
        if st.button('Convertir'):
            if not lista_archivos_word:
                st.error('Seleccione un archivo.')
            else:
                for archivo in lista_archivos_word:
                    nombre_salida = f'{archivo.name[:-4]}.docx'
                    convertir_pdf_word(archivo, nombre_salida)
                    st.success(f'El archivo {archivo.name} fue convertido con éxito.')
        
    if app_mode == 'Unir PDFs':
        st.title('Unir PDFs')
        lista_archivos_pdf = st.file_uploader('Seleccione archivos PDF', type='pdf', accept_multiple_files=True)
        carpeta_destino_pdf = st.text_input('Ingrese la carpeta destino donde se guardarán los archivos PDF.')
        
        if lista_archivos_pdf:
            archivos_nombres = [archivo.name for archivo in lista_archivos_pdf]
            archivos_seleccionados = st.multiselect('Ordenar archivos:', options=archivos_nombres)
            archivos_ordenados = [archivo for nombre in archivos_seleccionados for archivo in lista_archivos_pdf if archivo.name == nombre]
        
            if st.button('Unir'):
                if not archivos_ordenados:
                    st.error('Por favor, seleccione PDF para unir.')
                elif not carpeta_destino_pdf:
                    st.error('Por favor, ingrese la ruta con la carpeta de destino donde se guardarán los archivos PDF.')
                else:
                    unir_pdfs(archivos_ordenados, carpeta_destino_pdf)

if __name__ == "__main__":
    main()
