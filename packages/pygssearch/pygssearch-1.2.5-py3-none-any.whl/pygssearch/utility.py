import configparser
import hashlib
import os
import re
from dataclasses import dataclass
from math import ceil

from click import BadParameter
from drb.drivers.http import HTTPOAuth2
from requests.auth import HTTPBasicAuth


@dataclass
class Chunk:
    """
    DataClass representing the starting bytes and ending bytes
    to be downloaded for each chunk.
    """
    start: int
    end: int


def parse_config_file(config_file: str = None):
    """
    Check the config file for the service url,
    username and password, if no path for a config
    file is given it will check if a config file named
    .pygssearch.ini is present in the HOME repository.

    :param config_file: Path of the config file by default None
    :return: a tuple representing (service, username, password)
    """
    conf_path = config_file if config_file is not None else os.path.join(
        os.environ.get('HOME', '.'), ".pygssearch.ini")

    if os.path.isfile(conf_path):
        cfg = configparser.ConfigParser()
        cfg.read(conf_path)
        return dict(cfg['pygssearch'])
    return None


def parse_date(date: str):
    """
    Check if the format of the date given in argument is
    YYYY-MM-DD and return to the format YYY-MM-DDT00:00:00.0Z
    to be sent in an Odata query.
    If no match return the date given in argument.

    :param date: a string representing the date to check
    :return: The date at the right format
    """
    pattern_date_time = '[0-9]{4}-[0-9]{2}-[0-9]{2}.*'

    if re.match(pattern_date_time, date):
        if not date.endswith('Z'):
            date = date + 'T00:00:00.0Z'
    return date


def init_conf(service, username, password,
              token_url, client_id, client_secret, config):
    """
    Initialize the conf and if no service is found raise and exception.
    If a file config and a username, password is present the programme will
    take the ones given in argument.

    :param service: (str) url of the service
    :param username: (str) username to connect to the service
    :param password: (str) password to connect to the service
    :param client_secret: (str)
    :param client_id: (str)
    :param token_url: (str)
    :param config: (str) path to a config file
    :return: a tuple (service, username, password)
    """
    auth = None
    conf = parse_config_file(config_file=config)

    if conf is not None:
        if service is None:
            service = conf.get("service", service)

        if username is None and password is None:
            username = conf.get("username", username)
            password = conf.get("password", password)

        if token_url is None or client_id is None or client_secret is None:
            token_url = conf.get("token_url", token_url)
            client_id = conf.get("client_id", client_id)
            client_secret = conf.get("client_secret", client_secret)

    if service is None:
        raise BadParameter("Service url is missing (See --help)")

    if token_url is not None or client_id is not None or \
            client_secret is not None:
        auth = HTTPOAuth2(
            username=username, password=password,
            token_url=token_url, client_id=str(client_id),
            client_secret=str(client_secret))
    elif username is not None and password is not None:
        auth = HTTPBasicAuth(username=username, password=password)

    return service, auth


def _proxy_url_control_and_fix(url: str) -> str:
    '''
    Ensure the passed URL is well formed and fix is scheme is missing.
    If missing automatically add "http://"
    '''
    if not url.startswith('http') and not url.startswith('socks'):
        return "http://" + url
    else:
        return url


def _proxy_parse_param_to_dictionary(proxy_param: str) -> dict:
    '''
    Parse a proxy parameter to be used as a proxy.
    The general usage in python seems to define a list of servers related to
    a protocol.
    '''
    try:
        return eval(proxy_param)
    except Exception:
        url = _proxy_url_control_and_fix(proxy_param)
        return _proxy_parse_param_to_dictionary(
            '{' + f'"http":"{url}","https":"{url}","ftp":"{url}"' + '}')


def proxy_param_to_os_env(proxy_param: str):
    proxy = _proxy_parse_param_to_dictionary(proxy_param)
    for protocol in proxy.keys():
        variable = protocol + '_PROXY'
        os.environ[variable.upper()] = os.environ[variable.lower()] =\
            _proxy_url_control_and_fix(proxy[protocol])


def slice_file(file_size: int, chunk_size=4194304):
    """
    Slices file as a list of ranges. Ranges are computed from the size of the
    file divide by the chunk size. A chunk is a minimum piece of the file to
    be transferred.

    The chunk size is default 4Mb and can be modified. Some bench shows that
    too small chunks reduces the transfer performances (could depend on the
    network MTU). Too big also could raise problem because of the memory
    usage.

    :param file_size: (int) the file size to be transferred in byte.
    :param chunk_size: (int) the minimum chunk size in bytes (default 4194304).
    :return: A list of offset position chnuks in the input data to be transfer
        ([begin offset, end offset] in byte).
    """
    if not file_size:
        raise ValueError("Size of file is required.")

    chunk_list = []
    chunk_number = ceil(file_size / chunk_size)
    for chunk_count in range(chunk_number):
        start = chunk_count * chunk_size
        end = start + chunk_size - 1
        end = end if file_size > end else file_size - 1
        chunk_list.append(Chunk(start=start, end=end))

    return chunk_list


def footprint_extract(geojson_obj):
    """
    Extract the footprint from a GeoJson.

    :param geojson_obj: (dict) the data extracted from a json file.
    :return: A list of coordinates
    """
    if "coordinates" in geojson_obj:
        geo_obj = geojson_obj
    elif "geometry" in geojson_obj:
        geo_obj = geojson_obj["geometry"]
    else:
        geo_obj = {"type": "GeometryCollection", "geometries": []}
        for feature in geojson_obj["features"]:
            geo_obj["geometries"].append(feature["geometry"])

    def ensure_2d(geo_obj):
        if isinstance(geo_obj[0], (list, tuple)):
            return list(map(ensure_2d, geo_obj))
        else:
            return geo_obj[:2]

    def check_bounds(geo_obj):
        if isinstance(geo_obj[0], (list, tuple)):
            return list(map(check_bounds, geo_obj))
        else:
            if geo_obj[0] > 180 or geo_obj[0] < -180:
                raise ValueError("Longitude is out of bounds,"
                                 "check your JSON format or data ")
            if geo_obj[1] > 90 or geo_obj[1] < -90:
                raise ValueError("Latitude is out of bounds, "
                                 "check your JSON format or data")

    # Discard z-coordinate, if it exists
    if geo_obj["type"] == "GeometryCollection":
        for idx, geo in enumerate(geo_obj["geometries"]):
            geo_obj["geometries"][idx]["coordinates"] = ensure_2d(
                geo["coordinates"])
            check_bounds(geo["coordinates"])
    else:
        geo_obj["coordinates"] = ensure_2d(geo_obj["coordinates"])
        check_bounds(geo_obj["coordinates"])

    # Some GeoJSON don't have geometries key
    # (https://datatracker.ietf.org/doc/html/rfc7946#appendix-A)
    if "geometries" in geo_obj:
        return geo_obj['geometries'][0]['coordinates'][0]
    else:
        return geo_obj['coordinates'][0]


def file_as_bytes(file):
    with file:
        return file.read()


def compute_md5(file) -> str:
    return hashlib.md5(file_as_bytes(open(file, 'rb'))).hexdigest()
