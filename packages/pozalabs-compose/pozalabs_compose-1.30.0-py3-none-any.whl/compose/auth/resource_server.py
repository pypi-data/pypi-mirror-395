import abc

from . import vo


class ResourceServer(abc.ABC):
    @abc.abstractmethod
    def get_resource(self, access_token: str) -> vo.UserResource:
        raise NotImplementedError
