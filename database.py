import sqlite3

class DatabaseManager:
    def __init__(self, db_name="delicias_coffee.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establece la conexión a la base de datos."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Crea las tablas PRODUCTOS e INGREDIENTES si no existen."""
        # Tabla de Productos (Lo que se vende en el POS)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL,
                habilitado INTEGER NOT NULL DEFAULT 1 -- 1: Habilitado, 0: Deshabilitado
            )
        """)

        # Tabla de Ingredientes/Toppings (Lo que se habilita/deshabilita en inventario)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                estado INTEGER NOT NULL DEFAULT 1 -- 1: Habilitado, 0: Deshabilitado
            )
        """)
        
        # Tabla de Ventas (Para guardar el registro de transacciones)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                total REAL NOT NULL,
                detalle TEXT NOT NULL -- Guardaremos los detalles de la venta en JSON o TEXTO
            )
        """)
        
        self.conn.commit()
        self.seed_data()

    def seed_data(self):
        """Inserta algunos datos iniciales si las tablas están vacías."""
        # Productos iniciales (Categoría: WAFFLES)
        self.cursor.execute("SELECT COUNT(*) FROM productos")
        if self.cursor.fetchone()[0] == 0:
            productos_iniciales = [
                ("Waffle Clásico", "WAFFLES", 60.00, 1),
                ("Waffle Oreo", "WAFFLES", 75.00, 1),
                ("Creppa Salada", "CREPAS", 85.00, 1),
                ("Frappe Mocha", "FRAPPES", 45.00, 1),
            ]
            self.cursor.executemany("INSERT INTO productos (nombre, categoria, precio, habilitado) VALUES (?, ?, ?, ?)", productos_iniciales)

        # Ingredientes iniciales
        self.cursor.execute("SELECT COUNT(*) FROM ingredientes")
        if self.cursor.fetchone()[0] == 0:
            ingredientes_iniciales = [
                ("Fresas", 1),
                ("Crema Batida", 1),
                ("Plátanos", 1),
                ("Chispas Chocolate", 1),
                ("Rompopé", 0), # Deshabilitado por defecto
            ]
            self.cursor.executemany("INSERT INTO ingredientes (nombre, estado) VALUES (?, ?)", ingredientes_iniciales)
            
        self.conn.commit()
        
    def execute_query(self, query, params=()):
        """Ejecuta una consulta y devuelve los resultados."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
        
    def execute_commit(self, query, params=()):
        """Ejecuta una consulta que modifica la DB (INSERT, UPDATE, DELETE)."""
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.lastrowid

# Asegura que la DB se configure al inicio
db = DatabaseManager()