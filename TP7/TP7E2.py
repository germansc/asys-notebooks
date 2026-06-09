# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.22.0",
#     "matplotlib==3.10.8",
#     "numpy==2.4.4",
# ]
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Análisis de Sistemas y Señales

    ## TP7 - Ejercicio 2

    En este notebook estudiamos la TDF de una secuencia cosenoidal finita y analizamos qué ocurre al cambiar la cantidad de muestras `N` y la frecuencia normalizada $s_0$.

    $$x[n] = \cos(2\pi s_0 n), \qquad 0 \le n \le N-1$$

    El objetivo es reproducir e interpretar los resultados pedidos en la guía:
    - comparar los casos `N = 49, 50, 51`,
    - relacionar la TDF con la TFTD,
    - representar el eje horizontal en frecuencia física, y entender el efecto de `fftshift`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1. Parámetros interactivos

    Elegimos la longitud de la secuencia y la frecuencia lineal normalizada del coseno.

    En la guía se usa por defecto $s = 1/10$:

    $$x[n] = \cos\left(2\pi \frac{n}{10}\right),$$

    Y se comenta que podemos interpretar que dicha secuencia viene de muestrear la SVIC $x(t) = cos(2\pi t)$ a una tasa de $f_s = 10$.
    """)
    return


@app.cell
def _(mo):
    N_ui = mo.ui.number(start=5, stop=100, step=1, value=50, label="N")
    s0_ui = mo.ui.slider(
        start=0.025,
        stop=0.475,
        step=0.01,
        value=0.10,
        label=r"$s_0$",
        show_value=True,
    )

    mo.hstack([N_ui, s0_ui], justify="center", gap=5)
    return N_ui, s0_ui


@app.cell
def _(N_ui, np, s0_ui):
    N = int(N_ui.value)
    s0 = float(s0_ui.value)

    Ts = 0.1
    fs = 1 / Ts

    n = np.arange(N)
    k = np.arange(N)
    x = np.cos(2 * np.pi * s0 * n)

    X = np.fft.fft(x)
    X_mag = np.abs(X)

    f = np.arange(N) * fs / N
    f_shift = np.fft.fftshift(np.fft.fftfreq(N, d=Ts))
    X_shift = np.fft.fftshift(X)
    X_shift_mag = np.abs(X_shift)

    s_k = np.arange(N) / N
    s_k_shift = np.fft.fftshift(np.fft.fftfreq(N, d=1.0))

    dense_nfft = 32 * N
    s_dense_shift = np.fft.fftshift(np.fft.fftfreq(dense_nfft, d=1.0))
    X_dense_shift = np.fft.fftshift(np.fft.fft(x, dense_nfft))

    k0 = N * s0
    nearest_bin = int(np.round(k0))
    bin_offset = k0 - nearest_bin
    aligned = np.isclose(bin_offset, 0.0, atol=1e-12)

    f0 = s0 / Ts
    return (
        N,
        Ts,
        X_dense_shift,
        X_mag,
        X_shift_mag,
        aligned,
        f,
        f0,
        f_shift,
        k,
        k0,
        n,
        nearest_bin,
        s0,
        s_dense_shift,
        s_k_shift,
        x,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2. Secuencia en el tiempo

    La TDF se calcula sobre secuencias de largo finito. Por eso, aunque la señal original esté indicada como un coseno puro, el análisis espectral depende tanto de $s_0$ como de la ventana temporal implícita de longitud $N$.
    """)
    return


@app.cell
def _(Ts, n, plt, x):
    _fig_time, _ax_time = plt.subplots(figsize=(10, 4))
    _markerline, _stemlines, _baseline = _ax_time.stem(
        n, x, linefmt="C0-", markerfmt="C0o", basefmt="k-"
    )
    plt.setp(_stemlines, linewidth=1.5)
    plt.setp(_markerline, markersize=5)

    _ax_time.set_title("x[n]")
    _ax_time.set_xlabel("n")
    _ax_time.set_ylabel("x[n]")
    _ax_time.grid(True, alpha=0.2)
    _ax_time.set_ylim(-1.2, 1.2)
    _ax_time.set_xlim(-0.5, max(len(n) - 0.5, 1))

    def _n_to_t(_n):
        return _n * Ts

    def _t_to_n(_t):
        return _t / Ts

    _ax_time_top = _ax_time.secondary_xaxis("top", functions=(_n_to_t, _t_to_n))
    _ax_time_top.set_xlabel("t [s]")

    _fig_time.tight_layout()

    _fig_time
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3. TDF de N puntos

    La definición de la TDF evalúa la secuencia sobre una grilla de frecuencias normalizadas discreta:

    $$s_k = \frac{k}{N}, \qquad k = 0, 1, \dots, N-1.$$

    Entonces, un coseno de frecuencia $s_0$ tendrá sus máximos exactamente sobre bins de la TDF solo si $s_0$ coincide con algún valor de esa grilla.
    """)
    return


@app.cell(hide_code=True)
def _(N, aligned, f0, k0, mo, nearest_bin, s0):
    estado = (
        "La frecuencia cae exactamente sobre un bin de la TDF."
        if aligned
        else "La frecuencia **no cae** exactamente sobre un bin de la TDF."
    )

    mo.md(
        rf"""
        #### Lectura rápida del caso actual

        Para los parámetros elegidos:

        - `N = {N}`
        - $s_0 = {s0:.2f}$
        - $f_0 = {f0:.2f}$ Hz, usando $T_s = 0.1s$ (o $f_s = 10$).
        - la componente positiva ideal debería caer en $k_0 = N s_0 = {k0:.2f}$
        - el bin entero más cercano es $k = {nearest_bin}$

        **Interpretación:** {estado}

        Cuando $k_0$ es entero, la energía del coseno queda concentrada en dos muestras de la TDF.
        Cuando $k_0$ no es entero, la energía se reparte entre varios bins.
        """
    )
    return


@app.cell
def _(X_mag, X_shift_mag, f, f_shift, k, plt):
    _fig_spectrum, (_ax_k, _ax_f) = plt.subplots(1, 2, figsize=(12, 4.5))

    _ax_k.plot(k, X_mag, ".", color="purple", markersize=8)
    _ax_k.set_title(r"$|X[k]|$")
    _ax_k.set_xlabel("k")
    _ax_k.set_ylabel("Módulo")
    _ax_k.grid(True, alpha=0.2)

    _ax_f.plot(f, X_mag, ".", color="blue", markersize=8, label="sin shift")
    _ax_f.plot(
        f_shift, X_shift_mag, ".", color="darkorange", markersize=6, label="fftshift"
    )
    _ax_f.set_title("Mismo espectro con eje en Hz")
    _ax_f.set_xlabel("f [Hz]")
    _ax_f.set_ylabel("Módulo")
    _ax_f.grid(True, alpha=0.2)
    _ax_f.legend()

    _fig_spectrum.tight_layout()
    _fig_spectrum
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5. Vinculación entre TFTD y TDF

    La TDF puede interpretarse como un muestreo de la TFTD de la secuencia finita observada.

    $$ X[k] = \sum^{N-1}_{n = 0}x[n]e^{-j2\pi k/N} = \sum^{\infty}_{n = -\infty}x[n] \sqcap_N[n-N/2] e^{-j2\pi k/N} = X_N(e^{j2\pi s})\vert_{s = k/N} $$

    Si tomamos las `N` muestras disponibles y formamos la secuencia truncada,
    su TFTD es una función continua de $s$, mientras que la TDF evalúa esa función solamente en los puntos
    $s_k = k/N$.

    En la figura siguiente se muestra una TDF más densa en frecuencia (a partir de extender con muchos ceros la secuencia) para visualizar esa envolvente,
    junto con las muestras exactas de la TDF.
    """)
    return


@app.cell
def _(X_dense_shift, X_shift_mag, np, plt, s_dense_shift, s_k_shift):
    _fig_dtft, _ax_dtft = plt.subplots(figsize=(10, 4.5))

    _ax_dtft.plot(
        s_dense_shift,
        np.abs(X_dense_shift),
        color="steelblue",
        linewidth=2,
        label="TFTD",
    )
    _ax_dtft.plot(
        s_k_shift,
        X_shift_mag,
        ".",
        color="crimson",
        markersize=10,
        label="muestras de la TDF",
    )

    _ax_dtft.set_title("La TDF como muestreo de la TFTD")
    _ax_dtft.set_xlabel(r"$s$")
    _ax_dtft.set_ylabel("Módulo")
    _ax_dtft.grid(True, alpha=0.2)
    _ax_dtft.legend()
    _fig_dtft.tight_layout()

    _fig_dtft
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6. Comparación con distintos valores de N:

    Si dejamos $s_0 = 0.1$, entonces

    $$k_0 = N s_0 = \frac{N}{10}.$$

    Esto permite entender inmediatamente la diferencia entre los tres casos:

    - para $N = 50$, resulta $k_0 = 5$, entero;
    - para $N = 49$, resulta $k_0 = 4.9$, no entero;
    - para $N = 51$, resulta $k_0 = 5.1$, no entero.

    Por eso el caso $N = 50$, la secuencia continene un número entero de períodos del coseno, por lo que en la TDF concentra la energía en dos bins. Para los casos de $49$ y $51$ el último período del coseno aparece "truncado" en la secuencia, por lo que deberá haber energía en otras frecuencias que causen esa transición.
    """)
    return


@app.cell
def _(Ts, np, plt, s0):
    Ns = [49, 50, 51]
    _fig_compare, _axes_compare = plt.subplots(2, 3, figsize=(14, 7), sharey="row")

    for idx, N_i in enumerate(Ns):
        n_i = np.arange(N_i)
        X_i = np.fft.fft(np.cos(2 * np.pi * s0 * n_i))
        mag_i = np.abs(X_i)

        k_i = np.arange(N_i)
        f_i_shift = np.fft.fftshift(np.fft.fftfreq(N_i, d=Ts))
        mag_i_shift = np.abs(np.fft.fftshift(X_i))

        _ax_top = _axes_compare[0, idx]
        _ax_bot = _axes_compare[1, idx]

        _ax_top.plot(k_i, mag_i, ".", color="purple", markersize=8)
        _ax_top.set_title(f"N = {N_i}")
        _ax_top.set_xlabel("k")
        _ax_top.grid(True, alpha=0.2)

        _ax_bot.plot(f_i_shift, mag_i_shift, ".", color="darkorange", markersize=8)
        _ax_bot.set_xlabel("f [Hz]")
        _ax_bot.grid(True, alpha=0.2)

    _axes_compare[0, 0].set_ylabel(r"$|X[k]|$")
    _axes_compare[1, 0].set_ylabel(r"$|\mathrm{fftshift}(X)|$")
    _fig_compare.suptitle("Comparación para N = 49, 50 y 51", y=1.02)
    _fig_compare.tight_layout()

    _fig_compare
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7. ¿Qué hace `fftshift`?

    El comando `fftshift` no cambia los valores espectrales: solo reordena las muestras para que la frecuencia cero quede en el centro del eje.

    - sin `fftshift`, la TDF aparece ordenada como `0, 1, 2, ..., N-1`, representando a las frecuencias normalizadas en el rango $s = [0...1)$;
    - con `fftshift`, las frecuencias negativas quedan a la izquierda y las positivas a la derecha, representando a las frecuencias normalizadas en el rango $s = [-1/2...1/2)$.

    Notar que aplicar `fftshift` requiere entonces re-definir el vector de frecuencias en los gráficos respectivamente, y se debe  tener cierto cuidado dependiendo de si el número de muestras es par o impar.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
