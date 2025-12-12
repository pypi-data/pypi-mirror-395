import json


def get_request_content(request):
    try:
        if hasattr(request, 'data'):
            if isinstance(request.data, str):
                return request.data

            if isinstance(request.data, (dict, list)):
                return json.dumps(request.data, ensure_ascii=False)
    except Exception as e:
        msg = f'Warning: Failed to get request content, ({type(e)}) {e}'
        print(msg)
        return msg


def get_response_content(request, response):
    try:
        if hasattr(response, 'data'):
            try:
                return response.rendered_content.decode("utf-8", errors="replace")
            except AssertionError:
                response.accepted_renderer = request.accepted_renderer
                response.accepted_media_type = request.accepted_media_type
                response.renderer_context = {'view': None, 'args': (), 'kwargs': {}, 'request': request}

                return response.rendered_content.decode("utf-8", errors="replace")

        return response.content.decode('utf-8')
    except Exception as e:
        msg = f'Warning: Failed to get response content, ({type(e)}) {e}'
        print(msg)
        return msg


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
