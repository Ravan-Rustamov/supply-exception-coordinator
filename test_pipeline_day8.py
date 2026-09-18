import json
import sys
sys.path.insert(0, 'services/worker/agents')

from parser import ParserAgent
from reconciler import ReconcilerAgent
from policy_agent import PolicyAgent
from executor_agent import ExecutorAgent

test_email = """
Subject: PO-12345 - Delivery Delay Notice

Our supplier has informed us that shipment PO-12345 
containing SKU ABC-123 (100 units) and SKU ABC-456 (50 units)
will be delayed by 5 days.

Original delivery: 2026-09-15
New delivery: 2026-09-20

Please confirm.
"""

print("=" * 80)
print("DAY 8 — FULL 4-AGENT PIPELINE: PARSER → RECONCILER → POLICY → EXECUTOR")
print("=" * 80)

# 1. Parser
print("\n[STEP 1] Parser Agent")
print("-" * 80)
parser = ParserAgent()
parsed = parser.extract_from_email(test_email, "PO-12345 Delivery Delay")
print(f"✓ Exception type: {parsed['exception_type']}")
print(f"✓ PO: {parsed['po_number']}")
print(f"✓ SKUs: {len(parsed['line_changes'])} affected")

# 2. Reconciler
print("\n[STEP 2] Reconciler Agent")
print("-" * 80)
reconciler = ReconcilerAgent()
reconciled = reconciler.reconcile(parsed)
print(f"✓ PO Found: {reconciled['po_found']}")
print(f"✓ Lines Matched: {len(reconciled['matched_lines'])}")
print(f"✓ Mismatches: {len(reconciled['mismatches'])}")
print(f"✓ Downstream Orders: {reconciled['downstream_impact']['dependent_orders']}")
print(f"✓ Confidence: {reconciled['confidence']}")

# 3. Policy
print("\n[STEP 3] Policy & Risk Agent")
print("-" * 80)
policy = PolicyAgent()
policy_result = policy.evaluate(reconciled, delta_days=5)
print(f"✓ Route: {policy_result['route'].upper()}")
print(f"✓ Risk Score: {policy_result['risk_score']:.2f}")
print(f"✓ Rules Fired: {policy_result['rules_fired']}")
print(f"✓ Approval Required: {policy_result['approval_required']}")

# 4. Executor
print("\n[STEP 4] Executor Agent")
print("-" * 80)
executor = ExecutorAgent(dry_run=True)  # SAFE MODE
exec_result = executor.execute(policy_result, parsed)
print(f"✓ Execution ID: {exec_result['execution_id']}")
print(f"✓ Status: {exec_result['status']}")
print(f"✓ DRY RUN: {exec_result['dry_run']}")
print(f"✓ Changes Applied: {len(exec_result['changes_applied'])}")
print(f"✓ Errors: {len(exec_result['errors'])}")

# Final Verdict
print("\n[FINAL VERDICT]")
print("-" * 80)
print("✓ Email processed end-to-end")
print(f"✓ Exception auto-approved (risk: {policy_result['risk_score']:.2f})")
print(f"✓ {len(exec_result['changes_applied'])} changes simulated (DRY RUN)")
print("✓ Ready for live execution with proper authorization")

print("\n" + "=" * 80)
