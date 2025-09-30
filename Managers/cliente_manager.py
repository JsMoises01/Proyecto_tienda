# managers/cliente_manager.py
from typing import List
from managers.db_manager import DBManager
from modelos.cliente import Cliente

class ClienteManager:
    def crear(self, nombre: str, email: str, telefono: str = "") -> Cliente:
        with DBManager.conectar() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO clientes (nombre, email, telefono) VALUES (?, ?, ?)",
                        (nombre.strip(), email.strip(), telefono.strip()))
            conn.commit()
            idc = cur.lastrowid
        return Cliente(idc, nombre, email, telefono)

    def listar(self) -> List[Cliente]:
        with DBManager.conectar() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_cliente, nombre, email, telefono FROM clientes ORDER BY id_cliente")
            rows = cur.fetchall()
            return [Cliente(r["id_cliente"], r["nombre"], r["email"], r["telefono"]) for r in rows]

    def obtener(self, id_cliente: int) -> Cliente | None:
        with DBManager.conectar() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_cliente, nombre, email, telefono FROM clientes WHERE id_cliente = ?", (id_cliente,))
            r = cur.fetchone()
            return Cliente(r["id_cliente"], r["nombre"], r["email"], r["telefono"]) if r else None

    def eliminar(self, id_cliente: int) -> bool:
        with DBManager.conectar() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
            conn.commit()
            return cur.rowcount > 0
