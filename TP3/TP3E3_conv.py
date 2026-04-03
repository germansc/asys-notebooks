# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "ipywidgets==8.1.8",
#     "marimo>=0.22.0",
#     "matplotlib==3.10.8",
#     "numpy==2.4.4",
# ]
# ///

import marimo

__generated_with = "0.22.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Análisis de Sistemas y Señales:

    ## Sobre este notebook

    Este notebook tiene como objetivo mostrar la operación de convolución entre dos señales continuas, $x(t)$ y $h(t)$, de una manera visual e interactiva.

    ### Consultas y contacto
    - german.scillone@ing.unlp.edu.ar
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1. Importar Librerías

    Importamos las librerías que vamos a utilizar: `numpy` para los cálculos y `matplotlib` para las gráficas.
    """)
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt

    return np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2. Definición de las Señales

    Vamos a definir algunas de las funciones de referencia que tenemos como `cajon(t)`, `escalon(t)` y `triangulo(t)`, en función de un dado vector de tiempo `t`.

    En base a estas, podemos definir las señales a convolucionar. Por defecto usaremos:

    - $x(t) = 1/2\sqcap(t-1)$
    - $h(t) = \sqcap(t/2)$

    Con `t` definido en el rango [-8, 8]. Pero pueden modificar estos valores para visualizar otras convoluciones. Por ejemplo: np.exp(-t)*escalon(t)
    """)
    return


@app.cell
def _(mo, np):
    def cajon(t):
        """
        Define una función cajón.
        Vale 1 para valores de t entre '-1/2' y '1/2', y 0 en el resto.
        """
        return np.where((np.abs(t) <= 1/2), 1, 0)

    def triangulo(t):
        """
        Define una función triangular.
        """
        return np.where(np.abs(t) <= 1, 1 - np.abs(t), 0)

    def escalon(t):
        """
        Define una función escalón, que vale 1 para t > 0, o 0 caso contrario.
        """
        return np.where((t > 0), 1, 0)

    x_str = mo.ui.text(label="x(t) =", value="0.5*cajon(t-1)")
    h_str = mo.ui.text(label="h(t) =", value="cajon(t/2)")

    mo.vstack([x_str, h_str])
    return cajon, escalon, h_str, triangulo, x_str


@app.cell
def _(cajon, escalon, h_str, np, triangulo, x_str):
    # Definimos un vector de tiempo común para trabajar.
    t = np.linspace(-8, 8, 2000)

    namespace = {"np": np, "t": t, "cajon": cajon, "triangulo": triangulo, "escalon": escalon}

    try:
        x_t = eval(x_str.value, {"__builtins__": {}}, namespace)
        h_t = eval(h_str.value, {"__builtins__": {}}, namespace)
    except:
        print("No se pudieron evaluar los campos de x(t) o h(t)!")

    # Trato de obtener las discontinuidades de h referidas a t = 0 para marcarlas durante la convolución, considerando saltos de más de 1/4 de la señal.
    _h_range = np.max(np.abs(h_t)) if np.max(np.abs(h_t)) > 0 else 1.0
    _thresh = 0.25 * _h_range
    _diff_h = np.abs(np.diff(h_t))
    edge_idx = np.where(_diff_h > _thresh)[0] + 1

    _nonzero = np.nonzero(h_t)[0]
    if len(_nonzero):
        candidates = []
        if _nonzero[0] != 0:
            candidates.append(_nonzero[0])
        if _nonzero[-1] != len(h_t) - 1:
            candidates.append(_nonzero[-1])

        candidates = np.array(candidates)
        new = candidates[~np.isin(candidates, edge_idx)]
        edge_idx = np.sort(np.concatenate([edge_idx, new]))

    # Redondeo a 1 decimal.
    edge_times = np.round(t[edge_idx], 1)

    # Agrego la marca de t = 0 también para referenciar en el desplazamiento.
    if not np.any(edge_times == 0.0):
        edge_times = np.sort(np.append(edge_times, 0.0))

    edge_times
    return edge_times, h_t, t, x_t


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3. Visualización de las señales

    Visualicemos las dos señales que vamos a convolucionar:
    """)
    return


@app.cell
def _(h_t, np, plt, t, x_t):
    fig1, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(12, 6))

    _xmax, _xmin = max(np.max(x_t) * 1.2, 0.1), min(np.min(x_t) * 1.2, -0.1)
    _hmax, _hmin = max(np.max(h_t) * 1.2, 0.1), min(np.min(h_t) * 1.2, -0.1)

    # Limito las graficas coherentemente, para facilitar la comparacion.
    figmin, figmax = min(_xmin, _hmin), max(_xmax,_hmax)

    # Gráfica de x(t)
    _ax1.plot(t, x_t, linewidth=2)
    _ax1.set_title('$x(t)$')
    _ax1.set_xlabel('t')
    _ax1.set_ylabel('$x(t)$')
    _ax1.grid(linestyle='--', linewidth=.1)
    _ax1.set_ylim(figmin, figmax)
    _ax1.set_xlim(-4, 4)

    # Gráfica de h(t)
    _ax2.plot(t, h_t, linewidth=2)
    _ax2.set_title('$h(t)$')
    _ax2.set_xlabel('t')
    _ax2.set_ylabel('$h(t)$')
    _ax2.grid(linestyle='--', linewidth=.1)
    _ax2.set_ylim(figmin, figmax)
    _ax2.set_xlim(-4, 4)
    plt.tight_layout()

    fig1
    return figmax, figmin


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4. La Operación de Convolución

    La convolución de dos funciones continuas, $x(t)$ y $h(t)$, se define como la integral del producto de una función con la versión **reflejada y desplazada** de la otra. El resultado es una nueva función, $y(t)$, donde la variable $t$ representa el desplazamiento aplicado a la función reflejada antes del producto.

    La fórmula es:

    $$ y(t) = \{ x * h \}(t) = \int_{-\infty}^{\infty} x(\tau)\,h(t - \tau)\,d\tau $$

    - **$\tau$**: Variable de integración; consideramos las señales como funciones de $\tau$ dentro del integrando.
    - **$x(\tau)$**: Primera señal, que permanece fija en la operación.
    - **$h(t - \tau)$** (equivalente a **$h(-(\tau - t))$**): Segunda señal. El término $t - \tau$ implica que $h(\tau)$ se **refleja** ($h(-\tau)$) y luego se **desplaza** una cantidad $t$.
    - **$t$**: Variable independiente de la salida. Para cada valor de $t$, se evalúa la integral, generando así la señal $y(t)$ punto a punto.

    **Propiedad importante:** la convolución es **conmutativa**, es decir $\{x * h\} = \{h * x\}$. En este caso estamos transformando $h(t)$, pero podríamos haber elegido reflejar y desplazar $x(t)$ y el resultado sería el mismo. Pueden probarlo intercambiando las definciones de $x(t)$ y $h(t)$.

    En el análisis de sistemas lineales e invariantes en el tiempo (SLIT), la convolución es de sumo interés ya que permite determinar la salida ante cualquier entrada $x(t)$, al realizar la operación entre la entrada y la respuesta impulsional del sistema $h(t)$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5. Visualización Interactiva

    El siguiente bloque te permite variar el desplazamiento $t$ con un slider, y observar cómo cambian las tres gráficas para entender el proceso:

    1.  **Gráfica 1 (Izquierda)**: Muestra la señal fija $x(\tau)$ (azul) y la señal invertida y desplazada $h(t - \tau)$ (rojo), y el valor de desplazamiento t en la barra negra vertical.
    2.  **Gráfica 2 (Derecha)**: Muestra el producto punto a punto de las dos señales anteriores, es decir **el integrando** de la convolución para un valor de $t$ dado. El **área sombreada en rojo** representa el valor de la integral de dicho producto. Este área es, literalmente, el valor de $y(t)$ en ese instante $t$.
    3.  **Gráfica 3 (Abajo)**: Muestra la señal de salida $y(t)$ que se va construyendo a medida que barremos el valor de $t$. El punto resalta el valor actual que se está calculando, es decir el valor del área sombreada en la gráfica 2.
    """)
    return


@app.cell
def _(h_t, np, plt, t, x_t):
    # Vamos a definir las figuras en función de tau
    tau = t  # Mismo rango que definimos antes.
    dt = t[1] - t[0]

    # Pre-calculamos la convolución completa como referencia para el tercer gráfico.
    y_complete = np.convolve(x_t, h_t, mode='full') * dt
    t_conv = np.arange(0, len(y_complete)) * dt + 2*t[0]


    fig2, axes = plt.subplot_mosaic(
        [["top_left", "top_right"],
         ["bot",   "bot"]],
        figsize=(12, 10)
    )

    ax1, ax2, ax3 = axes["top_left"], axes["top_right"], axes["bot"]
    return ax1, ax2, ax3, fig2, t_conv, tau, y_complete


@app.cell
def _(mo):
    slider = mo.ui.slider(start=-3.0, stop=5.0, step=0.05, value=-3, label='Tiempo (t)', show_value=True)
    slider
    return (slider,)


@app.cell
def _(
    ax1,
    ax2,
    ax3,
    edge_times,
    fig2,
    figmax,
    figmin,
    h_t,
    np,
    plt,
    slider,
    t_conv,
    tau,
    x_t,
    y_complete,
):
    t_val = slider.value

    # Obtenemos la función reflejada y desplazada por el valor de t_val del slider.
    h_rd_t = np.interp(t_val - tau, tau, h_t, left=0.0, right=0.0)

    # SUBPLOT 1: Señales x(τ) y h(t-τ) superpuestas
    ax1.clear()
    ax1.plot(tau, x_t, 'b-', linewidth=2, label="x(τ)", alpha=0.8)
    ax1.plot(tau, h_rd_t, 'r-', linewidth=2, label=f'h({t_val:.2f}-τ)', alpha=0.8)
    ax1.set_xlabel("τ (variable de integración)")
    ax1.set_ylabel('Amplitud')  
    ax1.set_title('Señales: x(τ) y h(t-τ)')
    ax1.grid(linestyle='--', linewidth=.1)
    ax1.legend() 
    ax1.set_ylim(figmin, figmax)
    ax1.set_xlim(-4, 4)
    ax1.axvline(x=t_val, color='black', linestyle='--', alpha=0.3, label=f't = {t_val:.2f}')

    # SUBPLOT 2: Integrando: producto x(τ) · h(t-τ)
    integrando = x_t * h_rd_t
    ax2.clear()
    ax2.plot(tau, integrando, 'g-', linewidth=2, label='x(τ) · h(t-τ)')
    ax2.fill_between(tau, 0, integrando, alpha=0.4, color='green', label=f'Área = {np.trapezoid(integrando, tau):.3f}')
    ax2.set_xlabel('τ (variable de integración)')
    ax2.set_ylabel('Amplitud')
    ax2.set_title('Integrando (Producto x(τ) · h(t-τ))')
    ax2.grid(True, alpha=0.3)
    ax2.legend()  # Linea con el valor de t_val:
    ax2.set_ylim(figmin, figmax)
    ax2.set_xlim(-4, 4)

    # SUBPLOT 3: Convolución y(t)
    t_indices = t_conv <= t_val
    ax3.clear()
    ax3.plot(t_conv[t_indices], y_complete[t_indices], 'purple', linewidth=3, label='y(t) = x(t) * h(t)')
    ax3.plot(t_conv, y_complete, 'purple', linewidth=1, alpha=0.3, linestyle='--', label='y(t) completa')

    if t_val >= t_conv[0] and t_val <= t_conv[-1]:
        idx_current = np.argmin(np.abs(t_conv - t_val))
        if idx_current < len(y_complete):
            ax3.plot(t_val, y_complete[idx_current], 'ro', markersize=8, 
                     label=f'y({t_val:.2f}) = {y_complete[idx_current]:.3f}')

    ax3.set_xlabel('Tiempo t')
    ax3.set_ylabel('y(t)')
    ax3.set_title('Resultado de la convolución')
    ax3.grid(True, alpha=0.1)
    ax3.legend()
    ax3.set_ylim(figmin, figmax)
    ax3.set_xlim(-4, 4)

    for mark in edge_times:
        mark_idx = t_val - mark
        if mark_idx > 4 or mark_idx < -4:
            continue
        ax1.axvline(x=mark_idx, linestyle='-', alpha=0.2, label='_nolegend_')
        ax1.text(mark_idx, -0.08, 't' if mark == 0 else f't{-mark:+0.1f}', ha='center', va='bottom', fontsize=10, rotation=0)
        ax2.axvline(x=mark_idx, linestyle=':', alpha=0.2, label='_nolegend_')
        ax2.text(mark_idx, -0.08, 't' if mark == 0 else f't{-mark:+0.1f}', ha='center', va='bottom', fontsize=10, rotation=0)
    plt.tight_layout()

    fig2
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
