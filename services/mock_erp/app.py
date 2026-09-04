"""Mock ERP service."""
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Mock ERP")

PURCHASE_ORDERS = {
    "PO-001": {
        "po_number": "PO-001",
        "supplier_id": "ACME-001",
        "lines": [
            {"line_num": 1, "sku": "WIDGET-A", "qty": 100, "delivery_date": "2026-09-15"}
        ]
    }
}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/po/{po_number}")
def get_po(po_number: str):
    if po_number not in PURCHASE_ORDERS:
        raise HTTPException(status_code=404, detail="PO not found")
    return PURCHASE_ORDERS[po_number]

@app.post("/po/{po_number}/reschedule")
def reschedule_delivery(po_number: str, new_date: str, reason: str, dry_run: bool = True):
    if po_number not in PURCHASE_ORDERS:
        raise HTTPException(status_code=404, detail="PO not found")
    
    po = PURCHASE_ORDERS[po_number]
    old_date = po["lines"][0].get("delivery_date")
    
    if not dry_run:
        po["lines"][0]["delivery_date"] = new_date
    
    return {
        "po_number": po_number,
        "old_date": old_date,
        "new_date": new_date,
        "reason": reason,
        "dry_run": dry_run,
        "status": "ok"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
