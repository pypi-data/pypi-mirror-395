import unittest
from pathlib import Path
from tira.io_utils import load_metadata_of_dataset_from_directory

class TestMultiAuthorDataset(unittest.TestCase):
    def test_multi_author_complete(self):
        load_metadata_of_dataset_from_directory(Path("tests/resources/example-datasets/multi-author-analysis/"), "inputs", "truths", "train")
