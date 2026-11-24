"""Menú principal del Sistema Clínico El Esfuerzo (paradigma estructurado).

Ejecutar con:  python main.py
Requiere Python 3.10 o superior (se usa match/case).
"""
from datos_prueba import generar_pacientes_de_prueba
from modelos import leer_fecha
from sistema import SistemaClinico


def registrar_paciente(sistema):
    dni = input("DNI (8 dígitos): ")
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ")
    telefono = input("Teléfono (9 dígitos): ")
    try:
        nuevo = sistema.registrar_paciente(
            dni, nombres, apellidos, leer_fecha(nacimiento), telefono)
        print("Paciente registrado:", nuevo.mostrar_ficha())
        print("Se creó su historial clínico.")
        print("Total de pacientes:", sistema.total_pacientes)
    except ValueError as error:
        print("No se pudo registrar:", error)


def buscar_por_dni(sistema):
    dni = input("Ingrese el DNI: ")
    paciente = sistema.buscar_por_dni(dni.strip())
    if paciente is not None:
        print("Paciente encontrado:", paciente.mostrar_ficha())
    else:
        print("No existe un paciente con ese DNI.")


def buscar_por_apellido(sistema):
    texto = input("Ingrese el apellido: ")
    try:
        encontrados = sistema.buscar_por_apellido(texto)
    except ValueError as error:
        print(error)
        return
    print(f"Se encontraron {len(encontrados)} paciente(s).")
    if len(encontrados) > 5:
        print("Se muestran solo los primeros 5:")
    for paciente in encontrados[:5]:
        print("  ", paciente.mostrar_ficha())


def agregar_atencion(sistema):
    dni = input("DNI del paciente: ")
    diagnostico = input("Diagnóstico: ")
    tratamiento = input("Tratamiento: ")
    notas = input("Notas (opcional): ")
    documento = input("Documento adjunto (opcional, nombre del archivo): ")
    try:
        sistema.agregar_atencion(dni, diagnostico, tratamiento,
                                 notas, documento)
        print("Atención registrada en el historial clínico.")
    except ValueError as error:
        print("No se pudo registrar la atención:", error)


def ver_historial(sistema):
    dni = input("DNI del paciente: ")
    paciente = sistema.buscar_por_dni(dni.strip())
    if paciente is None:
        print("No existe un paciente con ese DNI.")
        return
    print("Historial clínico de", paciente.mostrar_ficha())
    lineas = paciente.historial.resumen()
    if not lineas:
        print("  Sin atenciones registradas.")
    for numero, linea in enumerate(lineas, start=1):
        print(f"  {numero}. {linea}")


def main():
    # Hospital simulado con 500 pacientes ficticios ya registrados
    sistema = SistemaClinico(generar_pacientes_de_prueba())
    opcion = ""
    while opcion != "6":
        print("\n=== SISTEMA CLÍNICO EL ESFUERZO ===")
        print("1. Registrar paciente nuevo")
        print("2. Buscar paciente por DNI")
        print("3. Buscar pacientes por apellido")
        print("4. Agregar atención a un paciente")
        print("5. Ver historial clínico de un paciente")
        print("6. Salir")
        opcion = input("Elija una opción: ")

        match opcion:
            case "1":
                registrar_paciente(sistema)
            case "2":
                buscar_por_dni(sistema)
            case "3":
                buscar_por_apellido(sistema)
            case "4":
                agregar_atencion(sistema)
            case "5":
                ver_historial(sistema)
            case "6":
                print("Programa finalizado.")
            case _:
                # El guion bajo es el "default" del switch
                print("Opción no válida. Elija del 1 al 6.")


if __name__ == "__main__":
    main()
