# interfaces/consola/main.py
"""
Ejecútalo desde la raíz del proyecto:
    python -m interfaces.consola.main
o
    python interfaces/consola/main.py
"""

from managers.db_manager import DBManager
from managers.cliente_manager import ClienteManager
from managers.producto_manager import ProductoManager
from managers.venta_manager import VentaManager

cm = ClienteManager()
pm = ProductoManager()
vm = VentaManager()

def menu():
    DBManager.inicializar()  # inicializa DB al arrancar
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1) Clientes")
        print("2) Productos")
        print("3) Ventas")
        print("0) Salir")
        op = input("> ").strip()
        if op == "1":
            menu_clientes()
        elif op == "2":
            menu_productos()
        elif op == "3":
            menu_ventas()
        elif op == "0":
            break
        else:
            print("Opción inválida")

def menu_clientes():
    while True:
        print("\n-- CLIENTES --")
        print("1) Crear")
        print("2) Listar")
        print("3) Ver por ID")
        print("4) Eliminar")
        print("0) Volver")
        op = input("> ").strip()
        if op == "1":
            nombre = input("Nombre: ")
            email = input("Email: ")
            tel = input("Teléfono: ")
            c = cm.crear(nombre, email, tel)
            print("Creado:", c)
        elif op == "2":
            for c in cm.listar():
                print(c)
        elif op == "3":
            try:
                cid = int(input("ID: "))
                print(cm.obtener(cid))
            except ValueError:
                print("ID inválido")
        elif op == "4":
            try:
                cid = int(input("ID a eliminar: "))
                ok = cm.eliminar(cid)
                print("Eliminado" if ok else "No existe")
            except ValueError:
                print("ID inválido")
        elif op == "0":
            break

def menu_productos():
    while True:
        print("\n-- PRODUCTOS --")
        print("1) Crear")
        print("2) Listar")
        print("3) Ver por ID")
        print("4) Actualizar stock")
        print("0) Volver")
        op = input("> ").strip()
        if op == "1":
            nombre = input("Nombre: ")
            try:
                precio = float(input("Precio: "))
                stock = int(input("Stock: "))
            except ValueError:
                print("Precio/stock inválido")
                continue
            p = pm.crear(nombre, precio, stock)
            print("Creado:", p)
        elif op == "2":
            for p in pm.listar():
                print(p)
        elif op == "3":
            try:
                pid = int(input("ID: "))
                print(pm.obtener(pid))
            except ValueError:
                print("ID inválido")
        elif op == "4":
            try:
                pid = int(input("ID: "))
                nuevo = int(input("Nuevo stock: "))
                ok = pm.actualizar_stock(pid, nuevo)
                print("OK" if ok else "No existe")
            except ValueError:
                print("Datos inválidos")
        elif op == "0":
            break

def menu_ventas():
    while True:
        print("\n-- VENTAS --")
        print("1) Registrar venta")
        print("2) Listar ventas")
        print("3) Ver detalle venta")
        print("0) Volver")
        op = input("> ").strip()
        if op == "1":
            try:
                id_cliente = int(input("ID cliente: "))
            except ValueError:
                print("ID inválido"); continue
            items = []
            while True:
                try:
                    id_prod = int(input("ID producto (0 finalizar): "))
                except ValueError:
                    print("ID inválido"); continue
                if id_prod == 0: break
                try:
                    qty = int(input("Cantidad: "))
                except ValueError:
                    print("Cantidad inválida"); continue
                items.append((id_prod, qty))
            if not items:
                print("Venta cancelada (sin items)"); continue
            try:
                idv = vm.crear(id_cliente, items)
                print("Venta registrada id:", idv)
            except Exception as e:
                print("Error:", e)
        elif op == "2":
            for v in vm.listar():
                print(v)
        elif op == "3":
            try:
                idv = int(input("ID venta: "))
            except ValueError:
                print("ID inválido"); continue
            detalle = vm.detalle(idv)
            if not detalle:
                print("Sin detalle / no existe")
            else:
                for d in detalle:
                    print(dict(d))
        elif op == "0":
            break

if __name__ == "__main__":
    menu()
