from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy

#Печенье
cookie_transport = CookieTransport(cookie_name="TuneON", cookie_max_age=3600)


#Секрет, никому не рассказывайте
SECRET = "SECRET"

#Срок годности печенья
def get_jwt_strategy() -> JWTStrategy:
    #Да, я у мамы стратег
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

#Печенье упаковано
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

