import segno
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def generate_custom_qr(data, description='', output='qr_code.png', scale=10, light=(255, 255, 255,), dark=(217, 37, 217,), border=1):
    '''
    Generate a custom QR code with a description.
    '''
    try:
        # Generate QR code with segno
        qr = segno.make(data)
        
        # Convert QR code to Pillow image
        buffer = BytesIO()
        qr.save(buffer, kind='png', scale=scale, dark=dark, light=light, border=border)
        buffer.seek(0)
        img = Image.open(buffer)

        # Add description
        if description:
            img = img.convert("RGBA")
            width, height = img.size
            new_height = height + 30  # Add space for description
            new_img = Image.new("RGBA", (width, new_height), "WHITE")
            new_img.paste(img, (0, 0))

            draw = ImageDraw.Draw(new_img)
            max_width = width - 20  # Maximum width for the text box
            font_size = 10  # Starting font size
            font_path = "fonts/Arial.ttf"  # Path to the TrueType font file

            # Adjust font size to fit within the text box
            while True:
                font = ImageFont.truetype(font_path, font_size)
                text_bbox = draw.textbbox((0, 0), description[:60], font=font)
                text_width = text_bbox[2] - text_bbox[0]
                if text_width <= max_width or font_size <= 20:
                    break
                font_size -= 1

            text_position = ((width - text_width) // 2, height + 10)
            draw.text(text_position, description[:60], fill="black", font=font)
            img = new_img

        # Save the processed image to a buffer using Pillow
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Use segno's save method to apply customizations and save the final image
        with open(output, 'wb') as f:
            f.write(buffer.getvalue())

        print(f"QR Code saved as {output}")
        return output
    except Exception as e:
        print(f"An error occurred while generating QR Code: {e}")

# Example usage
# generate_custom_qr("https://example.com", "SExample QR Code 125 89", output='segno_custom_qr_code.png', scale=10, border=1, dark=(217, 37, 217,))


from kivymd.icon_definitions import md_icons

def generate_custom_qr_icon(data, description='', output='qr_code.png', scale=10, light=(255, 255, 255), dark=(0, 0, 0), border=1, icon_name=None , info_text_color=(36, 56, 237,) , info_text_back_color="WHITE",icon_color=(238, 252, 40,)):
    '''
    Generate a custom QR code with an Icon and description
    '''
    try:
        # Generate QR code with segno
        qr = segno.make(data)
        
        # Convert QR code to Pillow image
        buffer = BytesIO()
        qr.save(buffer, kind='png', scale=scale, dark=dark, light=light, border=border)
        buffer.seek(0)
        img = Image.open(buffer)

        # Add description
        if description:
            img = img.convert("RGBA")
            width, height = img.size
            new_height = height + 30  # Add space for description
            new_img = Image.new("RGBA", (width, new_height), info_text_back_color) # text back-ground color
            new_img.paste(img, (0, 0))

            draw = ImageDraw.Draw(new_img)
            max_width = width - 20  # Maximum width for the text box
            font_size = 15  # Starting font size
            font_path = "fonts/Arial.ttf"  # Path to the TrueType font file

            # Adjust font size to fit within the text box
            while True:
                font = ImageFont.truetype(font_path, font_size)
                text_bbox = draw.textbbox((0, 0), description[:60], font=font)
                text_width = text_bbox[2] - text_bbox[0]
                if text_width <= max_width or font_size <= 20:
                    break
                font_size -= 1

            text_position = ((width - text_width) // 2, height + 4) # text pos on white-background
            draw.text(text_position, description[:60], fill=info_text_color, font=font) # text color , font
            img = new_img

        # Overlay icon
        if icon_name and icon_name in md_icons:
            icon_char = md_icons[icon_name]
            icon_font_path = "fonts/materialdesignicons-webfont.ttf"  # Path to the Material Design Icons font file
            icon_font = ImageFont.truetype(icon_font_path, size=50)  # Adjust size as needed
            icon_size = min(width, height) // 5  # Icon size is 1/4th of the QR code size

            # Create an image for the icon with a white background
            icon_img = Image.new("RGBA", (icon_size, icon_size), (255, 255, 255, 235))
            draw_icon = ImageDraw.Draw(icon_img)
            text_bbox = draw_icon.textbbox((0, 0), icon_char, font=icon_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_position = ((icon_size - text_width) // 2, (icon_size - text_height) // 2)
            draw_icon.text(text_position, icon_char, font=icon_font, fill=icon_color) # icon color

            # Resize the icon to fit within the QR code
            icon_img = icon_img.resize((icon_size, icon_size), Image.LANCZOS)

            # Overlay the icon on the QR code
            icon_position = ((width - icon_size) // 2, (height - icon_size) // 2)
            img.paste(icon_img, icon_position, icon_img)

        # Save the processed image to a buffer using Pillow
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Use segno's save method to apply customizations and save the final image
        with open(output, 'wb') as f:
            f.write(buffer.getvalue())

        print(f"QR Code saved as {output}")
        return output
    except Exception as e:
        print(f"An error occurred while generating QR Code: {e}")

# Example usage
# generate_custom_qr("https://example.com", "Example QR Code", output='segno_custom_qr_code.png', scale=10, border=1, dark=(217, 37, 217,), icon_name='cog')
# Example usage
# generate_custom_qr("https://example.com", "Example QR Code", output='XXsegno_custom_qr_code.png', scale=10, border=1, dark=(217, 37, 217,),)
# Example usage
generate_custom_qr_icon("https://example.com", description="https://example.com/id=pol?9800", output='IXsegno_custom_qr_code.png', scale=10, border=1, dark=(217, 37, 217,), icon_name='google')