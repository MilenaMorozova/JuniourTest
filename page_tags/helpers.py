from django.http import HttpResponseBadRequest, HttpResponseServerError


def request_type(request_method):
    def decorator(func):
        def wrap(request, **kwargs):
            if request_method != request.method:
                return HttpResponseBadRequest(f"Only {request_method} method supported")

            return func(request, **kwargs)
        return wrap
    return decorator


def catch_view_exception(func):
    def wrap(request, **kwargs):
        try:
            return func(request, **kwargs)
        except Exception as e:
            return HttpResponseServerError(e)
    return wrap
