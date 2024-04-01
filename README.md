# Voucher QR Code Generator

This script generates QR codes with auto-generated serial codes, overlays them onto a voucher template based on user configurations, uploads them to Google Drive, and saves the codes with their links to a Google Spreadsheet.

## Steps
1. Install [Python 3.11](https://www.python.org/downloads/release/python-3118) and [Poetry](https://python-poetry.org/docs/#installation).
2. [Setup Poetry environment](https://python-poetry.org/docs/managing-environments).
3. Run `poetry install`.
4. Clone config.ini.example to `config.ini`.
5. Fill in `serial_code`, `qr_code`, `voucher_count`, `google_drive` and `google_spreadsheet`.
6. Fill in `google_form` if wanna generate Google Form link and saved it in QR code. **(Optional)**
7. Run `main.py`.