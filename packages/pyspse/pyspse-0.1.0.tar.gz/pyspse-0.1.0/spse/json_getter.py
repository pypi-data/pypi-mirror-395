"""
SPSE JSON Data Getter
Retrieves JSON data from SPSE DataTables API
"""

from urllib.parse import urlencode
import logging
from pathlib import Path
from .config import (
    SPSE_BASE_URL,
    SPSE_JSON_HEADERS,
    REQUEST_TIMEOUT,
    build_paths,
    DEFAULT_CATEGORY
)


class SPSEJsonGetter:
    """Handles JSON data retrieval from SPSE DataTables API"""
    
    def __init__(self, cookie_manager, output_base=None, category=None):
        """
        Initialize JSON getter with cookie manager
        
        Args:
            cookie_manager: SPSECookieManager instance with valid session
        """
        self.base_url = SPSE_BASE_URL
        self.session = cookie_manager.get_session()
        self.spse_session_cookie = cookie_manager.spse_session_cookie
        self.authenticity_token = self._extract_authenticity_token()
        self.output_base = Path(output_base) if output_base else Path('.')
        self.paths = build_paths(category or DEFAULT_CATEGORY)
    
    def _extract_authenticity_token(self):
        """Extract authenticity token from SPSE_SESSION cookie"""
        if self.spse_session_cookie and '___AT=' in self.spse_session_cookie:
            parts = self.spse_session_cookie.split('___AT=')
            if len(parts) > 1:
                token = parts[1].split('&')[0]
                return token
        return None
    
    def _build_datatables_params(self, draw=1, start=0, length=25, search='', order_column=5, order_dir='desc'):
        """
        Build DataTables POST parameters
        
        Args:
            draw: DataTables draw counter
            start: Starting record index
            length: Number of records to return
            search: Search query
            order_column: Column index to order by (default: 5 for date)
            order_dir: Order direction ('asc' or 'desc')
        
        Returns:
            dict: Parameters for POST request
        """
        params = {
            'draw': draw,
            'start': start,
            'length': length,
            'search[value]': search,
            'search[regex]': 'false',
            'order[0][column]': order_column,
            'order[0][dir]': order_dir,
        }
        
        # Add column definitions (0-5)
        for i in range(6):
            params[f'columns[{i}][data]'] = i
            params[f'columns[{i}][name]'] = ''
            params[f'columns[{i}][searchable]'] = 'true' if i != 3 else 'false'
            params[f'columns[{i}][orderable]'] = 'true' if i != 3 else 'false'
            params[f'columns[{i}][search][value]'] = ''
            params[f'columns[{i}][search][regex]'] = 'false'
        
        if self.authenticity_token:
            params['authenticityToken'] = self.authenticity_token
        
        return params
    
    def get_data(self, endpoint_type='tender', tahun=2026, draw=1, start=0, length=25, search=''):
        """
        Get JSON data from SPSE API
        
        Args:
            endpoint_type: 'tender' or 'nontender'
            tahun: Year to fetch data for
            draw: DataTables draw counter
            start: Starting record index
            length: Number of records per page
            search: Search query
        
        Returns:
            dict: JSON response from API or None if failed
        """
        endpoint_map = {
            'tender': self.paths["tender_api"],
            'nontender': self.paths["nontender_api"],
        }
        endpoint = endpoint_map.get(endpoint_type, self.paths["tender_api"])

        referer_map = {
            'tender': f'{SPSE_BASE_URL}{self.paths["tender_path"]}',
            'nontender': f'{SPSE_BASE_URL}{self.paths["nontender_path"]}',
        }
        referer = referer_map.get(endpoint_type, referer_map['tender'])
        
        response = None
        try:
            url = f"{self.base_url}{endpoint}?tahun={tahun}"
            data = self._build_datatables_params(
                draw=draw,
                start=start,
                length=length,
                search=search
            )
            headers = SPSE_JSON_HEADERS.copy()
            headers['Referer'] = referer
            
            logging.debug(f"Requesting: {url}")
            response = self.session.post(
                url,
                data=data,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            # Check if response is HTML (error page)
            if 'text/html' in response.headers.get('Content-Type', ''):
                logging.error("Response is HTML, not JSON; SPSE may be offline or blocking.")
                return None
            
            try:
                json_data = response.json()
            except Exception as e:
                logging.error(f"Failed to parse JSON: {e}")
                if response.headers.get('Content-Encoding') == 'br':
                    import brotli
                    import json
                    try:
                        logging.debug("Attempting manual brotli decompression...")
                        decompressed = brotli.decompress(response.content)
                        json_data = json.loads(decompressed.decode('utf-8'))
                        logging.info("Manual brotli decompression successful")
                    except Exception as e2:
                        logging.error(f"Manual brotli decompression failed: {e2}")
                        return None
                else:
                    return None
            
            data_count = len(json_data.get('data', []))
            logging.info(f"Data retrieved: {data_count} records")
            
            self._save_json(json_data, endpoint_type, tahun, search)
            
            return json_data
            
        except Exception as e:
            logging.error(f"Error fetching data: {str(e)}")
            if response:
                logging.debug(f"Response text (first 500 chars): {response.text[:500]}")
            return None
    
    def _save_json(self, json_data, endpoint_type, tahun, search=''):
        """Save JSON data to file"""
        import json
        from datetime import datetime
        
        try:
            json_dir = self.output_base / 'json'
            json_dir.mkdir(exist_ok=True, parents=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            search_suffix = f"_{search.replace(' ', '_')}" if search else ''
            filename = f"spse_{endpoint_type}_{tahun}{search_suffix}_{timestamp}.json"
            filepath = json_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            logging.info(f"JSON saved: {filepath}")
        except Exception as e:
            print(f"Warning: Failed to save JSON: {e}")
