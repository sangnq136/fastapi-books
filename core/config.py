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


settings = Settings()