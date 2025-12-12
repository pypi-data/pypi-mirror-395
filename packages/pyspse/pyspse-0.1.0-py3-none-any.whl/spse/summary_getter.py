"""
SPSE Summary Getter
Retrieves summary documents from SPSE tender announcement pages
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


class SPSESummaryGetter:
    """Handles summary document retrieval from SPSE announcement pages"""
    
    def __init__(self, cookie_manager, output_base=None, category=None):
        """
        Initialize summary getter with cookie manager
        
        Args:
            cookie_manager: SPSECookieManager instance with valid session
        """
        self.base_url = SPSE_BASE_URL
        self.session = cookie_manager.get_session()
        self.output_base = Path(output_base) if output_base else Path('.')
        self.paths = build_paths(category or DEFAULT_CATEGORY)
    
    def get_summary_document(self, nomor_pengadaan, endpoint_type='tender'):
        """
        Get summary document link from tender announcement page
        
        Args:
            nomor_pengadaan: Tender identification number
            endpoint_type: 'tender' or 'nontender'
        
        Returns:
            dict: Summary document information or None if not found
        """
        url_path_map = {
            'tender': self.paths["tender_path"],
            'nontender': self.paths["nontender_path"],
        }
        url_path = url_path_map.get(endpoint_type, self.paths["tender_path"])
        
        try:
            url = f"{self.base_url}{url_path}/{nomor_pengadaan}{SPSE_DETAIL_SUFFIX}"
            
            logging.debug(f"Fetching summary from: {url}")
            
            headers = {
                'Referer': f"{self.base_url}{url_path}"
            }
            
            response = self.session.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            summary_row = None
            for tr in soup.find_all('tr'):
                th = tr.find('th', class_='bgwarning')
                if th and 'Uraian Singkat Pekerjaan' in th.get_text():
                    summary_row = tr
                    break
            
            if not summary_row:
                logging.warning("Summary document row not found")
                return None
            
            td = summary_row.find('td')
            if not td:
                logging.warning("Summary document cell not found")
                return None
            
            link = td.find('a', href=True)
            if not link:
                logging.warning("Summary document link not found")
                return None
            
            doc_url = str(link['href'])
            doc_title = str(link.get('title', '')).strip()
            doc_name = link.get_text(strip=True).replace('\xa0', ' ')
            
            if doc_name.startswith(''):
                doc_name = doc_name[1:].strip()
            
            if doc_url.startswith('/'):
                doc_url = f"{self.base_url}{doc_url}"
            
            summary_info = {
                'nomor_pengadaan': nomor_pengadaan,
                'document_name': doc_name,
                'document_title': doc_title,
                'download_url': doc_url,
                'page_url': url
            }
            
            logging.debug(f"Summary document found: {doc_name}")
            
            return summary_info
            
        except Exception as e:
            logging.error(f"Error fetching summary: {str(e)}")
            return None
    
    def download_summary_document(self, summary_info, save_path=None):
        """
        Download summary document to file (follows redirects automatically)
        
        Args:
            summary_info: Dictionary with document information
            save_path: Directory to save the file
        
        Returns:
            str: Path to downloaded file or None if failed
        """
        try:
            download_url = summary_info.get('download_url')
            doc_name = summary_info.get('document_name', 'summary.pdf')
            nomor_pengadaan = summary_info.get('nomor_pengadaan', 'unknown')
            
            if not download_url:
                logging.error("No download URL provided")
                return None
            
            download_dir = Path(save_path) if save_path else self.output_base / 'summary'
            download_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"{nomor_pengadaan}.pdf"
            filepath = download_dir / filename
            
            logging.debug(f"Downloading summary for: {nomor_pengadaan}")
            
            response = self.session.get(
                download_url,
                timeout=REQUEST_TIMEOUT * 3,
                allow_redirects=True,
                stream=True
            )
            
            response.raise_for_status()
            
            content_type = response.headers.get('Content-Type', '')
            if 'application/pdf' not in content_type and 'application/octet-stream' not in content_type:
                logging.warning(f"Content-Type is {content_type}, expected PDF")
            
            total_size = 0
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        total_size += len(chunk)
            
            logging.info(f"Downloaded: {filepath} ({total_size:,} bytes)")
            
            return str(filepath)
            
        except Exception as e:
            logging.error(f"Error downloading document: {str(e)}")
            return None
