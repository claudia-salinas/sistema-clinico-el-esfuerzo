import random
import time


class Paciente:
    def __init__(self, dni, nombres, apellidos):
        # Validaciones: si algo está mal, se lanza un error
        if not (dni.isdigit() and len(dni) == 8):
            raise ValueError("El DNI debe tener 8 dígitos numéricos.")
        if nombres.strip() == "" or apellidos.strip() == "":
            raise ValueError("Los nombres y apellidos son obligatorios.")
        self.__dni = dni
        self.__nombres = nombres
        self.__apellidos = apellidos

    def obtener_nombre_completo(self):
        return f"{self.__nombres} {self.__apellidos}"

    def coincide_dni(self, dni):
        return self.__dni == dni

    @property
    def dni_enmascarado(self):
        return "****" + self.__dni[-4:]

    @property
    def apellidos(self):
        return self.__apellidos

    def mostrar_ficha(self):
        return f"{self.obtener_nombre_completo()} - DNI: {self.dni_enmascarado}"


# Datos ficticios para simular un hospital con pacientes ya registrados
NOMBRES = ["Ana", "Luis", "María", "Carlos", "Rosa", "José", "Lucía", "Pedro",
           "Carmen", "Jorge", "Elena", "Miguel", "Sofía", "Diego", "Paola"]
APELLIDOS = ["Quispe", "Flores", "Rojas", "Mendoza", "Vargas", "Castillo",
             "Torres", "Ramos", "Chávez", "Salazar", "Cruz", "Paredes"]


def generar_pacientes(cantidad):
    """Crea pacientes ficticios con DNI distintos."""
    random.seed(2026)  # con la misma semilla salen siempre los mismos datos
    dnis = random.sample(range(10000000, 100000000), cantidad)
    return [
        Paciente(
            str(dni),
            random.choice(NOMBRES),
            random.choice(APELLIDOS) + " " + random.choice(APELLIDOS))
        for dni in dnis
    ]


# 497 pacientes aleatorios + 3 pacientes conocidos = 500
pacientes = generar_pacientes(497)
pacientes.append(Paciente("12345678", "Ana", "Torres Flores"))
pacientes.append(Paciente("23456789", "Luis", "Rojas Vargas"))
pacientes.append(Paciente("34567890", "María", "Mendoza Cruz"))

# ---------------------------------------------------------------
# PRUEBA DE VIABILIDAD: ¿la búsqueda es rápida con 500 pacientes?
# ---------------------------------------------------------------
print("=== PRUEBA DE VIABILIDAD ===")
print("Total de pacientes registrados:", len(pacientes))

inicio = time.perf_counter()
resultado = list(filter(lambda p: p.coincide_dni("12345678"), pacientes))
tiempo_dni = time.perf_counter() - inicio
print(f"Búsqueda por DNI: {tiempo_dni * 1000:.4f} ms")

inicio = time.perf_counter()
coincidencias = list(filter(
    lambda p: "rojas" in p.apellidos.lower(), pacientes))
tiempo_apellido = time.perf_counter() - inicio
print(f"Búsqueda por apellido: {tiempo_apellido * 1000:.4f} ms")

if tiempo_dni < 3 and tiempo_apellido < 3:
    print("CE-02: CUMPLE (las búsquedas tardan menos de 3 segundos)")
else:
    print("CE-02: NO CUMPLE")

# ---------------------------------------------------------------
# MENÚ: uso del sistema por el personal del hospital
# ---------------------------------------------------------------
opcion = ""
while opcion != "4":
    print("\n=== SISTEMA CLÍNICO EL ESFUERZO ===")
    print("1. Registrar paciente nuevo")
    print("2. Buscar paciente por DNI")
    print("3. Buscar pacientes por apellido")
    print("4. Salir")
    opcion = input("Elija una opción: ")

    if opcion == "1":
        dni = input("DNI (8 dígitos): ")
        nombres = input("Nombres: ")
        apellidos = input("Apellidos: ")
        try:
            if list(filter(lambda p: p.coincide_dni(dni), pacientes)):
                print("Ya existe un paciente con ese DNI.")
            else:
                nuevo = Paciente(dni, nombres, apellidos)
                pacientes.append(nuevo)
                print("Paciente registrado:", nuevo.mostrar_ficha())
                print("Total de pacientes:", len(pacientes))
        except ValueError as error:
            print("No se pudo registrar:", error)

    elif opcion == "2":
        dni_ingresado = input("Ingrese el DNI: ")
        encontrados = list(filter(
            lambda p: p.coincide_dni(dni_ingresado), pacientes))
        if encontrados:
            print("Paciente encontrado:", encontrados[0].mostrar_ficha())
        else:
            print("No existe un paciente con ese DNI.")

    elif opcion == "3":
        apellido_ingresado = input("Ingrese el apellido: ")
        encontrados = list(filter(
            lambda p: apellido_ingresado.lower() in p.apellidos.lower(),
            pacientes))
        print(f"Se encontraron {len(encontrados)} paciente(s).")
        if len(encontrados) > 5:
            print("Se muestran solo los primeros 5:")
        for paciente in encontrados[:5]:
            print("  ", paciente.mostrar_ficha())

    elif opcion == "4":
        print("Programa finalizado.")

    else:
        print("Opción no válida. Elija 1, 2, 3 o 4.")