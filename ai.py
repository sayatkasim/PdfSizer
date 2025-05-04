from PIL import Image, ImageFilter

def extend_image_to_fit_page(img, target_width, target_height):
    img_width, img_height = img.size
    img_ratio = img_width / img_height
    target_ratio = target_width / target_height

    if abs(img_ratio - target_ratio) < 0.01:
        return img  # Oranlar uyumluysa işlem yapma

    if img_ratio > target_ratio:
        # Yüksekliği uzat
        new_height = int(img_width / target_ratio)
        top_pad = (new_height - img_height) // 2
        extended = Image.new("RGB", (img_width, new_height), (0, 0, 0))
        blur_strip = img.crop((0, 0, img_width, 1)).resize((img_width, top_pad))
        blur_strip = blur_strip.filter(ImageFilter.GaussianBlur(20))
        extended.paste(blur_strip, (0, 0))  # üst
        extended.paste(img, (0, top_pad))
        extended.paste(blur_strip, (0, top_pad + img_height))  # alt
    else:
        # Genişliği uzat
        new_width = int(img_height * target_ratio)
        side_pad = (new_width - img_width) // 2
        extended = Image.new("RGB", (new_width, img_height), (0, 0, 0))
        blur_strip = img.crop((0, 0, 1, img_height)).resize((side_pad, img_height))
        blur_strip = blur_strip.filter(ImageFilter.GaussianBlur(20))
        extended.paste(blur_strip, (0, 0))  # sol
        extended.paste(img, (side_pad, 0))
        extended.paste(blur_strip, (side_pad + img_width, 0))  # sağ

    return extended
