"""
BRVMpy Volumes Scraper
Scrapes trading volumes data from BRVM
"""

import pandas as pd
from datetime import datetime
from brvmpy.scraper import BRVMScraper


def get_volumes():
    """
    Scrape trading volumes data from BRVM
    
    URL: https://www.brvm.org/en/volumes/0
    
    Returns:
        DataFrame with volume data including:
        - SYMBOL: Stock symbol
        - NAME: Company name
        - VOLUME: Trading volume
        - VALUE: Total value traded
        - TRANSACTIONS: Number of transactions
        - UPDATE_DATE: Date of extraction
        - ID: Unique identifier
    """
    url = "https://www.brvm.org/en/volumes/0"
    
    with BRVMScraper() as scraper:
        # Load the page
        if not scraper.load_page(url):
            return pd.DataFrame()
        
        # Extract table data
        data = scraper.extract_table()
        
        if not data:
            print("No data found on volumes page")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Typical volumes table: Symbol, Name, Volume, Value, Transactions
        if len(df.columns) >= 5:
            df.columns = [
                'SYMBOL',
                'NAME',
                'VOLUME',
                'VALUE',
                'TRANSACTIONS'
            ][:len(df.columns)]
        elif len(df.columns) >= 3:
            df.columns = ['SYMBOL', 'NAME', 'VOLUME'] + [f'COL_{i}' for i in range(3, len(df.columns))]
        
        # Clean numeric fields
        numeric_fields = ['VOLUME', 'VALUE', 'TRANSACTIONS']
        
        for field in numeric_fields:
            if field in df.columns:
                df[field] = (
                    df[field]
                    .astype(str)
                    .str.replace(' ', '', regex=False)
                    .str.replace(',', '.', regex=False)
                    .str.replace('FCFA', '', regex=False)
                )
                
                df[field] = pd.to_numeric(df[field], errors='coerce')
        
        # Add metadata
        today = datetime.now().strftime('%Y-%m-%d')
        df['UPDATE_DATE'] = today
        
        # Create ID
        if 'SYMBOL' in df.columns:
            df['ID'] = df['SYMBOL'].astype(str) + '-' + df['UPDATE_DATE']
        else:
            df['ID'] = df.index.astype(str) + '-' + df['UPDATE_DATE']
        
        # Remove empty rows
        df = df.dropna(how='all')
        
        return df


if __name__ == "__main__":
    # Test the scraper
    print("Scraping BRVM Volumes data...")
    df = get_volumes()
    print(f"\nFound {len(df)} records")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)
