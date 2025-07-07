import sqlite3

conn = sqlite3.connect("cotizador.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()

print("Tablas encontradas en cotizador.db:")
for tabla in tablas:
    print("-", tabla[0])

conn.close()
