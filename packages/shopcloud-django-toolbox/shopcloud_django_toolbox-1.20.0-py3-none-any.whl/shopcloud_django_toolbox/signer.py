from datetime import timedelta
from typing import Dict, Optional, Tuple

from django.conf import settings
from django.core import signing
from django.http import HttpRequest
from django.utils import dateparse, timezone

DJ_TOOLBOX_SIGNER_SETTINGS = getattr(settings, 'DJ_TOOLBOX_SIGNER', {
    'VERSION': "1",
})
if DJ_TOOLBOX_SIGNER_SETTINGS is None:
    DJ_TOOLBOX_SIGNER_SETTINGS = {}
VERSION = DJ_TOOLBOX_SIGNER_SETTINGS.get('VERSION', '1')


def represent_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def dumps(data: dict, **kwargs) -> Tuple[Optional[str], dict]:
    expire_in_hours = kwargs.get('expire_in_hours')
    if expire_in_hours is None:
        expire_in_hours = 12

    if not represent_int(expire_in_hours):
        raise ValueError('expire_in_hours is not a valid number')
    expire_in_hours = int(expire_in_hours)

    if kwargs.get('check_max_expired_in_hours', True):
        if expire_in_hours > 14 * 24:
            return None, {
                'errors': {
                    'expire_in_hours': 'expire_in_hours is to high'
                }
            }

    version_need = kwargs.get('version', VERSION)
    if version_need is None:
        version_need = VERSION
    data.update({
        "expire_at": (timezone.now() + timedelta(hours=expire_in_hours)).isoformat(),
        "v": VERSION
    })

    return signing.dumps(data, key=kwargs.get("key")), {}


def loads(value: str, **kwargs) -> Tuple[bool, dict]:
    version_need = kwargs.get('version', VERSION)
    if version_need is None:
        version_need = VERSION
    try:
        data = signing.loads(value, key=kwargs.get("key"))
    except Exception:
        return False, {
            'errors': {
                'sign': 'error by decode',
            }
        }

    version = data.pop("v", None)
    expire_at = data.pop("expire_at", None)

    if version is None:
        return False, {
            'errors': {
                'sign.v': 'is empyt',
            }
        }
    if version != version_need:
        return False, {
            'errors': {
                'sign.v': 'has wrong version',
            }
        }
    if expire_at is None:
        return False, {
            'errors': {
                'sign.expired_at': 'is empty',
            }
        }
    try:
        expire_at = dateparse.parse_datetime(expire_at)
    except Exception:
        return False, {
            'errors': {
                'sign.expired_at': 'can not parsed, wrong format',
            }
        }
    if expire_at < timezone.now():
        return False, {
            'errors': {
                'sign.expired_at': 'is to old',
            }
        }
    return True, data


def loads_from_request(request: HttpRequest, **kwargs) -> Tuple[bool, dict]:
    version_need = kwargs.get('version', VERSION)
    if version_need is None:
        version_need = VERSION
    value = request.GET.get("sign")
    if value is None:
        return False, {
            'errors': {
                'sign': 'is empty',
            }
        }
    if value.strip() == "":
        return False, {
            'errors': {
                'sign': 'is empty',
            }
        }
    return loads(value, key=kwargs.get("key"), version=version_need)
