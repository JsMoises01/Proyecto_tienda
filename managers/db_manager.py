# managers/db_manager.py
from pathlib import Path
import sqlite3

class DBManager:
    @staticmethod
    def _paths():
        here = Path(__file__).resolve()
        project_root = here.parent.parent  # ../
        db_dir = project_root / "base_datos"
        db_dir.mkdir(parents=True, exist_ok=True)
        db_file = db_dir / "proyecto.db"
        schema = db_dir / "esquema_sqlite.sql"
        return project_root, db_dir, db_file, schema

    @staticmethod
    def conectar():
        """Devuelve conexión sqlite3 con row_factory para acceder por nombre."""
        _, _, db_file, _ = DBManager._paths()
        conn = sqlite3.connect(str(db_file))
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def inicializar():
        """Ejecuta esquema_sqlite.sql si existe, si no crea tablas básicas."""
        _, db_dir, db_file, schema = DBManager._paths()
        with sqlite3.connect(str(db_file)) as conn:
            cur = conn.cursor()
            if schema.exists():
                sql = schema.read_text(encoding="utf-8")
                cur.executescript(sql)
            else:
                # Tablas por defecto (seguro)
                cur.executescript("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefono TEXT
                );
                CREATE TABLE IF NOT EXISTS productos (
                    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL,
                    stock INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS ventas (
                    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cliente INTEGER NOT NULL,
                    fecha TEXT NOT NULL,
                    monto_total REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS detalle_ventas (
                    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_venta INTEGER NOT NULL,
                    id_producto INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    subtotal REAL NOT NULL
                );
                """)
            conn.commit()
        print("✅ Base de datos inicializada:", db_file)
