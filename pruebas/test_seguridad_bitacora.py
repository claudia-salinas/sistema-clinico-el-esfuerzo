"""Pruebas de RNF-01 (cifrado), RF-04 (roles) y RF-05 (bitácora)."""
from datetime import date

import pytest

import seguridad
from bitacora import Bitacora
from modelos import Atencion, Paciente
from sistema import SistemaClinico
from usuarios import Administrativo, Medico


def crear_sistema():
    sistema = SistemaClinico()
    sistema.registrar_paciente("12345678", "Ana", "Torres Flores",
                               date(1990, 5, 14), "987654321")
    return sistema


# ---------- RNF-01: cifrado ----------
def test_cifrar_y_descifrar_devuelve_el_texto_original():
    token = seguridad.cifrar("Gripe")
    assert token != "Gripe"
    assert seguridad.descifrar(token) == "Gripe"


def test_descifrar_con_clave_incorrecta_lanza_error():
    token = seguridad.cifrar("dato secreto")
    # Se cambia la clave: se borra la guardada y se genera otra
    ruta = seguridad.ruta_en_datos("clave.key")
    import os
    os.remove(ruta)
    seguridad.limpiar_cache()
    with pytest.raises(ValueError):
        seguridad.descifrar(token)


def test_enmascarar_dni_deja_visibles_los_ultimos_4_digitos():
    assert seguridad.enmascarar_dni("12345678") == "****5678"
    assert seguridad.enmascarar_dni("123") == "***"


def test_paciente_guarda_dni_y_telefono_cifrados():
    paciente = Paciente("12345678", "Ana", "Torres", date(1990, 5, 14), "987654321")
    guardado = str(vars(paciente))
    assert "12345678" not in guardado
    assert "987654321" not in guardado
    assert paciente.coincide_dni("12345678")
    assert paciente.dni_enmascarado == "****5678"


def test_atencion_guarda_datos_clinicos_cifrados():
    atencion = Atencion("Gripe", "Reposo", "fiebre alta")
    guardado = str(vars(atencion))
    assert "Gripe" not in guardado and "Reposo" not in guardado
    assert atencion.diagnostico == "Gripe"
    assert "Tratamiento: Reposo" in atencion.mostrar()


# ---------- RF-04: roles ----------
def test_medico_ve_el_diagnostico_completo():
    sistema = crear_sistema()
    medico = Medico("mperez", "Marta Pérez")
    medico.agregar_atencion(sistema, "12345678", "Gripe", "Reposo")
    paciente = medico.buscar_por_dni(sistema, "12345678")
    assert "Diagnóstico: Gripe" in medico.ver_historial(paciente)[0]


def test_administrativo_no_ve_el_diagnostico():
    sistema = crear_sistema()
    Medico("mperez", "Marta Pérez").agregar_atencion(
        sistema, "12345678", "Gripe", "Reposo")
    admin = Administrativo("jlopez", "Juan López")
    paciente = admin.buscar_por_dni(sistema, "12345678")
    linea = admin.ver_historial(paciente)[0]
    assert "Gripe" not in linea and "Reposo" not in linea
    assert "[RESERVADO]" in linea


def test_administrativo_no_puede_agregar_atenciones():
    admin = Administrativo("jlopez", "Juan López")
    with pytest.raises(PermissionError):
        admin.agregar_atencion(crear_sistema(), "12345678", "Gripe", "Reposo")


def test_medico_no_puede_registrar_pacientes():
    medico = Medico("mperez", "Marta Pérez")
    with pytest.raises(PermissionError):
        medico.registrar_paciente(SistemaClinico(), "87654321", "Luis", "Rojas",
                                  date(1985, 11, 2), "976543210")


# ---------- RF-05: bitácora ----------
def test_bitacora_registra_quien_que_y_cuando_con_dni_enmascarado(tmp_path):
    bitacora = Bitacora(str(tmp_path / "b.log"))
    bitacora.registrar("mperez", "VER_HISTORIAL", dni="12345678")
    entrada = bitacora.leer()[0]
    assert entrada["usuario"] == "mperez"
    assert entrada["accion"] == "VER_HISTORIAL"
    assert entrada["dni"] == "****5678"
    assert entrada["fecha_hora"] != ""


def test_bitacora_guarda_el_archivo_cifrado(tmp_path):
    ruta = tmp_path / "b.log"
    Bitacora(str(ruta)).registrar("mperez", "VER_HISTORIAL", dni="12345678")
    contenido = ruta.read_text(encoding="utf-8")
    assert "mperez" not in contenido and "12345678" not in contenido


def test_bitacora_exige_usuario_y_accion(tmp_path):
    with pytest.raises(ValueError):
        Bitacora(str(tmp_path / "b.log")).registrar("", "VER_HISTORIAL")


def test_bitacora_filtra_por_usuario_y_accion(tmp_path):
    bitacora = Bitacora(str(tmp_path / "b.log"))
    bitacora.registrar("mperez", "VER_HISTORIAL")
    bitacora.registrar("jlopez", "BUSCAR_PACIENTE")
    assert len(bitacora.filtrar(usuario="jlopez")) == 1
    assert len(bitacora.filtrar(accion="VER_HISTORIAL")) == 1


def test_una_linea_danada_no_impide_leer_las_demas(tmp_path):
    ruta = tmp_path / "b.log"
    bitacora = Bitacora(str(ruta))
    bitacora.registrar("mperez", "VER_HISTORIAL")
    with open(ruta, "a", encoding="utf-8") as archivo:
        archivo.write("linea-danada\n")
    bitacora.registrar("jlopez", "BUSCAR_PACIENTE")
    entradas = bitacora.leer()
    assert len(entradas) == 2
    assert bitacora.lineas_danadas == 1
