'''
TO CONVERT AN IMAGE TO GRAYSCALE
'''

from PIL import Image

def convert_to_grayscale(input_image_path, output_image_path):
    # Open the image
    image = Image.open(input_image_path)
    
    # Convert the image to grayscale
    grayscale_image = image.convert('L')
    
    # Save the grayscale image
    grayscale_image.save(output_image_path)

# Example usage
input_image_path = './test_DOC.png'
output_image_path = './DOC_grayscale.png'

convert_to_grayscale(input_image_path, output_image_path)
