# modelos/venta.py
from datetime import datetime

class Venta:
    def __init__(self, id_venta: int | None, id_cliente: int, fecha: str, monto_total: float):
        self.id_venta = id_venta
        self.id_cliente = id_cliente
        self.fecha = fecha
        self.monto_total = float(monto_total)

    def __repr__(self):
        return f"Venta(id={self.id_venta}, cliente={self.id_cliente}, fecha='{self.fecha}', total={self.monto_total})"
