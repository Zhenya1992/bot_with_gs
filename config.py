import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")

MANAGER_ID = int(os.getenv("MANAGER_ID"))
