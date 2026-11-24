"""Datos ficticios para simular un hospital con pacientes ya registrados.

Todos los datos son inventados (restricción RD-04).
"""
import random
from datetime import date, timedelta

from modelos import Paciente

NOMBRES = ["Ana", "Luis", "María", "Carlos", "Rosa", "José", "Lucía", "Pedro",
           "Carmen", "Jorge", "Elena", "Miguel", "Sofía", "Diego", "Paola"]
APELLIDOS = ["Quispe", "Flores", "Rojas", "Mendoza", "Vargas", "Castillo",
             "Torres", "Ramos", "Chávez", "Salazar", "Cruz", "Paredes"]


def generar_pacientes(cantidad):
    """Crea pacientes ficticios con DNI distintos."""
    random.seed(2026)  # con la misma semilla salen siempre los mismos datos
    dnis = random.sample(range(10000000, 100000000), cantidad)
    primer_dia = date(1940, 1, 1)
    dias_posibles = (date(2024, 12, 31) - primer_dia).days
    pacientes = []
    for dni in dnis:
        nombres = random.choice(NOMBRES)
        apellidos = random.choice(APELLIDOS) + " " + random.choice(APELLIDOS)
        nacimiento = primer_dia + timedelta(days=random.randint(0, dias_posibles))
        telefono = "9" + str(random.randint(10000000, 99999999))
        pacientes.append(
            Paciente(str(dni), nombres, apellidos, nacimiento, telefono))
    return pacientes


def generar_pacientes_de_prueba():
    """497 pacientes aleatorios + 3 pacientes conocidos = 500."""
    pacientes = generar_pacientes(497)
    pacientes.append(Paciente("12345678", "Ana", "Torres Flores",
                              date(1990, 5, 14), "987654321"))
    pacientes.append(Paciente("23456789", "Luis", "Rojas Vargas",
                              date(1985, 11, 2), "976543210"))
    pacientes.append(Paciente("34567890", "María", "Mendoza Cruz",
                              date(2001, 3, 27), "965432109"))
    return pacientes
