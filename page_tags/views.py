from django.http import (
    HttpResponse, JsonResponse, HttpResponseNotFound
)
from django.views.decorators.csrf import csrf_exempt

from .page_backend import PageBackend
from .helpers import request_type, catch_view_exception
from .exceptions import PageTagsException

page_backend = PageBackend()


@csrf_exempt
@catch_view_exception
@request_type('POST')
def add_page_info(request, **kwargs):
    try:
        page_id, tags = page_backend.get_page_tags(request.POST['url'])
    except KeyError:
        return HttpResponseNotFound('No URL')
    except PageTagsException as e:
        return HttpResponse(status=e.status_code)

    result = {tag: len(tags[tag]) for tag in tags if tag != 'a'}
    result['a'] = tags['a']
    result['page_id'] = page_id
    return JsonResponse(result)


@csrf_exempt
@catch_view_exception
@request_type('GET')
def get_page_info(request, **kwargs):
    try:
        tags = page_backend.get_page_tags_by_id(kwargs['object_id'])
        tags['page_id'] = kwargs['object_id']
        return JsonResponse(tags)
    except KeyError:
        return HttpResponseNotFound
    except PageTagsException as e:
        return HttpResponse(status=e.status_code)
