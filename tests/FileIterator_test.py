import pytest
import gzip, zipfile, pathlib

from file_iterator.FileIterator import FileIterator, \
    PlainIterator, GzipIterator, ZipIterator
from file_iterator.Exceptions import FileIteratorException


def is_instance(path, type_, class_):
    return isinstance(
        FileIterator.get_iter(str(path), type_), 
        class_
    )

def test_file_factory_plain(txt_file):
    assert is_instance(txt_file, 'plain', PlainIterator)

def test_file_factory_gzip(gzip_file):
    assert is_instance(gzip_file, 'gzip', GzipIterator)

def test_file_factory_zip(zip_file):
    assert is_instance(zip_file, 'zip', ZipIterator)

def test_file_factory_invalid_type(txt_file):
    with pytest.raises(FileIteratorException):
        FileIterator.get_iter(str(txt_file), 'any')


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
    
    def test_lines_read_exhausted(self, iter_imp, lines_no):
        while next(iter_imp):
            pass
        assert iter_imp.lines_read == lines_no

    def test_natural_iteration(self, iter_imp):
        # "For loop behaviour."
        # for line in iter_imp: pass
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
    
    def test_non_exhausted_for_iteration(self, iter_imp):
        for line in iter_imp:
            pass
        assert iter_imp.lines_read == 0

    def test_copy_lines_read(self, iter_imp):
        for _ in range(5):
            next(iter_imp)
        copy = iter_imp.copy()
        assert copy.lines_read == iter_imp.lines_read
        
    def test_copy_same_next_line(self, iter_imp):
        for _ in range(5):
            next(iter_imp)
        copy = iter_imp.copy()
        assert next(copy) == next(iter_imp)

    def test_context_manager_lines_read(self, iter_imp, lines_no):
        with iter_imp as it:
            while next(it):
                pass
        assert it.lines_read == lines_no
    
    # def test_copy_has_same_events(self):
    #     pass


class TestPlainIter(FileIter):
    
    @pytest.fixture
    def iter_imp(self, plain_iter):
        yield plain_iter
    
    def test_file_name(self, plain_iter, name_txt):
        assert plain_iter.name == name_txt


class TestGzipIter(FileIter):
    
    @pytest.fixture
    def iter_imp(self, gzip_iter):
        yield gzip_iter
    
    def test_file_name(self, gzip_iter, name_gzip):
        assert gzip_iter.name == name_gzip


class TestZipIter(FileIter):
    
    @pytest.fixture
    def iter_imp(self, zip_iter):
        yield zip_iter
    
    def test_file_name(self, zip_iter, name_zip):
        assert zip_iter.name == name_zip