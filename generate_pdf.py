import os
from configparser import ConfigParser

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

            # Calculate position for the next image
            if position_x + new_width > width:
                position_x = 0
                position_y -= max_height
                if position_y < 0:
                    c.showPage()
                    position_y = height - max_height

            # Draw the image on the canvas
            c.drawInlineImage(img, position_x, position_y, width=new_width, height=max_height)
            position_x += new_width

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
    pdf_page_size = config.get('printing', 'pdf_page_size')
    orientation = config.get('printing', 'pdf_orientation')
    pdf_name = config.get('printing', 'pdf_name')
    pdf_name = f'{pdf_name}_{pdf_page_size}_{orientation}.pdf'

    resize_and_arrange_images(voucher_folder, pdf_folder, pdf_name, max_height_cm, pdf_page_size, orientation)


if __name__ == "__main__":
    generate()
