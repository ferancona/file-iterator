import pytest
import gzip, zipfile, pathlib

from iterator.FileIterator import LocalFileIterator, \
    PlainIterator, GzipIterator, ZipIterator
from iterator.Exceptions import FileIteratorException


def test_file_factory_plain(txt_file):
    assert isinstance(
        LocalFileIterator.get_iter(str(txt_file), 'plain'), 
        PlainIterator
    )

def test_file_factory_gzip(gzip_file):
    assert isinstance(
        LocalFileIterator.get_iter(str(gzip_file), 'gzip'), 
        GzipIterator
    )

def test_file_factory_zip(zip_file):
    assert isinstance(
        LocalFileIterator.get_iter(str(zip_file), 'zip'), 
        ZipIterator
    )

def test_file_factory_invalid_type(txt_file):
    with pytest.raises(FileIteratorException):
        LocalFileIterator.get_iter(str(txt_file), 'any')


class FileIter:
    
    @pytest.fixture
    def iter_imp(self):
        pass
    
    def test_lines_read_start(self, iter_imp):
        assert iter_imp.lines_read == 0
    
    def test_lines_read_next(self, iter_imp):
        for _ in range(5):
            next(iter_imp)
        assert iter_imp.lines_read == 5
    
    def test_lines_read_skip(self, iter_imp):
        iter_imp.skip_lines(5)
        assert iter_imp.lines_read == 5

    def test_natural_iteration(self, iter_imp):
        # "For loop behaviour."
        # for line in FileIter: pass
        it = iter(iter_imp)
        with pytest.raises(StopIteration):
            line = next(it)
            while line:
                line = next(it)

    def test_simplified_iteration(self, iter_imp):
        # Return None when file has been read.
        line = next(iter_imp)
        while line:
            line = next(iter_imp)
        assert line is None

    def test_copy_lines_read(self, iter_imp):
        for _ in range(5):
            next(iter_imp)
        copy = iter_imp.copy()
        assert copy.lines_read == iter_imp.lines_read

    def test_context_manager(self, iter_imp):
        with iter_imp as it:
            lines = [line for line in it]
        assert lines
    
    # def test_copy_has_same_events(self):
    #     pass


class TestPlainIter(FileIter):
    
    @pytest.fixture
    def iter_imp(self, plain_iter):
        yield plain_iter


class TestGzipIter(FileIter):
    
    @pytest.fixture
    def iter_imp(self, gzip_iter):
        yield gzip_iter


class TestZipIter(FileIter):
    
    @pytest.fixture
    def iter_imp(self, zip_iter):
        yield zip_iter