import qrcode
from PIL import Image
import requests
from io import BytesIO
import os

def generate_qr_with_logo(url):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Fetch favicon.ico
    favicon_url = url.rstrip('/') + '/assets/images/favicon.ico'
    response = requests.get(favicon_url)
    if response.status_code == 200:
        favicon = Image.open(BytesIO(response.content))
        # Resize the favicon
        favicon = favicon.resize((100, 100), Image.LANCZOS)
        # Calculate the position to paste the favicon
        pos = ((qr_img.size[0] - favicon.size[0]) // 2, (qr_img.size[1] - favicon.size[1]) // 2)
        qr_img.paste(favicon, pos)

    # Save the QR code image
    qr_img.save('qrcode_with_logo.png')

# call function
my_url = os.getenv("MY_URL")
generate_qr_with_logo(my_url)
