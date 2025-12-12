import logging
from typing import List
import requests
import geojson
import re

from drb.drivers.odata import ODataQueryPredicate
from drb.drivers.odata.odata_services_nodes import ODataServiceNodeCSC
from requests.auth import AuthBase

from pygssearch.source.download import Download


class OdataSourceError(Exception):
    pass


logger = logging.getLogger('pygssearch')


class OdataSource:
    """
    ODataSource Class is the implementation of DrbNode retrieval from an OData
    service.

    :param service: (str) the url of the product
    :param auth: (AuthBase) the authentication to access the service
    """

    def __init__(self, service: str, auth: AuthBase = None):
        self._service = service
        self.auth = auth
        self.__odata_service = ODataServiceNodeCSC(self.service,
                                                   auth=self.auth)

    @property
    def service(self):
        """
        Property to retrieve the property field as a string.

        :return: the service url as string.
        """
        return self._service

    def drb_request_products(self, query=None, query_order=None):
        return self.__odata_service[
            ODataQueryPredicate(
                filter=query,
                order=query_order
            )]

    def build_url_from_queries(self, query=None, query_controls=None) -> str:
        """
        Build the complete URL to be used in OData CSC service.
        """
        sep = '?'
        if query:
            query = sep + '$filter=' + query
            sep = '&'
        else:
            query = ''
        if query_controls:
            query = query + sep + query_controls
            sep = '&'
        return self.__odata_service.get_service_url() + f"/Products{query}"

    def request_products(self, query=None, query_controls=None):
        full_url = self.build_url_from_queries(query, query_controls)
        # CAHU-193: The requests library replaces all spaces by '%20',
        #    but note quotes "'". This make the GSS service fails with
        #    Http-500 Internal Error.
        full_url = full_url.replace("'", '%27')
        result = requests.get(full_url, auth=self.auth)
        result.raise_for_status()
        return geojson.loads(result.text)['value']

    def get_count(self, query=None, query_controls=None):
        # Checks if 'count' control is active
        if '$count=true' not in query_controls:
            if query_controls:
                query_controls += '&$count=true'
            else:
                query_controls = '$count=true'
        full_url = self.build_url_from_queries(query, query_controls)
        result = requests.get(full_url, auth=self.auth)
        return geojson.loads(result.text)['@odata.count']

    def get_metadatas(self, products: List, include=('Name', 'Id'), skip=0,
                      limit=10, exclude=()):
        for prd in [products[skip + x] for x in range(limit)]:
            yield OdataSource.get_metadata(prd, include, exclude)

    @staticmethod
    def get_metadata(product, include=('Name', 'Id'), exclude=()):
        if include == '_' or include[0] == '_':
            if hasattr(product, 'attribute_names'):
                include = [x[0] for x in product.attribute_names()]
            else:
                include = list(product.keys())
                attributes = product.get('Attributes')
                if attributes:
                    include.remove('Attributes')
                    include += [item['Name'] for item in attributes]

        meta = {}
        for e in include:
            if e not in exclude:
                if hasattr(product, 'attribute_names'):
                    meta[e] = product @ e
                else:
                    if e in product.keys():
                        meta[e] = product[e]
                    else:
                        attributes = product.get('Attributes')
                        if attributes:
                            item = [item for item in attributes
                                    if item['Name'] == e]
                            if not item:
                                continue
                            item = next(iter(item))
                            name = item['Name']
                            value = item['Value']
                            vtype = item["ValueType"]
                            if value is not None:
                                # remove the INSPIRE parametrized attributes
                                # with pattern value "{XXX}"
                                if vtype == 'String' and \
                                        re.search(r'^\{.*\}', str(value)):
                                    continue
                                # manage exclude list
                                if name in exclude:
                                    continue
                                if '_' not in include and name not in include:
                                    continue
                                meta[e] = value
                            else:
                                logger.warning(f"Attribute '{e}' not found.")
                        else:
                            logger.warning(
                                f"Product property '{e}' not found.")
        return meta

    def request(self, query=None, query_controls=None, include=('Name', 'Id')):
        """
        Request the odata services en retrieve the matching data.

        :param query: The OData filter to apply in the query.
        :param query_controls: the parameters to manage results.
        :param include: (tuple[str]) The list of attributes to be included
         into the results. default value is ('Name', 'Id').

        :return: A list of dict containing all the data asked
                 if no matching product return an empty list.
        """
        request = self.request_products(query, query_controls)

        limit = len(request)
        # Skip is set to 0 because, the shift is down at the query time.
        return list(self.get_metadatas(request, include, 0, limit))

    def download(self, query=None, query_controls=None,
                 output='.', threads=2, verify=False,
                 quiet=False) -> None:
        """
           Manages download of the products matching the query.
           Note: This method retrieves products results from direct requests
              call instead of Drb to bypass its current performances issues.
              Once fixed, the previous download has not been modified and
              can be reused.
        """
        # Prepare download manager
        dm = Download(output_folder=output, verify=verify, quiet=quiet,
                      threads=threads)

        products = self.request_products(query, query_controls)
        for product in products:
            drb_product = self.drb_request_products(
                f'Id eq {product["Id"]}')[0]
            dm.submit(drb_product)
        dm.wait()
