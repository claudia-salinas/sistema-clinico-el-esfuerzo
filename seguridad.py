"""Cifrado de datos y enmascarado de DNI (RNF-01).

Usa Fernet, de la biblioteca cryptography, para cifrar y descifrar textos.
La clave se guarda en datos/clave.key, una carpeta que no se sube al
repositorio (está en el .gitignore).

IMPORTANTE: si se pierde clave.key, los datos cifrados con ella ya no se
pueden recuperar. Por eso, si el archivo no existe y se genera una clave
nueva, el programa muestra un aviso.
"""
import os
import sys
from functools import lru_cache

from cryptography.fernet import Fernet, InvalidToken

# Carpeta "datos", junto a este archivo (así no depende desde dónde se ejecute)
CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")


def ruta_en_datos(nombre_archivo):
    """Devuelve la ruta de un archivo dentro de la carpeta datos (la crea si falta)."""
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    return os.path.join(CARPETA_DATOS, nombre_archivo)


@lru_cache(maxsize=1)
def cargar_clave():
    """Lee la clave del archivo. Si no existe, genera una nueva y la guarda.

    La clave se guarda en memoria después de la primera lectura, para no
    abrir el archivo en cada cifrado (con 500 pacientes serían miles de lecturas).
    """
    ruta = ruta_en_datos("clave.key")
    if not os.path.exists(ruta):
        print("AVISO: no se encontró datos/clave.key; se generó una clave nueva. "
              "Los datos cifrados con una clave anterior no se podrán leer.",
              file=sys.stderr)
        with open(ruta, "wb") as archivo:
            archivo.write(Fernet.generate_key())
    with open(ruta, "rb") as archivo:
        return archivo.read().strip()


def limpiar_cache():
    """Olvida la clave guardada en memoria (se usa en las pruebas)."""
    cargar_clave.cache_clear()


def cifrar(texto):
    """Cifra un texto y devuelve el resultado como texto."""
    fernet = Fernet(cargar_clave())
    return fernet.encrypt(texto.encode("utf-8")).decode("ascii")


def descifrar(texto_cifrado):
    """Descifra un texto cifrado con cifrar(). Lanza ValueError si falla."""
    fernet = Fernet(cargar_clave())
    try:
        return fernet.decrypt(texto_cifrado.encode("ascii")).decode("utf-8")
    except InvalidToken:
        raise ValueError("No se pudo descifrar: clave incorrecta o dato alterado.")


def enmascarar_dni(dni, visibles=4):
    """Oculta el DNI y deja visibles solo los últimos dígitos (12345678 -> ****5678)."""
    texto = str(dni).strip()
    if len(texto) <= visibles:
        return "*" * len(texto)
    return "*" * (len(texto) - visibles) + texto[-visibles:]
