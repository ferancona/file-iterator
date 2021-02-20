import pytest

import gzip, zipfile, pathlib


def write_nums(f, nums=10):
    for i in range(nums):
        f.write(i)

def get_path_obj(filename):
    return pathlib.Path(filename).resolve()


@pytest.fixture
def gzip_file():
    p = get_path_obj('test.gz')
    with gzip.open(str(p), 'w') as f:
        write_nums(f)
    yield p
    p.unlink()

@pytest.fixture
def txt_file():
    p = get_path_obj('test.txt')
    with open(str(p), 'w') as f:
        write_nums(f)
    yield p
    p.unlink()

@pytest.fixture
def zip_file():
    p_zip = get_path_obj('test.zip')
    p_txt = txt_file()
    with zipfile.ZipFile(str(p_zip), 'w') as z:
        z.write(str(p_txt))
    yield z
    p_zip.unlink()