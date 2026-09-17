import json
from policy_rules import PolicyRulesEngine

class PolicyAgent:
    def evaluate(self, reconciled_data, delta_days=5):
        """
        Reconciled data-yı policy rules-a qarşı kontrol edir
        """
        
        impact = reconciled_data.get("downstream_impact", {})
        confidence = reconciled_data.get("confidence", 0.95)
        
        # Rules evaluate et
        rule_result = PolicyRulesEngine.evaluate(
            delta_days=delta_days,
            downstream_impact=impact,
            confidence=confidence
        )
        
        result = {
            "po_number": reconciled_data.get("po_number"),
            "delta_days": delta_days,
            "route": rule_result["route"],
            "rules_fired": rule_result["rules_fired"],
            "risk_score": rule_result["risk_score"],
            "approval_required": rule_result["route"] in ["human", "deny"],
            "recommendation": self._get_recommendation(rule_result["route"], rule_result["risk_score"])
        }
        
        return result
    
    def _get_recommendation(self, route, risk_score):
        if route == "auto":
            return f"Auto-approve (Risk: {risk_score:.2f})"
        elif route == "human":
            return f"Escalate to human (Risk: {risk_score:.2f})"
        else:
            return f"Deny - too risky (Risk: {risk_score:.2f})"

if __name__ == "__main__":
    agent = PolicyAgent()
    
    reconciled = {
        "po_number": "PO-12345",
        "downstream_impact": {"dependent_orders": 2, "affected_customers": 2},
        "confidence": 0.95
    }
    
    print("Test 1 (5 days, 2 orders):")
    r1 = agent.evaluate(reconciled, delta_days=5)
    print(json.dumps(r1, indent=2))
    
    print("\nTest 2 (10 days, 2 orders):")
    r2 = agent.evaluate(reconciled, delta_days=10)
    print(json.dumps(r2, indent=2))
    
    print("\nTest 3 (20 days, 4 orders):")
    r3 = agent.evaluate({"po_number": "PO-12345", "downstream_impact": {"dependent_orders": 4}}, delta_days=20)
    print(json.dumps(r3, indent=2))
