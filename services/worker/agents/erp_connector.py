import json
from datetime import datetime

class ERPConnector:
    """
    Mock ERP connector - Production-da SAP/NetSuite olacaq
    """
    
    def __init__(self):
        self.transaction_log = []
    
    def update_po_delivery_date(self, po_number, sku, new_date, dry_run=True):
        """
        PO line-in delivery date-ini update edir
        dry_run=True: no actual changes (safe mode)
        """
        
        transaction_id = f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Simulate ERP update
        result = {
            "transaction_id": transaction_id,
            "status": "success",
            "dry_run": dry_run,
            "po_number": po_number,
            "sku": sku,
            "changes": {
                "field": "delivery_date",
                "old_value": "2026-09-15",
                "new_value": new_date,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Log transaction
        self.transaction_log.append({
            "transaction_id": transaction_id,
            "timestamp": datetime.now().isoformat(),
            "action": "update_po_delivery_date",
            "dry_run": dry_run,
            "details": result
        })
        
        return result
    
    def create_delivery_notification(self, po_number, new_date, dry_run=True):
        """
        Supplier-a notification email yaradır
        """
        
        transaction_id = f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        result = {
            "transaction_id": transaction_id,
            "status": "success",
            "action": "delivery_notification_sent",
            "recipient": "supplier@company.com",
            "message": f"PO {po_number} delivery updated to {new_date}"
        }
        
        self.transaction_log.append({
            "transaction_id": transaction_id,
            "timestamp": datetime.now().isoformat(),
            "action": "create_delivery_notification",
            "dry_run": dry_run,
            "details": result
        })
        
        return result
    
    def get_audit_log(self):
        """Tüm transactions-ı döndür"""
        return self.transaction_log

if __name__ == "__main__":
    erp = ERPConnector()
    
    r1 = erp.update_po_delivery_date("PO-12345", "ABC-123", "2026-09-20", dry_run=True)
    print("[DRY RUN] PO Update:")
    print(json.dumps(r1, indent=2))
    
    r2 = erp.create_delivery_notification("PO-12345", "2026-09-20", dry_run=True)
    print("\n[DRY RUN] Notification:")
    print(json.dumps(r2, indent=2))
    
    print("\n[AUDIT LOG]:")
    print(json.dumps(erp.get_audit_log(), indent=2))
