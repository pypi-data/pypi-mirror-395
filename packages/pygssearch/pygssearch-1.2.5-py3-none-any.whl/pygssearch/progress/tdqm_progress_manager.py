import logging
import functools

from pygssearch.progress.progress import TdqmProgressManager

from pygssearch.utility import compute_md5

logger = logging.getLogger('pygssearch')

progresses = {}


class PygssearchWrongChecksumException(Exception):
    pass


def progress_chunk_handling(func):
    @functools.wraps(func)
    def wrapper_chunk_download(*args, **kwargs):
        filename = kwargs.get('filename')
        start = kwargs.get('start')
        stop = kwargs.get('stop')
        quiet = kwargs.get('quiet')
        writer = kwargs.get('writer')
        checksum = kwargs.get('checksum')

        try:
            value = func(*args, **kwargs)  # process transfer
        except Exception as e:
            raise e
        if not quiet:
            update_progress(name=filename, inc=stop - start + 1)
        if writer.size_written >= writer.file_size:
            writer.close()
            if not quiet:
                remove_progress(filename)
            if checksum is not None:
                md5 = compute_md5(writer.final_filename)
                logger.debug(f"Compute MD5 for {filename}: "
                             f"computed={md5}/reference={checksum}")
                if md5 != checksum:
                    raise PygssearchWrongChecksumException(
                        f"{filename}: computed={md5}, expected={checksum}")
        return value

    return wrapper_chunk_download


def get_progress_manager(name: str, total: int):
    global progresses
    if name in progresses.keys():
        return progresses[name]
    return TdqmProgressManager(name=name,
                               total=total,
                               unit="Bytes",
                               colour="GREEN")


def append_progress(name: str, total: int):
    global progresses
    progresses[name] = get_progress_manager(name, total)


def update_progress(name: str, inc: int):
    global progresses
    progress = progresses.get(name)
    if progress:
        progress.update(inc)


def remove_progress(name: str):
    global progresses
    progress = progresses.get(name)
    if progress:
        progress.close()
        del progresses[name]
