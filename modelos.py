"""Clases del dominio del Sistema Clínico El Esfuerzo.

Aquí se aplica la programación orientada a objetos: cada clase guarda sus
datos como atributos privados (con doble guion bajo) y los expone solo
mediante propiedades o métodos controlados.
"""
from datetime import date, datetime

from seguridad import cifrar, descifrar, enmascarar_dni


def leer_fecha(texto):
    """Convierte un texto con formato dd/mm/aaaa en un objeto date."""
    try:
        fecha = datetime.strptime(texto.strip(), "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("La fecha debe tener el formato dd/mm/aaaa.")
    if fecha > date.today():
        raise ValueError("La fecha no puede ser futura.")
    return fecha


class Atencion:
    """Una atención médica registrada en el historial de un paciente."""

    def __init__(self, diagnostico, tratamiento, notas="", fecha=None):
        if diagnostico.strip() == "" or tratamiento.strip() == "":
            raise ValueError("El diagnóstico y el tratamiento son obligatorios.")
        # Si no se indica la fecha, se usa la de hoy
        self.__fecha = fecha if fecha is not None else date.today()
        # Los datos clínicos se guardan cifrados (RNF-01)
        self.__diagnostico = cifrar(diagnostico.strip())
        self.__tratamiento = cifrar(tratamiento.strip())
        self.__notas = cifrar(notas.strip())
        self.__documentos = []

    @property
    def fecha(self):
        return self.__fecha

    @property
    def diagnostico(self):
        return descifrar(self.__diagnostico)

    @property
    def documentos(self):
        # Se devuelve una copia para que nadie modifique la lista original
        return list(self.__documentos)

    def adjuntar_documento(self, nombre_archivo):
        """Registra el nombre de un documento clínico adjunto a la atención."""
        if nombre_archivo.strip() == "":
            raise ValueError("El nombre del documento no puede estar vacío.")
        self.__documentos.append(nombre_archivo.strip())

    def mostrar(self):
        notas = descifrar(self.__notas)
        texto = (f"{self.__fecha.strftime('%d/%m/%Y')} | "
                 f"Diagnóstico: {descifrar(self.__diagnostico)} | "
                 f"Tratamiento: {descifrar(self.__tratamiento)}")
        if notas:
            texto += f" | Notas: {notas}"
        if self.__documentos:
            texto += " | Documentos: " + ", ".join(self.__documentos)
        return texto


class HistorialClinico:
    """Conjunto de atenciones de un paciente, en orden de registro."""

    def __init__(self):
        self.__atenciones = []

    def agregar_atencion(self, atencion):
        self.__atenciones.append(atencion)

    @property
    def atenciones(self):
        return list(self.__atenciones)

    def cantidad(self):
        return len(self.__atenciones)

    def resumen(self):
        """Devuelve una línea de texto por cada atención (uso de map)."""
        return list(map(lambda atencion: atencion.mostrar(), self.__atenciones))


class Paciente:
    """Paciente del hospital. Al crearlo se crea también su historial clínico."""

    def __init__(self, dni, nombres, apellidos, fecha_nacimiento, telefono):
        # Validaciones: si algo está mal, se lanza un error
        dni = dni.strip()
        telefono = telefono.strip()
        if not (dni.isdigit() and len(dni) == 8):
            raise ValueError("El DNI debe tener 8 dígitos numéricos.")
        if nombres.strip() == "" or apellidos.strip() == "":
            raise ValueError("Los nombres y apellidos son obligatorios.")
        if not (telefono.isdigit() and len(telefono) == 9):
            raise ValueError("El teléfono debe tener 9 dígitos numéricos.")
        # El DNI y el teléfono se guardan cifrados (RNF-01)
        self.__dni = cifrar(dni)
        self.__nombres = nombres.strip()
        self.__apellidos = apellidos.strip()
        self.__fecha_nacimiento = fecha_nacimiento
        self.__telefono = cifrar(telefono)
        self.__historial = HistorialClinico()

    def obtener_nombre_completo(self):
        return f"{self.__nombres} {self.__apellidos}"

    def coincide_dni(self, dni):
        return descifrar(self.__dni) == dni

    @property
    def dni_enmascarado(self):
        return enmascarar_dni(descifrar(self.__dni))

    @property
    def apellidos(self):
        return self.__apellidos

    @property
    def fecha_nacimiento(self):
        return self.__fecha_nacimiento

    @property
    def historial(self):
        return self.__historial

    def mostrar_ficha(self):
        return f"{self.obtener_nombre_completo()} - DNI: {self.dni_enmascarado}"
