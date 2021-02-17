class FileIteratorException(Exception):
    pass


class ExceptionRaiser:
    def __init__(self, exception):
        super().__init__()
        self.ex = exception
    def raise_ex(self):
        raise self.ex