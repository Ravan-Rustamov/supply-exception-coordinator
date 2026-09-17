import json
import sys
sys.path.insert(0, 'services/worker/agents')

from parser import ParserAgent
from reconciler import ReconcilerAgent
from policy_agent import PolicyAgent

test_email = """
Subject: PO-12345 - Delivery Delay

Shipment PO-12345 delayed 5 days.
SKU ABC-123, ABC-456
Original: 2026-09-15
New: 2026-09-20
"""

print("=" * 70)
print("DAY 7 — 3-AGENT PIPELINE: PARSER → RECONCILER → POLICY")
print("=" * 70)

# 1. Parser
print("\n[AGENT 1] Parser")
print("-" * 70)
parser = ParserAgent()
parsed = parser.extract_from_email(test_email, "PO-12345 Delay")
print(f"Exception: {parsed['exception_type']}")
print(f"PO: {parsed['po_number']}")
print(f"Lines: {len(parsed['line_changes'])} SKUs affected")

# 2. Reconciler
print("\n[AGENT 2] Reconciler")
print("-" * 70)
reconciler = ReconcilerAgent()
reconciled = reconciler.reconcile(parsed)
print(f"PO Found: {reconciled['po_found']}")
print(f"Matched: {len(reconciled['matched_lines'])} lines")
print(f"Mismatches: {len(reconciled['mismatches'])}")
print(f"Downstream Orders: {reconciled['downstream_impact']['dependent_orders']}")

# 3. Policy
print("\n[AGENT 3] Policy & Risk")
print("-" * 70)
policy = PolicyAgent()
policy_result = policy.evaluate(reconciled, delta_days=5)
print(f"Route: {policy_result['route'].upper()}")
print(f"Risk Score: {policy_result['risk_score']:.2f}")
print(f"Rules Fired: {policy_result['rules_fired']}")
print(f"Approval Required: {policy_result['approval_required']}")
print(f"Recommendation: {policy_result['recommendation']}")

# Summary
print("\n[PIPELINE VERDICT]")
print("-" * 70)
if policy_result['route'] == 'auto':
    print("✓ AUTO-APPROVED - Ready for Executor")
elif policy_result['route'] == 'human':
    print("⚠ HUMAN APPROVAL REQUIRED")
else:
    print("✗ DENIED - Exception blocked by policy")

print("\n" + "=" * 70)
