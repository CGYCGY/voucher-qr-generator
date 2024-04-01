import os
from configparser import ConfigParser

from PIL import Image
from reportlab.lib.pagesizes import portrait, landscape, A4
from reportlab.pdfgen import canvas


# Function to resize and arrange images on A4 paper with adjustable orientation
def resize_and_arrange_images(images_folder, output_folder, output_pdf, max_height=3.36, orientation='portrait'):
    # Define page size based on orientation
    if orientation == 'landscape':
        width, height = landscape(A4)
        pagesize = landscape(A4)
    else:
        width, height = portrait(A4)
        pagesize = portrait(A4)

    # Create a new PDF file in the printing folder
    output_path = os.path.join(output_folder, output_pdf)
    c = canvas.Canvas(output_path, pagesize=pagesize)

    # List all files in the images folder
    files = os.listdir(images_folder)
    files.sort(key=lambda x: os.path.getctime(os.path.join(images_folder, x)))

    # Initialize position variables
    position_x, position_y = 0, height

    # Loop through each image file
    for count, file in enumerate(files, 1):
        if file.endswith(".jpg") or file.endswith(".png"):
            print(f'{count}: Adding {file}')
            # Open the image file
            img = Image.open(os.path.join(images_folder, file))

            # Resize the image to the specified height
            new_height = max_height * 37.79527559  # Convert cm to points (1 cm = 37.79527559 points)
            ratio = new_height / float(img.size[1])
            new_width = int(float(img.size[0]) * float(ratio))
            img = img.resize((new_width, int(new_height)), Image.Resampling.LANCZOS)

            # Calculate position for the next image
            if position_x + img.size[0] > width:
                position_x = 0
                position_y -= img.size[1]
                if position_y < 0:
                    c.showPage()
                    position_y = height - img.size[1]

            # Draw the image on the canvas
            c.drawInlineImage(img, position_x, position_y, width=img.size[0], height=img.size[1])
            position_x += img.size[0]

    # Save the PDF file
    c.save()
    print(f'PDF generated and saved to {output_path}')


if __name__ == '__main__':
    # read config
    CONFIG = ConfigParser()
    CONFIG.read('config.ini')
    MAX_HEIGHT = CONFIG.getfloat('printing', 'voucher_height')
    VOUCHER_FOLDER = CONFIG.get('printing', 'voucher_folder')
    PDF_FOLDER = CONFIG.get('printing', 'pdf_folder')
    PDF_NAME = CONFIG.get('printing', 'pdf_name')
    PDF_NAME = f'{PDF_NAME}.pdf'
    ORIENTATION = CONFIG.get('printing', 'pdf_orientation')

    resize_and_arrange_images(VOUCHER_FOLDER, PDF_FOLDER, PDF_NAME, MAX_HEIGHT, ORIENTATION)
