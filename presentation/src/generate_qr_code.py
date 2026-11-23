import sys

import qrcode

is_web_app = sys.argv[1] == "web" if len(sys.argv) > 1 else False
url_web_app = "https://k4liber.github.io/definit-dsa/"
url_github_repo = "https://github.com/K4liber/definit"
url = url_web_app if is_web_app else url_github_repo
img_name = "web_app_qr_code.png" if is_web_app else "github_repo_qr_code.png"

# Generate the QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Create an image from the QR code
img = qr.make_image(fill_color="black", back_color="white")

# Save the image (e.g., as a PNG)
img.save(img_name)
