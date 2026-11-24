"""Clase gestora del Sistema Clínico El Esfuerzo.

Guarda la colección de pacientes y ofrece las operaciones principales.
Las búsquedas usan programación funcional (filter y lambda).
"""
from modelos import Atencion, Paciente


class SistemaClinico:

    def __init__(self, pacientes=None):
        self.__pacientes = list(pacientes) if pacientes else []

    @property
    def total_pacientes(self):
        return len(self.__pacientes)

    def buscar_por_dni(self, dni):
        """Devuelve el paciente con ese DNI, o None si no existe."""
        coincidencias = list(filter(
            lambda p: p.coincide_dni(dni), self.__pacientes))
        return coincidencias[0] if coincidencias else None

    def buscar_por_apellido(self, texto):
        """Devuelve la lista de pacientes cuyo apellido contiene el texto."""
        texto = texto.strip().lower()
        if len(texto) < 2:
            raise ValueError("Escriba al menos 2 letras del apellido.")
        return list(filter(
            lambda p: texto in p.apellidos.lower(), self.__pacientes))

    def registrar_paciente(self, dni, nombres, apellidos,
                           fecha_nacimiento, telefono):
        """Registra un paciente nuevo; su historial clínico se crea vacío."""
        nuevo = Paciente(dni, nombres, apellidos, fecha_nacimiento, telefono)
        if self.buscar_por_dni(dni.strip()) is not None:
            raise ValueError("Ya existe un paciente con ese DNI.")
        self.__pacientes.append(nuevo)
        return nuevo

    def agregar_atencion(self, dni, diagnostico, tratamiento,
                         notas="", documento="", fecha=None):
        """Agrega una atención al historial clínico del paciente con ese DNI."""
        paciente = self.buscar_por_dni(dni.strip())
        if paciente is None:
            raise ValueError("No existe un paciente con ese DNI.")
        atencion = Atencion(diagnostico, tratamiento, notas, fecha)
        if documento.strip() != "":
            atencion.adjuntar_documento(documento)
        paciente.historial.agregar_atencion(atencion)
        return atencion
