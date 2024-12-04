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

def generate_qr_code(data, output=''):
    try:
        output = output if output else f'src/qr/qr_code_{get_time()}.png'
        img = qrcode.make(data)
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