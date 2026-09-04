"""Mock Inbox service."""
from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json
from datetime import datetime
import uuid

app = FastAPI(title="Mock Inbox")

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

class Email(BaseModel):
    from_addr: str
    subject: str
    body: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/emails")
def receive_email(email: Email):
    email_id = str(uuid.uuid4())
    
    event = {
        "event_type": "email.received",
        "email_id": email_id,
        "from_addr": email.from_addr,
        "subject": email.subject,
        "body": email.body,
        "received_at": datetime.now().isoformat()
    }
    
    redis_client.lpush("queue:events", json.dumps(event))
    
    return {
        "status": "queued",
        "email_id": email_id,
        "timestamp": event["received_at"]
    }

@app.get("/emails")
def list_emails():
    events = redis_client.lrange("queue:events", 0, -1)
    return [json.loads(e) for e in events]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
