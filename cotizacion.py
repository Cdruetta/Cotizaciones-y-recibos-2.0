import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QInputDialog,
    QComboBox,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QApplication,
    QLabel,
    QGroupBox,
    QHeaderView,
)
from PyQt5.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt5.QtCore import QUrl, Qt, QTimer
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from db import obtener_clientes, obtener_productos, agregar_cliente, guardar_presupuesto


def obtener_ruta_archivo(nombre_archivo):
    if getattr(sys, "frozen", False):
        ruta = os.path.join(sys._MEIPASS, nombre_archivo)
    else:
        ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    return ruta


class CotizacionApp(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Generador de Cotizaciones y Recibos")
        self.setGeometry(100, 100, 800, 500)

        self.ultima_ruta_documento = None  # Ruta del último documento generado

        # Establecer ícono de la aplicación si existe
        icono_path = obtener_ruta_archivo("img/logo.ico")
        if os.path.exists(icono_path):
            self.setWindowIcon(QIcon(icono_path))

        # Layout principal
        self.layout = QVBoxLayout()

        # Layout horizontal para logo y leyenda
        logo_leyenda_layout = QHBoxLayout()

        self.logo_label = QLabel()
        pixmap = QPixmap(obtener_ruta_archivo("img/logo.png")).scaledToWidth(150)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.leyenda_label = QLabel(
            "SERVICIOS INFORMÁTICOS 💻\nDilkendein 1278 - Tel: 358-4268768"
        )
        self.leyenda_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        logo_leyenda_layout.addWidget(self.logo_label)
        logo_leyenda_layout.addWidget(self.leyenda_label)
        logo_leyenda_layout.setSpacing(5)

        self.layout.addLayout(logo_leyenda_layout)

        # --- Campos para mostrar información del cliente (solo lectura) --- #
        self.direccion_input = QLineEdit()
        self.direccion_input.setReadOnly(True)
        self.telefono_input = QLineEdit()
        self.telefono_input.setReadOnly(True)
        self.localidad_input = QLineEdit()
        self.localidad_input.setReadOnly(True)

        # Agrupación visual para los datos del cliente
        self.group_datos_cliente = QGroupBox("")
        self.layout_datos_cliente = QFormLayout()
        self.layout_datos_cliente.addRow("Dirección:", self.direccion_input)
        self.layout_datos_cliente.addRow("Teléfono:", self.telefono_input)
        self.layout_datos_cliente.addRow("Localidad:", self.localidad_input)
        self.group_datos_cliente.setLayout(self.layout_datos_cliente)

        # --- Diccionarios para almacenar productos seleccionados y sus precios --- #
        self.productos_precios = {}  # {descripcion: precio}
        self.productos_agregados = []  # lista de productos agregados al documento

        # --- Campos de entrada principales --- #
        self.cliente_dropdown = QComboBox()
        self.producto_dropdown = QComboBox()
        self.proveedor_dropdown = QComboBox()
        self.cantidad_input = QLineEdit()
        self.precio_input = QLineEdit()
        self.precio_input.setReadOnly(True)

        self.tipo_documento_dropdown = QComboBox()
        self.tipo_documento_dropdown.addItems(["Presupuesto", "Recibo"])

        # Layout del formulario principal
        self.form_layout = QFormLayout()
        self.form_layout.addRow("Cliente:", self.cliente_dropdown)
        self.form_layout.addRow(self.group_datos_cliente)
        self.form_layout.addRow("Producto:", self.producto_dropdown)
        self.form_layout.addRow("Proveedor:", self.proveedor_dropdown)
        self.form_layout.addRow("Cantidad:", self.cantidad_input)
        self.form_layout.addRow("Precio Unitario:", self.precio_input)
        self.form_layout.addRow("Tipo de Documento:", self.tipo_documento_dropdown)

        self.agregar_producto_btn = QPushButton("Agregar Producto")
        self.generar_btn = QPushButton("Generar Documento")
        self.nuevo_presupuesto_btn = QPushButton("Nuevo Documento")
        self.ir_carpeta_btn = QPushButton("Abrir carpeta del documento")
        self.ir_carpeta_btn.setEnabled(False)

        self.agregar_producto_btn.setMinimumHeight(50)
        self.generar_btn.setMinimumHeight(50)
        self.nuevo_presupuesto_btn.setMinimumHeight(50)
        self.ir_carpeta_btn.setMinimumHeight(50)

        # botones cliente
        self.agregar_cliente_btn = QPushButton("+ Cliente")
        self.modificar_cliente_btn = QPushButton("✎ Modificar Cliente")
        self.modificar_cliente_btn.setObjectName("btnModificar")
        self.eliminar_cliente_btn = QPushButton("✖ Eliminar Cliente")
        self.eliminar_cliente_btn.setObjectName("btnEliminar")

        # botones producto
        self.agregar_producto_db_btn = QPushButton("+ Producto")
        self.modificar_producto_btn = QPushButton("✎ Modificar Producto")
        self.modificar_producto_btn.setObjectName("btnModificar")
        self.eliminar_producto_btn = QPushButton("✖ Eliminar Producto")
        self.eliminar_producto_btn.setObjectName("btnEliminar")

        # botones proveedor
        self.agregar_proveedor_btn = QPushButton("+ Proveedor")
        self.modificar_proveedor_btn = QPushButton("✎ Modificar Proveedor")
        self.modificar_proveedor_btn.setObjectName("btnModificar")
        self.eliminar_proveedor_btn = QPushButton("✖ Eliminar Proveedor")
        self.eliminar_proveedor_btn.setObjectName("btnEliminar")

        self.agregar_cliente_btn.clicked.connect(self.abrir_dialogo_cliente)
        self.modificar_cliente_btn.clicked.connect(self.modificar_cliente)
        self.eliminar_cliente_btn.clicked.connect(self.eliminar_cliente)
        self.agregar_producto_db_btn.clicked.connect(self.abrir_dialogo_producto)
        self.modificar_producto_btn.clicked.connect(self.modificar_producto)
        self.eliminar_producto_btn.clicked.connect(self.eliminar_producto)
        self.agregar_proveedor_btn.clicked.connect(self.abrir_dialogo_proveedor)
        self.modificar_proveedor_btn.clicked.connect(self.modificar_proveedor)
        self.eliminar_proveedor_btn.clicked.connect(self.eliminar_proveedor)

        action_btns_layout = QHBoxLayout()
        action_btns_layout.addWidget(self.agregar_producto_btn)
        action_btns_layout.addWidget(self.generar_btn)
        action_btns_layout.addWidget(self.nuevo_presupuesto_btn)
        action_btns_layout.addWidget(self.ir_carpeta_btn)

        # Layout vertical para botones de clientes
        clientes_layout = QVBoxLayout()
        clientes_layout.addWidget(self.agregar_cliente_btn)
        clientes_layout.addWidget(self.modificar_cliente_btn)
        clientes_layout.addWidget(self.eliminar_cliente_btn)

        # Layout vertical para botones de productos
        productos_layout = QVBoxLayout()
        productos_layout.addWidget(self.agregar_producto_db_btn)
        productos_layout.addWidget(self.modificar_producto_btn)
        productos_layout.addWidget(self.eliminar_producto_btn)

        # Layout vertical para botones de proveedores
        proveedores_layout = QVBoxLayout()
        proveedores_layout.addWidget(self.agregar_proveedor_btn)
        proveedores_layout.addWidget(self.modificar_proveedor_btn)
        proveedores_layout.addWidget(self.eliminar_proveedor_btn)

        # Layout horizontal principal que contiene todas las secciones
        btns_layout = QHBoxLayout()
        btns_layout.addLayout(clientes_layout)
        btns_layout.addSpacing(30)  # espacio entre secciones
        btns_layout.addLayout(productos_layout)
        btns_layout.addSpacing(30)  # espacio entre secciones
        btns_layout.addLayout(proveedores_layout)

        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(btns_layout)
        self.layout.addLayout(action_btns_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Producto", "Proveedor", "Cantidad", "Precio Unitario", "Total"]
        )
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setDefaultSectionSize(30)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.agregar_producto_btn.clicked.connect(self.agregar_producto)
        self.generar_btn.clicked.connect(self.generar_documento)
        self.nuevo_presupuesto_btn.clicked.connect(self.nuevo_presupuesto)
        self.ir_carpeta_btn.clicked.connect(self.abrir_carpeta_documento)

        self.producto_dropdown.currentTextChanged.connect(
            self.actualizar_precio_unitario
        )
        self.cliente_dropdown.currentTextChanged.connect(self.actualizar_datos_cliente)

        self.frases = [
            "El éxito es la suma de pequeños esfuerzos repetidos cada día - GCsoft-2025 🌟",
            "Confía en el proceso - GCsoft-2025 🔄",
            "Hazlo con pasión o no lo hagas - GCsoft-2025 ❤️🔥",
            "La constancia supera al talento - GCsoft-2025 ⏳💪",
            "Tu actitud determina tu dirección - GCsoft-2025 🧭🚀",
            "Nunca es tarde para empezar - GCsoft-2025 ⏰🌱",
            "Paso a paso se llega lejos - GCsoft-2025 👣🏆",
            "Hoy es un buen día para avanzar - GCsoft-2025 ☀️➡️",
            "Cada línea de código es un paso hacia el futuro 🚀✨ - GCsoft-2025",
            "La perfección se construye con paciencia ⏳🛠️ - GCsoft-2025",
            "Tu esfuerzo hoy es tu orgullo mañana 💪🔥 - GCsoft-2025",
            "No esperes motivación, crea disciplina 🎯🧠 - GCsoft-2025",
            "Pequeños logros crean grandes proyectos 🐾🏆 - GCsoft-2025",
            "Lo simple también puede ser poderoso ⚡🔧 - GCsoft-2025",
            "Pensar diferente es el primer paso hacia la innovación 💡🚀 - GCsoft-2025",
            "Detrás de cada error hay una oportunidad de aprender 📚🔍 - GCsoft-2025",
            "El código más limpio nace de la claridad mental 🧹💻 - GCsoft-2025",
            "Persistir es el verdadero talento 🏃‍♂️🔥 - GCsoft-2025",
            "Pensar diferente es el primer paso hacia la innovación 💡🚀 - GCsoft-2025",
            "Pequeños logros crean grandes proyectos 🐾🏆 - GCsoft-2025",

        ]

        self.frase_actual = 5

        # Footer QLabel
        self.footer_label = QLabel(self.frases[self.frase_actual])
        self.footer_label.setAlignment(Qt.AlignCenter)
        self.footer_label.setStyleSheet("color: gray; font-size: 9pt; margin-top: 10px;")
        self.layout.addWidget(self.footer_label)

        # Timer para cambiar la frase cada 10 segundos
        self.timer_footer = QTimer()
        self.timer_footer.timeout.connect(self.actualizar_frase_footer)
        self.timer_footer.start(10000)  # 10000 ms = 10 segundos

        self.setStyleSheet(
            """
            QWidget {
                font-family: Arial;
                font-size: 12pt;
            }

            QPushButton {
                background-color: #FDD835;
                color: black;
                border: 0.5px solid black; 
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 10pt;
                font-weight: bold;
                min-width: 120px;
            }

            QPushButton:hover {
                background-color: #FB8C00; /* Naranja más fuerte al pasar el mouse */
                cursor: pointer;
            }

            QPushButton:pressed {
                background-color: #EF6C00; /* Naranja más oscuro al hacer clic */
            }

            QPushButton#btnEliminar {
                background-color: #E53935; /* rojo */
                color: white;
                border: 1px solid darkred;
            }

            QPushButton#btnEliminar:hover {
                background-color: #B71C1C; /* rojo más oscuro al pasar mouse */
            }

            QPushButton#btnEliminar:pressed {
                background-color: #7F0000; /* rojo aún más oscuro al hacer clic */
            }
            
                QPushButton#btnModificar {
                background-color: #42A5F5; /* azul medio */
                color: white;
                border: 1px solid #1565C0;
            }

            QPushButton#btnModificar:hover {
                background-color: #1E88E5; /* azul más intenso */
            }

            QPushButton#btnModificar:pressed {
                background-color: #0D47A1; /* azul oscuro */
            }

            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }

            QLabel {
                font-weight: bold;
            }

            QTableWidget {
                border: 1px solid #aaa;
                background-color: #fff;
            }

            QTableWidget::item {
                padding: 5px;
            }
        """
        )

        self.cargar_datos()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Confirmar salida",
            "¿Seguro que deseas salir de la aplicación?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def actualizar_frase_footer(self):
        self.frase_actual = (self.frase_actual + 1) % len(self.frases)
        self.footer_label.setText(self.frases[self.frase_actual])


    def modificar_cliente(self):
        cliente = self.cliente_dropdown.currentText()
        if cliente in self.clientes_data:
            datos = self.clientes_data[cliente]
            nuevo_telefono, ok1 = QInputDialog.getText(
                self, "Modificar Cliente", "Nuevo teléfono:", text=datos["Teléfono"]
            )
            if not ok1:
                return
            nueva_direccion, ok2 = QInputDialog.getText(
                self, "Modificar Cliente", "Nueva dirección:", text=datos["Dirección"]
            )
            if not ok2:
                return
            nueva_localidad, ok3 = QInputDialog.getText(
                self, "Modificar Cliente", "Nueva localidad:", text=datos["Localidad"]
            )
            if not ok3:
                return
            try:
                from db import modificar_cliente

                modificar_cliente(
                    cliente, nuevo_telefono, nueva_direccion, nueva_localidad
                )
                QMessageBox.information(
                    self, "Éxito", "Cliente modificado correctamente."
                )
                self.cargar_datos()
            except Exception as e:
                QMessageBox.warning(
                    self, "Error", f"No se pudo modificar el cliente: {e}"
                )

    def eliminar_cliente(self):
        cliente = self.cliente_dropdown.currentText()
        if cliente in self.clientes_data:
            reply = QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Seguro que deseas eliminar al cliente '{cliente}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                try:
                    from db import eliminar_cliente

                    eliminar_cliente(cliente)
                    QMessageBox.information(
                        self, "Éxito", "Cliente eliminado correctamente."
                    )
                    self.cargar_datos()
                except Exception as e:
                    QMessageBox.warning(
                        self, "Error", f"No se pudo eliminar el cliente: {e}"
                    )
            else:
                QMessageBox.information(
                    self, "Cancelado", "El cliente no fue eliminado."
                )

    def modificar_producto(self):
        producto = self.producto_dropdown.currentText()
        if producto:
            precio_actual = self.productos_precios.get(producto, 0)
            nuevo_precio_str, ok = QInputDialog.getText(
                self, "Modificar Producto", "Nuevo precio:", text=str(precio_actual)
            )
            if not ok:
                return
            try:
                nuevo_precio = float(nuevo_precio_str)
                from db import modificar_producto

                modificar_producto(producto, nuevo_precio)
                QMessageBox.information(
                    self, "Éxito", "Producto modificado correctamente."
                )
                self.cargar_datos()
            except Exception as e:
                QMessageBox.warning(
                    self, "Error", f"No se pudo modificar el producto: {e}"
                )

    def eliminar_producto(self):
        producto = self.producto_dropdown.currentText()
        if producto:
            reply = QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Seguro que deseas eliminar el producto '{producto}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                try:
                    from db import eliminar_producto

                    eliminar_producto(producto)
                    QMessageBox.information(
                        self, "Éxito", "Producto eliminado correctamente."
                    )
                    self.cargar_datos()
                except Exception as e:
                    QMessageBox.warning(
                        self, "Error", f"No se pudo eliminar el producto: {e}"
                    )
            else:
                QMessageBox.information(
                    self, "Cancelado", "El producto no fue eliminado."
                )

    def abrir_dialogo_cliente(self):
        nombre, ok = QInputDialog.getText(
            self, "Agregar Cliente", "Nombre del cliente:"
        )
        if ok and nombre:
            telefono, ok_tel = QInputDialog.getText(
                self, "Agregar Cliente", "Teléfono:"
            )
            if not ok_tel:
                return
            direccion, ok_dir = QInputDialog.getText(
                self, "Agregar Cliente", "Dirección:"
            )
            if not ok_dir:
                return
            localidad, ok_loc = QInputDialog.getText(
                self, "Agregar Cliente", "Localidad:"
            )
            if not ok_loc:
                return

            agregar_cliente(nombre, telefono, direccion, localidad)
            self.cargar_datos()
            self.cliente_dropdown.setCurrentText(nombre)

    def abrir_dialogo_producto(self):
        descripcion, ok = QInputDialog.getText(
            self, "Agregar Producto", "Descripción del producto:"
        )
        if ok and descripcion:
            precio_str, _ = QInputDialog.getText(self, "Agregar Producto", "Precio:")
            try:
                from db import agregar_producto

                precio = float(precio_str)
                agregar_producto(descripcion, precio)
                self.cargar_datos()
                self.producto_dropdown.setCurrentText(descripcion)
            except ValueError:
                QMessageBox.warning(self, "Error", "Precio inválido")

    def abrir_dialogo_proveedor(self):
        nombre, ok = QInputDialog.getText(
            self, "Agregar Proveedor", "Nombre del proveedor:"
        )
        if ok and nombre:
            telefono, ok_tel = QInputDialog.getText(
                self, "Agregar Proveedor", "Teléfono:"
            )
            if not ok_tel:
                return
            direccion, ok_dir = QInputDialog.getText(
                self, "Agregar Proveedor", "Dirección:"
            )
            if not ok_dir:
                return
            localidad, ok_loc = QInputDialog.getText(
                self, "Agregar Proveedor", "Localidad:"
            )
            if not ok_loc:
                return

            from db import agregar_proveedor

            agregar_proveedor(nombre, telefono, direccion, localidad)
            self.cargar_datos()  # Recargá el combo
            self.proveedor_dropdown.setCurrentText(nombre)

    def modificar_proveedor(self):
        proveedor = self.proveedor_dropdown.currentText()
        if proveedor in self.proveedores_data:
            datos = self.proveedores_data[proveedor]
            nuevo_telefono, ok1 = QInputDialog.getText(
                self, "Modificar Proveedor", "Nuevo teléfono:", text=datos["Teléfono"]
            )
            if not ok1:
                return
            nueva_direccion, ok2 = QInputDialog.getText(
                self, "Modificar Proveedor", "Nueva dirección:", text=datos["Dirección"]
            )
            if not ok2:
                return
            nueva_localidad, ok3 = QInputDialog.getText(
                self, "Modificar Proveedor", "Nueva localidad:", text=datos["Localidad"]
            )
            if not ok3:
                return
            try:
                from db import modificar_proveedor

                modificar_proveedor(
                    proveedor, nuevo_telefono, nueva_direccion, nueva_localidad
                )
                QMessageBox.information(
                    self, "Éxito", "Proveedor modificado correctamente."
                )
                self.cargar_datos()
            except Exception as e:
                QMessageBox.warning(
                    self, "Error", f"No se pudo modificar el proveedor: {e}"
                )

    def eliminar_proveedor(self):
        proveedor = self.proveedor_dropdown.currentText()
        if proveedor in self.proveedores_data:
            reply = QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Seguro que deseas eliminar al proveedor '{proveedor}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                try:
                    from db import eliminar_proveedor

                    eliminar_proveedor(proveedor)
                    QMessageBox.information(
                        self, "Éxito", "Proveedor eliminado correctamente."
                    )
                    self.cargar_datos()
                except Exception as e:
                    QMessageBox.warning(
                        self, "Error", f"No se pudo eliminar el proveedor: {e}"
                    )

    def obtener_numero_presupuesto(self):
        """Obtiene el siguiente número de presupuesto desde un archivo."""
        try:
            ruta_numero = obtener_ruta_archivo("numero_presupuesto.txt")
            if os.path.exists(ruta_numero):
                with open(ruta_numero, "r") as file:
                    numero = int(file.read().strip())
            else:
                numero = 1
            siguiente_numero = numero + 1
            with open(ruta_numero, "w") as file:
                file.write(str(siguiente_numero))
            return numero
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo obtener el número del presupuesto: {e}"
            )
            return 1

    def cargar_datos(self):
        try:
            # Cargar clientes desde SQLite
            clientes = obtener_clientes()
            self.clientes_data = {}
            self.cliente_dropdown.clear()
            for id_cliente, nombre, telefono, direccion, localidad in clientes:
                self.clientes_data[nombre] = {
                    "Teléfono": telefono,
                    "Dirección": direccion,
                    "Localidad": localidad,
                }
                self.cliente_dropdown.addItem(nombre)

            # Cargar productos desde SQLite
            productos = obtener_productos()
            self.productos_precios = {}
            self.producto_dropdown.clear()
            for id_producto, descripcion, precio in productos:
                self.productos_precios[descripcion] = precio
                self.producto_dropdown.addItem(descripcion)

            # Cargar proveedores desde SQLite
            from db import obtener_proveedores

            proveedores = obtener_proveedores()
            self.proveedores_data = {}
            self.proveedor_dropdown.clear()
            for id_prov, nombre, telefono, direccion, localidad in proveedores:
                self.proveedores_data[nombre] = {
                    "Teléfono": telefono,
                    "Dirección": direccion,
                    "Localidad": localidad,
                }
                self.proveedor_dropdown.addItem(nombre)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo cargar los datos desde la base de datos: {e}",
            )

    def actualizar_datos_cliente(self):
        cliente = self.cliente_dropdown.currentText()
        if cliente in self.clientes_data:
            datos = self.clientes_data[cliente]

            direccion = datos.get("Dirección", "").strip()
            if not direccion:
                direccion = "No especificada"
            self.direccion_input.setText(direccion)

            telefono = datos.get("Teléfono", "").strip()
            if not telefono:
                telefono = "No especificado"
            self.telefono_input.setText(telefono)

            localidad = datos.get("Localidad")
            if localidad is None:
                localidad = ""
            localidad = localidad.strip()
            if not localidad:
                localidad = "No especificada"
            self.localidad_input.setText(localidad)
        else:
            self.direccion_input.clear()
            self.telefono_input.clear()
            self.localidad_input.clear()

    def actualizar_precio_unitario(self):
        producto = self.producto_dropdown.currentText()
        precio = self.productos_precios.get(producto, 0)
        self.precio_input.setText(f"{precio:.2f}")

    def agregar_producto(self):
        try:
            producto = self.producto_dropdown.currentText()
            proveedor = self.proveedor_dropdown.currentText()
            cantidad_texto = self.cantidad_input.text()
            precio_texto = self.precio_input.text()

            if not producto or not proveedor or not cantidad_texto or not precio_texto:
                raise ValueError("Todos los campos deben estar completos.")

            cantidad = int(cantidad_texto)
            precio_unitario = float(precio_texto)

            if cantidad <= 0 or precio_unitario <= 0:
                raise ValueError("Cantidad y precio deben ser mayores que cero.")

            total = cantidad * precio_unitario

            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(producto))
            self.table.setItem(row_position, 1, QTableWidgetItem(proveedor))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(cantidad)))
            self.table.setItem(
                row_position, 3, QTableWidgetItem(f"{precio_unitario:.2f}")
            )
            self.table.setItem(row_position, 4, QTableWidgetItem(f"{total:.2f}"))

            self.productos_agregados.append(
                (producto, proveedor, cantidad, precio_unitario, total)
            )
        except ValueError as e:
            QMessageBox.warning(self, "Entrada Inválida", str(e))

    def nuevo_presupuesto(self):
        self.cliente_dropdown.setCurrentIndex(0)
        self.producto_dropdown.setCurrentIndex(0)
        self.proveedor_dropdown.setCurrentIndex(0)
        self.cantidad_input.clear()
        self.precio_input.clear()
        self.table.setRowCount(0)
        self.productos_agregados = []
        self.ir_carpeta_btn.setEnabled(False)  # Deshabilitar botón nuevo documento
        QMessageBox.information(
            self,
            "Nuevo Documento",
            "Los datos han sido limpiados, ahora puedes crear un nuevo documento.",
        )

    def generar_documento(self):
        cliente = self.cliente_dropdown.currentText()
        if not cliente:
            QMessageBox.warning(self, "Cliente", "Debe seleccionar un cliente.")
            return

        if not self.productos_agregados:
            QMessageBox.warning(self, "Productos", "Debe agregar al menos un producto.")
            return

        tipo_documento = self.tipo_documento_dropdown.currentText()
        if tipo_documento == "Presupuesto":
            file_path = self.generar_presupuesto(cliente, self.productos_agregados)
        elif tipo_documento == "Recibo":
            file_path = self.generar_recibo(cliente, self.productos_agregados)

        # Guardar presupuesto en la base de datos SQLite
        try:
            # Buscar cliente_id
            # Buscar cliente_id
            cliente_id = None
            for (
                id_cliente,
                nombre,
                telefono,
                direccion,
                localidad,
            ) in obtener_clientes():
                if nombre == cliente:
                    cliente_id = id_cliente
                    break

            # Si no existe, lo agregamos (opcional)
            if cliente_id is None:
                agregar_cliente(
                    cliente,
                    self.telefono_input.text(),
                    self.direccion_input.text(),
                    self.localidad_input.text(),
                )
                for id_cliente, nombre, _, _, _ in obtener_clientes():
                    if nombre == cliente:
                        cliente_id = id_cliente
                        break

            total_presupuesto = sum([prod[4] for prod in self.productos_agregados])
            fecha = datetime.now().strftime("%Y-%m-%d")

            guardar_presupuesto(cliente_id, fecha, total_presupuesto)
        except Exception as e:
            QMessageBox.warning(
                self, "Error Base de Datos", f"No se pudo guardar el presupuesto: {e}"
            )

        self.ultima_ruta_documento = file_path
        self.ir_carpeta_btn.setEnabled(True)

        QMessageBox.information(
            self, "Éxito", f"{tipo_documento} generado: {file_path}"
        )

    def abrir_carpeta_documento(self):
        if self.ultima_ruta_documento and os.path.exists(self.ultima_ruta_documento):
            carpeta = os.path.dirname(self.ultima_ruta_documento)
            QDesktopServices.openUrl(QUrl.fromLocalFile(carpeta))
        else:
            QMessageBox.warning(
                self, "Advertencia", "No se encontró el documento o la carpeta."
            )

    def generar_presupuesto(self, cliente, productos):
        numero_presupuesto = self.obtener_numero_presupuesto()
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "presupuestos")
        os.makedirs(desktop_path, exist_ok=True)
        file_path = os.path.join(
            desktop_path, f"presupuesto_{numero_presupuesto}_{cliente}.pdf"
        )
        return self.generar_pdf(
            cliente, productos, "Presupuesto", numero_presupuesto, file_path
        )

    def generar_recibo(self, cliente, productos):
        numero_recibo = self.obtener_numero_presupuesto()
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "recibos")
        os.makedirs(desktop_path, exist_ok=True)
        file_path = os.path.join(desktop_path, f"recibo_{numero_recibo}_{cliente}.pdf")
        return self.generar_pdf(cliente, productos, "Recibo", numero_recibo, file_path)

    def generar_pdf(self, cliente, productos, tipo, numero, file_path):

        document = SimpleDocTemplate(file_path, pagesize=landscape(letter))
        elements = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle("EmpresaStyle", fontSize=14, alignment=1)
        datos_style = ParagraphStyle("DatosStyle", fontSize=10, alignment=1)

        logo_path = obtener_ruta_archivo("img/logo.png")
        if not os.path.exists(logo_path):
            print(f"El archivo del logo no se encuentra en: {logo_path}")

        logo = Image(logo_path, width=150, height=100)

        company_name = "SERVICIOS INFORMÁTICOS"
        datos_contacto = (
            "Dilkendein 1278 - Tel: 358-4268768 - Email: cristian.e.druetta@gmail.com"
        )

        company_name_paragraph = Paragraph(f"<b>{company_name}</b>", title_style)
        datos_contacto_paragraph = Paragraph(f"<i>{datos_contacto}</i>", datos_style)

        header_table = Table(
            [[logo, company_name_paragraph, datos_contacto_paragraph]],
            colWidths=[150, 250, 250],
        )
        header_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        elements.append(header_table)
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>{tipo} N° {numero}</b>", title_style))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"<b>Cliente:</b> {cliente}", styles["Normal"]))
        elements.append(
            Paragraph(
                f"<b>Dirección:</b> {self.direccion_input.text()}", styles["Normal"]
            )
        )
        elements.append(
            Paragraph(
                f"<b>Teléfono:</b> {self.telefono_input.text()}", styles["Normal"]
            )
        )
        elements.append(
            Paragraph(
                f"<b>Localidad:</b> {self.localidad_input.text()}", styles["Normal"]
            )
        )

        fecha = datetime.now().strftime("%d/%m/%Y")
        elements.append(Paragraph(f"<b>Fecha:</b> {fecha}", styles["Normal"]))
        elements.append(Spacer(1, 12))

        data = [["Producto", "Cantidad", "Precio Unitario", "Total"]]
        total_general = 0
        for producto, proveedor, cantidad, precio_unitario, total in productos:
            data.append(
                [producto, cantidad, f"${precio_unitario:.2f}", f"${total:.2f}"]
            )
            total_general += total

        total_text = f"${total_general:.2f}"
        total_paragraph = Paragraph(
            f"<b>{total_text}</b>",
            ParagraphStyle("BoldStyle", fontSize=12, fontName="Helvetica-Bold"),
        )
        data.append(["", "", "Total:", total_paragraph])

        col_widths = [400, 80, 100, 100]
        table = Table(data, colWidths=col_widths)
        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                ]
            )
        )

        elements.append(table)

        footer_style = ParagraphStyle(
            "FooterStyle", parent=styles["Normal"], alignment=1
        )
        elements.append(Spacer(1, 12))
        elements.append(
            Paragraph("Este documento tiene validez por 7 días.", footer_style)
        )
        elements.append(
            Paragraph("© GCsoft-2025. Todos los derechos reservados.", footer_style)
        )

        document.build(elements)
        return file_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CotizacionApp()
    window.show()
    sys.exit(app.exec_())
