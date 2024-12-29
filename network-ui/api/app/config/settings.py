from pydantic_settings import BaseSettings
import json
import os

class Settings(BaseSettings):
    # Comment out or remove these lines
    # database_server: str = "http://arangodb:8529"
    # database_name: str = "jalapeno"
    # credentials_path: str = "/credentials/auth"
    
    # Add your test configuration
    database_server: str = "http://198.18.133.104:30852"  # your IP and port
    database_name: str = "jalapeno"
    username: str = "root"
    password: str = "jalapeno"
