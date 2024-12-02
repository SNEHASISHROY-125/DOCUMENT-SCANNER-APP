
'''
SCANNER APP FOR SCANNED DOCUMENTS( PDF )

ADD-ONS:
1. OCR
2. DATA-INPUT SHEET FOR DATA EXTRACTION ( EXEL SHEET ) 
'''

# Import Kivy modules
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.utils import platform




# Import OpenCV
# import cv2 
import datetime
# import numpy as np
# from PIL import Image as PILImage

from kivy.core.window import Window

# default pic (as small review thumbnail)
global default_pic 
global time
# time = datetime.datetime.now()
default_pic = '.ico_not_found.png'

class ImageCaptureApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Create a Camera widget
        self.camera = Camera(resolution=(640, 480), play=True)
        self.layout.add_widget(self.camera)

        # Create a button to capture an image
        capture_btn = Button(text='Capture Image', size_hint=(None, None))
        capture_btn.bind(on_press=self.capture_image)
        self.layout.add_widget(capture_btn)

        # Create an Image widget to display captured images
        self.image_widget = Image()
        self.layout.add_widget(self.image_widget)

        # by default default_pic
        self.image_widget.texture = Image(source= default_pic).texture

        return self.layout

    def capture_image(self, instance):
        # Capture the current frame from the camera
        image_texture = self.camera.texture
        
        if image_texture:
            # Save the captured image to a file
            global time
            time =datetime.datetime.now()
            IMG_name = str(time)[::5] +'.png'  #taking image name upto 5 charectores of date
            image_texture.save(IMG_name)

            # update default pic
            global default_pic
            default_pic = IMG_name
            print('after click default pic',type(default_pic))

            # Load and display the saved image in the Image widget
            saved_image_texture = Image(source= default_pic).texture
            self.image_widget.texture = saved_image_texture

if __name__ == '__main__':
    # Set the window size
    # Window.size = (800, 600)
    if platform == 'android':   
        from plyer import permission
        if permission.check_permission('CAMERA') != 'granted':
            permission.request_permission('CAMERA')
    
    # default_pic = 'captured_image'
    print(default_pic)

    # Run the app
    ImageCaptureApp().run()



        
# # Run the Kivy application
# if __name__ == '__main__':
#     CameraApp().run()
