import logging
import re
import sys

import click
import pygssearch
import requests
from drb.drivers.http import HTTPOAuth2
from requests.auth import HTTPBasicAuth
from pygssearch import OdataSource
from pygssearch import query_builder, query_controls_builder
from pygssearch.progress.progress import TqdmLoggingHandler
from pygssearch.utility import init_conf, proxy_param_to_os_env
import geojson

logger = logging.getLogger('pygssearch')
logger.setLevel(logging.INFO)
logger.addHandler(TqdmLoggingHandler())


@click.command(help=f"""
This library PyGSSearch aims to support query and download product
from the GSS catalogue, the download can be start
with command line and also in python script. It authorize limiting
the connections to respect the services quota policies.
""")
@click.option('--service', '-s',
              type=str,
              default=None,
              envvar="GSS_SERVICE",
              help='The OData CSC root Service URL to requests data')
@click.option('--filter', '-f',
              type=str,
              help="The OData filter to query Products in the remote service.")
@click.option('--footprint',
              type=str,
              help="Create a GeoJSON file at the provided path with "
                   "footprints and metadata of the returned products. "
                   "Set to ‘-’ for stdout. The GeoJSON property fields can be "
                   "configured with '--attributes', '--format' and "
                   "'--exclude' parameters")
@click.option('--username', '-u',
              type=str, default=None,
              envvar="GSS_USERNAME",
              help="Service connection username.")
@click.option('--password', '-p',
              type=str,
              default=None,
              envvar="GSS_PASSWORD",
              help="Service connection password.")
@click.option('--token_url',
              type=str,
              default=None,
              help="Url to retrieve the token.")
@click.option('--client_id',
              type=str,
              default=None,
              help="The client identifier.")
@click.option('--client_secret',
              type=str,
              default=None,
              help="The client secret.")
@click.option('--proxy',
              type=str,
              default=None,
              help="Proxy URL or dict configuration.")
@click.option('--thread_number', '-t',
              type=int,
              default=2,
              help="Number of parallel download threads (default:2).")
@click.option('--limit', '-l',
              type=int,
              default=10,
              help="Limit the number matching products (default: 10)")
@click.option('--skip',
              type=int,
              help="Skip a number matching products (default: 0)",
              default=0)
@click.option('--output', '-o',
              type=str,
              default=".",
              help='The directory to store the downloaded files.')
@click.option('--start', '-S',
              type=str,
              help="start date of the query in  the format "
                   "YYYY-MM-DD or an expression like NOW-1DAY.")
@click.option('--end', '-E',
              type=str,
              help="End date of the query")
@click.option('--geometry', '-g', type=str,
              help="Path to a GeoJson file containing a search area or"
                   "a series of entries of tuple of coordinates "
                   "separated by a coma")
@click.option('--uuid',
              type=str,
              multiple=True,
              help="Select a specific product UUID. "
                   "Can be set more than once.")
@click.option('--name', '-n',
              type=str,
              multiple=True,
              help="Select specific product(s) by filename. "
                   "Can be set more than once.")
@click.option('--mission', '-m',
              type=click.Choice(["1", "2", "3", "5"]),
              help="Limit search to a Sentinel satellite (constellation).")
@click.option('--instrument', '-I',
              help="Limit search to a specific instrument "
                   "on a Sentinel satellite (i.e. MSI, SAR, OLCI ...).")
@click.option('--product_type', '-P',
              type=str,
              help="Limit search to a Sentinel product type.")
@click.option('--cloud',
              type=int,
              help="Maximum cloud cover (in percent).")
@click.option('--download', '-d',
              is_flag=True,
              help="Download all the results of the query.")
@click.option('--order_by', '-O',
              type=str,
              multiple=True,
              help="Specify the keyword to order the result."
                   "Prefix ‘-’ for descending order, '+' for ascending. "
                   "Default ascending.")
@click.option('--verify', '-v',
              is_flag=True,
              help="Check the file integrity using his hash"
                   ", use with the download option.")
@click.option('--config', '-C',
              type=str,
              default=None,
              help="Give the path to a configuration file to the .ini format")
@click.option('--quiet', '-q',
              is_flag=True,
              help="Silent mode: only errors are reported,"
                   "use with the download option.")
@click.option('--version',
              is_flag=True,
              help="Show version number and exit.")
@click.option('--format', '-F',
              multiple=True,
              default=('Name', 'Id'),
              help="Define the response of the query by default show "
                   "the name and id, of each matching product of the query. "
                   "To show all information use '_'. Current existing fixed "
                   "properties in OData CSC products are Id, Name, "
                   "ContentType, ContentLength, OriginDate, PublicationDate, "
                   "ModificationDate, Online, EvictionDate, Checksum, "
                   "ContentDate, Footprint, GeoFootprint.")
@click.option('--attributes',
              is_flag=True,
              help="Includes the extended attributes of the product "
                   "into the GeoJSON properties.")
@click.option('--exclude',
              multiple=True,
              default=(),
              help="The list of attributes to be excluded from the output.")
@click.option('--logs',
              is_flag=True,
              help="Print debug log message and no progress bar,"
                   "use with the download option.")
@click.option('--debug',
              is_flag=True,
              help="Print debug log message.")
@click.option('--show_url',
              is_flag=True,
              help="Print URL used to request OData service to perform the "
                   "given parameters. The service in not contacted.")
@click.option('--count',
              is_flag=True,
              help="returns the number of products returned by the given "
                   "parameters.")
@click.option('--check_service',
              is_flag=True,
              help="Controls if the Odata service is accessible.")
def cli(service, filter, footprint, username, password, token_url,
        client_id, client_secret, proxy, thread_number, limit, skip,
        output, start, end, geometry, uuid, name, mission,
        instrument, product_type, cloud, download, order_by, verify,
        config, quiet, version, format, attributes, exclude, logs, debug,
        show_url, count, check_service):
    if debug:
        logger.setLevel(logging.DEBUG)
    elif logs:
        logger.setLevel(logging.DEBUG)
        quiet = True
    elif quiet:
        logger.setLevel(logging.WARNING)

    if version:
        logger.info(pygssearch.__version__)
        return

    service, auth = init_conf(
        service, username, password, token_url,
        client_id, client_secret, config)

    if check_service:
        if url_ok(service, auth):
            print(f"OData service `{service}` is accessible.")
            sys.exit(0)
        else:
            print(f"Cannot access OData service `{service}`.")
            sys.exit(2)

    # Manage Proxy configuration
    if proxy:
        proxy_param_to_os_env(proxy)

    if isinstance(auth, HTTPBasicAuth):
        logger.debug("Establish connection to the service "
                     "using basic authentication")
    elif isinstance(auth, HTTPOAuth2):
        logger.debug("Establish connection to the service "
                     "using OAuth2 authentication")
    elif auth is None:
        logger.debug("Establish connection to the service "
                     "without authentication")

    # Prepare filter
    query = query_builder(
        filter=filter,
        date=(start, end),
        geometry=geometry,
        id=uuid,
        name=name,
        mission=mission,
        instrument=instrument,
        product_type=product_type,
        cloud=cloud)

    expand = None
    if attributes:
        expand = 'Attributes'

    # Count only requires the value
    if count:
        limit = 0

    query_controls = query_controls_builder(
        count=count,
        orders=order_by,
        skip=skip,
        limit=limit,
        expand=expand)

    # Connect to the service
    source = OdataSource(service=service, auth=auth)

    # Start with info requests.
    if show_url:
        print(source.build_url_from_queries(query, query_controls))
    elif count:
        print(source.get_count(query, query_controls))
    elif download:
        source.download(query=query, query_controls=query_controls,
                        threads=thread_number,
                        verify=verify,
                        output=output, quiet=quiet)
    elif footprint:
        # Minimal inclusion shall include 'GeoFootprint'
        if 'GeoFootprint' not in format:
            format += ('GeoFootprint',)

        # Manage the footprint output
        if footprint == "-":
            output = sys.stdout
        else:
            output = open(footprint, "w")
        # Retrieve the product list within a range
        products = source.request_products(query, query_controls)

        # Header
        output.write('{"type":"FeatureCollection", "features": [')
        for product in products:
            geo = request_product_to_geojson(product, format, exclude=exclude)
            output.write(geo)
            # Detects end of list to manage trailer coma
            if product == products[-1]:
                output.write("\n")
            else:
                output.write(",\n")
        # trailer
        output.write(']}\n')
        if output != sys.stdout:
            output.close()
        sys.exit(0)
    else:
        # Query filter
        products = source.request(query, query_controls, format)
        logger.setLevel(logging.INFO)
        logger.info(products)


def product_to_geojson(product, add_attributes_flag: bool = False,
                       format=('Id', 'Name')):
    geo = dict()
    geo['properties'] = dict()
    geo['type'] = "Feature"
    geo['geometry'] = product @ 'GeoFootprint'
    geo['properties'] = OdataSource.get_metadata(product, format,
                                                 ('GeoFootprint', 'Footprint'))

    # Report the product Attributes if requested.
    # Call to attributes raises new calls to GSS that may reduce
    # the performances (shall be deactivated by default).
    if add_attributes_flag:
        for attribute in product['Attributes']:
            if attribute.value:
                # remove the INSPIRE parametrized attributes
                # with pattern value "{XXX}"
                if (attribute.attributes['ValueType', None] == 'String'
                        and re.match(r'.*\{.*\}', str(attribute.value))):
                    continue
                geo['properties'][attribute.name] = attribute.value
    return geojson.dumps(geo)


def request_product_to_geojson(product, include=('Id', 'Name'), exclude=()):
    exclude += ('GeoFootprint', 'Footprint')
    geo = dict()
    geo['properties'] = dict()
    geo['type'] = "Feature"
    geo['geometry'] = product['GeoFootprint']
    geo['properties'] = OdataSource.get_metadata(
        product, include=include, exclude=exclude)
    return geojson.dumps(geo)


def url_ok(url, auth=None):
    """
    Controls the passed url is accessible.
    """
    try:
        # Use http HEADER
        try:
            response = requests.head(url, auth=auth)
        except Exception:
            return False
        # check the status code
        if response.status_code < 400:
            return True
        else:
            return False
    except requests.ConnectionError as e:
        return e


if __name__ == '__main__':
    cli()
