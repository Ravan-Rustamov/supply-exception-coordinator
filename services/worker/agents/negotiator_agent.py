import json
from datetime import datetime

class NegotiatorAgent:
    """
    Supplier communication - draft responses
    """
    
    def prepare_response(self, parsed_delta, policy_result):
        """
        Supplier-a cavab əmali hazırlayır
        """
        
        negotiation_id = f"NEG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        po_number = parsed_delta.get('po_number')
        line_changes = parsed_delta.get('line_changes', [])
        
        if policy_result['route'] == 'auto':
            tone = "acknowledgement"
            body = f"""
Dear Supplier,

Thank you for notifying us of the delivery date change for {po_number}.

We have reviewed the new delivery dates and confirm acceptance:
"""
            for lc in line_changes:
                body += f"\n- SKU {lc['sku']}: {lc['old_delivery_date']} → {lc['new_delivery_date']}"
            
            body += """

We have updated our systems and downstream commitments accordingly.
Please confirm receipt of this message.

Best regards,
Procurement Team
"""
        
        elif policy_result['route'] == 'human':
            tone = "escalation"
            body = f"""
Dear Supplier,

Your delivery date change notification for {po_number} requires management review.

We will respond within 24 hours.

Regards,
Procurement Team
"""
        
        else:
            tone = "rejection"
            body = f"""
Dear Supplier,

We cannot accept the delivery date change for {po_number} 
due to downstream customer commitments.

Please advise alternative solutions.

Regards,
Procurement Team
"""
        
        return {
            'negotiation_id': negotiation_id,
            'po_number': po_number,
            'tone': tone,
            'status': policy_result['route'],
            'draft_email': {
                'to': 'supplier@company.com',
                'subject': f'RE: {po_number} - Delivery Date Confirmation',
                'body': body
            },
            'ready_to_send': policy_result['route'] == 'auto'
        }

if __name__ == "__main__":
    agent = NegotiatorAgent()
    
    parsed = {'po_number': 'PO-12345', 'line_changes': [{'sku': 'ABC-123', 'old_delivery_date': '2026-09-15', 'new_delivery_date': '2026-09-20'}]}
    policy = {'route': 'auto', 'risk_score': 0.3}
    
    response = agent.prepare_response(parsed, policy)
    print("[Negotiator Output]")
    print(json.dumps(response, indent=2))
