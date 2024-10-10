import streamlit as st
import os
import pythoncom
import PyPDF2
from docx2pdf import convert
from pdf2docx import Converter

def generador_nombre_unico(carpeta, nombre_base):
    
    contador = 0 
    nombre_archivo = f'{nombre_base}.pdf'
    ruta_archivo = os.path.join(carpeta, nombre_archivo)
    while os.path.exists(ruta_archivo):
        contador += 1
        nombre_archivo = f'{nombre_base}_{contador}.pdf'
        ruta_archivo = os.path.join(carpeta, nombre_archivo)
    return ruta_archivo


def convertidor_archivos(carpeta_origen, carpeta_destino, archivos_docx_individuales = None):

    # Inicializar COM
    pythoncom.CoInitialize()

    # Condicional para manejar archivos "docx" indivuales    
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
            st.write(f'* El archivo --{archivo_temp}-- ha sido convertido con éxito a PDF. \nEl mismo ha sido guardado en la ruta --{carpeta_destino}--.')
            
            # Eliminar el archivo temporal despues de la conversión
            os.remove(archivo_temp)
            
        st.success('Conversión realizada con éxito!')
        
    # Condicional para manejar carpetas con archivos "docx"     
    elif os.path.isdir(carpeta_origen):
        archivos_docx = [archivo for archivo in os.listdir(carpeta_origen) if archivo.endswith('.docx')]
        for archivo in archivos_docx:
            convert(archivo, carpeta_destino)
            st.write(f'* El archivo --{archivo}-- ha sido convertido con exito a PDF. \nEl mismo ha sido guardado en la ruta --{carpeta_destino}--.')
    
        st.success('Conversión realizada con éxito!')
    
    else:
        st.write('ERROR: No se encontró la carpeta y/o el archivo.')
    
    # Desinizializar COM
    pythoncom.CoUninitialize()
    

def unir_pdfs(lista_archivos_pdf, carpeta_destino_pdf, nombre_base = 'pdfs_unidos'):
    
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
        
        st.success('Unión realizada con éxito!')
        
    else:
        st.write(f"La ruta {lista_archivos_pdf} no es un válida.")


def convertir_pdf_word(pdf, nombre_salida):
    
    cv = Converter(pdf)
    cv.convert(nombre_salida, start = 0, end = None)
    cv.close()
    
    

def main():
    st.sidebar.title('Navegación')
    app_mode = st.sidebar.selectbox('Elige una opción', ['Convertidor Word a PDF', 'Convertidor PDF a Word', 'Unir PDFs'])
    
    if app_mode == 'Convertidor Word a PDF':
        st.title('Convertidor Word a PDF')
        # Input del usuario para seleccionar archivos ".docx"
        archivos_docx_individuales = st.file_uploader('Seleccione archivos word', type = 'docx', accept_multiple_files= True)

        # Inputs del usuario para seleccionar carpeta_origen y carpeta_destino
        carpeta_origen = st.text_input('Ingrese la ruta de la carpeta donde se encuentran los archivos ".docx"') 
        carpeta_destino = st.text_input('Ingrese la carpeta destino donde se guardarán los archivos PDF.')     
            
            
        # Boton para iniciar la conversación 
        if st.button('Convertir'):
            if not archivos_docx_individuales and not carpeta_origen:
                st.error('Por favor, seleccione un archivo Word o una carpeta la cual posea archivos Word.')
            elif not carpeta_destino:
                st.error('Por favor, ingrese la ruta con la carpeta de destino donde se descargarán los archivos PDF.')
            else:
                convertidor_archivos(carpeta_origen, carpeta_destino, archivos_docx_individuales)
    
    if app_mode == 'Convertidor PDF a Word':
        
        st.title('Convertidor PDF a Word')
        
        lista_archivos_word = st.file_uploader('Seleccione los archivos PDF para convertir:', type = 'pdf', accept_multiple_files= True)

            
        if st.button('Convertir'):
            if not lista_archivos_word:
                st.error('Seleccione un archivo.')
            else:
                for archivo in lista_archivos_word:
                    nombre_salida = f'{archivo.name[:-4]}.docx'
                    convertir_pdf_word(archivo, nombre_salida)  # Aquí 'archivo' es el objeto del archivo subido

                    st.success(f'El archivo {archivo.name} fue convertido con éxito.')
        
    if app_mode == 'Unir PDFs':
        st.title('Unir PDFs')
        # Input del usuario para seleccionar archivos ".docx"
        lista_archivos_pdf = st.file_uploader('Seleccione archivos PDF', type = 'pdf', accept_multiple_files= True)
               
        # Input del usuario para seleccionar la carpeta de destino
        carpeta_destino_pdf = st.text_input('Ingrese la carpeta destino donde se guardarán los archivos PDF.')     
        
        if lista_archivos_pdf:
            # Mostrar los archivos cargados en una selección
            archivos_nombres = [archivo.name for archivo in lista_archivos_pdf]
            archivos_seleccionados = st.multiselect('Ordenar archivos:', options=archivos_nombres)

            # Reordenar archivos según la selección
            archivos_ordenados = [archivo for nombre in archivos_seleccionados 
                                for archivo in lista_archivos_pdf 
                                if archivo.name == nombre]
        
            # Boton para iniciar la conversación 
            if st.button('Unir'):
                if not archivos_ordenados:
                    st.error('Por favor, seleccione PDF para ser unido.')
                elif not carpeta_destino_pdf:
                    st.error('Por favor, ingrese la ruta con la carpeta de destino donde se descargarán los archivos PDF.')
                else:
                    unir_pdfs(lista_archivos_pdf, carpeta_destino_pdf)        


        
if __name__ == "__main__":
    main()