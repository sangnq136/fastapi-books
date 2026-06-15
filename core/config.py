import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    @property
    def SECRET_KEY(self):
        return os.getenv("SECRET_KEY")

    @property
    def ALGORITHM(self):
        return os.getenv("ALGORITHM", "HS256")
    
    @property
    def TOKEN_EXPIRE_MINUTES(self):
        return int(os.getenv("TOKEN_EXPIRE_MINUTES", "20"))
    
    @property
    def CORS_ORIGINS(self):
        origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000")
        return origins.split(",")

settings = Settings()
