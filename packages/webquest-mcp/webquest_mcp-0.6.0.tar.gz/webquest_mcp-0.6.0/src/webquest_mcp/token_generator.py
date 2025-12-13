from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from pydantic import Field, PositiveInt, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    auth_secret: SecretStr = Field(default=...)
    auth_audience: str = Field(default="webquest-mcp")
    auth_expiration_days: PositiveInt = Field(default=365)
    auth_subject: str = Field(default=...)


def main() -> None:
    load_dotenv()

    settings = Settings()
    secret = settings.auth_secret.get_secret_value()

    delta = timedelta(days=settings.auth_expiration_days)
    expiration_days = datetime.now(timezone.utc) + delta

    payload = {
        "aud": settings.auth_audience,
        "exp": expiration_days,
        "sub": settings.auth_subject,
    }

    token = jwt.encode(payload, secret, algorithm="HS256")
    print(f"Generated token:\n{token}\n")
    print("You can provide this token to your MCP client.")


if __name__ == "__main__":
    main()
