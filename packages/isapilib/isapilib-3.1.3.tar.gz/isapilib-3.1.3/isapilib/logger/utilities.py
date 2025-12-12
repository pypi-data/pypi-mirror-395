import json
from datetime import timezone, datetime

from django.conf import settings

from isapilib.api.models import ApiLogs
from isapilib.core.get_functions import get_request_content_function, get_response_content_function
from isapilib.core.utilities import is_test

get_request_content = get_request_content_function()
get_response_content = get_response_content_function()

force_insert = getattr(settings, 'FORCE_INSERT_LOGS', False)


def insert_log(request, response, interfaz, tipo, time=0):
    if is_test() and not force_insert: return
    try:
        log = ApiLogs()
        log.user_id = getattr(request.user, 'pk', None)
        log.tipo = str(tipo or '')
        log.header = str(json.dumps(dict(request.headers)))
        log.request = get_request_content(request)
        log.response = get_response_content(request, response)
        log.status = response.status_code
        log.url = request.build_absolute_uri()
        log.interfaz = str(interfaz or '')
        log.response_time = time
        log.fecharegistro = datetime.now(tz=timezone.utc)
        log.save(using='default')
    except Exception as e:
        print(f'Warning: Failed to save logs, ({type(e)}) {e}')
