from database import BibliotecaDB

def mostrar_menu():
    print("\n==============================")
    print("   BIBLIOTECA PERSONAL     ")
    print("==============================")
    print("1. Agregar nuevo libro")
    print("2. Ver listado de libros")
    print("3. Actualizar informacion de un libro")
    print("4. Eliminar libro existente")
    print("5. Buscar libros")
    print("6. Salir")
    print("==============================")

def solicitar_estado():
    """Valida que el estado ingresado sea Leido o No leido."""
    while True:
        estado = input("Estado de lectura (Leido / No leido): ").strip().capitalize()
        if estado in ["Leido", "No leido"]:
            return estado
        print("Opcion invalida. Por favor escriba 'Leido' o 'No leido'.")

def main():
    db = BibliotecaDB()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion (1-6): ").strip()

        if opcion == "1":
            print("\n--- Agregar Nuevo Libro ---")
            titulo = input("Titulo: ").strip()
            autor = input("Autor: ").strip()
            genero = input("Genero: ").strip()
            estado = solicitar_estado()

            if titulo and autor and genero:
                db.agregar_libro(titulo, autor, genero, estado)
                print("Libro agregado exitosamente.")
            else:
                print("Error: Los campos de texto no pueden estar vacios.")

        elif opcion == "2":
            print("\n--- Listado de Libros ---")
            libros = db.obtener_libros()
            if not libros:
                print("No hay libros registrados en la biblioteca.")
            else:
                for libro in libros:
                    print(f"ID: {libro[0]} | Titulo: {libro[1]} | Autor: {libro[2]} | Genero: {libro[3]} | Estado: {libro[4]}")

        elif opcion == "3":
            print("\n--- Actualizar Libro ---")
            libros = db.obtener_libros()
            if not libros:
                print("No hay libros para actualizar.")
                continue

            for libro in libros:
                print(f"ID: {libro[0]} | Titulo: {libro[1]}")

            try:
                libro_id = int(input("Ingrese el ID del libro que desea actualizar: "))
            except ValueError:
                print("Error: Debe ingresar un numero entero valido.")
                continue

            print("\nIngrese los nuevos datos:")
            titulo = input("Nuevo titulo: ").strip()
            autor = input("Nuevo autor: ").strip()
            genero = input("Nuevo genero: ").strip()
            estado = solicitar_estado()

            if titulo and autor and genero:
                actualizado = db.actualizar_libro(libro_id, titulo, autor, genero, estado)
                if actualizado:
                    print("Libro actualizado correctamente.")
                else:
                    print("No se encontro un libro con el ID especificado.")
            else:
                print("Error: Los campos principales son obligatorios.")

        elif opcion == "4":
            print("\n--- Eliminar Libro ---")
            libros = db.obtener_libros()
            if not libros:
                print("No hay libros para eliminar.")
                continue

            for libro in libros:
                print(f"ID: {libro[0]} | Titulo: {libro[1]}")

            try:
                libro_id = int(input("Ingrese el ID del libro a eliminar: "))
                eliminado = db.eliminar_libro(libro_id)
                if eliminado:
                    print("Libro eliminado correctamente.")
                else:
                    print("No se encontro un libro con el ID especificado.")
            except ValueError:
                print("Error: Debe ingresar un ID numerico valido.")

        elif opcion == "5":
            print("\n--- Buscar Libros ---")
            print("Buscar por:")
            print("1. Titulo")
            print("2. Autor")
            print("3. Genero")
            sub_op = input("Seleccione criterio (1-3): ").strip()

            criterios_map = {"1": "titulo", "2": "autor", "3": "genero"}
            if sub_op in criterios_map:
                criterio = criterios_map[sub_op]
                valor = input(f"Ingrese el {criterio} a buscar: ").strip()
                resultados = db.buscar_libros(criterio, valor)

                if not resultados:
                    print("No se encontraron coincidencias.")
                else:
                    print(f"\nSe encontraron {len(resultados)} resultado(s):")
                    for libro in resultados:
                        print(f"ID: {libro[0]} | Titulo: {libro[1]} | Autor: {libro[2]} | Genero: {libro[3]} | Estado: {libro[4]}")
            else:
                print("Opcion de busqueda invalida.")

        elif opcion == "6":
            print("\nGracias por usar el Administrador de Biblioteca. Saliendo...")
            break
        else:
            print("Opcion invalida. Por favor, elija un numero entre 1 y 6.")

if __name__ == "__main__":
    main()