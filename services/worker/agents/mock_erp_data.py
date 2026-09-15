PURCHASE_ORDERS = {
    "PO-12345": {
        "po_number": "PO-12345",
        "supplier_id": "SUP-001",
        "lines": [
            {"line_id": "PO-12345-001", "sku": "ABC-123", "qty_ordered": 100, "delivery_date": "2026-09-15", "status": "open"},
            {"line_id": "PO-12345-002", "sku": "ABC-456", "qty_ordered": 50, "delivery_date": "2026-09-15", "status": "open"}
        ]
    }
}

DEPENDENT_ORDERS = {
    "SO-55555": {"sales_order": "SO-55555", "customer": "Customer ABC", "depends_on": ["PO-12345"]},
    "SO-55556": {"sales_order": "SO-55556", "customer": "Customer XYZ", "depends_on": ["PO-12345"]}
}

def get_po(po_number):
    return PURCHASE_ORDERS.get(po_number)

def get_dependent_orders(po_number):
    return [so for so in DEPENDENT_ORDERS.values() if po_number in so.get("depends_on", [])]
