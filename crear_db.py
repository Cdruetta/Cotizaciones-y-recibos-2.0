import sqlite3


def crear_base_de_datos():
    conn = sqlite3.connect("cotizador.db")  # crea el archivo si no existe
    cursor = conn.cursor()

    # Tabla de clientes
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT,
            localidad TEXT
        )
    """
    )

    # Tabla de productos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """
    )

    # Tabla de presupuestos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS presupuestos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            fecha TEXT,
            total REAL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """
    )

    conn.commit()
    conn.close()
    print("Base de datos creada con éxito.")


if __name__ == "__main__":
    crear_base_de_datos()
