"""
BRVMpy Obligations Scraper
Scrapes bonds (obligations) data from BRVM
"""

import pandas as pd
from datetime import datetime
from brvmpy.scraper import BRVMScraper


def get_obligations():
    """
    Scrape obligations (bonds) data from BRVM
    
    URL: https://www.brvm.org/en/cours-obligations/0
    
    Returns:
        DataFrame with bonds data including:
        - Symbol/Code
        - Name
        - Volume
        - Prices
        - Yield information
        - UPDATE_DATE
        - ID
    """
    url = "https://www.brvm.org/en/cours-obligations/0"
    
    with BRVMScraper() as scraper:
        # Load the page
        if not scraper.load_page(url):
            return pd.DataFrame()
        
        # Extract table data
        data = scraper.extract_table()
        
        if not data:
            print("No data found on obligations page")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Dynamic column naming based on actual data
        # Typical bonds table: Code, Name, Volume, Previous, Current, Yield, etc.
        if len(df.columns) >= 3:
            # First column is usually the bond code
            df.columns = ['CODE', 'NAME'] + [f'COL_{i}' for i in range(2, len(df.columns))]
        
        # Clean numeric fields (any column that looks numeric)
        for col in df.columns:
            if col not in ['CODE', 'NAME']:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(' ', '', regex=False)
                    .str.replace(',', '.', regex=False)
                    .str.replace('%', '', regex=False)
                    .str.replace('FCFA', '', regex=False)
                )
                
                # Try to convert to numeric
                df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Add metadata
        today = datetime.now().strftime('%Y-%m-%d')
        df['UPDATE_DATE'] = today
        
        # Create ID from first column + date
        if 'CODE' in df.columns:
            df['ID'] = df['CODE'].astype(str) + '-' + df['UPDATE_DATE']
        else:
            df['ID'] = df.index.astype(str) + '-' + df['UPDATE_DATE']
        
        # Remove empty rows
        df = df.dropna(how='all')
        
        return df


if __name__ == "__main__":
    # Test the scraper
    print("Scraping BRVM Obligations data...")
    df = get_obligations()
    print(f"\nFound {len(df)} bonds")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nColumns:")
    print(df.columns.tolist())
