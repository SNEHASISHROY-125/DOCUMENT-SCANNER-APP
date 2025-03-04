"""
This module provides functions to generate various types of barcodes and QR codes.

Functions:
    generate_ean13_barcode(data: str, output: str) -> None
        Generates an EAN-13 barcode from the provided 12-digit data and saves it to the specified output file.
        Parameters:
            data (str): A 12-digit string representing the EAN-13 barcode data.
            output (str): The file path where the generated barcode image will be saved.
        Raises:
            ValueError: If the provided data is not 12 digits long.
            Exception: If an error occurs during barcode generation.

    generate_code128_barcode(data: str, output: str) -> None
        Generates a Code 128 barcode from the provided data and saves it to the specified output file.
        Parameters:
            data (str): A string representing the Code 128 barcode data.
            output (str): The file path where the generated barcode image will be saved.
        Raises:
            Exception: If an error occurs during barcode generation.

    generate_upc_barcode(data: str, output: str) -> None
        Generates a UPC-A barcode from the provided 11-digit data and saves it to the specified output file.
        Parameters:
            data (str): An 11-digit string representing the UPC-A barcode data.
            output (str): The file path where the generated barcode image will be saved.
        Raises:
            ValueError: If the provided data is not 11 digits long.
            Exception: If an error occurs during barcode generation.

    generate_qr_code(data: str, output: str) -> None
        Generates a QR code from the provided data and saves it to the specified output file.
        Parameters:
            data (str): A string representing the QR code data.
            output (str): The file path where the generated QR code image will be saved.
        Raises:
            Exception: If an error occurs during QR code generation.

Usage:
    This module can be run as a standalone script to generate example barcodes and QR codes with predefined data.
    Example:


"""

'''
EAN-13 Barcode
    EAN-13 stands for "European Article Number" and is a 13-digit barcode standard.
    It is widely used internationally for marking products often sold at retail points of sale.
    The barcode consists of 12 digits of data and a single check digit.
    The first two or three digits usually represent the country code, followed by the manufacturer code, product code, and a check digit.
UPC Barcode
UPC stands for "Universal Product Code" and is a barcode symbology used in the United States and Canada.
The most common version is UPC-A, which consists of 12 digits.
Similar to EAN-13, it includes a manufacturer code, product code, and a check digit.
UPC barcodes are used for tracking trade items in stores.
Code 128 Barcode
Code 128 is a high-density linear barcode symbology.
It can encode all 128 ASCII characters, making it versatile for various applications.
Code 128 is used in logistics and transportation industries for tracking items through the supply chain.
It is also used in healthcare and other industries where a large amount of data needs to be encoded in a small space.

'''



from io import BytesIO
from barcode import EAN13, Code128, UPCA
from barcode.writer import ImageWriter
import qrcode
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def get_time() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")

def generate_ean13_barcode(data, output=''):
    if len(data) != 12:
        raise ValueError("EAN-13 data must be 12 digits long")
    try:
        output = output if output else f'src/ean13_barcode_{get_time()}.png'
        ean = EAN13(data, writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        with open(output, 'wb') as f:
            f.write(buffer.getvalue())
        buffer.close()
        print(f"EAN-13 barcode saved as {output}")
        return output
    except Exception as e:
        print(f"An error occurred while generating EAN-13 barcode: {e}")

def generate_code128_barcode(data, output=''):
    try:
        output = output if output else f'src/code128_barcode_{get_time()}.png'
        code128 = Code128(data, writer=ImageWriter())
        buffer = BytesIO()
        code128.write(buffer)
        with open(output, 'wb') as f:
            f.write(buffer.getvalue())
        buffer.close()
        print(f"Code 128 barcode saved as {output}")
        return output
    except Exception as e:
        print(f"An error occurred while generating Code 128 barcode: {e}")

def generate_upc_barcode(data, output=''):
    if len(data) != 11:
        raise ValueError("UPC-A data must be 11 digits long")
    try:
        output = output if output else f'src/upc_barcode_{get_time()}.png'
        upc = UPCA(data, writer=ImageWriter())
        buffer = BytesIO()
        upc.write(buffer)
        with open(output, 'wb') as f:
            f.write(buffer.getvalue())
        buffer.close()
        print(f"UPC-A barcode saved as {output}")
        return output
    except Exception as e:
        print(f"An error occurred while generating UPC-A barcode: {e}")

def generate_qr_code(data, description='',output='') -> str:
    try:
        output = output if output else f'src/qr/qr_code_{get_time()}.png'
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        img = img.convert("RGBA")
        width, height = img.size
        # Add description
        if description:
            new_height = height + 50  # Add space for description
            new_img = Image.new("RGBA", (width, new_height), "WHITE")
            new_img.paste(img, (0, 0))

            draw = ImageDraw.Draw(new_img)
            font = ImageFont.load_default()
            text_bbox = draw.textbbox((0, 0), description, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_position = ((width - text_width) // 2, height + 10)
            draw.text(text_position, description, fill="black", font=font)
            img = new_img

        # Save image to buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        with open(output, 'wb') as f:
            f.write(buffer.getvalue())
        buffer.close()
        print(f"QR Code saved as {output}")
        return output
    except Exception as e:
        print(f"An error occurred while generating QR Code: {e}")

# if __name__ == "__main__":
#     ean13_data = "123456782023"  # Example data for EAN-13 (12 digits)
#     code128_data = "ABC123456789"  # Example data for Code 128
#     upc_data = "12345678901"  # Example data for UPC-A (11 digits)
#     qr_data = "https://example.com"  # Example data for QR Code

#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

#     generate_ean13_barcode(ean13_data, f'src/ean13_barcode_{datetime.now().strftime("%Y%m%d%H%M%S")}.png')
#     generate_code128_barcode(code128_data, f'src/code128_barcode_{datetime.now().strftime("%Y%m%d%H%M%S")}.png')
#     generate_upc_barcode(upc_data, f'src/upc_barcode_{datetime.now().strftime("%Y%m%d%H%M%S")}.png')
#     generate_qr_code(qr_data, f'src/qr/qr_code_{datetime.now().strftime("%Y%m%d%H%M%S")}.png')


import segno , os ,shutil , tempfile
from urllib.request import urlopen
import certifi
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO



def generate_custom_qr(data, description='', output='', scale=10, light=(255, 255, 255,), dark=(217, 37, 217,), border=1) -> str:
    '''
    Generate a custom QR code with a description.
    '''
    try:
        output = output if output else f'src/qr/qr_code_{get_time()}.png'
        # Generate QR code with segno
        qr = segno.make(data)
        
        # Convert QR code to Pillow image
        buffer = BytesIO()
        qr.save(buffer, kind='png', scale=scale, dark=dark, light=light, border=border)
        buffer.seek(0)
        img = Image.open(BytesIO(buffer.getvalue()))

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
# generate_custom_qr("https://example.com", "SExample QR Code 125 89", output='I9segno_custom_qr_code.png', scale=10, border=1, dark=(217, 37, 217,))


from kivymd.icon_definitions import md_icons
from PIL import Image, ImageDraw , ImageSequence

def generate_custom_qr_icon(data, description='', output='', scale=10, light=(255, 255, 255), dark=(0, 0, 0), border=1, icon_name=None , info_text_color=(36, 56, 237,) , info_text_back_color="WHITE",icon_color=(238, 252, 40,),micro:bool=False) -> str:
    '''
    Generate a custom QR code with an Icon and description
    '''
    try:
        output = output if output else f'src/qr/qr_code_{get_time()}.png'
        # Generate QR code with segno
        qr = segno.make(data,micro=micro)
    
        # Convert QR code to Pillow image
        buffer = BytesIO()
        qr.save(buffer, kind='png', scale=scale, dark=dark, light=light, border=border)
        buffer.seek(0)
        img = Image.open(buffer)

        img = img.convert("RGBA")
        width, height = img.size
        # Add description
        if description:
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

        # if micro is True -> skip icon-add
        if not micro:
            # Overlay icon
            if icon_name and icon_name in md_icons:
                icon_char = md_icons[icon_name]
                icon_font_path = "fonts/materialdesignicons-webfont.ttf"  # Path to the Material Design Icons font file
                icon_size = min(width, height) // 5  # Icon size is 1/4th of the QR code size
                icon_font = ImageFont.truetype(icon_font_path, size=icon_size)  # Adjust size as needed

                # Create an image for the icon with a white background
                icon_img = Image.new("RGBA", (icon_size, icon_size), (dark[0],dark[1],dark[2],255,)) # icon back-ground color
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
        print(data,description,output,scale,light,dark,border,icon_name,info_text_color,info_text_back_color,icon_color)
        print(f"An error occurred while generating QR Code: {e}")

def generate_animated_qr_code(data:str,file_:str) -> str:
    '''
    file_:str -> path to the raw image file
    data:str -> data to be encoded in the qr code
    '''
    qrcode = segno.make(data, error='h')
    # self.status = "10"
    if os.path.isfile(file_):
        print('yes a file', file_)
        # determine the file type
        try:
            with Image.open(file_) as img:
                    image_format = img.format.lower()
                    if not file_.endswith(".gif"): output = file_ + '.' + image_format
                    else : output = file_
        except Exception as e: 
            print('The file is not a valid image.', e)
            return
        qrcode.to_artistic(background=file_, target=output, scale=10)
        # self.status = "50"
    else: 
        print('no a file')
        return
    try:
        if  image_format == 'gif':
            with Image.open(output) as gif:
                frames = []
                
                # Process each frame
                for frame in ImageSequence.Iterator(gif):
                    # Ensure the frame is in the same mode as the original GIF
                    processed_frame = frame.copy()
                    
                    # Optional: If transparency needs normalization
                    if processed_frame.mode == "P":
                        palette = processed_frame.getpalette()
                        transparency_index = processed_frame.info.get('transparency', None)
                        
                        if transparency_index is not None:
                            # Replace transparency index with a solid color if needed
                            processed_frame = processed_frame.convert("RGBA")
                            transparent_color = (255, 255, 255, 0)  # White with full transparency
                            new_frame = Image.new("RGBA", gif.size, transparent_color)
                            new_frame.paste(processed_frame, (0, 0), processed_frame)
                            processed_frame = new_frame.convert("P", palette=Image.ADAPTIVE)
                            processed_frame.putpalette(palette)
                    
                    frames.append(processed_frame)
                save_as = output
                # Save the processed GIF with consistent palette
                frames[0].save(
                    save_as,
                    save_all=True,
                    append_images=frames[1:],
                    loop=0,
                    duration=gif.info.get("duration", 100),
                    disposal=2  # Proper disposal method
                )
                # self.status = "100"
                # 
        else: save_as = output
        # copyfile(save_as, output)
        qr_lives_at = f'src/qr/animated_qr_code_{get_time()}' + '.' + image_format
        shutil.copyfile(save_as, qr_lives_at)
        return qr_lives_at
    except Exception as e:
        print('The file is not a valid image.\n' "error", e)
        return

def _verify_and_fetch_from_url(url:str) -> list[str,str]:
    '''
    [``bg_file_path:str``, ``raw_file_path:str``]
    '''
    # Download the image from the URL
    # url = 'https://ci3.googleusercontent.com/meips/ADKq_Nb8AgH6eOB3xeD5UFQEwsIuzmY8x9ngEA63u62xOr82ptFtVfPSz7Nb6UmgBJ8YXbvmEhhKKevYWSFL4gj2MCjlSaV66UiZtkbCv2y4RqcDyUkWeBmxnDWygWmckGwaJ-bF5z2nDIWXpAIIZRtCzL1cty_7uK6vZKXb=s0-d-e1-ft#https://m.media-amazon.com/images/G/01/outbound/OutboundTemplates/Amazon_logo_US._BG255,255,255_.png'
    try:
        # url = inpt.children[-1].text
        response = urlopen(url, cafile=certifi.where())
        response_content = response.read()
    except Exception as e: 
        print(url,'Error:', e)
        return
    # create temp AImage source
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(response_content)
        bg_file_path = tmp_file.name
        tmp_file.close()
    # create temp rawImage source
    with tempfile.NamedTemporaryFile(delete=False) as raw_tmp_file:
        raw_tmp_file.write(response_content)
        raw_tmp_file.close()
    # release resources
        response_content = None
        
        name = raw_tmp_file.name

    # Check if the file exists
    if os.path.isfile(bg_file_path):
        print('yes a file', bg_file_path)
        
        # Determine the file type using Pillow
        try:
            with Image.open(bg_file_path) as img:
                image_format = img.format.lower()
                if image_format in ['gif', 'png', 'jpg', 'jpeg']:
                    print(f'The file is a valid image of type: {image_format}')
                    if image_format == 'gif':
                        # Open and process the GIF
                        with Image.open(bg_file_path) as gif:
                            frames = []
                
                            # Process each frame
                            for frame in ImageSequence.Iterator(gif):
                                # Ensure the frame is in the same mode as the original GIF
                                processed_frame = frame.copy()
                                
                                # Optional: If transparency needs normalization
                                if processed_frame.mode == "P":
                                    palette = processed_frame.getpalette()
                                    transparency_index = processed_frame.info.get('transparency', None)
                                    
                                    if transparency_index is not None:
                                        # Replace transparency index with a solid color if needed
                                        processed_frame = processed_frame.convert("RGBA")
                                        transparent_color = (255, 255, 255, 0)  # White with full transparency
                                        new_frame = Image.new("RGBA", gif.size, transparent_color)
                                        new_frame.paste(processed_frame, (0, 0), processed_frame)
                                        processed_frame = new_frame.convert("P", palette=Image.ADAPTIVE)
                                        processed_frame.putpalette(palette)
                                
                                frames.append(processed_frame)
                            # Save the reprocessed GIF with normalized transparency
                            frames[0].save(
                                bg_file_path+".gif",
                                save_all=True,
                                append_images=frames[1:],
                                loop=0,
                                duration=gif.info.get("duration", 100),  # Retain original frame duration
                                disposal=2,  # Properly dispose of previous frames
                            )
                            source = bg_file_path+".gif"
                    else: source = bg_file_path
                    # change Imge source
                    # self.AImage.source = source
                    # print('raw file:', self.rawImage)
                    return [source, name]
                else:
                    print('The file is not a valid image.')
                    # set default source
                    # self.AImage.source = ""
        except Exception as e:
            print('Error processing the image:', e)
            return []
    else:
        print('no a file')

# Example usage
# generate_custom_qr("https://example.com", "Example QR Code", output='segno_custom_qr_code.png', scale=10, border=1, dark=(217, 37, 217,), icon_name='cog')
# Example usage
# generate_custom_qr("https://example.com", "Example QR Code", output='XXsegno_custom_qr_code.png', scale=10, border=1, dark=(217, 37, 217,),)
# Example usage
# generate_custom_qr_icon("example.com",micro=True, description="https://example.com/id=pol?9800", output='IXsegno_custom_qr_code.png', scale=10, border=1, dark=(217, 37, 217,), icon_name='twitch', info_text_color=(36, 56, 237,), info_text_back_color="WHITE", icon_color=(238, 252, 40,))

