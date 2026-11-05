# MalayaRol - Lanzador D20

## Descripción

Proyecto desarrollado en Python utilizando la biblioteca Pygame.

## Requisitos

- Windows 10 o superior.
- Python 3.13 (64 bits).
- Pygame 2.6.1.
- Visual Studio Code (recomendado).

## 1. Instalar Python 3.13

Descargar Python desde la página oficial:

https://www.python.org/downloads/windows/

Seleccionar una versión de Python 3.13 y descargar **Windows installer (64-bit)**.

Durante la instalación:

1. Ejecutar el instalador.
2. Marcar la opción `Add Python to PATH`.
3. Seleccionar `Install Now`.
4. Esperar a que finalice la instalación.

Comprobar la instalación desde PowerShell:

```powershell
py -3.13 --version
```

## 2. Actualizar pip

Abrir una terminal en Visual Studio Code y ejecutar:

```powershell
py -3.13 -m pip install --upgrade pip
```

## 3. Instalar Pygame

Ejecutar el siguiente comando:

```powershell
py -3.13 -m pip install pygame
```

## 4. Verificar la instalación

Comprobar que Pygame se instaló correctamente:

```powershell
py -3.13 -c "import pygame; print(pygame.version.ver)"
```

La versión esperada es:

```text
2.6.1
```

## 5. Ejecutar el proyecto

Desde la carpeta principal del proyecto, ejecutar:

```powershell
py -3.13 lanzador_d20/main.py
```

## Tecnologías utilizadas

- Python 3.13
- Pygame 2.6.1

## Autor

Renato416

GitHub: https://github.com/Renato416
