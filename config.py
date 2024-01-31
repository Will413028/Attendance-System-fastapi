from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 60
    environment: str
    instance_connection_name :str
    db_user: str
    db_pass: str
    db_name: str
    workday_cut_off_time: str

    class Config:
        env_file = ".env"
