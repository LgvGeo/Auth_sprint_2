import jwt
from fastapi import Depends

from db.redis_cache_storage import RedisCacheStorage, get_cache_storage
from settings.config import CommonSettings

SETTINGS = CommonSettings()


class TokenValidationError(Exception):
    pass


class PermissionDenied(Exception):
    pass


class JwtService:
    def __init__(self, cache_storage: RedisCacheStorage):
        self.cache_storage = cache_storage

    async def validate_access_token(self, token):
        try:
            payload = jwt.decode(
                token, SETTINGS.secret_key, algorithms=['HS256'])
            is_token_in_cache = await self.cache_storage.get_from_cache(token)
            if is_token_in_cache or payload['type'] != 'access':
                raise ValueError
        except Exception:
            raise TokenValidationError('error')

    async def get_token_payload(self, token):
        payload = jwt.decode(token, SETTINGS.secret_key, algorithms=['HS256'])
        return payload

    async def check_roles(self, token, roles: list[str]):
        user_roles = jwt.decode(
            token, SETTINGS.secret_key,
            algorithms=['HS256']
        )['roles']
        roles = set(roles)
        for role in user_roles:
            if role in roles:
                return
        raise PermissionDenied


def get_jwt_service(
        cache_storage: RedisCacheStorage = Depends(get_cache_storage)
):
    return JwtService(cache_storage)
