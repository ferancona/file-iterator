import events
import gzip, zipfile


class ReadEvents(events.Events):
    __events__ = ('on_start_file_reading', 'on_stop_file_reading', 
                  'on_end_file_reached', 'on_end_reached')

    @property
    def file_events(self):
        return ('on_start_file_reading', 'on_stop_file_reading', 
                'on_end_file_reached')


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