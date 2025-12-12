"""
BRVMpy Actions Scraper
Scrapes stock (actions) data from BRVM
"""

import pandas as pd
from datetime import datetime
from brvmpy.scraper import BRVMScraper


def get_actions():
    """
    Scrape actions (stocks) data from BRVM
    
    URL: https://www.brvm.org/en/cours-actions/0
    
    Returns:
        DataFrame with columns:
        - SYMBOL: Stock symbol
        - NAME: Company name
        - VOLUME: Trading volume
        - PREVIOUS_PRICE: Previous closing price
        - OPENING_PRICE: Opening price
        - CLOSING_PRICE: Current/closing price
        - CHANGE_PERCENT: Percentage change
        - UPDATE_DATE: Date of data extraction
        - ID: Unique identifier (SYMBOL-DATE)
    """
    url = "https://www.brvm.org/en/cours-actions/0"
    
    with BRVMScraper() as scraper:
        # Load the page
        if not scraper.load_page(url):
            return pd.DataFrame()
        
        # Extract table data
        data = scraper.extract_table()
        
        if not data:
            print("No data found on actions page")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Expected columns (adjust based on actual table structure)
        # Typical BRVM actions table has: Symbol, Name, Volume, Previous, Opening, Closing, Change%
        if len(df.columns) >= 7:
            df.columns = [
                'SYMBOL',
                'NAME',
                'VOLUME',
                'PREVIOUS_PRICE',
                'OPENING_PRICE',
                'CLOSING_PRICE',
                'CHANGE_PERCENT'
            ][:len(df.columns)]
        
        # Clean numeric fields
        numeric_fields = ['VOLUME', 'PREVIOUS_PRICE', 'OPENING_PRICE', 'CLOSING_PRICE', 'CHANGE_PERCENT']
        
        for field in numeric_fields:
            if field in df.columns:
                df[field] = (
                    df[field]
                    .astype(str)
                    .str.replace(' ', '', regex=False)  # Remove spaces
                    .str.replace(',', '.', regex=False)  # Convert comma to dot
                    .str.replace('%', '', regex=False)  # Remove % sign
                    .str.replace('FCFA', '', regex=False)  # Remove currency
                )
                
                # Convert to float, handle errors
                df[field] = pd.to_numeric(df[field], errors='coerce')
        
        # Add metadata columns
        today = datetime.now().strftime('%Y-%m-%d')
        df['UPDATE_DATE'] = today
        df['ID'] = df['SYMBOL'].astype(str) + '-' + df['UPDATE_DATE']
        
        # Remove any completely empty rows
        df = df.dropna(how='all')
        
        return df


if __name__ == "__main__":
    # Test the scraper
    print("Scraping BRVM Actions data...")
    df = get_actions()
    print(f"\nFound {len(df)} stocks")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)
