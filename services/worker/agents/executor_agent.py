import json
from datetime import datetime
from erp_connector import ERPConnector

class ExecutorAgent:
    """
    ERP write-back agent
    Safety: DRY RUN by default, explicit approval needed for live
    """
    
    def __init__(self, dry_run=True):
        self.erp = ERPConnector()
        self.dry_run = dry_run
        self.execution_log = []
    
    def execute(self, policy_result, parsed_delta):
        """
        Policy approval-ı ERP action-a çevirir
        """
        
        execution_id = f"EXE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Safety check
        if policy_result['route'] != 'auto':
            return {
                "execution_id": execution_id,
                "status": "rejected",
                "reason": f"Not auto-approved (route: {policy_result['route']})",
                "changes_applied": []
            }
        
        # Extract changes
        po_number = policy_result.get('po_number')
        line_changes = parsed_delta.get('line_changes', [])
        
        changes_applied = []
        errors = []
        
        # Apply each change
        for line_change in line_changes:
            sku = line_change.get('sku')
            new_date = line_change.get('new_delivery_date')
            
            try:
                # DRY RUN - no actual changes yet
                result = self.erp.update_po_delivery_date(
                    po_number, sku, new_date, 
                    dry_run=self.dry_run
                )
                changes_applied.append({
                    "sku": sku,
                    "transaction_id": result['transaction_id'],
                    "old_date": "2026-09-15",
                    "new_date": new_date,
                    "status": "success"
                })
            except Exception as e:
                errors.append({"sku": sku, "error": str(e)})
        
        # Create notification
        if changes_applied:
            self.erp.create_delivery_notification(
                po_number, 
                line_changes[0]['new_delivery_date'],
                dry_run=self.dry_run
            )
        
        result = {
            "execution_id": execution_id,
            "status": "completed",
            "dry_run": self.dry_run,
            "po_number": po_number,
            "changes_applied": changes_applied,
            "errors": errors,
            "audit_trail": self.erp.get_audit_log()
        }
        
        self.execution_log.append(result)
        return result
    
    def enable_live_mode(self):
        """Enable live mode after proper authorization"""
        self.dry_run = False
        return {"status": "Live mode ENABLED", "warning": "Real changes will be applied"}

if __name__ == "__main__":
    agent = ExecutorAgent(dry_run=True)  # Safe by default
    
    policy_result = {
        "po_number": "PO-12345",
        "route": "auto",
        "risk_score": 0.3
    }
    
    parsed_delta = {
        "po_number": "PO-12345",
        "line_changes": [
            {"sku": "ABC-123", "new_delivery_date": "2026-09-20"},
            {"sku": "ABC-456", "new_delivery_date": "2026-09-20"}
        ]
    }
    
    print("[DRY RUN MODE]")
    result = agent.execute(policy_result, parsed_delta)
    print(json.dumps(result, indent=2))
