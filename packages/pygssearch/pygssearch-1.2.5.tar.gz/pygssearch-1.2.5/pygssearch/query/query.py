import ast
import geojson
import logging
import os
import uuid
from typing import Union

from drb.drivers.odata import (
    ExpressionFunc,
    ExpressionType, LogicalOperator,
    ComparisonOperator, GroupingOperator)

from pygssearch.utility import parse_date, footprint_extract

logger = logging.getLogger('pygssearch')
default_limit = 10
default_skip = 0


class QueryBuilderError(Exception):
    pass


def __concat_query(query_a, query_b):
    if query_a is None:
        return query_b
    else:
        return LogicalOperator.lo_and(query_a, query_b)


def query_builder(
        filter: str = None,
        date: tuple = (None, None),
        geometry: Union[tuple, str] = (),
        id: Union[tuple, str, uuid.UUID] = (),
        name: Union[tuple, str] = (),
        mission: int = None,
        instrument: str = None,
        product_type: str = None,
        cloud: str = None):
    """
    Help to build the odata query corresponding to a series of
    filter given in argument,
    the user can give a filter already wrote and this builder
    will append it with a logical
    and to the query built.

    :param filter: (str) an already wrote Odata query to apply.
                    by default None.
    :param date: (tuple[str, str]) A tuple of date the first one corresponding
                 to the ContentDate/Start and the second one for the End
                 (by default (None, None)
    :param geometry: Can be a path to the geojson file containing a footprint
                     or a series of coordinate containing in a tuple separated
                     by a coma. default ()
    :param id: A series of uuid matching a series of product by default ()
    :param name: A series of complete name or part on the name of a product
                 this will call the contains method on the field name.
                 by default ()
    :param mission: Filter on the sentinel mission can be 1, 2, 3 or 5.
                    by default None
    :param instrument: Filter on the instrument.
                       by default None by default None
    :param product_type: Filter on the product type you want ot retrieve.
                         by default None
    :param cloud: Maximum cloud cover in percent by default None

    :return: The filter string to be pass to the OData Service.
    """

    query = None
    if filter:
        query = ExpressionType.property(filter)

    if mission is not None:
        query_mission = ExpressionFunc.startswith(
            ExpressionType.property('Name'),
            f'S{int(mission)}')
        query = __concat_query(query, query_mission)

    if instrument is not None:
        query_lambda = ExpressionFunc.any('d', LogicalOperator.lo_and(
            ComparisonOperator.eq(
                ExpressionType.property('d/Name'),
                ExpressionType.string('instrumentShortName')),
            ComparisonOperator.eq(
                ExpressionType.property('d/Value'),
                ExpressionType.string(instrument))))
        query_instrument = ExpressionType.property(
            f"StringAttributes/{query_lambda.evaluate()}")
        query = __concat_query(query, query_instrument)

    if product_type is not None:
        query_lambda = ExpressionFunc.any('d', LogicalOperator.lo_and(
            ComparisonOperator.eq(
                ExpressionType.property('d/Name'),
                ExpressionType.string('productType')),
            ComparisonOperator.eq(
                ExpressionType.property('d/Value'),
                ExpressionType.string(product_type))))
        query_type = ExpressionType.property(
            f"StringAttributes/{query_lambda.evaluate()}")
        query = __concat_query(query, query_type)

    if cloud is not None:
        query_lambda = ExpressionFunc.any(
            'd', LogicalOperator.lo_and(
                ComparisonOperator.eq(
                    ExpressionType.property(
                        'd/Name'), ExpressionType.string('cloudCover')),
                ComparisonOperator.lt(
                    ExpressionType.property(
                        'd/OData.CSC.DoubleAttribute/Value'),
                    ExpressionType.number(cloud))))
        query_could = ExpressionType.property(
            f"Attributes/OData.CSC.DoubleAttribute/{query_lambda.evaluate()}")
        query = __concat_query(query, query_could)

    if date[0] is not None or date[1] is not None:
        if date[0] is not None:
            parsed_date = parse_date(date[0])

            query_start = ComparisonOperator.ge(
                ExpressionType.property('ContentDate/Start'),
                ExpressionType.property(parsed_date))
            query = __concat_query(query, query_start)

        if len(date) > 1 and date[1] is not None:
            parsed_date = parse_date(date[1])

            query_end = ComparisonOperator.lt(
                ExpressionType.property('ContentDate/End'),
                ExpressionType.property(parsed_date))
            query = __concat_query(query, query_end)

    if geometry:
        if os.path.exists(geometry):
            with open(geometry) as f:
                geo = geojson.load(f)
                if not geo.is_valid:
                    raise QueryBuilderError(
                        f"GeoJSON file {geometry} is invalid.")
            geo = footprint_extract(geo)
        else:
            geo = ast.literal_eval(geometry)

        geometry = ExpressionType.footprint(geo)
        query_geo = ExpressionFunc.csc_intersect(ExpressionType.property(
            'location=Footprint'),
            ExpressionType.property(
                f'area={geometry.evaluate()}'))
        query = __concat_query(query, query_geo)

    if len(name) > 0:
        if isinstance(name, str):
            query_name = ExpressionFunc.contains(
                ExpressionType.property('Name'),
                name)
        elif len(name) == 1:
            query_name = ExpressionFunc.contains(
                ExpressionType.property('Name'),
                name[0])
        else:
            tmp = ''
            for n in name:
                tmp += ExpressionFunc.contains(
                    ExpressionType.property('Name'), n).evaluate() + ' or '
            query_name = GroupingOperator.group(
                ExpressionType.property(tmp[:len(tmp) - 4]))
        query = __concat_query(query, query_name)

    if isinstance(id, uuid.UUID) or isinstance(id, str):
        query_uuid = ComparisonOperator.eq(
            ExpressionType.property('Id'),
            ExpressionType.property(id))
        query = __concat_query(query, query_uuid)
    elif len(id) > 0:
        if len(id) == 1:
            query_uuid = ComparisonOperator.eq(
                ExpressionType.property('Id'),
                ExpressionType.property(id[0]))
        else:
            tmp = ''
            for product_id in id:
                tmp += ComparisonOperator.eq(
                    ExpressionType.property('Id'),
                    ExpressionType.property(product_id)).evaluate() + ' or '
            query_uuid = GroupingOperator.group(
                ExpressionType.property(tmp[:len(tmp) - 4]))
        query = __concat_query(query, query_uuid)

    if query is not None:
        logger.debug(f"The query build is {query.evaluate()}")
        return query.evaluate()
    else:
        return None


def query_controls_builder(
        format: str = "json",
        count: bool = False,
        orders: tuple = None,
        skip: int = default_skip,
        limit: int = default_limit,
        expand: str = None,
        select: str = None) -> str:
    """
        This function build standard OData controls to handle results returns:
        $orderby, $skip, $top, $expand and others query control can be
        expanded here with the list of controls.
        To avoid any miss-usage of the OData API, this client controls forces
        the number of results to 10, for more results, the user shall define
        manually this limit.

        :param count: The ``$count`` system query option allows clients to
         request a count of the matching resources included with the resources
         in the response. The ``$count`` query option has a Boolean value of
         true or false.

        :param orders: The order system query option allows clients to request
         resources in a particular order. When the property includes '-'
         modifier, the display order is considered descending, otherwise,
         it is considered ascending regarding the given property value.
         This orders parameter is a list of orders.

        :param skip: A number of items in the queried collection that are to
         be skipped and not included in the results. A client can request a
         particular page of items by combining limit and skip

        :param limit: is the $top parameter in OData query. The $top system
         query option requests the number of items in the queried collection
         to be included in the result

        :param expand: The expand system query option specifies the related
         resources or media streams to be included in line with retrieved
         resources. Each expandItem is evaluated relative to the entity
         containing the navigation or stream property being expanded.

        :param select: This system query option allows clients to request a
         specific set of properties for each entity or complex type.
         The select query option is often used in conjunction with the expand
         system query option, to define the extent of the resource graph to
         return ($expand) and then specify a subset of properties for each
         resource in the graph ($select).

        :return a non-empty string containing with the OData query controls
         to be applied during the filtering request.
    """
    query_controls = [f'$top={limit}', f'$skip={skip}', f'$format={format}']
    if count:
        query_controls.append("$count=true")
    if expand:
        query_controls.append(f'$expand={expand}')
    if select:
        query_controls.append(f'$select={select}')

    if orders:
        order_string = ''
        for order in orders:
            if order.startswith('-'):
                orderby = f'{order[1:]} desc'
            elif order.startswith('+'):
                orderby = f'{order[1:]} asc'
            else:
                orderby = f'{order} asc'
            if order == orders[-1]:
                order_string += orderby
            else:
                order_string += orderby + ','
        query_controls.append(f'$orderby={order_string}')

    if query_controls is not None:
        logger.debug(f"The query control build is {'&'.join(query_controls)}")

    return '&'.join(query_controls)
