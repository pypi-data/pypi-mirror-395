"""
BRVMpy Indices Scraper
Scrapes market indices data from BRVM
"""

import pandas as pd
from datetime import datetime
from brvmpy.scraper import BRVMScraper


def get_indices():
    """
    Scrape market indices data from BRVM
    
    URL: https://www.brvm.org/en/indices
    
    Returns:
        DataFrame with indices data including:
        - INDEX_NAME: Name of the index
        - VALUE: Current index value
        - CHANGE: Point change
        - CHANGE_PERCENT: Percentage change
        - UPDATE_DATE: Date of extraction
        - ID: Unique identifier
    """
    url = "https://www.brvm.org/en/indices"
    
    with BRVMScraper() as scraper:
        # Load the page
        if not scraper.load_page(url):
            return pd.DataFrame()
        
        # Extract table data
        data = scraper.extract_table()
        
        if not data:
            print("No data found on indices page")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Typical indices table: Name, Value, Change, Change%
        if len(df.columns) >= 4:
            df.columns = [
                'INDEX_NAME',
                'VALUE',
                'CHANGE',
                'CHANGE_PERCENT'
            ][:len(df.columns)]
        elif len(df.columns) >= 2:
            df.columns = ['INDEX_NAME', 'VALUE'] + [f'COL_{i}' for i in range(2, len(df.columns))]
        
        # Clean numeric fields
        numeric_fields = ['VALUE', 'CHANGE', 'CHANGE_PERCENT']
        
        for field in numeric_fields:
            if field in df.columns:
                df[field] = (
                    df[field]
                    .astype(str)
                    .str.replace(' ', '', regex=False)
                    .str.replace(',', '.', regex=False)
                    .str.replace('%', '', regex=False)
                    .str.replace('+', '', regex=False)  # Remove + sign
                )
                
                df[field] = pd.to_numeric(df[field], errors='coerce')
        
        # Add metadata
        today = datetime.now().strftime('%Y-%m-%d')
        df['UPDATE_DATE'] = today
        
        # Create ID
        if 'INDEX_NAME' in df.columns:
            df['ID'] = (
                df['INDEX_NAME']
                .astype(str)
                .str.replace(' ', '_', regex=False)
                + '-' + df['UPDATE_DATE']
            )
        else:
            df['ID'] = df.index.astype(str) + '-' + df['UPDATE_DATE']
        
        # Remove empty rows
        df = df.dropna(how='all')
        
        return df


if __name__ == "__main__":
    # Test the scraper
    print("Scraping BRVM Indices data...")
    df = get_indices()
    print(f"\nFound {len(df)} indices")
    print("\nData:")
    print(df)
