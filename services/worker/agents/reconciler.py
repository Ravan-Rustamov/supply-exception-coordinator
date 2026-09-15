import json
from mock_erp_data import get_po, get_dependent_orders

class ReconcilerAgent:
    def reconcile(self, parsed_delta):
        po_number = parsed_delta.get("po_number")
        result = {
            "po_number": po_number,
            "po_found": False,
            "matched_lines": [],
            "mismatches": [],
            "downstream_impact": {"dependent_orders": 0, "affected_customers": 0},
            "confidence": 0.0
        }
        
        po = get_po(po_number)
        if not po:
            return result
        
        result["po_found"] = True
        
        parser_lines = {lc["sku"]: lc for lc in parsed_delta.get("line_changes", [])}
        
        for po_line in po["lines"]:
            sku = po_line["sku"]
            if sku in parser_lines:
                result["matched_lines"].append({"sku": sku, "qty": po_line["qty_ordered"]})
                if parser_lines[sku].get("new_delivery_date") != po_line["delivery_date"]:
                    result["mismatches"].append({"sku": sku, "field": "delivery_date"})
        
        dependent = get_dependent_orders(po_number)
        result["downstream_impact"]["dependent_orders"] = len(dependent)
        result["downstream_impact"]["affected_customers"] = len(set(so["customer"] for so in dependent))
        result["confidence"] = 0.95 if result["matched_lines"] else 0.0
        
        return result

if __name__ == "__main__":
    agent = ReconcilerAgent()
    parsed = {
        "po_number": "PO-12345",
        "line_changes": [
            {"sku": "ABC-123", "new_delivery_date": "2026-09-20"},
            {"sku": "ABC-456", "new_delivery_date": "2026-09-20"}
        ]
    }
    result = agent.reconcile(parsed)
    print("[Reconciler Output]")
    print(json.dumps(result, indent=2))
