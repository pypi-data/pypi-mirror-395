"""
Main Entry Point.

This script serves as the entry point for the FundStack CLI application.
It invokes the main event loop from the CLI module.
"""

from .cli import handle_user_choice

if __name__ == "__main__":
    handle_user_choice()
