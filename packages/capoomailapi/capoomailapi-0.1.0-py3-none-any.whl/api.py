import os
import uuid
import time
import firebase_admin
from firebase_admin import credentials, db

def get_service_account_path():
    """
    Detect service account JSON path automatically.
    Priority:
    1. ./servicecode.json in current working directory
    2. Absolute path inside capoomailapi folder
    """
    relative_path = "./servicecode.json"
    absolute_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "servicecode.json"
    )

    if os.path.exists(relative_path):
        return relative_path
    elif os.path.exists(absolute_path):
        return absolute_path
    else:
        raise FileNotFoundError("servicecode.json not found in project folder")

# Initialize Firebase once
cred = credentials.Certificate(get_service_account_path())
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://capoomail-backend-default-rtdb.firebaseio.com/"
    })

class CapoomailAPI:
    def __init__(self):
        self.sent = []

    def send(self, receiver, sender, title, message):
        mail = {
            "body": message,
            "from": sender,
            "subject": title,
            "timestamp": int(time.time() * 1000),
            "to": receiver
        }

        random_id = str(uuid.uuid4())
        db.reference(f"messages/{random_id}").set(mail)

        self.sent.append(mail)
        return f"Mail sent from {sender} to {receiver} with subject '{title}'"

    def get_sent(self):
        return self.sent