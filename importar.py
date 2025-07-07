import sqlite3
import pandas as pd
import os

DB_PATH = "cotizador.db"
EXCEL_PATH = "base_datos.xlsx"  # Asegurate que esté en la misma carpeta


def importar_clientes(df, conn):
    df = df.dropna(subset=["Nombre"])  # Asegura que haya nombre
    for _, fila in df.iterrows():
        conn.execute(
            """
            INSERT OR IGNORE INTO clientes (nombre, telefono, direccion)
            VALUES (?, ?, ?)
        """,
            (
                str(fila.get("Nombre", "")).strip(),
                str(fila.get("Teléfono", "")).strip() if "Teléfono" in fila else "",
                str(fila.get("Dirección", "")).strip() if "Dirección" in fila else "",
            ),
        )


def importar_productos(df, conn):
    df = df.dropna(subset=["Nombre", "Precio"])  # Asegura que haya nombre y precio
    for _, fila in df.iterrows():
        conn.execute(
            """
            INSERT OR IGNORE INTO productos (descripcion, precio)
            VALUES (?, ?)
        """,
            (
                str(fila.get("Nombre", "")).strip(),
                float(fila.get("Precio", 0)),  # sin .strip() porque es numérico
            ),
        )


def importar_excel():
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ No se encontró el archivo {EXCEL_PATH}")
        return

    excel = pd.ExcelFile(EXCEL_PATH)
    conn = sqlite3.connect(DB_PATH)
    try:
        if "Clientes" in excel.sheet_names:
            df_clientes = pd.read_excel(excel, sheet_name="Clientes")
            importar_clientes(df_clientes, conn)
            print(f"✔ Clientes importados: {len(df_clientes)}")

        if "Productos" in excel.sheet_names:
            df_productos = pd.read_excel(excel, sheet_name="Productos")
            importar_productos(df_productos, conn)
            print(f"✔ Productos importados: {len(df_productos)}")

        conn.commit()
        print("✅ Importación completada.")
    except Exception as e:
        print(f"❌ Error al importar: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    importar_excel()
