#========================
#FILE: budget_service.py
#========================

"""
Budget Service Module.

This module handles budget-related operations including:
- Setting monthly budgets for specific categories
- Retrieving budget information
- Computing budget status (spent vs limit)
"""

import requests, time
from .firebase_config import DATABASE_URL
from .auth_service import get_session
from .wallet_service import get_all_transactions
from rich.console import Console
console = Console()

def _auth():
    """
    Helper function to retrieve the authentication token for Firebase requests.

    Returns:
        str: query string with auth token if session exists, else empty string.
    """
    session = get_session()
    if not session: return ""
    token = session.get("idToken")
    return f"?auth={token}" if token else ""

def _budget_path(uid, year, month):
    """
    Helper function to construct the database path for a specific month's budget.

    Args:
        uid (str): User ID.
        year (int): Year of the budget.
        month (int): Month of the budget.

    Returns:
        str: The database URL path.
    """
    return f"{DATABASE_URL}/users/{uid}/budgets/{year}/{month}"

def set_budget(uid, year, month, category, limit):
    """
    Sets a budget limit for a specific category in a given month.

    Args:
        uid (str): User ID.
        year (int): Year.
        month (int): Month.
        category (str): Budget category (e.g., 'Food').
        limit (float): The maximum amount allowed for this category.

    Returns:
        bool: True if the budget was successfully set, False otherwise.
    """
    data = {"category": category, "limit": limit, "updated_at": int(time.time())}
    r = requests.put(f"{_budget_path(uid,year,month)}/{category}.json{_auth()}", json=data)
    return r.status_code in (200,204)

def get_budgets(uid, year, month):
    """
    Retrieves all budgets set for a specific month.

    Args:
        uid (str): User ID.
        year (int): Year.
        month (int): Month.

    Returns:
        dict: A dictionary of budgets where keys are categories.
    """
    r = requests.get(f"{_budget_path(uid,year,month)}.json{_auth()}")
    if r.status_code != 200: return {}
    return r.json() or {}

def compute_budget_status(uid, year, month):
    """
    Computes the current status of budgets by comparing limits against actual spending.

    Args:
        uid (str): User ID.
        year (int): Year.
        month (int): Month.

    Returns:
        dict: A dictionary containing budget status for each category.
              Each entry includes limit, spent amount, remaining amount, and status (OK/OVERSPENT).
    """
    budgets = get_budgets(uid, year, month)
    txs = get_all_transactions(uid)

    spending = {}
    for tx in txs:
        t = tx.get("type")
        # Only consider outgoing transactions
        if t not in ["withdrawal","expense","transfer_out"]: continue
        cat = tx.get("category","General")
        amt = float(tx.get("amount",0))
        spending[cat] = spending.get(cat,0) + amt

    result = {}
    for cat, b in budgets.items():
        limit = b["limit"]
        spent = spending.get(cat,0)
        result[cat] = {
            "limit": limit,
            "spent": spent,
            "remaining": limit - spent,
            "status": "OK" if limit-spent >= 0 else "OVERSPENT"
        }
    return result