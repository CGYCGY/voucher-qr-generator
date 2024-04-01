import os
from configparser import ConfigParser

# Import Tkinter-related modules conditionally
try:
    import tkinter as tk
    from tkinter import filedialog
except ImportError:
    tk = None
    filedialog = None

from PIL import Image
from reportlab.lib.pagesizes import A4, A3, portrait, landscape
from reportlab.pdfgen import canvas


# Function to resize and arrange images on A4 or A3 paper
def resize_and_arrange_images(images_folder, output_folder, output_pdf, max_height_cm=1.5,
                              pdf_page_size='A4', orientation='portrait'):
    # Define page size based on orientation and pdf_page_size
    if pdf_page_size.upper() == 'A3':
        if orientation == 'landscape':
            page_size = landscape(A3)
        else:
            page_size = portrait(A3)
    else:
        if orientation == 'landscape':
            page_size = landscape(A4)
        else:
            page_size = portrait(A4)

    width, height = page_size

    # Create a new PDF file in the printing folder
    output_path = os.path.join(output_folder, output_pdf)
    c = canvas.Canvas(output_path, pagesize=page_size)

    # List all files in the images folder
    files = os.listdir(images_folder)
    files.sort(key=lambda x: os.path.getctime(os.path.join(images_folder, x)))

    # Convert max_height_cm to points (1 cm = 28.35 points)
    max_height = max_height_cm * 28.35

    # Initialize position variables
    position_x, position_y = 0, height - max_height

    # Loop through each image file
    for count, file in enumerate(files, 1):
        if file.endswith(".jpg") or file.endswith(".png"):
            print(f'{count}: Adding {file}')
            # Open the image file
            img = Image.open(os.path.join(images_folder, file))

            # Resize the image to the specified height
            ratio = max_height / float(img.size[1])
            new_width = int(float(img.size[0]) * float(ratio))
            img = img.resize((new_width, int(max_height)), Image.Resampling.LANCZOS)

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


def generate():
    # read config
    config = ConfigParser()
    config.read('config.ini')
    max_height_cm = config.getfloat('printing', 'voucher_height')
    voucher_folder = config.get('printing', 'voucher_folder')
    pdf_folder = config.get('printing', 'pdf_folder')
    pdf_name = config.get('printing', 'pdf_name')
    pdf_name = f'{pdf_name}.pdf'
    pdf_page_size = config.get('printing', 'pdf_page_size')
    orientation = config.get('printing', 'pdf_orientation')

    resize_and_arrange_images(voucher_folder, pdf_folder, pdf_name, max_height_cm, pdf_page_size, orientation)


if __name__ == "__main__":
    if tk is not None:
        # Tkinter-related code here (if needed)
        pass
    else:
        # Script is running without Tkinter (e.g., as an executable)
        generate()  # Call the generate function directly
