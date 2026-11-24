"""Prueba de viabilidad: ¿la búsqueda es rápida con 500 pacientes? (CE-02)

Se ejecuta aparte del menú:  python prueba_viabilidad.py
Cada búsqueda se repite varias veces y se calcula el promedio, para que la
medición sea más estable que con una sola ejecución.
"""
import time

from datos_prueba import generar_pacientes_de_prueba
from sistema import SistemaClinico

REPETICIONES = 100
LIMITE_SEGUNDOS = 3


def medir_promedio(busqueda):
    """Ejecuta la búsqueda varias veces y devuelve el tiempo promedio (s)."""
    inicio = time.perf_counter()
    for _ in range(REPETICIONES):
        busqueda()
    return (time.perf_counter() - inicio) / REPETICIONES


def main():
    sistema = SistemaClinico(generar_pacientes_de_prueba())
    print("=== PRUEBA DE VIABILIDAD ===")
    print("Total de pacientes registrados:", sistema.total_pacientes)
    print("Repeticiones por búsqueda:", REPETICIONES)

    tiempo_dni = medir_promedio(lambda: sistema.buscar_por_dni("12345678"))
    print(f"Búsqueda por DNI (promedio): {tiempo_dni * 1000:.4f} ms")

    tiempo_apellido = medir_promedio(lambda: sistema.buscar_por_apellido("rojas"))
    print(f"Búsqueda por apellido (promedio): {tiempo_apellido * 1000:.4f} ms")

    if tiempo_dni < LIMITE_SEGUNDOS and tiempo_apellido < LIMITE_SEGUNDOS:
        print("CE-02: CUMPLE (las búsquedas tardan menos de 3 segundos)")
    else:
        print("CE-02: NO CUMPLE")


if __name__ == "__main__":
    main()
