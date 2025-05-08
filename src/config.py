from pydantic_settings import BaseSettings

class Config(BaseSettings):
    SECRET_KEY: str
    SECRET_ALGORITEM: str

    @property
    def JWT_SECRET(self):
        return self.SECRET_KEY

    @property
    def JWT_ALGORITHM(self):
        return self.SECRET_ALGORITEM

    @property
    def REDIS_HOST(self):
        return getattr(self, "redis_host", None)

    @property
    def REDIS_PORT(self):
        return int(getattr(self, "redis_port", 6379))

    class Config:
        env_file = ".env"
        extra = "allow"

Config = Config()