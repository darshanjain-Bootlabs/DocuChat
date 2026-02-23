from dotenv import load_dotenv
from pydantic_settings import BaseSettings
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    GROQ_API_KEY: str
    app_name: str = "DocuChat"
    class Config:
        env_file = ".env"
settings = Settings()