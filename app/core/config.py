from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    GROQ_API_KEY: str
    app_name: str = "DocuChat"
    model_config = ConfigDict(
        env_file=".env"
    )
settings = Settings()