from logging import Handler, NOTSET

from tqdm import tqdm


class TdqmProgressManager:
    """
    This class is used to manage (create and update) each progress bar
    create when downloading et product.
    """
    def __init__(self, name: str, total: int, **kwargs):
        self._tqdm = tqdm(desc=name, total=total, **kwargs)

    @property
    def total(self):
        return self._tqdm.total

    @property
    def cursor(self):
        return self._tqdm.n

    def update(self, count: int = 1):
        self._tqdm.update(count)

    def close(self):
        self._tqdm.clear()
        self._tqdm.close()


class TqdmLoggingHandler(Handler):
    def __init__(self, level=NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except Exception:
            self.handleError(record)
