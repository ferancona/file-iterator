from .Utils import ReadEvents
from .Exceptions import FileIteratorException, ExceptionRaiser

import gzip, zipfile
from abc import ABC, abstractmethod
from pathlib import Path


class FileIterator(ABC):
    """
    Encapsulates the core of iteration logic and event firing.
    The class LocalFileIterator exists mainly for 2 reasons:
        - To provide unified iteration interface for different file types. 
        - To trigger events at specific points in time.
    """
    def __init__(self, name):
        super().__init__()
        if name:
            p = Path(name).resolve()
            self.name = p.name
            self.path = str(p)
        else:
            raise FileIteratorException(
                'Please provide a filename or filepath.'
            )
        self._ev = ReadEvents(ReadEvents.file_events)
        self._ev.on_end_file_reached += self.close
        
        self._lines_read = 0
        self._file = None
        self._iter = None
        
    # Factory Method.
    @classmethod
    def get_iter(cls, filepath, kind='plain'):
        if kind == 'plain':
            return PlainIterator(filepath)
        elif kind == 'zip':
            return ZipIterator(filepath)
        elif kind == 'gzip':
            return GzipIterator(filepath)
        else:
            raise FileIteratorException(
                'Please provide a valid kind (plain, zip or gzip).'
            )
        
    @property
    def lines_read(self):
        return self._lines_read

    @property
    def events(self):
        return self._ev
    
    @abstractmethod
    def _open(self):
        self._iter = iter(self._file)
        self._ev.on_start_file_reading()
    
    def __next__(self):
        try: 
            self._lines_read += 1
            return next(self._iter)
        except StopIteration:
            self._lines_read -= 1
            self._ev.on_end_file_reached()
            return None
        except TypeError:
            # First read.
            self._lines_read -= 1
            self._open()
            return next(self)
        except ValueError:
            # Read a closed file (when done).
            return None
    
    def __iter__(self):
        it = self.copy()
        it.events.on_end_file_reached += ExceptionRaiser(StopIteration).raise_ex
        return it
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.close()
        return True
    
    def copy(self):
        copy = self.__class__(self.name)
        if self.lines_read > 0:
            copy._open()
            copy._file.seek(self._file.tell())
            copy._lines_read = self._lines_read
        copy.events.on_start_file_reading += self._ev.on_start_file_reading
        copy.events.on_stop_file_reading += self._ev.on_stop_file_reading
        copy.events.on_end_file_reached += self._ev.on_end_file_reached
        return copy
    
    def skip_lines(self, num):
        for _ in range(num):
            next(self)
    
    def close(self):
        if self._file:
            self._file.close()
            self._ev.on_stop_file_reading()
        
    @classmethod
    def copy_iter(cls, iterator):
        return iterator.copy()


class PlainIterator(FileIterator):
    def __init__(self, name):
        super().__init__(name)
        
    def _open(self):
        self._file = open(self.path, 'rb')
        super()._open()


class GzipIterator(FileIterator):
    def __init__(self, name):
        super().__init__(name)
    
    def _open(self):
        self._file = gzip.open(self.path, 'rb')
        super()._open()


class ZipIterator(FileIterator):
    def __init__(self, name):
        super().__init__(name)
        
    def _open(self):
        self.__zip = zipfile.ZipFile(self.path)
        self._file = self.__zip.open(self.__zip.namelist()[0])
        super()._open()