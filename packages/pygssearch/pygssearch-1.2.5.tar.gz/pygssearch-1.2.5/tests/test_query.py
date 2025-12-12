import unittest
import uuid
import os

from pygssearch.query.query import query_builder, query_controls_builder
from pygssearch.query.query import default_limit, default_skip
from pygssearch.source.source import OdataSource


class TestQueryBuilder(unittest.TestCase):
    geo_file = 'geo.json'
    geo_query = "OData.CSC.Intersects(location=Footprint," \
                "area=geography'SRID=4326;Polygon(" \
                "(100.0 0.0,101.0 0.0,101.0 1.0,100.0 1.0,100.0 0.0))')"

    @classmethod
    def setUpClass(cls):
        cls.geo_path = os.path.join(os.path.dirname(__file__),
                                    'resources', cls.geo_file)

    def test_default_query(self):
        query = query_builder()
        self.assertIsNone(query)

    def test_default_query_control(self):
        query = query_controls_builder()
        self.assertRegex(query, fr"\$top={default_limit}")
        self.assertRegex(query, fr"\$skip={default_skip}")

    def test_date_filter(self):
        query = query_builder(date=('2020-21-12', None))
        self.assertEqual(query, 'ContentDate/Start ge 2020-21-12T00:00:00.0Z')

        query = query_builder(date=('2020-21-12T00:00:00.0Z', None))
        self.assertEqual(query, 'ContentDate/Start ge 2020-21-12T00:00:00.0Z')

        query = query_builder(date=('NOW', None))
        self.assertEqual(query, 'ContentDate/Start ge NOW')

        query = query_builder(date=('2020-21-12', "2020-21-12"))
        self.assertEqual(query,
                         'ContentDate/Start ge 2020-21-12T00:00:00.0Z '
                         'and ContentDate/End lt 2020-21-12T00:00:00.0Z')

        query = query_builder(date=(None, '2020-21-12'))
        self.assertEqual(query, 'ContentDate/End lt 2020-21-12T00:00:00.0Z')

    def test_geometry_filter(self):
        query = query_builder(geometry=self.geo_path)
        self.assertEqual(query, self.geo_query)

        query = query_builder(geometry="((1.0,1.0), (0.0,1.0), (0.0,0.0))")
        self.assertEqual(query,
                         "OData.CSC.Intersects(location=Footprint,"
                         "area=geography'SRID=4326;"
                         "Polygon((1.0 1.0,0.0 1.0,0.0 0.0))')")

        query = query_builder(geometry="((1.0, 1.0), (0.0, 1.0), (0.0, 0.0))")
        self.assertEqual(query,
                         "OData.CSC.Intersects(location=Footprint,"
                         "area=geography'SRID=4326;"
                         "Polygon((1.0 1.0,0.0 1.0,0.0 0.0))')")

    def test_filter(self):
        query = query_builder(filter='my awsomeodatafilter', name=('s1abs',))
        self.assertEqual(query,
                         "my awsomeodatafilter and contains(Name,'s1abs')")

    def test_uuid_filter(self):
        query = query_builder(id=('123456',))
        self.assertEqual(query, "Id eq 123456")

        query = query_builder(id='123456')
        self.assertEqual(query, "Id eq 123456")

        test_id = uuid.UUID('3d641f34-af4e-4a08-b7b0-5c6bebc1cbfc')
        query = query_builder(id=test_id)
        self.assertEqual(query, f"Id eq {str(test_id)}")

        query = query_builder(id=('123456', '7891011'))
        self.assertEqual(query, "(Id eq 123456 or Id eq 7891011)")

    def test_name_filter(self):
        query = query_builder(name=('s1A_GRD',))
        self.assertEqual(query, "contains(Name,'s1A_GRD')")

        query = query_builder(name='s1A_GRD')
        self.assertEqual(query, "contains(Name,'s1A_GRD')")

        query = query_builder(name=('s1A_GRD', 'S2B_SLC'))
        self.assertEqual(query, "(contains(Name,'s1A_GRD') or "
                                "contains(Name,'S2B_SLC'))")

    def test_mission_filter(self):
        query = query_builder(mission=1)
        self.assertEqual(query, "startswith(Name,'S1')")

        query = query_builder(mission=2)
        self.assertEqual(query, "startswith(Name,'S2')")

        query = query_builder(mission=3)
        self.assertEqual(query, "startswith(Name,'S3')")

        query = query_builder(mission=4)
        self.assertEqual(query, "startswith(Name,'S4')")

        query = query_builder(mission=5)
        self.assertEqual(query, "startswith(Name,'S5')")

        query = query_builder(mission=6)
        self.assertEqual(query, "startswith(Name,'S6')")

    def test_instrument_filter(self):
        query = query_builder(instrument='MSI')
        self.assertEqual(query, "StringAttributes/any("
                                "d:d/Name eq 'instrumentShortName' and "
                                "d/Value eq 'MSI')")

        query = query_builder(instrument='OLCI')
        self.assertEqual(query, "StringAttributes/any("
                                "d:d/Name eq 'instrumentShortName' and "
                                "d/Value eq 'OLCI')")

    def test_product_filter(self):
        query = query_builder(product_type='GRD')
        self.assertEqual(query, "StringAttributes/any("
                                "d:d/Name eq 'productType' and "
                                "d/Value eq 'GRD')")

        query = query_builder(product_type='L1B_RA_BD1')
        self.assertEqual(query, "StringAttributes/any("
                                "d:d/Name eq 'productType' and "
                                "d/Value eq 'L1B_RA_BD1')")

    def test_cloud_filter(self):
        query = query_builder(cloud='50')
        self.assertEqual(query, "Attributes/OData.CSC.DoubleAttribute/any("
                                "d:d/Name eq 'cloudCover' and "
                                "d/OData.CSC.DoubleAttribute/Value lt 50)")

        query = query_builder(cloud='25')
        self.assertEqual(query, "Attributes/OData.CSC.DoubleAttribute/any("
                                "d:d/Name eq 'cloudCover' and "
                                "d/OData.CSC.DoubleAttribute/Value lt 25)")

    def test_query_control_order(self):
        query = query_controls_builder(
            orders=('+ContentLength', '-PublicationDate'))
        self.assertRegex(query, r"\$orderby=ContentLength asc,"
                                r"PublicationDate desc")

        query = query_controls_builder(orders=('+ContentLength',))
        self.assertRegex(query, r"\$orderby=ContentLength asc")

        query = query_controls_builder(orders=('ContentLength',))
        self.assertRegex(query, r"\$orderby=ContentLength asc")

        query = query_controls_builder(orders=('-ContentLength',))
        self.assertRegex(query, r"\$orderby=ContentLength desc")

    def test_query_control_limit(self):
        # Check default
        query = query_controls_builder()
        self.assertRegex(query, rf"\$top={default_limit}")

        limit = 99999
        query = query_controls_builder(limit=limit)
        self.assertRegex(query, rf"\$top={limit}")

    def test_query_control_skip(self):
        # Check default
        query = query_controls_builder()
        self.assertRegex(query, rf"\$skip={default_skip}")

        skip = 77777
        query = query_controls_builder(skip=skip)
        self.assertRegex(query, rf"\$skip={skip}")

    def test_query_control_count(self):
        # Check default (nothing)
        query = query_controls_builder()
        self.assertFalse(query.find("count") > 0,
                         "'count' directive found in default call")

        count = True
        query = query_controls_builder(count=count)
        self.assertRegex(query, rf"\$count=true")

        count = False
        query = query_controls_builder(count=count)
        self.assertFalse(query.find("count") > 0,
                         "'count' directive found but false.")

    def test_query_control_select(self):
        # Check default (nothing)
        query = query_controls_builder()
        self.assertFalse(query.find("select") > 0,
                         "'select' directive found in default call")

        select = 'Attributes'
        query = query_controls_builder(select=select)
        self.assertRegex(query, rf"\$select={select}")

    def test_query_control_expand(self):
        # Check default (nothing)
        query = query_controls_builder()
        self.assertFalse(query.find("expand") > 0,
                         "'expand' directive found in default call")

        expand = 'Attributes'
        query = query_controls_builder(expand=expand)
        self.assertRegex(query, rf"\$expand={expand}")

    def test_query_control_format(self):
        # Check default (nothing)
        query = query_controls_builder()
        self.assertRegex(query, rf"\$format=json")

        format = 'xml'
        query = query_controls_builder(format=format)
        self.assertRegex(query, rf"\$format={format}")

    def test_query_control_mixed(self):
        order = '-ContentLength'
        limit = 6666
        skip = 3333
        count = True
        select = 'Nothing'
        expand = 'Something'
        format = 'xml'

        query = query_controls_builder(format=format,
                                       orders=(order,),
                                       limit=limit,
                                       skip=skip,
                                       count=count,
                                       select=select,
                                       expand=expand)

        self.assertRegex(query, rf"\$expand={expand}")
        self.assertRegex(query, rf"\$format={format}")
        self.assertRegex(query, rf"\$select={select}")
        self.assertRegex(query, rf"\$count=true")
        self.assertRegex(query, rf"\$skip={skip}")
        self.assertRegex(query, rf"\$orderby={order[1:]} desc")
        self.assertRegex(query, rf"\$top={limit}")

    def test_build_url(self):
        filter = 'ContentLenght lt 10000000'
        order = '-ContentLength'
        limit = 6666
        skip = 3333
        count = True
        select = 'Nothing'
        expand = 'Something'
        format = 'xml'

        query = query_builder(filter=filter)
        query_controls = query_controls_builder(format=format,
                                                count=count,
                                                orders=(order,),
                                                skip=skip,
                                                limit=limit,
                                                select=select,
                                                expand=expand)

        source = OdataSource(service='http://local.gael.fr/path')
        url = source.build_url_from_queries(query, query_controls)

        self.assertEqual(url, "http://local.gael.fr/path/Products?"
                              "$filter=ContentLenght lt 10000000&"
                              "$top=6666&"
                              "$skip=3333&"
                              "$format=xml&"
                              "$count=true&"
                              "$expand=Something&"
                              "$select=Nothing&"
                              "$orderby=ContentLength desc")
