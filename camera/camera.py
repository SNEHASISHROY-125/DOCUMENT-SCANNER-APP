from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.toast import toast
import cv2
from plyer import camera

KV = """
BoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        title: "Cross-Platform Camera App"
        elevation: 10
        md_bg_color: app.theme_cls.primary_color
        left_action_items: [["menu", lambda x: None]]

    Image:
        id: img_preview
        allow_stretch: True
        keep_ratio: False
        size_hint: 1, 1

    MDRaisedButton:
        text: "Capture Image"
        pos_hint: {"center_x": 0.5}
        on_release: app.capture_image()
"""

class CrossPlatformCameraApp(MDApp):
    def build(self):
        self.is_android = platform == "android"
        self.capture = None
        if not self.is_android:
            # For desktop, initialize OpenCV
            self.capture = cv2.VideoCapture(0)
            Clock.schedule_interval(self.update_frame, 1.0 / 30.0)  # 30 FPS

        return Builder.load_string(KV)

    def update_frame(self, dt):
        """Update the Image widget with frames from OpenCV (Desktop only)."""
        if self.capture:
            ret, frame = self.capture.read()
            if ret:
                # Convert frame to texture
                buffer = cv2.flip(frame, 0).tostring()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.root.ids.img_preview.texture = texture

    def capture_image(self):
        """Handle image capture based on platform."""
        if self.is_android:
            # Use Plyer on Android
            filepath = "/storage/emulated/0/Download/captured_image.jpg"
            try:
                camera.take_picture(filepath, self.on_picture_taken)
            except Exception as e:
                toast(f"Error: {e}")
        else:
            # Use OpenCV on desktop
            if self.capture:
                ret, frame = self.capture.read()
                if ret:
                    filepath = "captured_image.jpg"
                    cv2.imwrite(filepath, frame)
                    self.root.ids.img_preview.source = filepath
                    toast(f"Image saved to {filepath}")
                else:
                    toast("Failed to capture image!")

    def on_picture_taken(self, filepath):
        """Callback for Plyer's camera on Android."""
        if filepath:
            toast(f"Image saved to {filepath}")
            self.root.ids.img_preview.source = filepath
        else:
            toast("Failed to take picture!")

    def on_stop(self):
        """Release resources when the app stops."""
        if self.capture:
            self.capture.release()

if __name__ == "__main__":
    CrossPlatformCameraApp().run()
