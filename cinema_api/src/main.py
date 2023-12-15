import datetime
import logging
from contextlib import asynccontextmanager
from http import HTTPStatus

from elasticsearch import AsyncElasticsearch
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

from api.v1 import films, genres, persons
from db import elastic, redis
from db.redis import get_redis
from settings import config
from settings.logger import LOGGING


COMMON_SETTINGS = config.CommonSettings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    elstic_conf = config.ElasticsearchSettings()
    redis_conf = config.RedisSettings()
    elastic.es = AsyncElasticsearch(
        hosts=[f'{elstic_conf.host}:{elstic_conf.port}']
    )
    redis.redis = Redis(host=redis_conf.host, port=redis_conf.port)
    yield
    await elastic.es.close()
    await redis.redis.close()


app = FastAPI(
    title=COMMON_SETTINGS.project_name,
    docs_url='/api/cinema/docs/openapi',
    openapi_url='/api/cinema/docs/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


@app.middleware('http')
async def check_rate_limit(request: Request, call_next):
    host = request.headers.get('Host')
    redis_conn = await get_redis()
    pipe = redis_conn.pipeline()
    now = datetime.datetime.now()
    key = f'{host}:{now.minute}'
    pipe.incr(key, 1)
    pipe.expire(key, 59)
    result = await pipe.execute()
    request_number = result[0]
    if request_number > COMMON_SETTINGS.request_rate_limit:
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
    jaegrer_settings = config.JaegerSettings()
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: 'cinema'})
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=jaegrer_settings.host,
                agent_port=jaegrer_settings.port,
            )
        )
    )


if COMMON_SETTINGS.enable_tracer:
    configure_tracer()
FastAPIInstrumentor.instrument_app(app)

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])


class CustomUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "log_config": LOGGING,
        "log_level": logging.DEBUG
    }
