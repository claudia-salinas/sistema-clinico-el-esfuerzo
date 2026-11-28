# Sistema Clínico El Esfuerzo

Software multiparadigma en Python para el registro de historiales clínicos del Hospital Distrital El Esfuerzo.

## Requisitos

- Python 3.10 o superior (se usa match/case)
- Biblioteca cryptography (cifrado de datos) y pytest (pruebas)

## Instalación

```
git clone https://github.com/claudia-salinas/sistema-clinico-el-esfuerzo.git
cd sistema-clinico-el-esfuerzo
pip install -r requirements.txt
```

## Ejecución

```
python main.py
```

Al iniciar se elige un usuario. Cada rol ve solo sus opciones:

| Usuario | Rol | Puede |
|---|---|---|
| Marta Pérez, Raúl Quispe | Médico | Buscar pacientes, ver el historial completo y agregar atenciones |
| Juan López | Administrativo | Registrar y buscar pacientes; en el historial no ve diagnósticos |

## Seguridad

- El DNI, el teléfono y los datos clínicos (diagnóstico, tratamiento y notas) se guardan cifrados con Fernet (RNF-01).
- La bitácora (RF-05) registra quién hizo qué y cuándo, con el DNI enmascarado, y se guarda cifrada en `datos/bitacora.log`.
- La clave se guarda en `datos/clave.key`. Esa carpeta no se sube al repositorio (está en el .gitignore). Si se pierde la clave, los datos cifrados con ella no se pueden recuperar.

## Pruebas

```
python -m pytest pruebas
python prueba_viabilidad.py
```

## Archivos

| Archivo | Contenido |
|---|---|
| main.py | Menú principal e inicio de sesión |
| modelos.py | Clases Paciente, HistorialClinico y Atencion |
| sistema.py | Clase SistemaClinico (registro y búsquedas) |
| usuarios.py | Roles de usuario: Usuario, Medico y Administrativo (RF-04) |
| bitacora.py | Bitácora de acciones (RF-05) |
| seguridad.py | Cifrado y enmascarado de DNI (RNF-01) |
| datos_prueba.py | Pacientes ficticios para las pruebas |
| prueba_viabilidad.py | Medición del tiempo de búsqueda (CE-02) |
