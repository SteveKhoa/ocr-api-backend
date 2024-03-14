import datetime
import jose.jwt
from jose import JWTError, ExpiredSignatureError
import app._exceptions
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
DEFAULT_TOKEN_EXPIRE_MINUTES = 5  # 5 minutes
ALGORITHM = "HS256"


def create_id_token(
    authentication_data: dict,
    expires_delta: datetime.timedelta | None = None,
    server_secret_key: str = SECRET_KEY,
    jwt_algorithm: str = ALGORITHM,
    default_expiration_minutes: float = DEFAULT_TOKEN_EXPIRE_MINUTES,
):
    """
    Create Authentication JSON Web Token for payload `authentication_data`.
    The result is of type `str`.

    Default expiration is `exp=5` (minutes).
    """
    payload = authentication_data.copy()

    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=default_expiration_minutes
        )

    payload.update({"exp": expire})
    encoded_jwt = jose.jwt.encode(payload, server_secret_key, jwt_algorithm)

    return encoded_jwt


def verify_id_token(
    authentication_jwt: str,
    server_secret_key: str = SECRET_KEY,
    jwt_algorithm: str = ALGORITHM,
) -> dict:
    """
    Verify access_token `jwt` and extract payload out of the token.

    ## Returns
    `dict`: dictionary of data in the payload

    ## Raises
    - HTTP `InvalidJWTSignature` upon invalid or expired signature
    - HTTP `UndefinedJWTError` upon undefined token verification error
    """
    try:
        decoded_payload = jose.jwt.decode(
            authentication_jwt, server_secret_key, algorithms=[jwt_algorithm]
        )
    except JWTError:
        raise app._exceptions.InvalidJWTSignature()
    except:
        raise app._exceptions.UndefinedJWTError(
            "Undefined error occured during token verification."
        )

    return decoded_payload


def create_access_token():
    raise NotImplementedError()


def verify_access_token():
    raise NotImplementedError()
