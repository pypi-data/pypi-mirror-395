import os.path

import uuid
import logging

logger = logging.getLogger("pygssearch")


class FileWriter:
    """
    This class is used when the download is used to create and write
    the file to be downloaded.
    """
    def __init__(self, out_path: str, file_size: int):
        self.out_file = os.path.realpath(out_path + '.' +
                                         str(uuid.uuid4()))
        self.final_filename = out_path
        self.file_size = file_size
        self._size_written = 0

    @property
    def size_written(self):
        return self._size_written

    def _init_writer(self):
        if not os.path.exists(self.out_file):
            logger.debug(f"initializing {self.out_file}")
            # Prepare the file with its final size
            with open(self.out_file, "wb") as fp:
                fp.seek(self.file_size - 1)
                fp.write(b'\0')

    def write(self, chunk: bytes, offset: int):
        self._init_writer()
        with open(self.out_file, "r+b") as fp:
            fp.seek(offset)
            fp.write(chunk)
        self._size_written += len(chunk)

    def close(self):
        if os.path.exists(self.out_file):
            logger.debug(f'Move to file {self.final_filename}')
            os.rename(self.out_file, self.final_filename)
