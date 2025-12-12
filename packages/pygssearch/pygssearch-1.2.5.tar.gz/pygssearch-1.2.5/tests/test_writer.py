import os
import unittest

from pygssearch.destination.writer import FileWriter


class TestWriter(unittest.TestCase):
    test_file = 'toto.txt'

    @classmethod
    def setUpClass(cls):
        cls.test_path = os.path.join(os.path.dirname(__file__),
                                     'resources', cls.test_file)
        cls.write = b'my awesome test'
        cls.writer = FileWriter(cls.test_path, len(cls.write))

    @classmethod
    def tearDownClass(cls) -> None:
        # os.remove(cls.path)
        if os.path.exists(cls.test_path):
            os.remove(cls.test_path)

    def test_writer(self):
        self.assertIsInstance(self.writer, FileWriter)
        self.assertEqual(self.writer.file_size, len(self.write))
        self.assertEqual(self.writer.final_filename, self.test_path)
        self.assertEqual(self.writer.size_written, 0)
        self.assertFalse(os.path.exists(self.writer.out_file))

        self.writer._init_writer()

        self.assertTrue(os.path.exists(self.writer.out_file))
        self.assertFalse(os.path.exists(self.test_path))
        with open(self.writer.out_file) as fp:
            self.assertEqual(len(fp.read()), len(self.write))
            fp.close()

        self.writer.write(self.write[:8], 0)

        with open(self.writer.out_file) as fp:
            print()
            self.assertEqual(fp.read()[:8], self.write[:8].decode())
            self.assertNotEqual(fp.read()[8:], self.write[8:].decode())
            fp.close()

        self.writer.write(self.write[8:], 8)

        with open(self.writer.out_file) as fp:
            self.assertEqual(fp.read(), self.write.decode())
            fp.close()

        self.writer.close()

        self.assertEqual(self.writer.size_written, 15)
        self.assertFalse(os.path.exists(self.writer.out_file))
        self.assertTrue(os.path.exists(self.writer.final_filename))
