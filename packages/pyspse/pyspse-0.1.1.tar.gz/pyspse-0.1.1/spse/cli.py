import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
from .cookie_manager import SPSECookieManager
from .json_getter import SPSEJsonGetter
from .summary_getter import SPSESummaryGetter
from .detail_getter import SPSEDetailGetter
from .category_resolver import list_categories, search_categories
from .config import DEFAULT_CATEGORY


def main():
    parser = argparse.ArgumentParser(description='SPSE Data Getter')
    parser.add_argument(
        'type',
        nargs='?',
        choices=['tender', 'nontender'],
        help='Tipe pengadaan: tender atau nontender'
    )
    parser.add_argument(
        '--category', '-C',
        type=str,
        default=None,
        help='Slug kategori (segment URL) mis. nasional, padang, latihan'
    )
    parser.add_argument(
        '--list-categories',
        action='store_true',
        help='Tampilkan daftar kategori (slug + nama) lalu keluar'
    )
    parser.add_argument(
        '--search-category',
        type=str,
        default=None,
        help='Cari kategori berdasarkan nama/slug (case-insensitive) lalu keluar'
    )
    parser.add_argument(
        '--tahun', '-T',
        type=int,
        default=datetime.now().year,
        help='Tahun data yang akan diambil (default: tahun sekarang)'
    )
    parser.add_argument(
        '--length', '-L',
        type=int,
        default=25,
        help='Jumlah data per halaman (default: 25)'
    )
    parser.add_argument(
        '--start', '-S',
        type=int,
        default=0,
        help='Index awal data (default: 0)'
    )
    parser.add_argument(
        '--search', '-Q',
        type=str,
        default='',
        help='Query pencarian untuk nama paket (contoh: "komputer" atau "note book")'
    )
    parser.add_argument(
        '--mode', '-M',
        choices=['data', 'all'],
        default='data',
        help='Mode pengambilan: data (extract detail ke CSV) atau all (termasuk download dokumen summary)'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Level log'
    )
    
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level), format='[%(levelname)s] %(message)s')

    # Handle category listing/search then exit
    if args.list_categories:
        for item in list_categories():
            print(f"{item.get('newUrlPath','')}: {item.get('name','')}")
        return 0
    if args.search_category:
        results = search_categories(args.search_category)
        if not results:
            print("Tidak ditemukan kategori yang cocok")
            return 1
        for item in results:
            print(f"{item.get('newUrlPath','')}: {item.get('name','')}")
        return 0

    if not args.type:
        parser.error("type is required (tender|nontender) unless listing/searching categories")

    output_base = Path('.')
    category_slug = args.category or DEFAULT_CATEGORY
    category_base = output_base / category_slug
    category_base.mkdir(parents=True, exist_ok=True)
    
    cookie_manager = SPSECookieManager()
    cookie_manager.get_spse_session_cookie(args.type, category=category_slug)
    
    logging.debug(f"isset_cookies (SPSE_SESSION): {cookie_manager.is_spse_session_set()}")
    
    if cookie_manager.is_spse_session_set():
        json_getter = SPSEJsonGetter(cookie_manager, output_base=category_base, category=category_slug)
        
        data = json_getter.get_data(
            endpoint_type=args.type,
            tahun=args.tahun,
            start=args.start,
            length=args.length,
            search=args.search
        )
        
        if data:
            search_info = f" dengan query '{args.search}'" if args.search else ""
            logging.info(f"Berhasil mengambil data tahun {args.tahun}{search_info}")
            
            logging.info("=== Extracting Detail Data ===")
            detail_getter = SPSEDetailGetter(cookie_manager, output_base=category_base, category=category_slug)
            
            records = data.get('data', [])
            total = len(records)
            details_list = []
            
            for idx, record in enumerate(records, 1):
                nomor_pengadaan = record[0] if len(record) > 0 else None
                
                if not nomor_pengadaan:
                    continue
                
                logging.debug(f"[{idx}/{total}] Processing: {nomor_pengadaan}")
                
                detail_data = detail_getter.get_detail_data(
                    nomor_pengadaan,
                    args.type
                )
                
                if detail_data:
                    details_list.append(detail_data)
                    logging.debug("  Detail extracted")
                else:
                    logging.warning("  Detail not found")
            
            if details_list:
                csv_path = detail_getter.save_details_to_csv(
                    details_list,
                    args.type,
                    args.tahun,
                    args.search,
                    save_path=category_base / 'detail'
                )
                logging.info("=== Extract Detail ===")
                logging.info(f"Total: {total} | Success: {len(details_list)} | Failed: {total - len(details_list)}")
            else:
                logging.warning("=== Extract Detail ===")
                logging.warning("No detail data extracted")
            
            if args.mode == 'all':
                logging.info("=== Downloading Summary Documents ===")
                summary_getter = SPSESummaryGetter(cookie_manager, output_base=category_base, category=category_slug)
                
                records = data.get('data', [])
                total = len(records)
                success_count = 0
                fail_count = 0
                
                for idx, record in enumerate(records, 1):
                    nomor_pengadaan = record[0] if len(record) > 0 else None
                    
                    if not nomor_pengadaan:
                        continue
                    
                    logging.debug(f"[{idx}/{total}] Processing: {nomor_pengadaan}")
                    
                    summary_info = summary_getter.get_summary_document(
                        nomor_pengadaan,
                        args.type
                    )
                    
                    if summary_info:
                        filepath = summary_getter.download_summary_document(summary_info)
                        if filepath:
                            success_count += 1
                        else:
                            fail_count += 1
                    else:
                        logging.warning("  Summary not found")
                        fail_count += 1
                
                logging.info("=== Download Summary ===")
                logging.info(f"Total: {total} | Success: {success_count} | Failed: {fail_count}")
        else:
            logging.error("Gagal mengambil data")
            return 1
    else:
        logging.error("Gagal mendapatkan cookie, tidak bisa mengambil data")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
