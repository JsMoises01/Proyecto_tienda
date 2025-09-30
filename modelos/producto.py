# modelos/producto.py
class Producto:
    def __init__(self, id_producto: int | None, nombre: str, precio: float, stock: int):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)

    def __repr__(self):
        return f"Producto(id={self.id_producto}, nombre='{self.nombre}', precio={self.precio}, stock={self.stock})"
