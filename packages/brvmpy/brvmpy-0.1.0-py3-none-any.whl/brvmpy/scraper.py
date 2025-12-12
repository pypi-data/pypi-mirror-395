"""
BRVMpy Base Scraper
Core scraping functionality for BRVM website
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from brvmpy.utils import get_driver
import time


class BRVMScraper:
    """
    Base scraper class for BRVM website
    Handles page loading, table extraction, and driver management
    """
    
    def __init__(self):
        """Initialize scraper with Chrome driver"""
        self.driver = get_driver()
    
    def load_page(self, url, wait_seconds=5):
        """
        Load a BRVM page and wait for content to render
        
        Args:
            url: URL to load
            wait_seconds: Time to wait for page load (default: 5)
        
        Returns:
            bool: True if page loaded successfully
        """
        try:
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(wait_seconds)
            
            # Wait for table to be present
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            
            return True
        
        except Exception as e:
            print(f"Error loading page {url}: {str(e)}")
            return False
    
    def extract_table(self, selector="table.table tbody tr"):
        """
        Extract table data from current page
        
        Args:
            selector: CSS selector for table rows (default: "table.table tbody tr")
        
        Returns:
            list: List of rows, where each row is a list of cell texts
        """
        try:
            # Find all table rows
            rows = self.driver.find_elements(By.CSS_SELECTOR, selector)
            
            if not rows:
                # Try alternative selector
                rows = self.driver.find_elements(By.CSS_SELECTOR, "tbody tr")
            
            data = []
            
            for row in rows:
                # Get all cells in the row
                cells = row.find_elements(By.TAG_NAME, "td")
                
                if not cells:
                    cells = row.find_elements(By.TAG_NAME, "th")
                
                # Extract text from each cell
                row_data = [cell.text.strip() for cell in cells]
                
                # Only add non-empty rows
                if any(row_data):
                    data.append(row_data)
            
            return data
        
        except Exception as e:
            print(f"Error extracting table: {str(e)}")
            return []
    
    def close(self):
        """Close the browser and quit the driver"""
        try:
            self.driver.quit()
        except:
            pass
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - auto-close driver"""
        self.close()
