import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN_TG")

MANAGER_ID = int(os.getenv("MANAGER_ID"))
DRIVERS = [7213094751, 7003041125, 915010491]
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDS_PATH", "services/creds/credentials.json")