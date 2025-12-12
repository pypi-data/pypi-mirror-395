# middleware/Authentication_middleware.py
from fastmcp import Context
class AuthMiddleware:
    async def __call__(self, context: Context, call_next):
        client_env = context or {}
        # context.metadata = {
        #     "api_key": client_env.get("API_KEY"),
        #     "secret_key": client_env.get("SECRET_KEY"),
        #     "base_url": client_env.get("BASE_URL"),
        #     "zone_uuid": client_env.get("ZONE_UUID"),
        # }

        return await call_next(context)
