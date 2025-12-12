from django.conf import settings
from django.utils.module_loading import import_string


def get_request_content_function():
    try:
        get_request_content = import_string(settings.GET_REQUEST_CONTENT_FUNCTION)
    except Exception:
        from isapilib.logger.logging import get_request_content

    return get_request_content


def get_response_content_function():
    try:
        get_response_content = import_string(settings.GET_RESPONSE_CONTENT_FUNCTION)
    except Exception:
        from isapilib.logger.logging import get_response_content

    return get_response_content


def get_insert_log_function():
    try:
        insert_log = import_string(settings.INSERT_LOG_FUNCTION)
    except Exception:
        from isapilib.logger.utilities import insert_log

    return insert_log


def get_safe_method_function():
    try:
        safe_method = import_string(settings.SAFE_METHOD_FUNCTION)
    except Exception:
        from isapilib.core.decorators import safe_method

    return safe_method
