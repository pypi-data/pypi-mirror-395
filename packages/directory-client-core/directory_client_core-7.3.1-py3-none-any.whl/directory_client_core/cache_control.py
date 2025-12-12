import abc


class AbstractCacheControl(abc.ABC):

    def __init__(self, value):
        self.value = value

    @property
    @abc.abstractmethod
    def header_name(self):
        return ''

    @property
    def headers(self):
        return {
            self.header_name: self.value
        }


class ETagCacheControl(AbstractCacheControl):
    header_name = 'If-None-Match'
