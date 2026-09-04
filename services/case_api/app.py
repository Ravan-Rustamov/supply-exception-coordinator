"""Case API service."""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import redis

app = FastAPI(title="Case API")

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return HTMLResponse("""
    <html>
        <head><title>Case API</title></head>
        <body>
            <h1>Supply Exception Coordinator</h1>
            <ul>
                <li><a href="/cases">View Cases</a></li>
                <li><a href="/approvals">Pending Approvals</a></li>
            </ul>
        </body>
    </html>
    """)

@app.get("/cases")
def list_cases():
    return {"cases": []}

@app.get("/cases/{case_id}")
def get_case(case_id: str):
    return {"case_id": case_id, "status": "new"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
