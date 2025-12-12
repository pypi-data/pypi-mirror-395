"""
CLI Interface Module.

This module provides the Command Line Interface for the FundStack application.
It handles:
- User input collection and validation
- Menu display and navigation
- Integration with backend services (Auth, Wallet, Budget, Report)
- Displaying data using Rich tables and panels
"""

from multiprocessing.util import info
import re
import getpass
from .auth_service import register_user, login_user, logout_user, get_session
from .budget_service import compute_budget_status
from .report_service import generate_report
from .wallet_service import (
    create_wallet, list_wallets, get_wallet,
    deposit, withdraw, transfer, get_all_transactions
)
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

console = Console()

# ------------------
# VALIDATION HELPERS
# ------------------

def input_name():
    """
    Prompts user for their full name and validates it.
    
    Returns:
        str: Validated name (only alphabets and spaces, min length 2).
    """
    while True:
        name = Prompt.ask("[bold cyan]Full Name[/]").strip()
        if re.match(r"^[A-Za-z ]{2,}$", name):
            return name
        console.print("[bold red]❌ Invalid name.[/] Use only letters and spaces (min. 2 characters). Try again.")

def input_age():
    """
    Prompts user for their age and validates it.

    Returns:
        str: Validated age (16-100).
    """
    while True:
        age = Prompt.ask("[bold cyan]Age[/]").strip()
        if age.isdigit() and 16 <= int(age) <= 100:
            return age
        console.print("[bold red]❌ Invalid age.[/] Enter a number between 16 and 120.")

def input_phone():
    """
    Prompts user for phone number and validates it.

    Returns:
        str: Validated phone number (numeric, >= 10 digits).
    """
    while True:
        phone = Prompt.ask("[bold cyan]Phone Number[/]").strip()
        if phone.isdigit() and len(phone) >= 10:
            return phone
        console.print("[bold red]❌ Invalid phone number.[/] Must be numeric and at least 10 digits.")

def input_pan():
    """
    Prompts user for PAN number and validates format.

    Returns:
        str: Validated PAN (Format: ABCDE1234F).
    """
    while True:
        pan = Prompt.ask("[bold cyan]PAN[/]").strip().upper()
        if re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", pan):
            return pan
        console.print("[bold red]❌ Invalid PAN format.[/] Expected format: [yellow]ABCDE1234F[/]")

def input_email():
    """
    Prompts user for email and performs basic validation.

    Returns:
        str: Validated email address.
    """
    while True:
        email = Prompt.ask("[bold cyan]Email[/]").strip()
        if "@" in email and "." in email:
            return email
        console.print("[bold red]❌ Invalid email format.[/] Try again.")

def input_password():
    """
    Prompts user for password (hidden input).

    Returns:
        str: Validated password (min 6 chars).
    """
    while True:
        pw = getpass.getpass("🔒 Password (min 6 characters): ").strip()
        if len(pw) >= 6:
            return pw
        console.print("[bold red]❌ Password too short.[/] Try again.")

# --------------------------------------------------------------------
# MENU DISPLAY
# --------------------------------------------------------------------

def show_menu():
    """
    Displays the main menu options based on the user's login state.
    """
    session = get_session()

    console.print("\n[bold cyan]========================[/]")
    console.print("[bold cyan]      FUNDSTACK CLI       [/]")
    console.print("[bold cyan]========================[/]\n")

    if session:
        console.print(f"[green]Logged in as →[/] [bold]{session.get('email')}[/]\n")
        console.print("[bold yellow]3.[/] Logout")
        console.print("[bold yellow]4.[/] Wallets → Create Wallet")
        console.print("[bold yellow]5.[/] Wallets → List Wallets")
        console.print("[bold yellow]6.[/] Wallets → Wallet Details")
        console.print("[bold yellow]7.[/] Wallets → Deposit")
        console.print("[bold yellow]8.[/] Wallets → Withdraw")
        console.print("[bold yellow]9.[/] Wallets → Transfer")
        console.print("[bold yellow]10.[/] Budget → Set Monthly Budget")
        console.print("[bold yellow]11.[/] Budget → View Budget Status")
        console.print("[bold yellow]12.[/] Reports → Generate Monthly Report (Gemini AI)")
        console.print("[bold yellow]13.[/] Exit\n")
    else:
        console.print("[bold yellow]1.[/] Register")
        console.print("[bold yellow]2.[/] Login")
        console.print("[bold yellow]3.[/] Exit\n")

    console.print("[bold cyan]===================================[/]")


def require_login_session():
    """
    Checks if a user session exists.

    Returns:
        dict or None: Session data if logged in, else None.
    """
    session = get_session()
    if not session:
        console.print("[bold red]⚠ You must login first to access wallet features.[/]")
        return None
    return session

# --------------------------------------------------------------------
# MAIN HANDLER
# --------------------------------------------------------------------

def handle_user_choice():
    """
    Main application loop.
    Handles user input and routes to appropriate service functions.
    """
    while True:
        show_menu()
        session = get_session()

        # --------------------------------------------------
        # NOT LOGGED IN MODE
        # --------------------------------------------------
        if not session:
            choice = Prompt.ask("[bold cyan]Select an option (1-3)[/]").strip()

            if choice == "1":
                console.print(Panel.fit("📝 SECURE REGISTRATION", style="bold green"))
                name = input_name()
                age = input_age()
                phone = input_phone()
                pan = input_pan()
                email = input_email()
                pw = input_password()

                register_user(email, pw, name, age, phone, pan)

            elif choice == "2":
                console.print(Panel.fit("🔐 LOGIN", style="bold blue"))
                email = Prompt.ask("[bold cyan]Email[/]").strip()
                pw = getpass.getpass("🔒 Password: ").strip()
                login_user(email, pw)

            elif choice == "3":
                console.print("[bold magenta]👋 Goodbye![/]")
                break

            else:
                console.print("[bold red]❌ Invalid option. Try again.[/]")
                continue

        # --------------------------------------------------
        # LOGGED IN MODE
        # --------------------------------------------------
        else:
            choice = Prompt.ask("[bold cyan]Select an option (3-13)[/]").strip()
            uid = session["localId"]

            # Logout
            if choice == "3":
                logout_user()

            # Create wallet
            elif choice == "4":
                console.print(Panel.fit("💼 CREATE WALLET", style="bold green"))
                name = Prompt.ask("Wallet name (e.g., Savings)").strip()
                currency = Prompt.ask("Currency (INR/USD/EUR)", default="INR").strip().upper() or "INR"
                initial = Prompt.ask("Initial balance (optional)", default="").strip()
                try:
                    initial_val = float(initial) if initial else 0.0
                except:
                    console.print("[bold red]❌ Invalid initial balance.[/]")
                    continue

                wid = create_wallet(uid, name, currency, initial_val)
                if wid:
                    console.print(f"[bold green]✔ Wallet created:[/] [yellow]{wid}[/]")
                else:
                    console.print("[bold red]❌ Failed to create wallet.[/]")

            # List wallets
            elif choice == "5":
                console.print(Panel.fit("💰 YOUR WALLETS", style="bold cyan"))
                wallets = list_wallets(uid)
                if not wallets:
                    console.print("[bold red]⚠ No wallets found.[/]")
                else:
                    table = Table(title="Your Wallets", box=box.ROUNDED)
                    table.add_column("Name", style="cyan", no_wrap=True)
                    table.add_column("Currency", style="magenta")
                    table.add_column("Balance", style="green")
                    table.add_column("Wallet ID", style="yellow")

                    for w in wallets:
                        table.add_row(
                            str(w.get("name", "")),
                            str(w.get("currency", "")),
                            str(w.get("balance", 0)),
                            str(w.get("id", ""))
                        )

                    console.print(table)

            # Wallet details
            elif choice == "6":
                wid = Prompt.ask("Enter wallet ID").strip()
                w = get_wallet(uid, wid)
                if not w:
                    console.print("[bold red]❌ Wallet not found.[/]")
                else:
                    console.print(Panel.fit("📄 WALLET DETAILS", style="bold cyan"))
                    for k, v in w.items():
                        console.print(f"[bold]{k}[/]: {v}")

            # Deposit
            elif choice == "7":
                console.print(Panel.fit("💰 DEPOSIT", style="bold green"))
                wid = Prompt.ask("Wallet ID").strip()
                amt = Prompt.ask("Amount").strip()
                cat = Prompt.ask("Category (e.g., Salary, Refund)").strip()
                note = Prompt.ask("Note").strip()

                try:
                    amt_val = float(amt)
                except:
                    console.print("[bold red]❌ Invalid amount.[/]")
                    continue

                ok = deposit(uid, wid, amt_val, note, cat)
                console.print("[bold green]✔ Deposit successful.[/]" if ok else "[bold red]❌ Deposit failed.[/]")

            # Withdraw
            elif choice == "8":
                console.print(Panel.fit("🧾 WITHDRAW", style="bold yellow"))
                wid = Prompt.ask("Wallet ID").strip()
                amt = Prompt.ask("Amount").strip()
                cat = Prompt.ask("Category (e.g., Food, Shopping)").strip()
                note = Prompt.ask("Note").strip()

                try:
                    amt_val = float(amt)
                except:
                    console.print("[bold red]❌ Invalid amount.[/]")
                    continue

                ok = withdraw(uid, wid, amt_val, note, cat)
                console.print("[bold green]✔ Withdrawal successful.[/]" if ok else "[bold red]❌ Withdrawal failed.[/]")

            # Transfer
            elif choice == "9":
                console.print(Panel.fit("🔁 TRANSFER", style="bold magenta"))
                src = Prompt.ask("From wallet ID").strip()
                dst = Prompt.ask("To wallet ID").strip()
                amt = Prompt.ask("Amount").strip()
                cat = Prompt.ask("Category (Optional)").strip()
                note = Prompt.ask("Note").strip()

                try:
                    amt_val = float(amt)
                except:
                    console.print("[bold red]❌ Invalid amount.[/]")
                    continue

                ok = transfer(uid, src, dst, amt_val, note, cat)
                console.print("[bold green]✔ Transfer complete.[/]" if ok else "[bold red]❌ Transfer failed.[/]")

            # Set Monthly Budget
            elif choice == "10":
                from .budget_service import set_budget
                console.print(Panel.fit("📊 SET MONTHLY BUDGET", style="bold blue"))
                year = int(Prompt.ask("Year (YYYY)"))
                month = int(Prompt.ask("Month (1-12)"))
                category = Prompt.ask("Category").strip()
                limit = float(Prompt.ask("Monthly limit"))
                ok = set_budget(uid, year, month, category, limit)
                console.print("[bold green]✔ Budget saved.[/]" if ok else "[bold red]❌ Failed to save budget.[/]")

            # View Budget Status
            elif choice == "11":
                from .budget_service import compute_budget_status
                console.print(Panel.fit("📊 BUDGET STATUS", style="bold blue"))
                year = int(Prompt.ask("Year"))
                month = int(Prompt.ask("Month (1-12)"))
                status = compute_budget_status(uid, year, month)

                if not status:
                    console.print("[bold yellow]No budgets set for this period.[/]")
                else:
                    table = Table(title=f"Budget Status {year}-{str(month).zfill(2)}", box=box.SIMPLE_HEAVY)
                    table.add_column("Category", style="cyan")
                    table.add_column("Limit", style="magenta")
                    table.add_column("Spent", style="yellow")
                    table.add_column("Remaining", style="green")
                    table.add_column("Status", style="red")

                    for cat, info in status.items():
                        table.add_row(
                            cat,
                            str(info["limit"]),
                            str(info["spent"]),
                            str(info["remaining"]),
                            info["status"]
                        )

                    console.print(table)

            # Generate Monthly Report (Gemini AI)
            elif choice == "12":
                from .report_service import generate_report
                from .budget_service import compute_budget_status

                console.print(Panel.fit("🤖 GEMINI AI MONTHLY REPORT", style="bold magenta"))
                year = int(Prompt.ask("Year"))
                month = int(Prompt.ask("Month (1-12)"))
                txs = get_all_transactions(uid)
                budget = compute_budget_status(uid, year, month)
                console.print("\n[bold cyan]Generating report via Gemini AI...[/]\n")
                result = generate_report(txs, budget, year, month)
                safe_text = result if isinstance(result, str) else str(result)
                console.print(Panel.fit(safe_text, style="bold green"))

            # Exit
            elif choice == "13":
                console.print("[bold magenta]👋 Goodbye![/]")
                break

            else:
                console.print("[bold red]❌ Invalid option.[/]")
                continue
