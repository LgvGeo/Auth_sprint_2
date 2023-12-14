import datetime
import logging
from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from redis.asyncio import Redis
from uvicorn.workers import UvicornWorker

from api.v1 import roles, users
from db import redis
from db.redis import get_redis
from settings import config
from settings.logger import LOGGING


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_conf = config.RedisSettings()
    redis.redis = Redis(host=redis_conf.host, port=redis_conf.port)
    yield
    await redis.redis.close()


app = FastAPI(
    title=config.CommonSettings().project_name,
    docs_url='/api/auth/docs/openapi',
    openapi_url='/api/auth/docs/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


@app.middleware('http')
async def check_rate_limit(request: Request, call_next):
    common_settings = config.CommonSettings()
    host = request.headers.get('Host')
    redis_conn = await get_redis()
    pipe = redis_conn.pipeline()
    now = datetime.datetime.now()
    key = f'{host}:{now.minute}'
    pipe.incr(key, 1)
    pipe.expire(key, 59)
    result = await pipe.execute()
    request_number = result[0]
    if request_number > common_settings.request_rate_limit:
        return Response(
            'request num exceeded',
            HTTPStatus.TOO_MANY_REQUESTS
        )
    response = await call_next(request)
    return response


@app.middleware('http')
async def before_request(request: Request, call_next):
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return ORJSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={'detail': 'X-Request-Id is required'}
        )
    request_id = request.headers.get('X-Request-Id')
    tracer = trace.get_tracer(__name__)
    span = tracer.start_span(str(request.url))
    span.set_attribute('http.request_id', request_id)
    span.end()
    response = await call_next(request)
    return response


def configure_tracer() -> None:
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: 'auth'})
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name='jaeger',
                agent_port=6831,
            )
        )
    )


configure_tracer()
FastAPIInstrumentor.instrument_app(app)

app.include_router(users.router, prefix='/api/v1/users', tags=['users'])
app.include_router(roles.router, prefix='/api/v1/roles', tags=['roles'])


class CustomUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        'log_config': LOGGING,
        'log_level': logging.DEBUG
    }
