import sqlite3
from sqlite3 import Error, Connection

def crear_conexion() -> Connection | None:
    """Crea o conecta a la base de datos SQLite"""
    try:
        conexion = sqlite3.connect("gremio_aventuras.db")
        conexion.execute("PRAGMA foreign_keys = ON;")
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def inicializar_base_datos():
    """Crea las tablas y datos iniciales si no existen"""
    conexion = crear_conexion()
    if conexion is not None:
        cursor = conexion.cursor()

        # 1. Tabla Héroes
        cursor.execute("""
            -- language=SQLite
            CREATE TABLE IF NOT EXISTS heroes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                clase TEXT NOT NULL,
                nivel_experiencia INTEGER NOT NULL CHECK (nivel_experiencia > 0)
            );
        """)

        # 2. Tabla Misiones
        cursor.execute("""
            -- language=SQLite
            CREATE TABLE IF NOT EXISTS misiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                nivel_dificultad INTEGER NOT NULL CHECK (nivel_dificultad BETWEEN 1 AND 5),
                localizacion TEXT NOT NULL,
                recompensa INTEGER NOT NULL CHECK (recompensa >= 0)
            );
        """)

        # 3. Tabla Monstruos
        cursor.execute("""
            -- language=SQLite
            CREATE TABLE IF NOT EXISTS monstruos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                nivel_amenaza INTEGER NOT NULL CHECK (nivel_amenaza BETWEEN 1 AND 10)
            );
        """)

        # 4. Tabla Puente: Misiones y Héroes (Muchos a Muchos)
        cursor.execute("""
            -- language=SQLite
            CREATE TABLE IF NOT EXISTS misiones_heroes (
                mision_id INTEGER,
                heroe_id INTEGER,
                PRIMARY KEY (mision_id, heroe_id),
                FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE,
                FOREIGN KEY (heroe_id) REFERENCES heroes(id) ON DELETE CASCADE
            );
        """)

        # 5. Tabla Puente: Misiones y Monstruos (Muchos a Muchos)
        cursor.execute("""
            -- language=SQLite
            CREATE TABLE IF NOT EXISTS misiones_monstruos (
                mision_id INTEGER,
                monstruo_id INTEGER,
                PRIMARY KEY (mision_id, monstruo_id),
                FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE,
                FOREIGN KEY (monstruo_id) REFERENCES monstruos(id) ON DELETE CASCADE
            );
        """)

        # Datos de prueba iniciales (solo si la tabla está vacía)
        cursor.execute("SELECT COUNT(*) FROM heroes;")
        resultado = cursor.fetchone()
        if resultado and resultado[0] == 0:
            cursor.executemany("INSERT INTO heroes (nombre, clase, nivel_experiencia) VALUES (?, ?, ?);", [
                ("Aragorn", "Guerrero", 15),
                ("Gandalf", "Mago", 20),
                ("Legolas", "Arquero", 14)
            ])
            cursor.executemany("INSERT INTO misiones (nombre, nivel_dificultad, localizacion, recompensa) VALUES (?, ?, ?, ?);", [
                ("Rescatar la Aldea", 2, "Bosque Oscuro", 500),
                ("Derrotar al Dragón", 5, "Montaña de Fuego", 5000)
            ])
            cursor.executemany("INSERT INTO monstruos (nombre, tipo, nivel_amenaza) VALUES (?, ?, ?);", [
                ("Goblin Explorador", "Goblin", 3),
                ("Smaug", "Dragón", 10)
            ])
            cursor.executemany("INSERT OR IGNORE INTO misiones_heroes (mision_id, heroe_id) VALUES (?, ?);", [
                (1, 1), (1, 3), (2, 1), (2, 2)
            ])
            cursor.executemany("INSERT OR IGNORE INTO misiones_monstruos (mision_id, monstruo_id) VALUES (?, ?);", [
                (1, 1), (2, 2)
            ])
            conexion.commit()

        conexion.close()

def mostrar_heroes():
    conexion = crear_conexion()
    if conexion is not None:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM heroes;")
        print("\n--- LISTA DE HÉROES ---")
        for row in cursor.fetchall():
            print(f"ID: {row[0]} | Nombre: {row[1]} | Clase: {row[2]} | Nivel: {row[3]}")
        conexion.close()

def mostrar_misiones():
    conexion = crear_conexion()
    if conexion is not None:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM misiones;")
        print("\n--- LISTA DE MISIONES ---")
        for row in cursor.fetchall():
            print(f"ID: {row[0]} | Misión: {row[1]} | Dificultad (1-5): {row[2]} | Lugar: {row[3]} | Oro: {row[4]}")
        conexion.close()

def mostrar_monstruos():
    conexion = crear_conexion()
    if conexion is not None:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM monstruos;")
        print("\n--- LISTA DE MONSTRUOS ---")
        for row in cursor.fetchall():
            print(f"ID: {row[0]} | Nombre: {row[1]} | Tipo: {row[2]} | Amenaza (1-10): {row[3]}")
        conexion.close()

def registrar_heroe():
    nombre = input("Nombre del héroe: ")
    clase = input("Clase (Guerrero, Mago, etc.): ")
    try:
        nivel = int(input("Nivel de experiencia: "))
    except ValueError:
        print("Error: El nivel de experiencia debe ser un número entero.")
        return

    conexion = crear_conexion()
    if conexion is not None:
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO heroes (nombre, clase, nivel_experiencia) VALUES (?, ?, ?);", (nombre, clase, nivel))
            conexion.commit()
            print("¡Héroe registrado con éxito!")
        except Error as e:
            print(f"Error al registrar (verifica que el nivel sea mayor a 0): {e}")
        finally:
            conexion.close()

def menu():
    inicializar_base_datos()
    while True:
        print("\n==================================")
        print(" GESTIÓN DE GREMIO DE AVENTURAS ")
        print("==================================")
        print("1. Ver lista de Héroes")
        print("2. Ver lista de Misiones")
        print("3. Ver lista de Monstruos")
        print("4. Registrar un nuevo Héroe")
        print("5. Salir")

        opcion = input("Elige una opción (1-5): ")

        if opcion == "1":
            mostrar_heroes()
        elif opcion == "2":
            mostrar_misiones()
        elif opcion == "3":
            mostrar_monstruos()
        elif opcion == "4":
            registrar_heroe()
        elif opcion == "5":
            print("\n¡Hasta luego, aventurero!")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    menu()