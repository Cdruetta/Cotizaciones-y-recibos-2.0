import sqlite3

conn = sqlite3.connect("cotizador.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(clientes)")
columnas = [col[1] for col in cursor.fetchall()]

if "localidad" not in columnas:
    print("Agregando columna 'localidad'...")
    cursor.execute("ALTER TABLE clientes ADD COLUMN localidad TEXT")
    conn.commit()
    print("Columna agregada con éxito.")
else:
    print("La columna 'localidad' ya existe.")

conn.close()
