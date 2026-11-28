"""Bitácora de acciones del sistema (RF-05): quién hizo qué y cuándo.

El DNI se guarda siempre enmascarado y cada línea se guarda cifrada (RNF-01).
"""
import json
import os
from datetime import datetime

import seguridad


class Bitacora:

    def __init__(self, ruta=None, cifrar=True):
        # Si no se indica una ruta, se guarda en la carpeta datos
        self.__ruta = ruta if ruta else seguridad.ruta_en_datos("bitacora.log")
        self.__cifrar = cifrar
        self.__lineas_danadas = 0

    @property
    def ruta(self):
        return self.__ruta

    @property
    def lineas_danadas(self):
        """Cantidad de líneas que no se pudieron leer en la última lectura."""
        return self.__lineas_danadas

    def registrar(self, usuario, accion, dni=None, detalle=""):
        """Agrega una entrada a la bitácora y la devuelve."""
        if not usuario or not accion:
            raise ValueError("El usuario y la acción son obligatorios.")
        entrada = {
            "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "usuario": str(usuario),
            "accion": str(accion),
            "dni": seguridad.enmascarar_dni(dni) if dni else "",
            "detalle": str(detalle),
        }
        linea = json.dumps(entrada, ensure_ascii=False)
        if self.__cifrar:
            linea = seguridad.cifrar(linea)
        with open(self.__ruta, "a", encoding="utf-8") as archivo:
            archivo.write(linea + "\n")
        return entrada

    def leer(self):
        """Devuelve todas las entradas como lista de diccionarios.

        Si una línea está dañada (clave incorrecta o dato alterado), se omite
        y se cuenta en lineas_danadas; así una sola línea no impide leer el resto.
        """
        self.__lineas_danadas = 0
        if not os.path.exists(self.__ruta):
            return []
        entradas = []
        with open(self.__ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea == "":
                    continue
                try:
                    if self.__cifrar:
                        linea = seguridad.descifrar(linea)
                    entradas.append(json.loads(linea))
                except ValueError:
                    # json.JSONDecodeError también es un ValueError
                    self.__lineas_danadas += 1
        return entradas

    def filtrar(self, usuario=None, accion=None):
        """Devuelve las entradas de un usuario y/o una acción."""
        return list(filter(
            lambda e: (usuario is None or e["usuario"] == usuario)
            and (accion is None or e["accion"] == accion),
            self.leer()))
