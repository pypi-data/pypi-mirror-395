# Service Documentation

This document provides detailed information about the backend services used in FundStack CLI.

## Authentication Service (`auth_service.py`)
Handles all user identity operations.
- **Functions**:
  - `register_user(email, password, name, age, phone, pan)`: Signs up a new user and creates a profile.
  - `login_user(email, password)`: Authenticates a user and starts a session.
  - `logout_user()`: Clears the local session.
  - `get_session()`: Retrieves current session data.

## Wallet Service (`wallet_service.py`)
The core banking engine of the application.
- **Functions**:
  - `create_wallet(uid, name, currency, initial)`: Creates a new wallet.
  - `list_wallets(uid)`: Returns all wallets for a user.
  - `deposit(uid, wid, amt, note, cat)`: Adds funds to a wallet.
  - `withdraw(uid, wid, amt, note, cat)`: Removes funds from a wallet.
  - `transfer(uid, src, dst, amt, note, cat)`: Moves funds between wallets.
  - `get_all_transactions(uid)`: Aggregates history across all wallets.

## Budget Service (`budget_service.py`)
Manages spending limits.
- **Functions**:
  - `set_budget(uid, year, month, category, limit)`: Defines a spending limit.
  - `compute_budget_status(uid, year, month)`: Calculates spending vs limits.
  - `get_budgets(uid, year, month)`: Retrieves budget configuration.

## Report Service (`report_service.py`)
AI-powered financial analysis.
- **Functions**:
  - `generate_report(transactions, budget_status, year, month)`: Sends data to Gemini AI to generate a text summary of financial health.

## Configuration (`firebase_config.py`)
Contains static configuration for external services.
- **Constants**:
  - `API_KEY`: Google Cloud API Key.
  - `DATABASE_URL`: Firebase Realtime Database URL.
