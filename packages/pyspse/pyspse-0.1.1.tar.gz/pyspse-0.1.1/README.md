# PySPSE

> Paket & CLI untuk crawl data tender/nontender SPSE (https://spse.inaproc.id/)

[![Version](https://img.shields.io/badge/version-0.1.0-blue)](https://pypi.org/project/pyspse/) [![Python](https://img.shields.io/badge/python-3.9%2B-yellow.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

PySPSE menyediakan CLI dan API Python untuk mengambil data tender dan nontender SPSE Versi Nasional, menyimpan JSON, CSV detail, dan PDF summary.

## DISCLAIMER

PySPSE dibuat mandiri, tanpa hubungan dengan pemilik atau pengelola SPSE. Tujuannya: eksperimen teknis, studi data publik, dan mempermudah pemantauan informasi pengadaan. Dilarang membanjiri atau mengganggu layanan SPSE, dilarang dipakai untuk hal yang melanggar hukum, dan segala risiko serta dampak ditanggung pengguna. Rawat sumber daya publik: pakai secukupnya, santun terhadap beban server, dan patuhi aturan yang berlaku.

# Quickstart

## Pemasangan

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pyspse               # rilis PyPI
# atau untuk pengembangan lokal
pip install -e .
```

CLI terpasang sebagai `pyspse`. Dependensi utama: requests, brotli, beautifulsoup4.

## Penggunaan CLI

```bash
pyspse tender -T 2025 -L 10           # detail tender 2025 → detail/
pyspse nontender -T 2024 -L 25        # detail nontender 2024
pyspse tender -T 2025 -L 50 -S 100    # paging start 100, 50 baris
pyspse tender -T 2025 -L 10 -M all    # plus unduh PDF summary → summary/
pyspse --list-categories              # tampilkan slug kategori yang tersedia
pyspse --search-category "padang"      # cari kategori berisi padang
pyspse tender -C padang -T 2025       # gunakan kategori padang
```

Argumen utama:
- `type`: `tender` | `nontender`
- `-C, --category`: slug kategori (segment URL), default `nasional`
- `--list-categories`: tampilkan seluruh kategori lalu keluar
- `--search-category <term>`: cari kategori berdasar nama/slug lalu keluar
- `-T, --tahun`: tahun data (default: tahun berjalan)
- `-L, --length`: jumlah data per halaman (default 25)
- `-S, --start`: index awal (default 0)
- `-Q, --search`: kata kunci nama paket (opsional)
- `-M, --mode`: `data` (detail→CSV) | `all` (detail + PDF summary)
- `--log-level`: `DEBUG|INFO|WARNING|ERROR` (default `INFO`)

### Tentang kategori
- SPSE punya banyak segmen URL, mis. `https://spse.inaproc.id/padang/lelang`. Gunakan `-C padang` agar request diarahkan ke segmen itu.
- Lihat daftar slug: `pyspse --list-categories | head`. Cari slug: `pyspse --search-category "kemenkeu"`.
- Output otomatis dipisah per kategori: `<kategori>/json`, `<kategori>/detail`, `<kategori>/summary`.

## Penggunaan sebagai Paket

```python
from spse.cookie_manager import SPSECookieManager
from spse.detail_getter import SPSEDetailGetter
from spse.summary_getter import SPSESummaryGetter
from spse.category_resolver import find_by_slug

cookie_manager = SPSECookieManager()
category = "padang"  # slug kategori; default "nasional"
cookie_manager.get_spse_session_cookie('tender', category=category)

detail_getter = SPSEDetailGetter(cookie_manager, category=category)
detail = detail_getter.get_detail_data('10092297000', 'tender')
detail_getter.save_details_to_csv([detail], 'tender', 2025)

summary_getter = SPSESummaryGetter(cookie_manager, category=category)
info = summary_getter.get_summary_document('10092297000', 'tender')
summary_getter.download_summary_document(info)
```

# Struktur Proyek

```
.
├── pyproject.toml           # metadata & entry point CLI
├── spse/                    # paket utama
│   ├── __init__.py
│   ├── cli.py               # CLI (pyspse)
│   ├── config.py            # konfigurasi URL/header/path
│   ├── cookie_manager.py    # sesi & cookie SPSE
│   ├── json_getter.py       # ambil JSON DataTables
│   ├── detail_getter.py     # scrap detail → CSV
│   └── summary_getter.py    # ambil link & unduh PDF summary
├── <kategori>/json/         # log JSON per kategori (default kategori: nasional)
├── <kategori>/detail/       # CSV detail per kategori
└── <kategori>/summary/      # PDF summary per kategori
```

# Format Output

## JSON
- Lokasi: `json/spse_{type}_{tahun}_{timestamp}.json`
- Isi: respon DataTables SPSE.

## CSV Detail
- Lokasi: `detail/spse_{type}_{tahun}_{timestamp}.csv`
- Delimiter: `;`
- Kolom: `nomor_pengadaan` + seluruh field pengumuman dalam snake_case, `alasan_diulang`, `scraped_at`.

## PDF Summary
- Lokasi: `summary/{nomor_pengadaan}.pdf` (mode `-M all`).

# Uninstall

```bash
pip uninstall pyspse
```

# License

MIT
