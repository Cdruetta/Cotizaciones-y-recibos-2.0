import sqlite3

conn = sqlite3.connect("cotizador.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(clientes)")
columnas = cursor.fetchall()

print("Columnas de la tabla 'clientes':")
for col in columnas:
    print(f"- {col[1]}")

conn.close()
