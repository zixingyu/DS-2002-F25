#!/usr/bin/env python3

import sys
import update_portfolio
import generate_summary

def run_production_pipeline():
    """Execute the complete production pipeline: ETL + Reporting."""
    
    print("=== Starting Production Pipeline ===", file=sys.stderr)
    
    print("\n[1/2] Running ETL: Updating portfolio...", file=sys.stderr)
    update_portfolio.main()
    
    print("\n[2/2] Generating summary report...", file=sys.stderr)
    generate_summary.main()
    
    print("\n=== Production Pipeline Complete ===", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()
