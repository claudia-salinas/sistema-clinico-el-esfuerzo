"""Configuración común de las pruebas: usa una carpeta temporal para la clave."""
import os
import sys

import pytest

# Permite importar los módulos del proyecto desde la carpeta pruebas
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import seguridad  # noqa: E402


@pytest.fixture(autouse=True)
def carpeta_datos_temporal(tmp_path, monkeypatch):
    """Cada prueba usa su propia clave y su propia carpeta datos."""
    monkeypatch.setattr(seguridad, "CARPETA_DATOS", str(tmp_path))
    seguridad.limpiar_cache()
    yield
    seguridad.limpiar_cache()
