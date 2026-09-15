import json
import sys
sys.path.insert(0, 'services/worker/agents')

from parser import ParserAgent
from reconciler import ReconcilerAgent

# Test email
test_email = """
Subject: PO-12345 - Urgent Delivery Delay

Our supplier has informed us that shipment for PO-12345 
will be delayed by 5 days due to production issues.

Affected:
- SKU ABC-123 (Qty 100)
- SKU ABC-456 (Qty 50)

Original delivery: 2026-09-15
New delivery: 2026-09-20

Please confirm by EOD.
"""

print("=" * 60)
print("DAY 6 — PARSER + RECONCILER PIPELINE TEST")
print("=" * 60)

# 1. Parser
print("\n[STEP 1] Parser Agent")
print("-" * 40)
parser = ParserAgent()
parsed = parser.extract_from_email(test_email, "PO-12345 - Delivery Delay")
print(json.dumps(parsed, indent=2))

# 2. Reconciler
print("\n[STEP 2] Reconciler Agent")
print("-" * 40)
reconciler = ReconcilerAgent()
reconciled = reconciler.reconcile(parsed)
print(json.dumps(reconciled, indent=2))

# 3. Summary
print("\n[PIPELINE SUMMARY]")
print("-" * 40)
print(f"✓ Exception detected: {parsed['exception_type']}")
print(f"✓ PO matched: {reconciled['po_found']}")
print(f"✓ Lines reconciled: {len(reconciled['matched_lines'])}")
print(f"✓ Mismatches: {len(reconciled['mismatches'])}")
print(f"✓ Impact: {reconciled['downstream_impact']['dependent_orders']} downstream orders")
print(f"✓ Ready for Policy Agent: {reconciled['confidence'] > 0.8}")

print("\n" + "=" * 60)
