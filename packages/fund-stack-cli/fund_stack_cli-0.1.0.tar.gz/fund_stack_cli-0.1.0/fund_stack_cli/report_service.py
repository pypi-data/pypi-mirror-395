from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
import json

console = Console()

def generate_report(transactions, budget_status, year, month):
    """Generate a monthly financial report using Gemini (official google-genai client)."""

    from google import genai
    client = genai.Client(api_key="AIzaSyD1lxc2pXIQATjRr77EVhDacgo9qGinNk8")

    # Clean prompt
    prompt = f"""
Create a user-friendly monthly financial report.

MONTH: {year}-{str(month).zfill(2)}

### TRANSACTIONS (JSON) ###
{json.dumps(transactions, indent=2)}

### BUDGET STATUS (JSON) ###
{json.dumps(budget_status, indent=2)}

### REQUIRED OUTPUT ###
1. Total Income
2. Total Expenses
3. Category-wise Spending Summary
4. Overspending alerts
5. Savings estimate
6. Recommendations for next month

Write in clean human-friendly language with bullet points.
"""

    # Animated loading spinner
    with Live(Spinner("dots", text="Generating monthly AI report..."), refresh_per_second=10):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
        except Exception as e:
            return f"❌ Gemini API Error:\n{str(e)}"

    # Safely extract response text
    try:
        result = response.text
        if not result:
            return "❌ Gemini returned an empty response."
        return result

    except Exception as e:
        return f"❌ Failed to extract text from Gemini response:\n{e}"
