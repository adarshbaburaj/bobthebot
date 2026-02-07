"""
AI-Powered Agent for Tenant Maintenance Classification

Uses Google Gemini (gemini-1.5-flash) to understand maintenance requests
and provide intelligent classification, cost estimation, and vendor assignment.

🤖 This is the REAL AI agent - replaces mock_logic.py
"""

import os
import json
import logging
from typing import Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("✓ Gemini API configured successfully")
else:
    logger.warning("⚠️  GEMINI_API_KEY not found - AI agent will not work")


# System prompt that defines BobTheBot's personality and rules
SYSTEM_PROMPT = """You are BobTheBot, a professional property maintenance manager for residential properties in Dubai, UAE.

Your job is to analyze tenant maintenance requests and provide structured assessments.

## Your Responsibilities:
1. Understand the maintenance issue from the tenant's description
2. Classify the issue type (Plumbing, AC, Electrical, General Maintenance, or other)
3. Assess priority level (LOW, MEDIUM, HIGH)
4. Estimate repair cost in AED (United Arab Emirates Dirham)
5. Recommend if it needs human approval or can be auto-assigned

## Classification Guidelines:

**HIGH Priority** (Usually >1000 AED):
- Water leaks, burst pipes, sewage issues
- Electrical hazards, power outages
- AC completely broken in summer
- Structural damage
- Safety hazards

**MEDIUM Priority** (Usually 400-1000 AED):
- AC not cooling well but working
- Minor plumbing issues (slow drains, dripping taps)
- Door/window issues
- Appliance repairs

**LOW Priority** (Usually <400 AED):
- Light bulbs, minor fixtures
- Small cosmetic issues
- Non-urgent general maintenance

## Cost Estimation (Important):
- Be realistic and slightly conservative
- Dubai typical costs:
  - Plumber emergency: 800-2000 AED
  - AC repair: 400-1500 AED
  - Electrician: 500-1500 AED
  - Handyman: 200-600 AED
  - Parts can add 200-1000 AED

## Output Format (CRITICAL):
You must respond with a valid JSON object with these exact keys:
{
  "issue_type": "Plumbing | AC | Electrical | General Maintenance | Other",
  "priority": "LOW | MEDIUM | HIGH",
  "estimated_cost": <number in AED>,
  "reasoning": "<brief explanation>",
  "needs_clarification": <true|false>,
  "clarification_question": "<question if needs_clarification is true, else null>"
}

## Behavior:
- Be professional, calm, and concise
- If the description is vague or missing critical details, set needs_clarification to true
- Never make up information - if uncertain, ask for clarification
- Always provide reasoning for your assessment

## Example Inputs and Expected Outputs:

Input: "Water leaking from the ceiling in bathroom"
Output: {"issue_type": "Plumbing", "priority": "HIGH", "estimated_cost": 1500, "reasoning": "Ceiling leak indicates pipe issue, requires immediate attention", "needs_clarification": false, "clarification_question": null}

Input: "AC not cooling"
Output: {"issue_type": "AC", "priority": "MEDIUM", "estimated_cost": 600, "reasoning": "AC cooling issue, likely gas refill or filter", "needs_clarification": false, "clarification_question": null}

Input: "Something is broken"
Output: {"issue_type": "General Maintenance", "priority": "LOW", "estimated_cost": 300, "reasoning": "Vague description", "needs_clarification": true, "clarification_question": "Could you please describe what is broken and share a photo if possible?"}
"""


def load_vendors() -> list:
    """Load vendor data from vendors.json"""
    try:
        vendors_path = os.path.join(os.path.dirname(__file__), 'vendors.json')
        with open(vendors_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("vendors.json not found")
        return []


def get_vendor_by_category(category: str) -> Optional[str]:
    """Match a vendor to the issue category"""
    vendors = load_vendors()

    # Map issue types to vendor categories
    category_map = {
        "plumbing": "Plumbing",
        "ac": "AC",
        "electrical": "General",
        "general": "General",
        "general maintenance": "General"
    }

    vendor_category = category_map.get(category.lower(), "General")

    for vendor in vendors:
        if vendor['category'].lower() == vendor_category.lower():
            return vendor['name']

    return "Auto-assigned vendor"


def call_gemini(user_message: str) -> Dict:
    """
    Call Google Gemini API with the user's maintenance request

    Args:
        user_message: The tenant's description of the issue

    Returns:
        Dict with AI analysis result
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not configured. Please set it in .env file")

    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Construct the full prompt
        full_prompt = f"{SYSTEM_PROMPT}\n\nTenant Message: {user_message}\n\nProvide your analysis as JSON:"

        # Generate response
        response = model.generate_content(full_prompt)

        # Parse the JSON response
        response_text = response.text.strip()

        # Sometimes Gemini wraps JSON in markdown code blocks, clean it
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        # Parse JSON
        ai_result = json.loads(response_text)

        logger.info(f"Gemini analysis: {ai_result}")
        return ai_result

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {e}")
        logger.error(f"Raw response: {response.text}")
        # Fallback to a default response
        return {
            "issue_type": "General Maintenance",
            "priority": "MEDIUM",
            "estimated_cost": 500,
            "reasoning": "AI response parsing failed, using default classification",
            "needs_clarification": True,
            "clarification_question": "Could you please provide more details about the issue?"
        }
    except Exception as e:
        logger.error(f"Gemini API call failed: {e}")
        raise


def analyze_issue(text: str) -> dict:
    """
    Analyze a maintenance issue using Google Gemini AI

    This is the main entry point called by bot.py
    Maintains the same interface as mock_logic.analyze_issue()

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

    try:
        # Call Gemini for AI analysis
        ai_result = call_gemini(text)

        # Extract AI results
        issue_type = ai_result.get('issue_type', 'General Maintenance')
        priority = ai_result.get('priority', 'MEDIUM')
        estimated_cost = ai_result.get('estimated_cost', 500)
        reasoning = ai_result.get('reasoning', '')
        needs_clarification = ai_result.get('needs_clarification', False)
        clarification_question = ai_result.get('clarification_question')

        # CRITICAL: Enforce cost threshold rule in Python (don't trust the model)
        if estimated_cost > 1000:
            status = "Waiting for human approval (cost > 1000 AED)"
        elif needs_clarification:
            status = "Vendor auto-assigned"
        else:
            status = "Vendor auto-assigned"

        # Get appropriate vendor
        vendor = get_vendor_by_category(issue_type)

        # Build response in the expected format
        result = {
            "issue_type": issue_type,
            "priority": priority,
            "estimated_cost": estimated_cost,
            "status": status,
            "vendor": vendor,
            "needs_clarification": needs_clarification,
            "clarification_question": clarification_question
        }

        logger.info(f"Final analysis: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in analyze_issue: {e}")
        # Fallback to safe defaults if AI fails
        return {
            "issue_type": "General Maintenance",
            "priority": "MEDIUM",
            "estimated_cost": 500,
            "status": "Processing error - please try again or contact support",
            "vendor": "Auto-assigned vendor"
        }


# Test function for local development
if __name__ == "__main__":
    # Test cases
    test_cases = [
        "There is water leaking from the ceiling in the bathroom",
        "The AC is not cooling properly",
        "Door handle broken",
        "Power outlet not working",
        "Something is broken"
    ]

    print("🧪 Testing AI Agent with Gemini:\n")

    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found. Please set it in .env file")
        print("   Add this line to .env:")
        print("   GEMINI_API_KEY=your_api_key_here")
    else:
        for test in test_cases:
            print(f"Input: {test}")
            result = analyze_issue(test)
            print(f"Result: {result}")
            print()
