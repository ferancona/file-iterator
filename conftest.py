import pytest
import gzip, zipfile, pathlib

from iterator.FileIterator import PlainIterator, \
    GzipIterator, ZipIterator
from iterator.FileGroupIterator import FileGroupIterator


# Helper functions.
def write_nums(f, lines_no):
    for i in range(lines_no):
        f.write(f'{i}\n'.encode())

def get_path_obj(filename):
    return pathlib.Path(filename).resolve()


@pytest.fixture
def lines_no():
    return 10

@pytest.fixture
def name_txt():
    return 'test.txt'

@pytest.fixture
def name_gzip():
    return 'test.gz'

@pytest.fixture
def name_zip():
    return 'test.zip'

@pytest.fixture
def names(txt_file, gzip_file, zip_file):
    return [txt_file, gzip_file, zip_file]

@pytest.fixture
def txt_file(name_txt):
    p = get_path_obj(name_txt)
    with open(str(p), 'wb') as f:
        write_nums(f)
    yield p
    p.unlink()

@pytest.fixture
def gzip_file(name_gzip):
    p = get_path_obj(name_gzip)
    with gzip.open(str(p), 'wb') as f:
        write_nums(f)
    yield p
    p.unlink()

@pytest.fixture
def zip_file(txt_file, name_zip):
    p_txt = txt_file
    p_zip = get_path_obj(name_zip)
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

@pytest.fixture
def group_iter(names):
    it = FileGroupIterator(names)
    yield it
    it.close()