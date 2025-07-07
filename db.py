import sqlite3

DB_NAME = "cotizador.db"

# --- PRODUCTOS ---


def agregar_producto(descripcion, precio):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (descripcion, precio) VALUES (?, ?)",
        (descripcion, precio),
    )
    conn.commit()
    conn.close()


def obtener_productos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, descripcion, precio FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos


def eliminar_producto(id_producto):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conn.commit()
    conn.close()


def actualizar_producto(id_producto, descripcion, precio):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET descripcion = ?, precio = ? WHERE id = ?",
        (descripcion, precio, id_producto),
    )
    conn.commit()
    conn.close()


# --- CLIENTES ---


def agregar_cliente(nombre, telefono, direccion, localidad):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clientes (nombre, telefono, direccion, localidad) VALUES (?, ?, ?)",
        (nombre, telefono, direccion, localidad),
    )
    conn.commit()
    conn.close()


def obtener_clientes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, telefono, direccion, localidad FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes


def modificar_cliente(nombre, telefono, direccion, localidad):
    conn = sqlite3.connect("cotizador.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes SET telefono=?, direccion=?, localidad=?
        WHERE nombre=?
    """, (telefono, direccion, localidad, nombre))
    conn.commit()
    conn.close()

def modificar_producto(descripcion, nuevo_precio):
    conn = sqlite3.connect("cotizador.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE productos SET precio=?
        WHERE descripcion=?
    """, (nuevo_precio, descripcion))
    conn.commit()
    conn.close()


# --- PRESUPUESTOS ---


def guardar_presupuesto(cliente_id, fecha, total):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO presupuestos (cliente_id, fecha, total) VALUES (?, ?, ?)",
        (cliente_id, fecha, total),
    )
    conn.commit()
    conn.close()


def obtener_presupuestos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.id, c.nombre, p.fecha, p.total
        FROM presupuestos p
        JOIN clientes c ON p.cliente_id = c.id
    """
    )
    presupuestos = cursor.fetchall()
    conn.close()
    return presupuestos
