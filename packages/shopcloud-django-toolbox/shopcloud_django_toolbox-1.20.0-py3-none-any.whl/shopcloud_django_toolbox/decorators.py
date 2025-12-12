from functools import wraps
from typing import Optional

from django.http import HttpResponseForbidden
from django.middleware.http import ConditionalGetMiddleware
from django.utils.decorators import decorator_from_middleware

from . import signer

conditional_page = decorator_from_middleware(ConditionalGetMiddleware)


def require_toolbox_sign(needed_keys: Optional[list] = None):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):

            is_valid, data = signer.loads_from_request(request)
            if not is_valid:
                return HttpResponseForbidden("sign is not valid")
            if isinstance(needed_keys, list):
                for key in needed_keys:
                    if key not in data:
                        return HttpResponseForbidden(f"key '{key}' not in sign")
            return func(request, *args, **kwargs)

        return inner

    return decorator
