import numpy as np

######################################################################
# Window function
######################################################################


class Window:
    def __init__(self):
        pass

    def in_time_domain(self, nsamples) -> np.ndarray:
        raise NotImplementedError


######################################################################


class RectangularWindow(Window):
    def in_time_domain(self, nsamples) -> np.ndarray:
        return np.ones(shape=(nsamples,))


######################################################################


class HannWindow(Window):
    def in_time_domain(self, nsamples) -> np.ndarray:
        a = np.pi / nsamples * np.arange(nsamples)
        return np.sin(a) ** 2
