from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://andre:SenhaSqlDev!@localhost:5432/cursos_fastapi'

    class Config:
        case_senitive = True

settings: Settings = Settings()        