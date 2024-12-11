import os
import requests
from bs4 import BeautifulSoup

download_folder = r"./favicons/"  # Folder where the favicon will be saved

def download_favicon(url, filename='drcode'):
    '''
    DOWNLOAD's FAVICON FROM WEBSITE
    =======
    '''
    # filename += '.png'
    save_folder = download_folder
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    try:
        # Make an HTTP request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was not successful

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the favicon link tag
        favicon_link = soup.find('link', {'rel': 'icon'})

        if favicon_link and 'href' in favicon_link.attrs:
            favicon_url = favicon_link['href']

            # Download the favicon
            favicon_response = requests.get(favicon_url)
            favicon_response.raise_for_status()  # Raise an exception if the download was not successful

            # Extract the favicon filename from the URL
            if filename:
                favicon_filename = os.path.join(save_folder, filename+'_raw.png')
            else:
                favicon_filename = os.path.join(save_folder, os.path.basename(favicon_url))

            # Save the favicon to the specified folder
            with open(favicon_filename, 'wb') as f:
                f.write(favicon_response.content)

            # Detect the file type and convert to PNG if necessary
            if not favicon_filename.endswith('.png'):
                with Image.open(favicon_filename) as img:
                    if img.format == 'ICO':  # Check if the image format is ICO
                        converted_filename = os.path.splitext(favicon_filename)[0] + '_raw.png'
                        img.save(converted_filename, 'PNG')
                        os.remove(favicon_filename)  # Remove the original ICO file
                        favicon_filename = converted_filename
            
            edit_favicon(input_path= f"{save_folder}/{filename}_raw.png", output_path= f"{save_folder}/{filename}.png" , upscale_factor= 1.2)

            print(f"Favicon downloaded successfully: {favicon_filename}")
            edit_favicon(input_path= f"{save_folder}/{filename}_raw.png", output_path= f"{save_folder}/{filename}_x.png" , upscale_factor= 1.8)
            return f"{save_folder}/{filename}.png"

        else:
            print("Favicon not found on the website. url")
    except Exception as e:
        print(f"An error occurred: {e}")
        try:
            # Directly download the favicon.ico file
            favicon_url = f"{url}/favicon.ico"
            favicon_response = requests.get(favicon_url)
            favicon_response.raise_for_status()  # Raise an exception if the download was not successful

            # Save the favicon to the specified folder
            favicon_filename = os.path.join(save_folder, filename + '_raw.png')
            with open(favicon_filename, 'wb') as f:
                f.write(favicon_response.content)

            edit_favicon(input_path= f"{save_folder}/{filename}_raw.png", output_path= f"{save_folder}/{filename}.png" , upscale_factor= 1.2)

            print(f"Favicon downloaded successfully: {favicon_filename}")
            edit_favicon(input_path= f"{save_folder}/{filename}_raw.png", output_path= f"{save_folder}/{filename}_x.png" , upscale_factor= 1.8)
            return f"{save_folder}/{filename}.png"

        except:
            # print(f"An error occurred: {e}")
            print("Favicon not found on the website. ico")


from PIL import Image

def edit_favicon(input_path, output_path, background_color=(255, 255, 255, 0), target_size=(1414 , 1304), upscale_factor=1.0):
    # Open the input favicon
    with Image.open(input_path) as img:
        # Calculate the new size based on the upscale factor
        new_size = (int(img.width * upscale_factor), int(img.height * upscale_factor))

        # Create a new image with the transparent background and new size
        new_img = Image.new("RGBA", new_size, background_color)

        # Paste the original favicon on the new image (to preserve transparency if the original has one)
        new_img.paste(img, ((new_size[0] - img.width) // 2, (new_size[1] - img.height) // 2), img)

        # Resize the new image to the target size
        new_img = new_img.resize(target_size, Image.LANCZOS)

        # Save the edited favicon to the output path
        new_img.save(output_path)


download_favicon('https://www.facebook.com/login/', 'google')