#!/usr/bin/env python3

import pandas as pd
import os
import sys

def generate_summary(portfolio_file):
    """Generate and print portfolio summary report."""
    
    if not os.path.exists(portfolio_file):
        print(f"Error: Portfolio file '{portfolio_file}' not found.", file=sys.stderr)
        sys.exit(1)
    
    df = pd.read_csv(portfolio_file)
    
    if df.empty:
        print("Portfolio is empty. No cards to report.")
        return
    
    total_portfolio_value = df['card_market_value'].sum()
    
    most_valuable_card = df.loc[df['card_market_value'].idxmax()]
    
    print(f"\nTotal Portfolio Value: ${total_portfolio_value:,.2f}")
    print(f"\nMost Valuable Card:")
    print(f"  Name: {most_valuable_card['card_name']}")
    print(f"  ID: {most_valuable_card['card_id']}")
    print(f"  Value: ${most_valuable_card['card_market_value']:,.2f}\n")

def main():
    """Production mode: use production portfolio file."""
    generate_summary('card_portfolio.csv')

def test():
    """Test mode: use test portfolio file."""
    generate_summary('test_card_portfolio.csv')

if __name__ == "__main__":
    test()
