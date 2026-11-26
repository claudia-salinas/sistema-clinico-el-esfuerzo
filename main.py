"""Menú principal del Sistema Clínico El Esfuerzo (paradigma estructurado).

Ejecutar con:  python main.py
Requiere Python 3.10 o superior (se usa match/case).

Antes de ver el menú, la persona elige con qué usuario ingresa (RF-04).
Cada rol ve solo las opciones que tiene permitidas: el personal
administrativo no puede ver diagnósticos ni agregar atenciones.
"""
from datos_prueba import generar_pacientes_de_prueba
from modelos import leer_fecha
from sistema import SistemaClinico
from usuarios import (Administrativo, Medico, AGREGAR_ATENCION, BUSCAR_PACIENTE,
                      REGISTRAR_PACIENTE, VER_HISTORIAL)


def crear_usuarios_de_prueba():
    """Usuarios ficticios del hospital: dos médicos y un administrativo."""
    return {
        "1": Medico("mperez", "Marta Pérez"),
        "2": Medico("rquispe", "Raúl Quispe"),
        "3": Administrativo("jlopez", "Juan López"),
    }


def iniciar_sesion(usuarios):
    """Pide elegir un usuario. Devuelve el usuario o None si decide salir."""
    while True:
        print("\n=== INICIO DE SESIÓN ===")
        for numero, usuario in usuarios.items():
            print(f"{numero}. {usuario.nombre_completo} ({usuario.rol})")
        print("0. Salir del programa")
        opcion = input("Elija un usuario: ").strip()
        if opcion == "0":
            return None
        if opcion in usuarios:
            return usuarios[opcion]
        print("Opción no válida.")


def registrar_paciente(sistema, usuario):
    dni = input("DNI (8 dígitos): ")
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ")
    telefono = input("Teléfono (9 dígitos): ")
    try:
        nuevo = usuario.registrar_paciente(
            sistema, dni, nombres, apellidos, leer_fecha(nacimiento), telefono)
        print("Paciente registrado:", nuevo.mostrar_ficha())
        print("Se creó su historial clínico.")
        print("Total de pacientes:", sistema.total_pacientes)
    except ValueError as error:
        print("No se pudo registrar:", error)


def buscar_por_dni(sistema, usuario):
    dni = input("Ingrese el DNI: ")
    paciente = usuario.buscar_por_dni(sistema, dni)
    if paciente is not None:
        print("Paciente encontrado:", paciente.mostrar_ficha())
    else:
        print("No existe un paciente con ese DNI.")


def buscar_por_apellido(sistema, usuario):
    texto = input("Ingrese el apellido: ")
    try:
        encontrados = usuario.buscar_por_apellido(sistema, texto)
    except ValueError as error:
        print(error)
        return
    print(f"Se encontraron {len(encontrados)} paciente(s).")
    if len(encontrados) > 5:
        print("Se muestran solo los primeros 5:")
    for paciente in encontrados[:5]:
        print("  ", paciente.mostrar_ficha())


def agregar_atencion(sistema, usuario):
    dni = input("DNI del paciente: ")
    diagnostico = input("Diagnóstico: ")
    tratamiento = input("Tratamiento: ")
    notas = input("Notas (opcional): ")
    documento = input("Documento adjunto (opcional, nombre del archivo): ")
    try:
        usuario.agregar_atencion(sistema, dni, diagnostico, tratamiento,
                                 notas, documento)
        print("Atención registrada en el historial clínico.")
    except ValueError as error:
        print("No se pudo registrar la atención:", error)


def ver_historial(sistema, usuario):
    dni = input("DNI del paciente: ")
    paciente = usuario.buscar_por_dni(sistema, dni)
    if paciente is None:
        print("No existe un paciente con ese DNI.")
        return
    print("Historial clínico de", paciente.mostrar_ficha())
    # Cada rol recibe el historial según lo que le toca ver
    lineas = usuario.ver_historial(paciente)
    if not lineas:
        print("  Sin atenciones registradas.")
    for numero, linea in enumerate(lineas, start=1):
        print(f"  {numero}. {linea}")


# Opciones del menú: (código, permiso que se necesita, texto, función)
OPCIONES = [
    ("1", REGISTRAR_PACIENTE, "Registrar paciente nuevo", registrar_paciente),
    ("2", BUSCAR_PACIENTE, "Buscar paciente por DNI", buscar_por_dni),
    ("3", BUSCAR_PACIENTE, "Buscar pacientes por apellido", buscar_por_apellido),
    ("4", AGREGAR_ATENCION, "Agregar atención a un paciente", agregar_atencion),
    ("5", VER_HISTORIAL, "Ver historial clínico de un paciente", ver_historial),
]


def menu_del_usuario(usuario):
    """Devuelve solo las opciones que el rol del usuario tiene permitidas."""
    return [opcion for opcion in OPCIONES if usuario.tiene_permiso(opcion[1])]


def trabajar_con_sesion(sistema, usuario):
    """Muestra el menú del usuario. Devuelve True si pidió cambiar de usuario."""
    while True:
        permitidas = menu_del_usuario(usuario)
        print("\n=== SISTEMA CLÍNICO EL ESFUERZO ===")
        print(f"Usuario: {usuario.nombre_completo} ({usuario.rol})")
        for codigo, _, texto, _ in permitidas:
            print(f"{codigo}. {texto}")
        print("6. Cambiar de usuario")
        print("7. Salir")
        opcion = input("Elija una opción: ").strip()

        codigos_permitidos = [o[0] for o in permitidas]
        match opcion:
            case "6":
                return True
            case "7":
                return False
            case "1" | "2" | "3" | "4" | "5" if opcion in codigos_permitidos:
                # Se busca la función solo entre las opciones de este rol
                elegida = next(o for o in permitidas if o[0] == opcion)
                try:
                    elegida[3](sistema, usuario)
                except PermissionError as error:
                    print("Acceso denegado:", error)
            case _:
                # El guion bajo es el "default" del switch
                print("Opción no válida o no disponible para su rol.")


def main():
    # Hospital simulado con 500 pacientes ficticios ya registrados
    sistema = SistemaClinico(generar_pacientes_de_prueba())
    usuarios = crear_usuarios_de_prueba()
    while True:
        usuario = iniciar_sesion(usuarios)
        if usuario is None:
            break
        if not trabajar_con_sesion(sistema, usuario):
            break
    print("Programa finalizado.")


if __name__ == "__main__":
    main()