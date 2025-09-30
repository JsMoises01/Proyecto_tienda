# modelos/cliente.py
class Cliente:
    def __init__(self, id_cliente: int | None, nombre: str, email: str, telefono: str = ""):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    def __repr__(self):
        return f"Cliente(id={self.id_cliente}, nombre='{self.nombre}', email='{self.email}')"
