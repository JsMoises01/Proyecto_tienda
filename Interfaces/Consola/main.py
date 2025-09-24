import sqlite3
from datetime import datetime

# Conexión a la base de datos
def conectar():
    return sqlite3.connect("../../BdD/tienda.db")

# Inicializar tablas
def inicializar_bd():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        cliente_id INTEGER,
        total REAL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    );
    """)

    conexion.commit()
    conexion.close()

# CRUD de productos
def agregar_producto():
    nombre = input("Nombre del producto: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock: "))

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", (nombre, precio, stock))
    conexion.commit()
    conexion.close()
    print("✅ Producto agregado con éxito.")

def listar_productos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()

    print("\n--- Lista de productos ---")
    for p in productos:
        print(f"ID: {p[0]} | {p[1]} | Precio: {p[2]} | Stock: {p[3]}")
    print("--------------------------\n")

# Menú principal
def menu():
    inicializar_bd()
    while True:
        print("=== MENÚ TIENDA AUTOPARTES ===")
        print("1. Agregar producto")
        print("2. Listar productos")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            listar_productos()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()
