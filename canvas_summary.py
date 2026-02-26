import requests
import os
from datetime import datetime, timedelta, timezone

API_TOKEN = os.getenv("canvas_token")
BASE_URL = "https://uta.instructure.com/api/v1"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

response = requests.get(
    f"{BASE_URL}/users/self/todo",
    headers=headers
)

items = response.json()
now = datetime.now(timezone.utc)
week_from_now = now + timedelta(days=7)

due_soon = []

for item in items:
    if item.get("assignment") and item["assignment"].get("due_at") and "DATA MINING" not in item["context_name"]:
        due_date = datetime.fromisoformat(item["assignment"]["due_at"].replace("Z", "+00:00"))
        if now <= due_date <= week_from_now:
            due_soon.append(item)

message = "Assignments Due This Week:\n\n"

for item in due_soon:
    name = item["assignment"]["name"]

    due = datetime.fromisoformat(item["assignment"]["due_at"].replace("Z", "+00:00"))
    due -= timedelta(hours=6)

    message += f"- {name} (Due {due.date()} @ {due.time()})\n"


requests.post(
    "https://api.pushover.net/1/messages.json",
    data={
        "token": os.getenv("pushover_api"),
        "user": os.getenv("pushover_user"),
        "message": message
    }
)

print(message)
