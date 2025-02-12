from kivy.app import App
import qrcode
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty
from kivy.metrics import dp
import time, threading
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class QRWidget(Widget):
    light_color = ListProperty([1, 1, 1, 1])  # Default light color (white)
    dark_color = ListProperty([0, 0, 0, 1])   # Default dark color (black)

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.matrix = self.generate_matrix(data)
        self.bind(size=self.update_canvas)
        self.bind(light_color=self.update_canvas)
        self.bind(dark_color=self.update_canvas)

    def generate_matrix(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr.get_matrix()

    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.matrix:
            return

        rows = len(self.matrix)
        cols = len(self.matrix[0]) if rows > 0 else 0
        if cols == 0:
            return

        # Calculate module size while maintaining aspect ratio
        widget_ratio = self.width / self.height
        qr_ratio = cols / rows

        if widget_ratio > qr_ratio:
            module_height = self.height / rows
            module_width = module_height
        else:
            module_width = self.width / cols
            module_height = module_width

        # Center the QR code in the widget
        x_offset = (self.width - (cols * module_width)) / 2
        y_offset = (self.height - (rows * module_height)) / 2

        with self.canvas:
            # Light background
            Color(*self.light_color)
            Rectangle(pos=self.pos, size=self.size)

            # Dark modules
            Color(*self.dark_color)
            for i, row in enumerate(self.matrix):
                for j, module in enumerate(row):
                    if module:
                        x = x_offset + j * module_width
                        y = y_offset + (rows - i - 1) * module_height
                        Rectangle(
                            pos=(x, y),
                            size=(module_width, module_height)
                        )

    def set_light_color(self, color):
        self.light_color = color

    def set_dark_color(self, color):
        self.dark_color = color

class QRCodeApp(App):
    qr = None
    def build(self):
        qr_widget = QRWidget("https://github.com/unsplash/unsplash")
        qr_widget.set_light_color([1, 1, 1, 1])  # Set light color to white
        qr_widget.set_dark_color([0, 0, 0, 1])   # Set dark color to black
        self.qr = qr_widget
        self.r()
        box = BoxLayout( orientation='vertical')
        box.add_widget(Label(text="QR Code"))
        box.add_widget(qr_widget)
        return box
    def _(self):
        time.sleep(5)
        self.qr.set_dark_color([.1, .2, .6, 1])
    def _st(self):	
        Clock.schedule_once(lambda x: self._() , 1)
    def r(self):
        threading.Thread(target=self._st).start()

if __name__ == '__main__':
    QRCodeApp().run()