"""Worker: Agent orchestrator."""
import redis
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

def process_events():
    logger.info("🔄 Worker started, listening for events...")
    
    while True:
        try:
            result = redis_client.brpop("queue:events", timeout=5)
            
            if result:
                _, event_json = result
                event = json.loads(event_json)
                
                logger.info(f"📧 Event: {event['event_type']} from {event.get('from_addr', '?')}")
                
                if event["event_type"] == "email.received":
                    process_email(event)
            else:
                logger.debug("⏳ No events, waiting...")
                
        except Exception as e:
            logger.error(f"❌ Error: {e}", exc_info=True)
            time.sleep(1)

def process_email(event):
    email_id = event["email_id"]
    logger.info(f"🔄 Processing email {email_id}")
    
    case_id = f"CASE-{email_id[:8]}"
    
    case = {
        "case_id": case_id,
        "email_id": email_id,
        "status": "NEW",
        "from": event.get("from_addr"),
        "subject": event.get("subject"),
    }
    
    redis_client.hset("cases", case_id, json.dumps(case))
    
    logger.info(f"✅ Case created: {case_id}")

if __name__ == "__main__":
    process_events()
