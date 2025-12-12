import json
import os
import unittest

import click.exceptions
from drb.drivers.http import HTTPOAuth2

from pygssearch.utility import (
    parse_config_file, init_conf,
    slice_file, Chunk,
    compute_md5, footprint_extract, proxy_param_to_os_env
)


class TestConf(unittest.TestCase):
    conf_file = 'conf.ini'
    conf_auth2_file = 'auth2.ini'
    geo_file = 'geo.json'
    geo_file_minimal = 'geo_minimal.json'
    md5 = "c9c8d3decde410c38a094b0c418f8656"
    expected = {'service': 'https://my_gss_catalogue.com',
                'username': 'user', 'password': 'pwd'}

    @classmethod
    def setUpClass(cls):
        cls.conf_path = os.path.join(os.path.dirname(__file__),
                                     'resources', cls.conf_file)
        cls.conf_auth2 = os.path.join(os.path.dirname(__file__),
                                      'resources', cls.conf_auth2_file)
        cls.geo_path = os.path.join(os.path.dirname(__file__),
                                    'resources', cls.geo_file)
        cls.geo_path_minimal = os.path.join(os.path.dirname(__file__),
                                            'resources', cls.geo_file_minimal)

    def test_load_conf(self):
        no_conf = parse_config_file(None)
        self.assertIsNone(no_conf)

        conf = parse_config_file(self.conf_path)
        self.assertIsInstance(conf, dict)
        self.assertEqual(conf, self.expected)

    def test_init_conf(self):
        conf = init_conf(None, None, None, None, None, None,
                         self.conf_path)
        self.assertEqual(conf[0], self.expected['service'])

        conf = init_conf(None, 'Toto', 'Tata', None, None, None,
                         self.conf_path)
        self.assertEqual(conf[1].username, 'Toto')
        self.assertEqual(conf[1].password, 'Tata')

        conf = init_conf(None, None, None, None, None, None, self.conf_auth2)
        self.assertEqual(conf[0], self.expected['service'])
        self.assertIsInstance(conf[1], HTTPOAuth2)

        with self.assertRaises(click.exceptions.BadParameter):
            init_conf(None, None, None, None, None, None, None)

    def test_slice_file(self):
        chunks = slice_file(3, 1)
        self.assertIsInstance(chunks, list)
        self.assertIsInstance(chunks[0], Chunk)
        self.assertEqual(len(chunks), 3)

        chunks = slice_file(7, 5)
        self.assertIsInstance(chunks, list)
        self.assertIsInstance(chunks[0], Chunk)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[1].start, 5)
        self.assertEqual(chunks[1].end, 6)

    def test_geojson_load(self):
        with open(self.geo_path) as f:
            geo = json.load(f)
        geo = footprint_extract(geo)
        self.assertIsNotNone(geo)
        self.assertIsInstance(geo, list)
        self.assertEqual(len(geo), 5)

    def test_geojson_load_minimal(self):
        with open(self.geo_path_minimal) as f:
            geo = json.load(f)
        geo = footprint_extract(geo)
        self.assertIsNotNone(geo)
        self.assertIsInstance(geo, list)
        self.assertEqual(len(geo), 5)

    def test_md5(self):
        self.assertEqual(
            compute_md5(self.conf_path),
            self.md5
        )

    def test_proxy_format_string_parameters(self):
        proxy_param_to_os_env('http://51.91.23.207:3128')
        self.assertEqual(os.environ['HTTP_PROXY'],
                         'http://51.91.23.207:3128')
        self.assertEqual(os.environ['HTTPS_PROXY'],
                         'http://51.91.23.207:3128')
        self.assertEqual(os.environ['FTP_PROXY'],
                         'http://51.91.23.207:3128')

        proxy_param_to_os_env('https://51.91.23.207:3128/')
        self.assertEqual(os.environ['HTTP_PROXY'],
                         'https://51.91.23.207:3128/')
        self.assertEqual(os.environ['HTTPS_PROXY'],
                         'https://51.91.23.207:3128/')
        self.assertEqual(os.environ['FTP_PROXY'],
                         'https://51.91.23.207:3128/')

        proxy_param_to_os_env('51.91.23.207:3128/')
        self.assertEqual(os.environ['HTTP_PROXY'],
                         'http://51.91.23.207:3128/')

        proxy_param_to_os_env('https://user:pass@51.91.23.207:3128/')
        self.assertEqual(os.environ['HTTP_PROXY'],
                         'https://user:pass@51.91.23.207:3128/')
        proxy_param_to_os_env('51.91.23.207:3128?q=AZERTT&requ=123')
        self.assertEqual(os.environ['HTTP_PROXY'],
                         'http://51.91.23.207:3128?q=AZERTT&requ=123')

    def test_proxy_format_dict_parameters(self):
        proxy_param_to_os_env(
            "{'http':  'http://51.91.23.207:3128', "
            " 'https': 'https://51.91.23.208:3128', "
            " 'ftp':   'http://51.91.23.210:3128'}")

        self.assertEqual(os.environ['HTTP_PROXY'],
                         'http://51.91.23.207:3128')
        self.assertEqual(os.environ['HTTPS_PROXY'],
                         'https://51.91.23.208:3128')
        self.assertEqual(os.environ['FTP_PROXY'],
                         'http://51.91.23.210:3128')

        proxy_param_to_os_env(
            "{'http':  '51.91.23.207:3128', "
            " 'https': '51.91.23.208:3128', "
            " 'ftp':   '51.91.23.209:3128'}")

        self.assertEqual(os.environ['HTTP_PROXY'],
                         'http://51.91.23.207:3128')
        self.assertEqual(os.environ['HTTPS_PROXY'],
                         'http://51.91.23.208:3128')
        self.assertEqual(os.environ['FTP_PROXY'],
                         'http://51.91.23.209:3128')
