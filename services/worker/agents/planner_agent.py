import json
from datetime import datetime

class PlannerAgent:
    """
    Orchestration agent - workflow routing + decision making
    """
    
    def plan_workflow(self, parsed_delta):
        """
        Exception-ə görsə workflow steps-i planlaşdırır
        """
        
        plan_id = f"PLAN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        exception_type = parsed_delta.get('exception_type', 'unknown')
        
        workflow_steps = {
            'delivery_date_change': [
                {'step': 1, 'agent': 'Reconciler', 'action': 'validate_against_erp'},
                {'step': 2, 'agent': 'Policy', 'action': 'risk_evaluation'},
                {'step': 3, 'agent': 'Negotiator', 'action': 'prepare_response'},
                {'step': 4, 'agent': 'Executor', 'action': 'apply_changes'},
                {'step': 5, 'agent': 'Notifier', 'action': 'send_confirmations'}
            ],
            'qty_change': [
                {'step': 1, 'agent': 'Reconciler', 'action': 'validate_qty'},
                {'step': 2, 'agent': 'Policy', 'action': 'risk_evaluation'},
                {'step': 3, 'agent': 'Executor', 'action': 'update_inventory'},
                {'step': 4, 'agent': 'Negotiator', 'action': 'notify_stakeholders'}
            ],
            'unknown': [
                {'step': 1, 'agent': 'Reconciler', 'action': 'investigate'},
                {'step': 2, 'agent': 'Escalator', 'action': 'human_review'}
            ]
        }
        
        steps = workflow_steps.get(exception_type, workflow_steps['unknown'])
        
        return {
            'plan_id': plan_id,
            'exception_type': exception_type,
            'workflow_steps': steps,
            'status': 'ready_for_execution'
        }

if __name__ == "__main__":
    agent = PlannerAgent()
    plan = agent.plan_workflow({'exception_type': 'delivery_date_change'})
    print("[Planner Output]")
    print(json.dumps(plan, indent=2))
