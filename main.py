from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
from gui import select_images
from ai import extend_image_to_fit_page

# Boyutlar (inç cinsinden): 8x10, 11x14, 16x20, 18x24, 24x36
sizes = [
    ("8x10", 8 * inch, 10 * inch),
    ("11x14", 11 * inch, 14 * inch),
    ("16x20", 16 * inch, 20 * inch),
    ("18x24", 18 * inch, 24 * inch),
    ("24x36", 24 * inch, 36 * inch)
]

input_folder = select_images   # klasörün adını değiştir
output_folder = "/Users/sayatkasimoglu/Desktop/etsy/7-plane/Image_Set"
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):
    if file.lower().endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(input_folder, file)
        img = Image.open(img_path)

        for name, width, height in sizes:
            img = extend_image_to_fit_page(img, width, height)
            c = canvas.Canvas(os.path.join(output_folder, f"{name}.pdf"), pagesize=(width, height))
            img_width, img_height = img.size
            img_ratio = img_width / img_height
            page_ratio = width / height

            # Görseli sayfa oranına göre merkezle ve boyutlandır
            if img_ratio > page_ratio:
                new_width = width
                new_height = width / img_ratio
            else:
                new_height = height
                new_width = height * img_ratio

            x = (width - new_width) / 2
            y = (height - new_height) / 2
            c.drawImage(img_path, x, y, new_width, new_height)
            c.showPage()
            c.save()
