class PolicyRulesEngine:
    RULES = {
        "delivery_delay_low": {
            "condition": lambda d, i: d <= 7 and i["dependent_orders"] <= 1,
            "route": "auto",
            "risk_score": 0.3
        },
        "delivery_delay_medium": {
            "condition": lambda d, i: 7 < d <= 14 and i["dependent_orders"] <= 3,
            "route": "human",
            "risk_score": 0.6
        },
        "delivery_delay_high": {
            "condition": lambda d, i: d > 14 or i["dependent_orders"] > 3,
            "route": "deny",
            "risk_score": 0.9
        }
    }
    
    @staticmethod
    def evaluate(delta_days, downstream_impact, confidence=0.95):
        fired_rules = []
        route = "auto"
        risk_score = 0.0
        
        for rule_name, rule in PolicyRulesEngine.RULES.items():
            try:
                if rule["condition"](delta_days, downstream_impact):
                    fired_rules.append(rule_name)
                    if rule["route"] == "deny":
                        route = "deny"
                    elif rule["route"] == "human" and route != "deny":
                        route = "human"
                    risk_score = max(risk_score, rule["risk_score"])
            except:
                pass
        
        return {"route": route, "rules_fired": fired_rules, "risk_score": risk_score}

if __name__ == "__main__":
    import json
    
    r1 = PolicyRulesEngine.evaluate(5, {"dependent_orders": 1, "affected_customers": 1})
    print("Test 1 (5 days, 1 order):")
    print(json.dumps(r1, indent=2))
    
    r2 = PolicyRulesEngine.evaluate(10, {"dependent_orders": 2, "affected_customers": 2})
    print("\nTest 2 (10 days, 2 orders):")
    print(json.dumps(r2, indent=2))
    
    r3 = PolicyRulesEngine.evaluate(20, {"dependent_orders": 4, "affected_customers": 3})
    print("\nTest 3 (20 days, 4 orders):")
    print(json.dumps(r3, indent=2))
