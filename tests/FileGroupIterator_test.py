import pytest
import gzip, zipfile, pathlib

from tests.FileIterator_test import FileIter


class TestGroupIter(FileIter):
    
    @pytest.fixture
    def iter_imp(self, group_iter):
        yield group_iter
    
    def test_files_read_start(self, iter_imp, names):
        assert iter_imp.curr_name == None

    def test_files_read_next(self, iter_imp, names, lines_no):
        next(iter_imp)
        assert iter_imp.curr_path == names[0]
    
    def test_lines_read_exhausted(self, iter_imp, lines_no, names):
        while next(iter_imp):
            pass
        assert iter_imp.lines_read == lines_no * len(names)
        
    def test_lines_read_skip_files(self, iter_imp):
        iter_imp.skip_files(1)
        assert iter_imp.lines_read == 0
        
    def test_lines_read_skip_all_file_lines(self, iter_imp, lines_no):
        iter_imp.skip_lines(lines_no + 1)
        assert iter_imp.lines_read == lines_no + 1
    
    def test_path_skip_lines(self, iter_imp, lines_no, names):
        iter_imp.skip_lines(lines_no + 1)
        assert iter_imp.curr_path == names[1]
        
    def test_path_skip_files(self, iter_imp, names):
        iter_imp.skip_files(1)
        assert iter_imp.curr_path == names[1]
        
    def test_path_skip_one_more(self, iter_imp, names):
        iter_imp.skip_files(len(names) + 1)
        assert iter_imp.curr_path == names[-1]
    
    def test_copy_lines_read_more_than_file(self, iter_imp, lines_no):
        for _ in range(lines_no + 1):
            next(iter_imp)
        copy = iter_imp.copy()
        assert copy.lines_read == iter_imp.lines_read
        
    def test_copy_files_read_more_than_file(self, iter_imp, lines_no):
        for _ in range(lines_no + 1):
            next(iter_imp)
        copy = iter_imp.copy()
        assert copy.files_read == iter_imp.files_read
    
    def test_copy_lines_read_more_than_all(self, iter_imp, lines_no, names):
        while next(iter_imp):
            pass
        copy = iter_imp.copy()
        assert copy.lines_read == iter_imp.lines_read
        
    def test_copy_files_read_more_than_all(self, iter_imp, lines_no, names):
        while next(iter_imp):
            pass
        copy = iter_imp.copy()
        assert copy.files_read == iter_imp.files_read
    
    def test_copy_same_next_line_next_file(self, iter_imp, lines_no):
        for _ in range(lines_no + 1):
            next(iter_imp)
        copy = iter_imp.copy()
        assert next(copy) == next(iter_imp)
    
    def test_context_manager_lines_read(self, iter_imp, lines_no, names):
        with iter_imp as it:
            while next(it):
                pass
        assert it.lines_read == lines_no * len(names)