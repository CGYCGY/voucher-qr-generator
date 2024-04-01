import os
import pickle
import random
import string
from configparser import ConfigParser

import pyqrcode
from PIL import Image
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


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


# Overlay QR code image onto the base image at the specified position and size
def overlay_qr_code(config: ConfigParser, base_image_path, qr_code_path, output_image_path):
    size_x = config.getint('qr_code', 'size_x')
    size_y = config.getint('qr_code', 'size_y')
    position_x = config.getint('qr_code', 'position_x')
    position_y = config.getint('qr_code', 'position_y')

    base_image = Image.open(base_image_path)
    qr_code = Image.open(qr_code_path)

    # Resize the QR code image to the specified size
    qr_code = qr_code.resize((size_x, size_y))

    # Paste the QR code image onto the base image at the specified position
    base_image.paste(qr_code, (position_x, position_y))

    # Save the resulting image to the output path
    base_image.save(output_image_path)

    print(f'QR code overlaid on the base image and saved to {output_image_path}')


# Authenticate with OAuth2 and return the credentials
def authenticate(scopes):
    """Authenticate with OAuth2 and return the credentials."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes=scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


# Upload file to Google Drive and get the sharable link
def upload_to_drive(credentials, file_path, folder_id, file_name):
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()

    # Get the sharable link
    file_url = file.get('webViewLink')
    return file_url


# Write Serial Number, Price, QR code, and Google Form link to the Google Sheet
def write_to_sheet(credentials, config: ConfigParser, template_rows, base_image_folder, output_image_folder):
    qr_folder_id = config.get('google_drive', 'qr_folder_id')  # QR code folder ID in Google Drive
    total_num_rows = 0
    record_log = []
    for template, num_rows in template_rows.items():
        base_image_path = f'{base_image_folder}/{template}.jpg'  # Set the base image path dynamically
        # Extract price from template name
        price = int(template.split('_')[-1])

        for _ in range(num_rows):
            serial_number = generate_serial_code(config)
            qr = pyqrcode.create(serial_number)
            qr_filename = f'qr_code_{serial_number}.png'  # Save QR code locally
            qr.png(f'qrcode/{qr_filename}', scale=8, quiet_zone=1)  # Generate QR code as PNG file

            # Overlay QR code onto base image and save
            output_image_path = f'{output_image_folder}/{template}_{serial_number}.jpg'
            overlay_qr_code(config, base_image_path, f'qrcode/{qr_filename}', output_image_path)

            # Upload overlay QR code to Google Drive and get the sharable link
            overlay_qr_url = upload_to_drive(credentials, output_image_path, qr_folder_id,
                                             output_image_path.split('/')[-1])

            total_num_rows += 1

        record = f'{num_rows} rows for {template} uploaded to Google Drive.'
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

# Authenticate and add rows for each template to the sheet
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
creds = authenticate(SCOPES)
template_rows = {
    'voucher_50': voucher_50_count,
    'voucher_100': voucher_100_count,
    'voucher_300': voucher_300_count,
    'voucher_1000': voucher_1000_count,
    'voucher_5000': voucher_5000_count
}
base_image_folder = 'template'  # Folder where base images are stored
output_image_folder = 'voucher'  # Folder where output images will be saved
write_to_sheet(creds, CONFIG, template_rows, base_image_folder, output_image_folder)
