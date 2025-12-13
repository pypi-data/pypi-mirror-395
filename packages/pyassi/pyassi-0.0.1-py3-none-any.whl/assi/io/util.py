import numpy as np

###########################################################################33


def to_db(x):
    return 10 * np.log10(x)


###########################################################################33


def autocorrelation_np(a, b, max_lag):
    assert a.ndim == 2 and b.ndim == 2
    N = a.shape[0]
    assert b.shape[0] == N
    assert max_lag < N
    cormat = np.empty((max_lag + 1, a.shape[1], b.shape[1]), dtype=a.dtype)
    second = np.conj(b[: N - max_lag, None, :])
    for lag in range(max_lag + 1):
        cormat[lag] = np.sum(a[lag : N - max_lag + lag, :, None] * second, axis=0)
    return cormat / (N - max_lag)


###########################################################################33


# ChatGPT generated.
def hue_to_rgb(hue: np.ndarray) -> np.ndarray:
    """
    Конвертирует массив оттенков (hue) из модели HSV в RGB при максимальных S и V.

    :param hue: Массив оттенков (hue) нормированных на интервал [0, 1]
    :return: Массив (R, G, B) с компонентами в диапазоне [0, 1]
    """
    hue = np.mod(hue * 6, 6)  # Переводим hue в диапазон [0, 6)
    c = 1.0  # S = 1, V = 1, значит C = V * S = 1.0
    x = 1 - np.abs(np.mod(hue, 2) - 1)

    conditions = [
        hue < 1,
        (hue >= 1) & (hue < 2),
        (hue >= 2) & (hue < 3),
        (hue >= 3) & (hue < 4),
        (hue >= 4) & (hue < 5),
        hue >= 5,
    ]
    values_r = [c, x, 0, 0, x, c]
    values_g = [x, c, c, x, 0, 0]
    values_b = [0, 0, x, c, c, x]

    r = np.select(conditions, values_r)
    g = np.select(conditions, values_g)
    b = np.select(conditions, values_b)
    rgb = np.stack([r, g, b], axis=-1)
    return rgb


def camp_to_rgb(z, minamp=1e-6, maxamp=1e0):
    a = np.angle(z) / np.pi
    v = np.abs(z)
    # v = np.maximum(0, (np.log(v)-np.log(minamp))/(np.log(maxamp)-np.log(minamp)) )
    v = np.sqrt(v)
    rgb = hue_to_rgb(a)
    rgb = v[..., None] * rgb
    vol = np.maximum(0, np.sum(rgb, axis=-1) - 1)
    return np.clip(rgb + vol[..., None], 0, 1)
