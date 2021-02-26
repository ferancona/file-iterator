import pytest

from file_iterator.Utils import FileManager


def test_is_gzipfile(gzip_file):
    assert FileManager.is_gzipfile(gzip_file)

def test_is_zipfile(zip_file):
    assert FileManager.is_zipfile(zip_file)