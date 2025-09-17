import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN_TG")

MANAGER_ID = int(os.getenv("MANAGER_ID"))
DRIVERS = [1020773508, 7003041125]