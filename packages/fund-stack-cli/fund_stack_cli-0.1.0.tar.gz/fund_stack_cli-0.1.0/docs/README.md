# FundStack CLI Documentation

Welcome to the documentation for **FundStack CLI**, a comprehensive personal finance management tool running in your terminal.

## Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Services](#services)

## Project Overview
FundStack CLI allows users to manage their finances directly from the command line. It supports:
- **User Authentication**: Secure signup and login using Firebase Auth.
- **Wallet Management**: Create multiple wallets (Savings, Spending, etc.) and track balances.
- **Transaction Tracking**: Record deposits, withdrawals, and transfers.
- **Budgeting**: Set monthly budgets and track spending against them.
- **AI Reports**: Generate monthly financial insights using Google Gemini AI.

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage
Upon running `python main.py`, you will be presented with an interactive menu.
- **New Users**: Select Option 1 to Register.
- **Existing Users**: Select Option 2 to Login.

Once logged in, you can access all financial features.

## Architecture
The project is structured into modular services:
- `auth_service.py`: Handles user identity.
- `wallet_service.py`: Core logic for wallets and transactions.
- `budget_service.py`: Logic for budget setting and tracking.
- `report_service.py`: AI integration for reporting.
- `cli.py`: The presentation layer handling user input and output.
- `firebase_config.py`: Configuration for backend connections.

For more details, see:
- [Service Documentation](SERVICES.md)
- [CLI Command Reference](CLI.md)
