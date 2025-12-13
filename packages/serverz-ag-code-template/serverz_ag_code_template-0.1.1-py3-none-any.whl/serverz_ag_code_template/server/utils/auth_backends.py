# auth_backends.py
from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend

from .user_manager import SECRET # 从 user_manager 引入 SECRET

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)  # JWT有效期1小时

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
