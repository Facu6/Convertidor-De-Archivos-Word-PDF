# CONVERTIDOR DE ARCHIVOS

## Descripción
Este proyecto es una aplicación web desarrollada con Streamlit que permite la conversión de archivos:

- **Convertir Word a PDF**
- **Convertir PDF a Word**
- **Unir múltiples archivos PDF en uno solo**

## Funcionalidades 

### Convertir Word a PDF 

- Cargar uno o varios archivos "docx" (ya sea seleccionando individualmente o detallando la carpeta donde se encuentran los archivos).
- Ingresar la carpeta de destino donde se descargarán los nuevos PDFs convertidos.

### Convertir PDF a Word

- Cargar uno o varios archivos ".pdf".
- Los archivos ".docx" se descargarán en la carpeta actual que se encuentran los PDFs.

### Unir múltiples archivos PDF en uno solo

- Cargar varios archivos PDF .
- Ordenar los archivos en la posición deseada, para que una vez unidos, sigan respetando el orden especificado.
- Ingresar la carpeta de destino donde se descargará el nuevo PDF.


## Instalación

Para ejecutar este proyecto localmente, sigue estos pasos: 

1. **Clona el repositorio:**

git clone https://github.com/Facu6/Convertidor-De-Archivos-Word-PDF.git
cd tu-repositorio

2. **Crea un entorno virtual e instálalo**

python -m venv venv
venv\Scripts\activate 

3. **Instala las dependencias**

pip install -r requirements.txt

4. **Ejecuta la aplicación**

streamlit run app.py

## Ejemplo de uso

1. Ejecuta la aplicación y abre el navegador en la dirección proporcionada por Streamlit.
2. Selecciona la opción deseada en el menú lateral:

    - Convertidor Word a PDF
    - Convertidor PDF a Word
    - Unir PDFs

3. Carga los archivos correspondientes y haz clic en "Convertir".
4. Descarga los archivos convertidos.

## Estructura del Proyecto

.
├── images
│   ├── PDF_Word.png
│   ├── Union_PDFs.png
│   └── Word_PDF.png
├── app.py
├── requirements.txt
└── README.md

- **images**
    Carpeta con las imagenes del deploy en Streamlit.

- **app.py**
    Este archivo contiene todo el código necesario para interfaz y la lógica de conversión de archivos utilizando Streamlit.

- **requirements.txt**
    Contiene todas las dependencias necesarias para ejecutar el proyecto.

## Contribución 

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama nueva (git checkout -b feature/nueva-funcionalidad).
3. Realiza tus cambios y haz commit (git commit -am 'Agrega nueva funcionalidad').
4. Sube la rama (git push origin feature/nueva-funcionalidad).
Abre un Pull Request.

## Contacto

📫 Puedes encontrarme en:
- [LinkedIn](https://www.linkedin.com/in/facundo-dispenza-2ab560298/) 
- [Email](mailto:dispenzafacu6@gmail.com).