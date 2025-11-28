import os
import uuid
import aiohttp
from typing import Dict


YOOKASSA_API = "https://api.yookassa.ru/v3/"

SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")
RETURN_URL = os.getenv("YOOKASSA_RETURN_URL", "")


pending_payments: Dict[str, dict] = {}

async def create_payment(amount: float, description: str, user_id: int, username:str):
    """Функция создания платежа в Yookassa"""

    idempotence_key = str(uuid.uuid4())
    payload = {
        "amount": {"value": f"{amount:.2f}", "currency": "RUB"},
        "confirmation": {"type": "redirect", "return_url": RETURN_URL},
        "capture": True,
        "description": description,
    }
    auth = aiohttp.BasicAuth(login=SHOP_ID, password=SECRET_KEY)

    async with aiohttp.ClientSession(auth=auth) as session:
        headers = {"Idempotence-Key": idempotence_key,
                   "Accept": "application/json"}

        async with session.post(f"{YOOKASSA_API}payments", json=payload, headers=headers) as resp:
            data = await resp.json()
            print(f"Создание платежа: {resp.status} {data}")
            if resp.status not in (200, 201):
                return RuntimeError(f"Ошибка создания платежа: {resp.status} {data}")

            payment_id = data.get("id")
            confirmation = data.get("confirmation", {})
            confirmation_url = confirmation.get("confirmation_url") or confirmation.get("url") or ""

            pending_payments[payment_id] = {
                "user_id": user_id,
                "username": username or "",
                "amount": amount,
                "status": "pending"
            }
            try:
                from services.google_sheets import add_record
                comment = f"Платеж {payment_id} создан"
                add_record("income", "yookassa_pending", amount, comment, user_id, username or "")

            except Exception as e:
                print(f"Ошибка добавления записи в Google Sheets: {e}")

            return  confirmation_url, payment_id