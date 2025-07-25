
# **Generador de Cotizaciones - GCsoft**

Bienvenido al generador de cotizaciones. Esta aplicación te permite crear cotizaciones personalizadas para clientes, seleccionar productos y proveedores, y generar documentos en formato PDF con un diseño profesional y detallado.

## **Requisitos**

Para ejecutar la aplicación, necesitarás tener instalados los siguientes paquetes:

- **PyQt5**: Para la interfaz gráfica.
- **Pandas**: Para manejar los datos de clientes, productos y proveedores.
- **ReportLab**: Para generar los archivos PDF de las cotizaciones.
- **Pillow (PIL)**: Para manejar la imagen del logo en las cotizaciones.

Puedes instalar las dependencias utilizando pip:

```bash
pip install pyqt5 pandas reportlab pillow
```

## **Características**

- **Interfaz gráfica intuitiva**: La aplicación está construida con PyQt5, permitiendo agregar productos, elegir clientes y proveedores, y generar cotizaciones en un entorno cómodo.
- **Generación de cotizaciones**: La cotización se genera en formato PDF con toda la información necesaria: cliente, productos, precios, y un total detallado.
- **Persistencia de datos**: Los datos de clientes, productos y proveedores se cargan desde un archivo Excel, y el número de presupuesto se maneja automáticamente.
- **Personalización de cotizaciones**: La cotización incluye el logo de la empresa, el número de presupuesto, y detalles del cliente.
- **Fácil gestión**: Puedes agregar productos al presupuesto, ver los detalles antes de generar la cotización y reiniciar los campos con un solo clic.

## **Instrucciones de uso**

1. **Cargar los datos**:
    - El sistema carga la información desde un archivo Excel (`base_datos.xlsx`) que contiene tres hojas: "Clientes", "Productos" y "Proveedores".
    - El archivo Excel debe tener las siguientes columnas:
        - **Clientes**: Nombre del cliente.
        - **Productos**: Nombre y precio de los productos.
        - **Proveedores**: Nombre de los proveedores.

2. **Añadir productos**:
    - Selecciona un cliente, producto, proveedor y la cantidad deseada.
    - El precio unitario se actualizará automáticamente cuando selecciones un producto.
    - Haz clic en "Agregar Producto" para agregarlo a la tabla.

3. **Generar cotización**:
    - Una vez hayas agregado todos los productos necesarios, haz clic en "Generar Cotización".
    - La cotización se generará en formato PDF, con un número único que se incrementa automáticamente y se guardará en una carpeta llamada `presupuestos` en tu escritorio.

4. **Nuevo presupuesto**:
    - Si deseas crear un nuevo presupuesto, haz clic en "Nuevo Presupuesto" para limpiar los campos y la tabla.

## **Estructura de Archivos**

```plaintext
.
├── base_datos.xlsx      # Archivo con la base de datos de clientes, productos y proveedores
├── logo.png             # Imagen del logo de la empresa (opcional)
├── numero_presupuesto.txt  # Archivo con el número de presupuesto actual
└── cotizacion_app.py    # El script de la aplicación principal
```

## **Notas Importantes**

- El archivo Excel debe estar en la misma carpeta que el script de la aplicación.
- Si el archivo `numero_presupuesto.txt` no existe, la aplicación creará uno automáticamente.
- El archivo generado en PDF será guardado en la carpeta `presupuestos` en el escritorio del usuario.

## **Contribuciones**

Si deseas contribuir a este proyecto, ¡adelante! Puedes hacer un fork del repositorio y enviar un pull request con tus mejoras. 

## **Licencia**

Este proyecto está licenciado bajo los términos de la licencia **MIT**. Puedes ver más detalles en el archivo `LICENSE`.
#   c r i s p y - S Q l i t e  
 