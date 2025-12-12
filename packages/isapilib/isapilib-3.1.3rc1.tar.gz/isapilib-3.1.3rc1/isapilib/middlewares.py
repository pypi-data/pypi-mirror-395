import io
import sys
import time

from django.conf import settings
from django.http import HttpResponse

from isapilib.auth.permissions import IsapilibPermission
from isapilib.core.exceptions import IsapiException
from isapilib.core.get_functions import get_insert_log_function, get_safe_method_function

insert_log = get_insert_log_function()
safe_method = get_safe_method_function()


class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = safe_method(get_response)
        self.interfaz = getattr(settings, 'INTERFAZ_NAME', '')
        self.exc = safe_method(self.launch_exception)

    def __call__(self, base_request):
        start = time.time()
        response = self.get_response(base_request)
        end = time.time()

        try:
            request = IsapilibPermission.get_current_request()
        except IsapiException:
            return response

        resolver_match = getattr(request, 'resolver_match', None)

        if resolver_match is None:
            raise IsapiException(
                'Request is not available in thread-local context. '
                'Make sure IsapilibPermission is set either in DEFAULT_PERMISSION_CLASSES '
                'or included in the view\'s permission_classes.'
            )

        try:
            view_class = resolver_match.func.view_class
        except AttributeError:
            view_class = resolver_match.func.cls

        view_name = getattr(view_class, 'log_name', view_class.__name__)

        if view_name.endswith('View'):
            view_name = view_name[:-len('View')]
        elif view_name.endswith('ViewSet'):
            view_name = view_name[:-len('ViewSet')]

        response_time = (end - start) * 1000

        insert_log(
            request=request,
            response=response,
            interfaz=self.interfaz,
            tipo=f'{view_name} {base_request.method}',
            time=response_time,
        )

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        request._middleware_renderer_context = {
            'request': request,
            'view': view_func,
            'args': view_args,
            'kwargs': view_kwargs,
        }

    def process_exception(self, _, exception):
        try:
            request = IsapilibPermission.get_current_request()
        except IsapiException:
            raise exception

        response = self.exc(exception)

        response.accepted_renderer = request.accepted_renderer
        response.accepted_media_type = request.accepted_media_type

        response.renderer_context = getattr(request, '_middleware_renderer_context', {})

        return HttpResponse(
            response.rendered_content,
            status=response.status_code,
            content_type='application/json',
        )

    @staticmethod
    def launch_exception(e):
        raise e


class ChunkedMiddleware:
    def __init__(self, get_response):
        development = any(arg for arg in sys.argv if "manage.py" in arg)
        support = any(s in arg for arg in sys.argv for s in ("uvicorn", "hypercorn", "daphne"))

        if not support and not development:
            raise Exception('Chunked request not supported. Use a server that handles Transfer-Encoding.')

        self.get_response = get_response

    def __call__(self, request):
        has_transfer_encoding = 'Transfer-Encoding' in request.headers
        transfer_encoding = request.headers.get('Transfer-Encoding')

        if has_transfer_encoding and transfer_encoding == 'chunked':
            content_length = request.META.get('CONTENT_LENGTH')
            if content_length in (None, '0'):
                request.META['CONTENT_LENGTH'] = str(len(request.body))
                request._stream = io.BytesIO(request.body)

        response = self.get_response(request)
        return response
