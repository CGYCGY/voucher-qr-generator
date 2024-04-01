import random
import string
from configparser import ConfigParser

import pyqrcode


# Function to generate a random 25-character Serial Number with symbols (-, ., _, ~)
def generate_serial_code(config: ConfigParser):
    lowercase_count = config.getint('serial_code', 'lowercase')
    uppercase_count = config.getint('serial_code', 'uppercase')
    digit_count = config.getint('serial_code', 'digit')
    symbol_count = config.getint('serial_code', 'symbol')
    serial_code_count = lowercase_count + uppercase_count + digit_count + symbol_count

    letters_lower = ''.join(random.choices(string.ascii_lowercase, k=lowercase_count))
    letters_upper = ''.join(random.choices(string.ascii_uppercase, k=uppercase_count))
    digits = ''.join(random.choices(string.digits, k=digit_count))
    symbols = ''.join(random.choices("-._~", k=symbol_count))  # Include symbols in the character set
    all_chars = letters_lower + letters_upper + digits + symbols
    if len(all_chars) < serial_code_count:
        raise ValueError(f'Character sets length is less than {serial_code_count}')
    serial_number = ''.join(random.sample(all_chars, k=serial_code_count))
    return serial_number


# Write Serial Number, Price, QR code, and Google Form link to the Google Sheet
def main(config: ConfigParser, template_rows):
    total_num_rows = 0
    record_log = []
    for template, num_rows in template_rows.items():
        for _ in range(num_rows):
            serial_number = generate_serial_code(config)
            qr = pyqrcode.create(serial_number)
            qr_filename = f'qr_code_{serial_number}.png'  # Save QR code locally
            qr.png(f'qrcode/{qr_filename}', scale=8, quiet_zone=1)  # Generate QR code as PNG file
            total_num_rows += 1

        record = f'{num_rows} rows for {template} generated locally.'
        record_log.append(record)
        print(record)

    print('\nRecord:')
    [print(value) for value in record_log]


# read config
CONFIG = ConfigParser()
CONFIG.read('config.ini')

voucher_50_count = CONFIG.getint('voucher_count', '50')
voucher_100_count = CONFIG.getint('voucher_count', '100')
voucher_300_count = CONFIG.getint('voucher_count', '300')
voucher_1000_count = CONFIG.getint('voucher_count', '1000')
voucher_5000_count = CONFIG.getint('voucher_count', '5000')

template_rows = {
    'voucher_50': voucher_50_count,
    'voucher_100': voucher_100_count,
    'voucher_300': voucher_300_count,
    'voucher_1000': voucher_1000_count,
    'voucher_5000': voucher_5000_count
}
main(CONFIG, template_rows)
