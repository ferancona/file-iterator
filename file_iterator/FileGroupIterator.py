from .Utils import ReadEvents, FileManager
from .FileIterator import FileIterator
from .Exceptions import FileIteratorException, ExceptionRaiser

from pathlib import Path


class FileGroupIterator:
    def __init__(self, filepaths):
        super().__init__()
        self.paths = []
        self._files = []
        self._files_iter = iter(self._files)
        self._ev = ReadEvents()
        if filepaths:
            for path in filepaths:
                self.add_iter_path(path)
        else:
            raise FileIteratorException('Please provide filepaths.')
        
        self._exhausted = False
        self._lines_accum = 0
        self._files_read = 0
        self._iter_file = None
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
        try:
            return self._iter.lines_read
        except AttributeError:
            # When _iter is None (start).
            return 0
    
    @property
    def files_read(self):
        return self._files_read
    
    @property
    def events(self):
        return self._ev
    
    def add_iter_path(self, path):
        iter_type = self.__iter_required(path)
        it = FileIterator.get_iter(path, iter_type)
        it.events.on_start_file_reading += self._ev.on_start_file_reading
        it.events.on_stop_file_reading += self._ev.on_stop_file_reading
        it.events.on_end_file_reached += self._ev.on_end_file_reached
        self._files.append(it)
        self.paths.append(it.path)
    
    def __next_file(self, next_=True):
        try:
            if self._iter_file and not self._exhausted:
                self._files_read += 1
                self._lines_accum += self.lines_read_file
            self._iter_file = next(self._files_iter)
            self._iter = iter(self._iter_file)
            if next_:
                return next(self)
        except StopIteration:
            self._exhausted = True
            self._lines_accum -= self.lines_read_file
            self._ev.on_end_reached()
            return None
    
    def __next__(self):
        try:
            return next(self._iter)
        except StopIteration:
            # Finished reading file.
            return self.__next_file()
        except TypeError:
            # First normal read.
            return self.__next_file()
    
    def __iter__(self):
        copy = self.copy()
        copy.events.on_end_reached += ExceptionRaiser(StopIteration).raise_ex
        return copy
    
    def copy(self):
        it = self.__class__(self.paths)
        if self.files_read > 0:
            it.skip_files(self.files_read)
        it._lines_accum = self._lines_accum
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
        # return True
    
    def close(self):
        files_left = len(self._files) - self.files_read
        self.skip_files(files_left)
    
    def skip_lines(self, num):
        for _ in range(num):
            next(self)
    
    def skip_files(self, num):
        closed = 0
        if not self._iter_file:
            # When skip_files() without any previous read.
            self.__next_file(next_=False)
        while closed < num and not self._exhausted:
            if self._iter_file:
                self._iter_file.close()
            closed += 1
            self.__next_file(next_=False)

    def __iter_required(self, path):
        if FileManager.is_gzipfile(path):
            return 'gzip'
        elif FileManager.is_zipfile(path):
            return 'zip'
        return 'plain'