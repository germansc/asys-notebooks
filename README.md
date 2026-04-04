# Notebooks Interactivos de ASyS/IPS

Notebooks interactivos para las materias **Análisis de Sistemas y Señales** e
**Introducción al Procesamiento de Señales** desarrollados con
[marimo](https://marimo.io/).


## Notebooks disponibles

| Notebook | Tema | Abrir en molab |
|---|---|---|
| `TP3/TP3E3_conv.py` | TP3 — Ejercicio 3: Convolución | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/germansc/asys-notebooks/blob/master/TP3/TP3E3_conv.py/wasm?show-code=false) |

> Los notebooks se pueden abrir en molab directamente en el navegador sin
> necesidad de instalar nada. Al abrirlos, se presenta una vista previa estática
> con la opción de hacer un **fork** a tu propio workspace de molab para
> ejecutarlos e interactuar con ellos.

---

## Ejecutar localmente

### Opción 1 —  Directamente con `uv` instalado

```bash
uvx marimo edit TP3/TP3E3_conv.py
```

Marimo instala automáticamente las dependencias declaradas en el notebook via `uv`.

### Opción 2 — Con Nix (entorno reproducible)

Requiere [Nix](https://nixos.org/) con flakes habilitados.

```bash
# Clonar el repo
git clone https://github.com/germansc/asys-notebooks
cd asys-notebooks

# Entrar al entorno de desarrollo
nix develop

# Abrir un notebook
marimo edit TP3/TP3E3_conv.py
```

El entorno Nix provee Python con las dependencias necesarias, `marimo` y `uv`.

###### 2025 | germansc
