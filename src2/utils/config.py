from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    model_config=SettingsConfigDict(env_file='.env',extra='ignore')

    DB_CONNECTION:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    

config=Config()

print(config.DB_CONNECTION)