from pydantic import BaseSettings

class Settings(BaseSettings):
    clave_jwt: str = "clave_ultra_secreta"
    algoritmo_jwt: str = "HS256"
    duracion_token: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
