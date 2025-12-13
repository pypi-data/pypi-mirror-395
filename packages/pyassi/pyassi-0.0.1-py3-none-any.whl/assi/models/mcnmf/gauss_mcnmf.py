import numpy as np
from tqdm import tqdm
from ssspy.bss.mnmf import GaussMNMF as GaussMNMFBase


class GaussMNMF(GaussMNMFBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.progress_bar = None

    def __call__(self, *args, n_iter: int = 100, **kwargs) -> np.ndarray:
        self.n_iter = n_iter

        return super().__call__(*args, n_iter=n_iter, **kwargs)  # type: ignore[bad-keyword-argument]

    def update_once(self) -> None:  # type: ignore[override]
        if self.progress_bar is None:
            self.progress_bar = tqdm(total=self.n_iter)

        super().update_once()

        self.progress_bar.update(1)  # type: ignore[missing-attribute]


def sdr(true_records, estim_source):
    exact = np.sum(true_records**2)
    errors = np.sum((estim_source - true_records) ** 2)
    return 10 * np.log10(exact / errors)
