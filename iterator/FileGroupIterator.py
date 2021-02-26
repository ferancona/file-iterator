from .Utils import ReadEvents, FileManager
from .FileIterator import LocalFileIterator
from .Exceptions import FileIteratorException, ExceptionRaiser

from pathlib import Path


class FileGroupIterator:
    def __init__(self, filepaths):
        super().__init__()
        self.paths = []
        self._files = []
        self._files_iter = iter(self._files)
        if filepaths:
            for path in filepaths:
                self.add_iter_path(path)
        else:
            raise FileIteratorException('Please provide filepaths.')
        self._ev = ReadEvents()
        
        self._exhausted = False
        self._lines_accum = 0
        self._files_read = 0
        self._file_iter = None
        self._iter = None
    
    @property
    def curr_name(self):
        try:
            return self._iter.name
        except: return None
    
    @property
    def curr_path(self):
        try:
            return self._iter.path
        except: return None
    
    @property
    def lines_read(self):
        return self._lines_accum + self.lines_read_file
    
    @property
    def lines_read_file(self):
        return self._iter.lines_read
    
    @property
    def files_read(self):
        return self._files_read
    
    @property
    def events(self):
        return self._ev
    
    def add_iter_path(self, path):
        iter_type = self.__iter_required(path)
        it = LocalFileIterator.get_iter(path, iter_type)
        it.events.on_start_reading += self._ev.on_start_file_reading
        it.events.on_stop_reading += self._ev.on_stop_file_reading
        it.events.on_end_file_reached += self._ev.on_end_file_reached
        self._files.append(it)
        self.paths += it.path
    
    def __next_file(self, next_=True):
        try:
            if not self._exhausted:
                self._files_read += 1
                self._lines_accum += self.lines_read_file
            self._file_iter = next(self._files_iter)
            self._iter = iter(self._file_iter)
            if next_:
                return next(self)
        except StopIteration:
            self._exhausted = True
            self._ev.on_end_reached()
            return None
    
    def __next__(self):
        try:
            return next(self._iter)
        except StopIteration:
            # Finished reading file.
            return self.__next_file()
        except TypeError:
            # First read.
            return self.__next_file()
    
    def __iter__(self):
        copy = self.copy()
        copy.events.on_end_reached += ExceptionRaiser(StopIteration).raise_ex
        return copy
    
    def copy(self):
        it = self.__class__(self.paths)
        if self.files_read > 0:
            it.skip_files(self.files_read)
        if self.lines_read_file > 0:
            it.skip_lines(self.lines_read_file)
        
        it.events.on_start_file_reading += self._ev.on_start_file_reading
        it.events.on_stop_file_reading += self._ev.on_stop_file_reading
        it.events.on_end_file_reached += self._ev.on_end_file_reached
        it.events.on_end_reached += self._ev.on_end_reached
        return it
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.close()
        return True
    
    def close(self):
        files_left = len(self._files) - self.files_read
        self.skip_files(files_left)
    
    def skip_lines(self, num):
        for _ in range(num):
            next(self)
    
    def skip_files(self, num):
        closed = 0
        while closed < num and not self._exhausted:
            if self._file_iter:
                self._file_iter.close()
            closed += 1
            self.__next_file(next_=False)

    def __iter_required(self, path):
        if FileManager.is_gzipfile(path):
            return 'gzip'
        elif FileManager.is_zipfile(path):
            return 'zip'
        return 'plain'


def test():
    file_lst = [
        'test.txt', 
        'test.txt.gz', 
        'test.zip'
    ]
    
    group_iter = FileGroupIterator(file_lst)
    for line in group_iter:
        # Do something with line.
        pass
    
    with FileGroupIterator(file_lst) as group_iter:
        # Do something with line.
        pass