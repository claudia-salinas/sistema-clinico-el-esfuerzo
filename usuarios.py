"""Roles de usuario del Sistema Clínico El Esfuerzo (RF-04).

Aquí se aplica la herencia y el polimorfismo: Usuario es la clase base y
Medico y Administrativo son sus clases hijas. Cada rol tiene permisos
distintos. Lo más importante es que el personal administrativo NO puede ver
los diagnósticos de los pacientes.
"""

# Nombres de los permisos (se usan como "etiquetas")
VER_DIAGNOSTICO = "ver_diagnostico"
AGREGAR_ATENCION = "agregar_atencion"
REGISTRAR_PACIENTE = "registrar_paciente"
BUSCAR_PACIENTE = "buscar_paciente"
VER_HISTORIAL = "ver_historial"


class Usuario:
    """Clase base: cualquier persona que usa el sistema.

    Las clases hijas definen sus permisos en el atributo PERMISOS.
    """

    ROL = "Usuario"
    PERMISOS = frozenset()  # la clase base no tiene ningún permiso

    def __init__(self, nombre_usuario, nombre_completo):
        if nombre_usuario.strip() == "" or nombre_completo.strip() == "":
            raise ValueError("El usuario y el nombre completo son obligatorios.")
        self.__nombre_usuario = nombre_usuario.strip()
        self.__nombre_completo = nombre_completo.strip()

    @property
    def nombre_usuario(self):
        return self.__nombre_usuario

    @property
    def nombre_completo(self):
        return self.__nombre_completo

    @property
    def rol(self):
        return self.ROL

    def tiene_permiso(self, permiso):
        """Devuelve True si el rol del usuario incluye ese permiso."""
        return permiso in self.PERMISOS

    def exigir_permiso(self, permiso):
        """Si el usuario no tiene el permiso, lanza PermissionError."""
        if not self.tiene_permiso(permiso):
            raise PermissionError(
                f"El rol {self.ROL} no tiene permiso para esta acción.")

    # ---------- Operaciones del sistema (cada una revisa el permiso) ----------

    def buscar_por_dni(self, sistema, dni):
        self.exigir_permiso(BUSCAR_PACIENTE)
        return sistema.buscar_por_dni(dni.strip())

    def buscar_por_apellido(self, sistema, texto):
        self.exigir_permiso(BUSCAR_PACIENTE)
        return sistema.buscar_por_apellido(texto)

    def registrar_paciente(self, sistema, dni, nombres, apellidos,
                           fecha_nacimiento, telefono):
        self.exigir_permiso(REGISTRAR_PACIENTE)
        return sistema.registrar_paciente(
            dni, nombres, apellidos, fecha_nacimiento, telefono)

    def agregar_atencion(self, sistema, dni, diagnostico, tratamiento,
                         notas="", documento="", fecha=None):
        self.exigir_permiso(AGREGAR_ATENCION)
        return sistema.agregar_atencion(
            dni, diagnostico, tratamiento, notas, documento, fecha)

    def ver_historial(self, paciente):
        """Devuelve una línea de texto por atención, según lo que el rol puede ver."""
        self.exigir_permiso(VER_HISTORIAL)
        return list(map(self._describir_atencion, paciente.historial.atenciones))

    def _describir_atencion(self, atencion):
        """Cada rol decide cuánto de la atención muestra (polimorfismo)."""
        raise NotImplementedError("Cada rol define qué datos de la atención ve.")


class Medico(Usuario):
    """Médico: ve el historial completo, incluidos los diagnósticos."""

    ROL = "Médico"
    PERMISOS = frozenset({
        BUSCAR_PACIENTE,
        VER_HISTORIAL,
        VER_DIAGNOSTICO,
        AGREGAR_ATENCION,
    })

    def _describir_atencion(self, atencion):
        # El médico ve la atención completa (fecha, diagnóstico, tratamiento...)
        return atencion.mostrar()


class Administrativo(Usuario):
    """Personal administrativo: registra y busca pacientes, pero NO ve diagnósticos."""

    ROL = "Administrativo"
    PERMISOS = frozenset({
        BUSCAR_PACIENTE,
        REGISTRAR_PACIENTE,
        VER_HISTORIAL,
    })

    def _describir_atencion(self, atencion):
        # Solo se muestra la fecha y los documentos adjuntos; el diagnóstico
        # y el tratamiento quedan ocultos.
        texto = (f"{atencion.fecha.strftime('%d/%m/%Y')} | "
                 f"Diagnóstico: [RESERVADO]")
        if atencion.documentos:
            texto += " | Documentos: " + ", ".join(atencion.documentos)
        return texto
