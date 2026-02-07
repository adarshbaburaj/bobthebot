"""
Mock AI Logic for Tenant Maintenance Agent

⚠️ IMPORTANT: This is a TEMPORARY PLACEHOLDER for demonstration purposes.
In production, this will be replaced with a real AI agent that:
- Uses LLM for issue classification
- Integrates with property management systems
- Makes real-time vendor assignments based on availability
- Has learning capabilities

Current implementation: Simple keyword matching
"""

import json
import os


def load_vendors():
    """Load mock vendor data from vendors.json"""
    try:
        vendors_path = os.path.join(os.path.dirname(__file__), 'vendors.json')
        with open(vendors_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def get_vendor_by_category(category: str):
    """Get a vendor name by category (for demonstration)"""
    vendors = load_vendors()
    for vendor in vendors:
        if vendor['category'].lower() == category.lower():
            return vendor['name']
    return "Auto-assigned vendor"


def analyze_issue(text: str) -> dict:
    """
    Analyze a maintenance issue and return classification.

    🤖 MOCKED LOGIC - This simulates what a real AI agent would do:
    - Natural language understanding
    - Historical pattern analysis
    - Dynamic cost estimation
    - Real-time vendor matching

    Args:
        text: The issue description from the tenant

    Returns:
        dict with keys:
            - issue_type: Classification of the issue
            - priority: LOW, MEDIUM, or HIGH
            - estimated_cost: Cost in AED
            - status: Human-readable status message
            - vendor: (optional) Assigned vendor name
    """

    text_lower = text.lower()

    # Plumbing issues - HIGH priority
    if any(keyword in text_lower for keyword in ['leak', 'water', 'plumbing', 'pipe', 'drain', 'toilet', 'sink']):
        vendor = get_vendor_by_category("Plumbing")
        return {
            "issue_type": "Plumbing Leak",
            "priority": "HIGH",
            "estimated_cost": 1500,
            "status": "Waiting for human approval (cost > 1000 AED)",
            "vendor": vendor
        }

    # AC issues - MEDIUM priority
    elif any(keyword in text_lower for keyword in ['ac', 'air', 'cool', 'conditioning', 'temperature', 'hot', 'cold']):
        vendor = get_vendor_by_category("AC")
        return {
            "issue_type": "AC Maintenance",
            "priority": "MEDIUM",
            "estimated_cost": 600,
            "status": "Vendor auto-assigned",
            "vendor": vendor
        }

    # Electrical issues - HIGH priority
    elif any(keyword in text_lower for keyword in ['electric', 'power', 'light', 'socket', 'outlet', 'switch']):
        return {
            "issue_type": "Electrical Issue",
            "priority": "HIGH",
            "estimated_cost": 1200,
            "status": "Waiting for human approval (cost > 1000 AED)",
            "vendor": "Auto-assigned vendor"
        }

    # General maintenance - LOW priority
    else:
        vendor = get_vendor_by_category("General")
        return {
            "issue_type": "General Maintenance",
            "priority": "LOW",
            "estimated_cost": 300,
            "status": "Vendor auto-assigned",
            "vendor": vendor
        }


if __name__ == "__main__":
    # Quick test
    test_cases = [
        "There is water leaking from the ceiling",
        "The AC is not cooling properly",
        "Door handle broken",
        "Power outlet not working"
    ]

    print("🧪 Testing mock logic:\n")
    for test in test_cases:
        result = analyze_issue(test)
        print(f"Input: {test}")
        print(f"Result: {result}")
        print()
