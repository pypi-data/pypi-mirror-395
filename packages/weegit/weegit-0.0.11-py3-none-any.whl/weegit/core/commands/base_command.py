from abc import abstractmethod


class BaseCommand:
    @abstractmethod
    def do(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    def undo(self, *args, **kwargs):
        raise NotImplemented
