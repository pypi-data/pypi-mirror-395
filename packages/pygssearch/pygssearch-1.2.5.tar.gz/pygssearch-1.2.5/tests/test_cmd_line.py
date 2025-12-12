import ast
import re
import os
import unittest

import geojson
from tempfile import NamedTemporaryFile

from click.testing import CliRunner

from pygssearch.cli import cli, url_ok
from unittest import TestCase, skipIf

# Warn this test does not use a https Odata mockup, only real online service
# that may not be online in the near future.
remote_sample_service = "https://vision.odata.gael.fr/odata/v1"


class TestCli(TestCase):
    runner = CliRunner()
    skip_url = not url_ok(remote_sample_service)

    def test_cli_version(self):
        result = self.runner.invoke(cli, ['--version'])
        self.assertEqual(result.exit_code, 0)
        self.assertIsNotNone(result.output)

    def test_cli_check_service(self):
        self.assertTrue(url_ok(remote_sample_service))
        self.assertFalse(url_ok("http://no_service/"))

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_orig(self):
        result = self.runner.invoke(cli, ['--service', remote_sample_service])
        self.assertEqual(result.exit_code, 0)
        output = ast.literal_eval(result.output)
        self.assertEqual(len(output), 10)
        # default contains (Name, Id)
        self.assertEqual(len(output[0]), 2)

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_orig_format(self):
        result = self.runner.invoke(cli, [
            '--service', remote_sample_service,
            '--format', "_"])
        self.assertEqual(result.exit_code, 0)
        output = ast.literal_eval(result.output)
        self.assertEqual(len(output), 10)
        # default contains (Name, Id)
        self.assertGreater(len(output[0]), 3)

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_orig_format_selection(self):
        result = self.runner.invoke(cli, [
            '--service', remote_sample_service,
            '--format', 'Id',
            '--format', 'Name',
            '--format', 'PublicationDate'])
        self.assertEqual(result.exit_code, 0)
        output = ast.literal_eval(result.output)
        print(output)
        self.assertEqual(len(output), 10)
        # default contains (Name, Id)
        self.assertEqual(len(output[0]), 3)

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service(self):
        result = self.runner.invoke(
            cli,
            ['--service', remote_sample_service,
             '--footprint', '-'])
        self.assertEqual(result.exit_code, 0)
        output = geojson.loads(result.output)
        self.assertEqual(output.get('type'), 'FeatureCollection')
        self.assertEqual(len(output.get('features')), 10)

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_in_file(self):
        with NamedTemporaryFile(suffix='.geojson') as tmp_file:
            result = self.runner.invoke(
                cli,
                ['--service', remote_sample_service,
                 '--footprint', tmp_file.name])
            self.assertEqual(result.exit_code, 0)
            output = geojson.load(tmp_file)
            self.assertEqual(output.get('type'), 'FeatureCollection')
            self.assertEqual(len(output.get('features')), 10)
            feature = output.get('features')[5]
            self.assertEqual(len(feature['properties']), 2)

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_in_file_with_attributes(self):
        with NamedTemporaryFile(suffix='.geojson') as tmp_file:
            result = self.runner.invoke(
                cli,
                ['--service', remote_sample_service,
                 '--footprint', tmp_file.name,
                 '--format', '_',
                 '--attributes'])
            self.assertEqual(result.exit_code, 0)
            output = geojson.load(tmp_file)
            self.assertEqual(output.get('type'), 'FeatureCollection')
            self.assertEqual(len(output.get('features')), 10)
            feature = output.get('features')[5]
            print(feature)
            self.assertGreater(len(feature['properties']), 3)
            self.assertIsNotNone(feature['properties'].get('coordinates'))

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_in_file_with_attributes_exclusion(self):
        with NamedTemporaryFile(suffix='.geojson') as tmp_file:
            result = self.runner.invoke(
                cli,
                ['--service', remote_sample_service,
                 '--footprint', tmp_file.name,
                 '--attributes',
                 '--format', '_',
                 '--exclude', 'coordinates',
                 '--exclude', 'brightCover'])
            self.assertEqual(result.exit_code, 0)
            output = geojson.load(tmp_file)
            feature = output.get('features')[5]
            print(feature)
            self.assertIsNone(feature['properties'].get('coordinates'))
            self.assertIsNone(feature['properties'].get('brightCover'))

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_in_file_with_attributes_inclusion(self):
        with NamedTemporaryFile(suffix='.geojson') as tmp_file:
            result = self.runner.invoke(
                cli,
                ['--service', remote_sample_service,
                 '--footprint', tmp_file.name,
                 '--attributes',
                 '--format', 'Name',
                 '--format', 'Id',
                 '--format', 'processingDate'])
            self.assertEqual(result.exit_code, 0)
            output = geojson.load(tmp_file)
            feature = output.get('features')[5]
            print(feature)
            self.assertIsNotNone(feature['properties'].get('Name'))
            self.assertIsNotNone(feature['properties'].get('Id'))
            self.assertIsNotNone(feature['properties'].get('processingDate'))

    @skipIf(skip_url, "Url not accessible")
    def test_cli_service_in_file_with_attributes_inclusion_all(self):
        with NamedTemporaryFile(suffix='.geojson') as tmp_file:
            result = self.runner.invoke(
                cli,
                ['--service', remote_sample_service,
                 '--footprint', tmp_file.name,
                 '--attributes',
                 '--format', '_'])
            self.assertEqual(result.exit_code, 0)
            output = geojson.load(tmp_file)
            feature = output.get('features')[5]
            print(feature)
            self.assertIsNotNone(feature['properties'].get('Name'))
            self.assertIsNotNone(feature['properties'].get('Id'))
            self.assertIsNotNone(feature['properties'].get('processingDate'))

    def test_cli_url_valid(self):
        result = self.runner.invoke(
            cli,
            ['--service', remote_sample_service,
             '--attributes',
             '--limit', 15,
             '--skip', 1,
             '--order_by', '+ContentLength',
             '--order_by', '-PublicationDate',
             '--filter', 'ContentLength lt 10000000',
             '--show_url'])
        self.assertEqual(result.exit_code, 0)
        print(result.output)
        # warn the trailer \n was added here because returned url is displayed
        # by cli with prnt command that add CRLR to the output. It is not #
        # normal case wrt the command controlled itself.
        self.assertEqual(result.output, remote_sample_service +
                         "/Products?"
                         "$filter=ContentLength lt 10000000&"
                         "$top=15&"
                         "$skip=1&"
                         "$format=json&"
                         "$expand=Attributes&"
                         "$orderby=ContentLength asc,PublicationDate desc\n")

    def test_cli_param_well_handled(self):
        result = self.runner.invoke(
            cli,
            ['--service', remote_sample_service,
             '--footprint', '-',
             '--attributes',
             '--end', '2023-07-05',
             '--start', '2023-07-04',
             '--exclude', 'coordinates',
             '--exclude', 'specificationTitle',
             '--uuid', '285cdd67-713d-436a-ae92-df26e376f4d0',
             '--name', 'Toto',
             '--name', 'titi',
             '--uuid', 'an-other-uuid',
             '--instrument', 'MSI',
             '--instrument', 'SAR',
             '--mission', '1',
             '--mission', '2',
             '--cloud', '50',
             '--limit', 15,
             '--skip', 1,
             '--order_by', '+ContentLength',
             '--order_by', '-PublicationDate',
             '--filter', 'ContentLength lt 10000000',
             '--show_url'])
        self.assertEqual(result.exit_code, 0)
        print(result.output)
        # warn the trailer \n was added here because returned url is displayed
        # by cli with prnt command that add CRLR to the output. It is not #
        # normal case wrt the command controlled itself.
        expected_result = (
            remote_sample_service +
            "/Products?"
            "$filter=ContentLength lt 10000000 and startswith(Name,'S2') and "
            "StringAttributes/any(d:d/Name eq 'instrumentShortName' and "
            "                       d/Value eq 'SAR') and "
            "Attributes/OData.CSC.DoubleAttribute/any(d:d/Name eq 'cloudCover'"
            "               and d/OData.CSC.DoubleAttribute/Value lt 50) and "
            "ContentDate/Start ge 2023-07-04T00:00:00.0Z and "
            "ContentDate/End lt 2023-07-05T00:00:00.0Z and "
            "(contains(Name,'Toto') or contains(Name,'titi')) and "
            "(Id eq 285cdd67-713d-436a-ae92-df26e376f4d0 or "
            " Id eq an-other-uuid)&"
            "$top=15&"
            "$skip=1&"
            "$format=json&"
            "$expand=Attributes&"
            "$orderby=ContentLength asc,PublicationDate desc\n")

        self.assertEqual(result.output, re.sub(r' +', ' ', expected_result))

    def test_cli_geometry(self):
        result = self.runner.invoke(
            cli,
            ['--service', remote_sample_service,
             '--geometry',
             '((1.0,1.0),(0.0,1.0),(0.0,0.0),(1.0,0.0),(1.0,1.0))',
             '--show_url'])
        self.assertEqual(result.exit_code, 0)
        print(result.output)
        expected_result = \
            ("$filter=OData.CSC.Intersects("
             "location=Footprint,area=geography'SRID=4326;"
             "Polygon((1.0 1.0,0.0 1.0,0.0 0.0,1.0 0.0,1.0 1.0))')")

        self.assertTrue(expected_result in result.output)

    @skipIf(skip_url, "Url not accessible")
    def test_cli_count(self):
        result = self.runner.invoke(
            cli,
            ['--service', remote_sample_service,
             '--count',
             '--attributes',
             '--limit', 15,
             '--skip', 1,
             '--order_by', '+ContentLength',
             '--order_by', '-PublicationDate',
             '--filter', 'ContentLength lt 10000000'])
        self.assertEqual(result.exit_code, 0)
        print(result.output)
        # WARN#1: the trailer \n was added here because returned url is
        # displayed by cli with prnt command that add CRLR to the output.
        # It is not normal case wrt the command controlled itself.

        # WARN#2: Currently (31/07/2024) vision return 11 products lower than
        # 10MB and it may change.
        self.assertGreaterEqual(int(result.output), 11)
