from io import StringIO

from django.core.management import call_command
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET


@require_GET
def security_txt(request):
    """
    securit.tyt

    ---

    add to the path
    path(".well-known/security.txt", core_views.security_txt),
    """
    lines = [
        "Contact: mailto:security@talk-point.de",
        "Expires: 2027-01-01T00:00:00.000Z",
        "Preferred-Languages: de, en"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
def health(request):
    return JsonResponse({'status': 'ok'})


@csrf_exempt
def management_db_migrate(request):
    if request.method == 'POST':
        out = StringIO()
        call_command('migrate', stdout=out)
        return JsonResponse({'status': 'ok', 'out': out.getvalue()})
    elif request.method == 'GET':
        out = StringIO()
        call_command('showmigrations', '-p', stdout=out)
        return JsonResponse({'status': 'ok', 'out': out.getvalue()})
