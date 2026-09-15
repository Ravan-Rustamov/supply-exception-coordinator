import json
import re
from datetime import datetime

class ParserAgent:
    """
    LLM-less parser: Regex + pattern matching
    Production-ready CPU performance (instant)
    """
    
    def extract_from_email(self, email_body: str, email_subject: str) -> dict:
        """
        Regex ile supplier e-poçtundan data çıxarır
        """
        
        full_text = f"{email_subject}\n{email_body}".upper()
        
        result = {
            "exception_type": "unknown",
            "po_number": None,
            "line_changes": [],
            "confidence": 0.0
        }
        
        # 1. PO Number çıxar (PO-XXXXX format)
        po_match = re.search(r'PO[:\s\-]*(\d{5,})', full_text)
        if po_match:
            result["po_number"] = f"PO-{po_match.group(1)}"
        
        # 2. SKU-ları çıxar (ABC-123 format, PO değil)
        all_codes = re.findall(r'([A-Z]{2,})-(\d{3,})', full_text)
        skus = [f"{code[0]}-{code[1]}" for code in all_codes if not code[0] == "PO"]
        
        # 3. Exception type detect et
        if "DELAY" in full_text or "LATE" in full_text:
            result["exception_type"] = "delivery_date_change"
        elif "QTY" in full_text or "QUANTITY" in full_text:
            result["exception_type"] = "qty_change"
        
        # 4. Tarihler
        dates = re.findall(r'(\d{4})[:\s\-](\d{2})[:\s\-](\d{2})', full_text)
        
        # 5. Line changes
        if len(dates) >= 2 and result["exception_type"] == "delivery_date_change":
            old_date = f"{dates[0][0]}-{dates[0][1]}-{dates[0][2]}"
            new_date = f"{dates[1][0]}-{dates[1][1]}-{dates[1][2]}"
            
            try:
                old_dt = datetime.strptime(old_date, "%Y-%m-%d")
                new_dt = datetime.strptime(new_date, "%Y-%m-%d")
                delta_days = (new_dt - old_dt).days
                
                for sku in set(skus):
                    result["line_changes"].append({
                        "sku": sku,
                        "old_delivery_date": old_date,
                        "new_delivery_date": new_date,
                        "delta_days": delta_days
                    })
                
                result["confidence"] = 0.95 if result["po_number"] and skus else 0.70
            except:
                pass
        
        return result

if __name__ == "__main__":
    agent = ParserAgent()
    
    result = agent.extract_from_email(
        """Our supplier has informed us that shipment for PO-12345
will be delayed.

SKU ABC-123 (Qty 100) and SKU ABC-456 (Qty 50)

Original delivery: 2026-09-15
New delivery: 2026-09-20""",
        "PO-12345 - Delivery Delay"
    )
    print("[Parser Output]")
    print(json.dumps(result, indent=2))
