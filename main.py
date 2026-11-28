"""Menú principal del Sistema Clínico El Esfuerzo (paradigma estructurado).

Ejecutar con:  python main.py
Requiere Python 3.10 o superior (se usa match/case).

Antes de ver el menú, la persona elige con qué usuario ingresa (RF-04).
Cada rol ve solo las opciones que tiene permitidas: el personal
administrativo no puede ver diagnósticos ni agregar atenciones.
Cada acción queda registrada en la bitácora (RF-05).
"""
from bitacora import Bitacora
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


def registrar_paciente(sistema, usuario, bitacora):
    dni = input("DNI (8 dígitos): ")
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ")
    telefono = input("Teléfono (9 dígitos): ")
    try:
        nuevo = usuario.registrar_paciente(
            sistema, dni, nombres, apellidos, leer_fecha(nacimiento), telefono)
        bitacora.registrar(usuario.nombre_usuario, "REGISTRAR_PACIENTE", dni=dni)
        print("Paciente registrado:", nuevo.mostrar_ficha())
        print("Se creó su historial clínico.")
        print("Total de pacientes:", sistema.total_pacientes)
    except ValueError as error:
        bitacora.registrar(usuario.nombre_usuario, "REGISTRAR_PACIENTE", dni=dni,
                           detalle=f"rechazado: {error}")
        print("No se pudo registrar:", error)


def buscar_por_dni(sistema, usuario, bitacora):
    dni = input("Ingrese el DNI: ")
    paciente = usuario.buscar_por_dni(sistema, dni)
    bitacora.registrar(usuario.nombre_usuario, "BUSCAR_PACIENTE", dni=dni,
                       detalle="encontrado" if paciente else "no encontrado")
    if paciente is not None:
        print("Paciente encontrado:", paciente.mostrar_ficha())
    else:
        print("No existe un paciente con ese DNI.")


def buscar_por_apellido(sistema, usuario, bitacora):
    texto = input("Ingrese el apellido: ")
    try:
        encontrados = usuario.buscar_por_apellido(sistema, texto)
    except ValueError as error:
        print(error)
        return
    bitacora.registrar(usuario.nombre_usuario, "BUSCAR_PACIENTE",
                       detalle=f"búsqueda por apellido: {len(encontrados)} resultado(s)")
    print(f"Se encontraron {len(encontrados)} paciente(s).")
    if len(encontrados) > 5:
        print("Se muestran solo los primeros 5:")
    for paciente in encontrados[:5]:
        print("  ", paciente.mostrar_ficha())


def agregar_atencion(sistema, usuario, bitacora):
    dni = input("DNI del paciente: ")
    diagnostico = input("Diagnóstico: ")
    tratamiento = input("Tratamiento: ")
    notas = input("Notas (opcional): ")
    documento = input("Documento adjunto (opcional, nombre del archivo): ")
    try:
        usuario.agregar_atencion(sistema, dni, diagnostico, tratamiento,
                                 notas, documento)
        bitacora.registrar(usuario.nombre_usuario, "AGREGAR_ATENCION", dni=dni)
        print("Atención registrada en el historial clínico.")
    except ValueError as error:
        # No se guarda el diagnóstico en la bitácora, solo el motivo del rechazo
        bitacora.registrar(usuario.nombre_usuario, "AGREGAR_ATENCION", dni=dni,
                           detalle=f"rechazado: {error}")
        print("No se pudo registrar la atención:", error)


def ver_historial(sistema, usuario, bitacora):
    dni = input("DNI del paciente: ")
    paciente = usuario.buscar_por_dni(sistema, dni)
    if paciente is None:
        bitacora.registrar(usuario.nombre_usuario, "VER_HISTORIAL", dni=dni,
                           detalle="no encontrado")
        print("No existe un paciente con ese DNI.")
        return
    print("Historial clínico de", paciente.mostrar_ficha())
    # Cada rol recibe el historial según lo que le toca ver
    lineas = usuario.ver_historial(paciente)
    bitacora.registrar(usuario.nombre_usuario, "VER_HISTORIAL", dni=dni)
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


def trabajar_con_sesion(sistema, usuario, bitacora):
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
                    elegida[3](sistema, usuario, bitacora)
                except PermissionError as error:
                    bitacora.registrar(usuario.nombre_usuario, "ACCESO_DENEGADO",
                                       detalle=str(error))
                    print("Acceso denegado:", error)
            case "1" | "2" | "3" | "4" | "5":
                # La opción existe, pero este rol no la tiene permitida
                bitacora.registrar(usuario.nombre_usuario, "ACCESO_DENEGADO",
                                   detalle=f"opción {opcion}")
                print("Opción no disponible para su rol.")
            case _:
                # El guion bajo es el "default" del switch
                print("Opción no válida.")


def main():
    # Hospital simulado con 500 pacientes ficticios ya registrados
    sistema = SistemaClinico(generar_pacientes_de_prueba())
    usuarios = crear_usuarios_de_prueba()
    bitacora = Bitacora()
    while True:
        usuario = iniciar_sesion(usuarios)
        if usuario is None:
            break
        bitacora.registrar(usuario.nombre_usuario, "INICIO_SESION")
        cambiar_usuario = trabajar_con_sesion(sistema, usuario, bitacora)
        bitacora.registrar(usuario.nombre_usuario, "CIERRE_SESION")
        if not cambiar_usuario:
            break
    print("Programa finalizado.")


if __name__ == "__main__":
    main()
