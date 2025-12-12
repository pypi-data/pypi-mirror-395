"""
SPSE Detail Getter
Retrieves detailed information from SPSE tender announcement pages
"""

from bs4 import BeautifulSoup
from pathlib import Path
import logging
from .config import (
    SPSE_BASE_URL,
    REQUEST_TIMEOUT,
    SPSE_DETAIL_SUFFIX,
    build_paths,
    DEFAULT_CATEGORY
)
import re


class SPSEDetailGetter:
    """Handles detailed data retrieval from SPSE announcement pages"""
    
    def __init__(self, cookie_manager, output_base=None, category=None):
        """
        Initialize detail getter with cookie manager
        
        Args:
            cookie_manager: SPSECookieManager instance with valid session
        """
        self.base_url = SPSE_BASE_URL
        self.session = cookie_manager.get_session()
        self.output_base = Path(output_base) if output_base else Path('.')
        self.paths = build_paths(category or DEFAULT_CATEGORY)
    
    def _normalize_field_name(self, field_name):
        """
        Normalize field name to snake_case
        
        Args:
            field_name: Original field name from HTML
        
        Returns:
            str: Normalized field name in snake_case
        """
        # Remove special characters and extra spaces
        normalized = field_name.strip()
        
        # Replace common variations
        normalized = normalized.replace('/', '_')
        normalized = normalized.replace('-', ' ')
        normalized = normalized.replace('?', '')
        normalized = normalized.replace('(', '')
        normalized = normalized.replace(')', '')
        
        # Convert to lowercase and replace spaces with underscore
        normalized = re.sub(r'\s+', '_', normalized.lower())
        
        # Remove multiple underscores
        normalized = re.sub(r'_+', '_', normalized)
        
        # Remove leading/trailing underscores
        normalized = normalized.strip('_')
        
        return normalized
    
    def _clean_html_content(self, html_text):
        """
        Clean HTML content to plain text with newlines preserved
        
        Args:
            html_text: Text that may contain HTML tags
        
        Returns:
            str: Plain text with newlines for better readability
        """
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_text, 'html.parser')
        
        # Replace <br> tags with newline
        for br in soup.find_all('br'):
            br.replace_with('\n')
        
        # Replace block elements with newline
        for tag in soup.find_all(['p', 'div', 'li', 'tr']):
            tag.insert_after('\n')
        
        # Get text
        text = soup.get_text(separator=' ')
        
        # Clean up excessive whitespace but preserve newlines
        lines = text.split('\n')
        cleaned_lines = [re.sub(r'\s+', ' ', line.strip()) for line in lines]
        
        # Remove empty lines and join
        text = '\n'.join(line for line in cleaned_lines if line)
        
        return text
    
    def get_detail_data(self, nomor_pengadaan, endpoint_type='tender'):
        """
        Get detailed data from tender announcement page
        
        Args:
            nomor_pengadaan: Tender identification number
            endpoint_type: 'tender' or 'nontender'
        
        Returns:
            dict: Detailed information or None if failed
        """
        # Map endpoint type to URL path
        url_path_map = {
            'tender': self.paths["tender_path"],
            'nontender': self.paths["nontender_path"],
        }
        url_path = url_path_map.get(endpoint_type, self.paths["tender_path"])
        
        try:
            url = f"{self.base_url}{url_path}/{nomor_pengadaan}{SPSE_DETAIL_SUFFIX}"
            
            logging.debug(f"Fetching detail from: {url}")
            
            # Set referer header
            headers = {
                'Referer': f"{self.base_url}{url_path}"
            }
            
            # Make GET request
            response = self.session.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data from table
            detail_data = {
                'nomor_pengadaan': nomor_pengadaan,
                'url': url
            }
            
            # Find all table rows
            for tr in soup.find_all('tr'):
                th = tr.find('th', class_='bgwarning')
                td = tr.find('td')
                
                if th and td:
                    # Get field name
                    field_name = th.get_text(strip=True)
                    
                    # Normalize field name to snake_case
                    normalized_field_name = self._normalize_field_name(field_name)
                    
                    # Get field value - clean HTML if needed
                    if normalized_field_name in ['syarat_kualifikasi']:
                        field_value = self._clean_html_content(str(td))
                    else:
                        field_value = td.get_text(strip=True).replace('\xa0', ' ')
                    
                    # Store in dictionary
                    detail_data[normalized_field_name] = field_value
            
            logging.debug(f"Detail data extracted: {len(detail_data)} fields")
            
            return detail_data
            
        except Exception as e:
            logging.error(f"Error fetching detail: {str(e)}")
            return None
    
    def save_details_to_csv(self, details_list, endpoint_type, tahun, search='', save_path=None):
        """
        Save multiple detail data to single CSV file with semicolon delimiter
        
        Args:
            details_list: List of dictionaries with detail information
            endpoint_type: 'tender' or 'nontender'
            tahun: Year
            search: Search query (optional)
            save_path: Directory to save the file
        
        Returns:
            str: Path to saved file or None if failed
        """
        import csv
        from datetime import datetime
        
        try:
            if not details_list:
                logging.warning("No detail data to save")
                return None
            
            # Create detail directory
            detail_dir = Path(save_path) if save_path else self.output_base / 'detail'
            detail_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            search_suffix = f"_{search.replace(' ', '_')}" if search else ''
            filename = f"spse_{endpoint_type}_{tahun}{search_suffix}_{timestamp}.csv"
            filepath = detail_dir / filename
            
            # Collect all unique field names from all records
            all_fields = set()
            for detail_data in details_list:
                all_fields.update(detail_data.keys())
            
            # Remove metadata fields
            all_fields.discard('url')
            
            # Ensure fields
            all_fields.add('alasan_diulang')
            all_fields.add('scraped_at')
            
            # Sort fields for consistent column order
            sorted_fields = ['nomor_pengadaan'] + sorted([f for f in all_fields if f != 'nomor_pengadaan'])
            
            # Write CSV with semicolon delimiter
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=sorted_fields, delimiter=';', extrasaction='ignore')
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for detail_data in details_list:
                    row_data = detail_data.copy()
                    row_data.pop('url', None)
                    row_data['scraped_at'] = datetime.now().isoformat()
                    if 'alasan_diulang' not in row_data:
                        row_data['alasan_diulang'] = None
                    writer.writerow(row_data)
            
            print(f"✓ CSV saved to: {filepath} ({len(details_list)} records)")
            
            return str(filepath)
            
        except Exception as e:
            print(f"✗ Error saving CSV: {str(e)}")
            return None
