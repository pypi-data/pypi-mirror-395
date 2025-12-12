from rest_framework.status import HTTP_400_BAD_REQUEST


class IsapiException(Exception):
    pass


class PermissionDenied(IsapiException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'{self.message}'


class CreationError(IsapiException):
    pass


class RequestError(IsapiException):
    def __init__(self, message, status=None):
        self.status = status or HTTP_400_BAD_REQUEST
        self.message = message

    def __str__(self):
        return f'{self.message}'


class ProcessError(IsapiException):
    def __init__(self, instance):
        self.instance = instance


class TraspasarArticuloError(ProcessError):
    def __init__(self, instance, *args, **kwargs):
        super().__init__(instance)
        self.kwargs = kwargs
        self.args = args
