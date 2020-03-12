import unittest
from distribution.transform import metadata_manager

class TestTransform(unittest.TestCase):
    def setUp(self):
        self.input_file = "../data/sql_metadata.xlsx"
        self.output_file = "../data/test_suite_file"

    def test_extract_data(self):
        manager = metadata_manager(self.input_file, self.output_file)
        master_metadata = manager.extract_data()
        self.assertIsNotNone(manager.extract_data())

    def test_create_pi_data_descriptors(self):
        pass

