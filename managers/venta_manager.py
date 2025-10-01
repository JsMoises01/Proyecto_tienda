# managers/venta_manager.py
from typing import List, Tuple
from managers.db_manager import DBManager
from modelos.venta import Venta
from datetime import datetime

class VentaManager:
    def crear(self, id_cliente: int, items: List[Tuple[int, int]]) -> int:
        """
        items: [(id_producto, cantidad), ...]
        Devuelve id_venta.
        """
        with DBManager.conectar() as conn:
            cur = conn.cursor()

            # verificar cliente
            cur.execute("SELECT 1 FROM clientes WHERE id_cliente = ?", (id_cliente,))
            if not cur.fetchone():
                raise ValueError("Cliente no existe")

            total = 0.0
            # validar productos y calcular total
            productos_info = {}
            for id_prod, qty in items:
                cur.execute("SELECT precio, stock FROM productos WHERE id_producto = ?", (id_prod,))
                r = cur.fetchone()
                if not r:
                    raise ValueError(f"Producto {id_prod} no encontrado")
                precio, stock = r["precio"], r["stock"]
                if qty <= 0:
                    raise ValueError("Cantidad debe ser > 0")
                if qty > stock:
                    raise ValueError(f"Stock insuficiente para producto {id_prod}")
                subtotal = precio * qty
                productos_info[id_prod] = (qty, precio, subtotal)
                total += subtotal

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("INSERT INTO ventas (id_cliente, fecha, monto_total) VALUES (?, ?, ?)",
                        (id_cliente, fecha, total))
            id_venta = cur.lastrowid

            # detalle y actualizar stock
            for id_prod, (qty, precio, subtotal) in productos_info.items():
                cur.execute("INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                            (id_venta, id_prod, qty, subtotal))
                cur.execute("UPDATE productos SET stock = stock - ? WHERE id_producto = ?", (qty, id_prod))

            conn.commit()
            return id_venta

    def listar(self) -> List[Venta]:
        with DBManager.conectar() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT v.id_venta, v.fecha, v.monto_total, v.id_cliente, c.nombre
                FROM ventas v
                JOIN clientes c ON v.id_cliente = c.id_cliente
                ORDER BY v.id_venta
            """)
            rows = cur.fetchall()
            return [Venta(r["id_venta"], r["id_cliente"], r["fecha"], r["monto_total"]) for r in rows]

    def detalle(self, id_venta: int):
        with DBManager.conectar() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT dv.id_detalle, dv.id_producto, p.nombre, dv.cantidad, dv.subtotal
                FROM detalle_ventas dv
                JOIN productos p ON dv.id_producto = p.id_producto
                WHERE dv.id_venta = ?
            """, (id_venta,))
            return cur.fetchall()
