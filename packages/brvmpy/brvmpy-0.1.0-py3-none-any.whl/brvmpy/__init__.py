"""
BRVMpy - BRVM Financial Data Scraper
======================================

A Python package for scraping financial data from the BRVM 
(Bourse Régionale des Valeurs Mobilières) website.

Scrapes data for:
- Actions (Stocks)
- Obligations (Bonds)
- Indices (Market Indices)
- Volumes (Trading Volumes)

Returns clean Pandas DataFrames ready for analysis.

Example:
    >>> import brvmpy
    >>> 
    >>> # Get actions (stocks) data
    >>> stocks = brvmpy.get('actions')
    >>> 
    >>> # Get indices data
    >>> indices = brvmpy.get('indices')
    >>> 
    >>> # Get all data types
    >>> all_data = brvmpy.get_all()

Author: Idriss Badolivier
Email: idrissbadoolivier@gmail.com
"""

from brvmpy.actions import get_actions
from brvmpy.obligations import get_obligations
from brvmpy.indices import get_indices
from brvmpy.volumes import get_volumes

__version__ = '0.1.0'
__author__ = 'Idriss Badolivier'
__email__ = 'idrissbadoolivier@gmail.com'

__all__ = [
    'get',
    'get_all',
    'get_actions',
    'get_obligations',
    'get_indices',
    'get_volumes'
]


def get(data_type):
    """
    Unified entry point for scraping BRVM data
    
    Args:
        data_type (str): Type of data to scrape
            - 'actions': Stock market data
            - 'obligations': Bonds data
            - 'indices': Market indices
            - 'volumes': Trading volumes
    
    Returns:
        pandas.DataFrame: Scraped and cleaned data
    
    Raises:
        ValueError: If data_type is not valid
    
    Example:
        >>> import brvmpy
        >>> stocks = brvmpy.get('actions')
        >>> print(f"Found {len(stocks)} stocks")
    """
    data_type = data_type.lower().strip()
    
    if data_type == 'actions':
        return get_actions()
    elif data_type == 'obligations':
        return get_obligations()
    elif data_type == 'indices':
        return get_indices()
    elif data_type == 'volumes':
        return get_volumes()
    else:
        raise ValueError(
            f"Invalid data_type: '{data_type}'. "
            "Valid options: 'actions', 'obligations', 'indices', 'volumes'"
        )


def get_all():
    """
    Get all BRVM data types in a single call
    
    Returns:
        dict: Dictionary with keys 'actions', 'obligations', 'indices', 'volumes'
              Each value is a pandas DataFrame
    
    Example:
        >>> import brvmpy
        >>> data = brvmpy.get_all()
        >>> print(f"Stocks: {len(data['actions'])}")
        >>> print(f"Indices: {len(data['indices'])}")
    """
    return {
        'actions': get_actions(),
        'obligations': get_obligations(),
        'indices': get_indices(),
        'volumes': get_volumes()
    }


# Convenience: allow direct import
# from brvmpy import get_actions, get_obligations, etc.
