import pytest
import gzip, zipfile, pathlib

from iterator.FileIterator import PlainIterator, \
    GzipIterator, ZipIterator


# Helper functions.
def write_nums(f, nums=10):
    for i in range(nums):
        f.write(f'{i}\n'.encode())

def get_path_obj(filename):
    return pathlib.Path(filename).resolve()


@pytest.fixture
def gzip_file():
    p = get_path_obj('test.gz')
    with gzip.open(str(p), 'wb') as f:
        write_nums(f)
    yield p
    p.unlink()

@pytest.fixture
def txt_file():
    p = get_path_obj('test.txt')
    with open(str(p), 'wb') as f:
        write_nums(f)
    yield p
    p.unlink()

@pytest.fixture
def zip_file(txt_file):
    p_txt = txt_file
    p_zip = get_path_obj('test.zip')
    with zipfile.ZipFile(str(p_zip), 'w') as z:
        z.write(str(p_txt))
    yield p_zip
    p_zip.unlink()

@pytest.fixture
def plain_iter(txt_file):
    it = PlainIterator(txt_file)
    yield it
    it.close()

@pytest.fixture
def gzip_iter(gzip_file):
    it = GzipIterator(gzip_file)
    yield it
    it.close()

@pytest.fixture
def zip_iter(zip_file):
    it = ZipIterator(zip_file)
    yield it
    it.close()