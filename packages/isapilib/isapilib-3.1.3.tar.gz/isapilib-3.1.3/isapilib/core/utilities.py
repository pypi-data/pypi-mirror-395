import sys

from django.conf import settings


def get_default_user():
    return getattr(settings, 'INTELISIS_USER', 'SOPDESA')


def get_dealer_field():
    return getattr(settings, 'DEALER_FIELD', 'dealerID')


def to_bool(s):
    if isinstance(s, bool):
        return s
    if isinstance(s, str):
        s = s.lower()
        if s in ['true', '1', 'yes']:
            return True
        elif s in ['false', '0', 'no']:
            return False
        else:
            return False
    return False


def get_sucursal_from_request(request):
    try:
        return request.user.branch.sucursal
    except Exception as e:
        return 0


def is_test():
    return sys.argv[1] == 'test'
