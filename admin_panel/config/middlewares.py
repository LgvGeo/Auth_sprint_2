import datetime
from http import HTTPStatus

from django.http import HttpResponse
from django_redis import get_redis_connection

from config.settings import REQUEST_RATE_LIMIT


class LimitRateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.headers.get('Host')
        redis_conn = get_redis_connection()
        pipe = redis_conn.pipeline()
        now = datetime.datetime.now()
        key = f'{host}:{now.minute}'
        pipe.incr(key, 1)
        pipe.expire(key, 59)
        result = pipe.execute()
        request_number = result[0]
        if request_number > REQUEST_RATE_LIMIT:
            response = HttpResponse('request num exceeded')
            response.status_code = HTTPStatus.TOO_MANY_REQUESTS
            return response

        response = self.get_response(request)
        return response
