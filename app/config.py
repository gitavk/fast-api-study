from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int
    db_name: str
    db_password: str
    db_user: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
