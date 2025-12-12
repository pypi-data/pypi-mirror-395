import concurrent.futures
import logging
import io
import os

from drb.core import DrbNode

from pygssearch.destination.writer import FileWriter
from pygssearch.progress.process_manager import ManagedPoolExecutor
from pygssearch.progress.tdqm_progress_manager import \
    append_progress, update_progress, remove_progress

logger = logging.getLogger("pygssearch")


def handler(node: DrbNode, output_folder: str = '.',
            verify=False, quiet=False, chunk_size=4096):
    file_size = node @ 'ContentLength'

    # prepare writer
    writer = FileWriter(
        out_path=os.path.join(output_folder, node.name),
        file_size=file_size)

    if not quiet:
        append_progress(node.name, file_size)

    buff = node.get_impl(io.BytesIO)
    current_position = 0
    while current_position < file_size:
        readed = buff.read(chunk_size)
        len_readed = len(readed)
        if len_readed > 0:
            writer.write(readed, current_position)
            current_position += len_readed
            update_progress(node.name, len_readed)

    remove_progress(node.name)
    writer.close()


class Download:
    """
    This class is used to handle the download of product after
    being initialized, you can submit each product to be
    downloaded to the pool.
    """

    def __init__(self, output_folder: str = '.',
                 verify=False, quiet=False, threads=4):
        self._bars = {}
        self._output_folder = output_folder
        self._chunk_size = 4096
        self._verify = verify
        self._quiet = quiet
        self._executor = ManagedPoolExecutor(
            max_workers=threads,
            fail_fast=False
        )
        self._futures = []

    def submit(self, node: DrbNode):
        future = self._executor.submit(handler,
                                       node=node,
                                       output_folder=self._output_folder,
                                       verify=self._verify,
                                       quiet=self._quiet,
                                       chunk_size=self._chunk_size)
        future.add_done_callback(future_callback_error_logger)

    def wait(self):
        for future in concurrent.futures.as_completed(self._futures):
            if future.exception() is not None:
                logger.error(f'ERROR: {future}: {future.exception()}')
                continue


def future_callback_error_logger(future):
    try:
        future.result()
    except Exception:
        logger.exception("Executor Exception")
