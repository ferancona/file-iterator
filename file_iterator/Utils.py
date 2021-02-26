import events
import gzip, zipfile


class ReadEvents(events.Events):
    __events__ = ('on_start_file_reading', 'on_stop_file_reading', 
                  'on_end_file_reached', 'on_end_reached')

    file_events = ('on_start_file_reading', 'on_stop_file_reading', 
                'on_end_file_reached')

    def copy(self, omit=None):
        # Copy callable attributes.
        copy = self.__class__()
        for attr in dir(self):
            if not attr.startswith('__'):
                if callable(getattr(self, attr)):
                    if getattr(self, attr) not in omit:
                        setattr(copy, attr, 
                                getattr(self, attr).copy(omit)
                        )
        return copy


class Read_EventSlot(events.events._EventSlot):
    def copy(self, omit=None):
        copy = self.__class__()
        omit = set(omit) if omit else set()
        for target in self.targets:
            if target not in omit:
                copy.targets.append(target)
        copy.__name__ = self.__name__
        return copy


class FileManager:
    @classmethod
    def is_gzipfile(cls, filepath):
        # First bytes of gzip files are: 1f8b.
        FIRST_BYTES = '1f8b'
        bytes_read = open(filepath, 'rb').read(2)
        return bytes_read.hex() == FIRST_BYTES

    @classmethod
    def is_zipfile(cls, filepath):
        return zipfile.is_zipfile(filepath)