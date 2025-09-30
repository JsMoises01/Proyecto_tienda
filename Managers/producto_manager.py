# managers/producto_manager.py
from typing import List
from managers.db_manager import DBManager
from modelos.producto import Producto

class ProductoManager:
    def crear(self, nombre: str, precio: float, stock: int) -> Producto:
        with DBManager.conectar() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                        (nombre.strip(), float(precio), int(stock)))
            conn.commit()
            pid = cur.lastrowid
        return Producto(pid, nombre, precio, stock)

    def listar(self) -> List[Producto]:
        with DBManager.conectar() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_producto, nombre, precio, stock FROM productos ORDER BY id_producto")
            rows = cur.fetchall()
            return [Producto(r["id_producto"], r["nombre"], r["precio"], r["stock"]) for r in rows]

    def obtener(self, id_producto: int) -> Producto | None:
        with DBManager.conectar() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_producto, nombre, precio, stock FROM productos WHERE id_producto = ?", (id_producto,))
            r = cur.fetchone()
            return Producto(r["id_producto"], r["nombre"], r["precio"], r["stock"]) if r else None

    def actualizar_stock(self, id_producto: int, nuevo_stock: int) -> bool:
        with DBManager.conectar() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE productos SET stock = ? WHERE id_producto = ?", (int(nuevo_stock), id_producto))
            conn.commit()
            return cur.rowcount > 0
