#!/usr/bin/env python3

import pandas as pd
import os
import sys

def _load_lookup_data(lookup_dir):
    """Load and process JSON card price data from lookup directory."""
    all_lookup_df = []
    
    for filename in os.listdir(lookup_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(lookup_dir, filename)
            
            with open(filepath, 'r') as f:
                data = pd.read_json(f)
            
            df = pd.json_normalize(data['data'])
            
            # Calculate market value: prioritize holofoil, fallback to normal, default to 0
            df['card_market_value'] = df.get('tcgplayer.prices.holofoil.market', 0.0).fillna(
                df.get('tcgplayer.prices.normal.market', 0.0)
            ).fillna(0.0)
            
            df = df.rename(columns={
                'id': 'card_id',
                'name': 'card_name',
                'number': 'card_number',
                'set.id': 'set_id',
                'set.name': 'set_name'
            })
            
            required_cols = ['card_id', 'card_name', 'card_number', 'set_id', 'set_name', 'card_market_value']
            all_lookup_df.append(df[required_cols].copy())
    
    lookup_df = pd.concat(all_lookup_df, ignore_index=True)
    
    lookup_df = lookup_df.sort_values('card_market_value', ascending=False)
    lookup_df = lookup_df.drop_duplicates(subset=['card_id'], keep='first')
    
    return lookup_df

def _load_inventory_data(inventory_dir):
    """Load and process CSV inventory data."""
    inventory_data = []
    
    for filename in os.listdir(inventory_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(inventory_dir, filename)
            df = pd.read_csv(filepath)
            inventory_data.append(df)
    
    if not inventory_data:
        return pd.DataFrame()
    
    inventory_df = pd.concat(inventory_data, ignore_index=True)
    
    inventory_df['card_id'] = (inventory_df['set_id'].astype(str) + '-' + 
                                 inventory_df['card_number'].astype(str))
    
    return inventory_df

def update_portfolio(inventory_dir, lookup_dir, output_file):
    """Main ETL function: merge inventory with lookup data and write portfolio."""
    
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)
    
    # Handle empty inventory
    if inventory_df.empty:
        print("Error: No inventory data found.", file=sys.stderr)
        # Create empty portfolio with headers
        empty_df = pd.DataFrame(columns=['card_name', 'card_id', 'set_name', 'card_market_value', 'index'])
        empty_df.to_csv(output_file, index=False)
        return
    
    if 'card_name' in inventory_df.columns:
        inventory_df = inventory_df.drop(columns=['card_name'])
    
    # Merge inventory with lookup data
    portfolio_df = pd.merge(
        inventory_df,
        lookup_df[['card_id', 'card_name', 'set_name', 'card_market_value']],
        on='card_id',
        how='left'
    )
    
    # Fill missing values
    portfolio_df['card_market_value'] = portfolio_df['card_market_value'].fillna(0.0)
    portfolio_df['set_name'] = portfolio_df['set_name'].fillna('NOT_FOUND')
    portfolio_df['card_name'] = portfolio_df['card_name'].fillna('UNKNOWN')
    
    # Create location index
    portfolio_df['index'] = (portfolio_df['binder_name'].astype(str) + '-' +
                              portfolio_df['page_number'].astype(str) + '-' +
                              portfolio_df['slot_number'].astype(str))
    
    # Select final columns
    final_cols = ['card_name', 'card_id', 'set_name', 'card_market_value', 'index']
    portfolio_df[final_cols].to_csv(output_file, index=False)
    
    print(f"Portfolio successfully written to {output_file}")

def main():
    """Production mode: use production directories and output file."""
    update_portfolio('./card_inventory/', './card_set_lookup/', 'card_portfolio.csv')

def test():
    """Test mode: use test directories and output file."""
    update_portfolio('./card_inventory_test/', './card_set_lookup_test/', 'test_card_portfolio.csv')

if __name__ == "__main__":
    print("Starting ETL Pipeline in Test Mode...", file=sys.stderr)
    test()
