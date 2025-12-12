# CLI Documentation

The Command Line Interface (CLI) is the primary way users interact with FundStack.

## Menu Structure

### Unauthenticated Menu
1. **Register**: Create a new account.
   - Prompts: Name, Age, Phone, PAN, Email, Password.
2. **Login**: Access an existing account.
   - Prompts: Email, Password.
3. **Exit**: Close the application.

### Authenticated Menu
3. **Logout**: End the current session.
4. **Wallets → Create Wallet**: Open a new wallet (e.g., "Travel Fund").
5. **Wallets → List Wallets**: View all wallets and their balances.
6. **Wallets → Wallet Details**: View specific details of a single wallet.
7. **Wallets → Deposit**: Add money to a wallet.
8. **Wallets → Withdraw**: Spend money from a wallet.
9. **Wallets → Transfer**: Move money between wallets.
10. **Budget → Set Monthly Budget**: Set a limit for a category (e.g., "Food").
11. **Budget → View Budget Status**: See how much you've spent vs your limit.
12. **Reports → Generate Monthly Report**: Request an AI analysis of your month.
13. **Exit**: Close the application.

## Input Validation
The CLI includes robust validation for user inputs:
- **Name**: Alphabets only, min 2 chars.
- **Age**: 16-100.
- **Phone**: Numeric, 10+ digits.
- **PAN**: Standard format (ABCDE1234F).
- **Email**: Basic format check.
- **Password**: Min 6 chars.

## Technologies Used
- **Rich**: For beautiful terminal output (tables, panels, colors).
- **Getpass**: For secure password entry.
