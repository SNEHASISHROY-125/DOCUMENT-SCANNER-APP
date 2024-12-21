from kivymd.tools.hotreload.app import MDApp   # hotreload-app
# from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.factory import Factory
import os

#
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty , ListProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.pickers import MDColorPicker
from typing import Union
import threading
from kivymd.uix.card import MDCard
# from kivymd.uix.textfield.textfield #import MDTextField


KV_DIR = os.path.join(os.path.dirname(__file__), "kv")

class CustomCard(MDCard):
    # icon = StringProperty()
    image_source = StringProperty()        

class MainApp(MDApp):
    # KV_FILES = [os.path.join(KV_DIR, kv_file) for kv_file in os.listdir(KV_DIR) if kv_file.endswith(".kv")]
    KV_FILES = [[os.path.join(KV_DIR, "main.kv"),os.path.join(KV_DIR, "UI.kv"),os.path.join('quick_create.kv'),os.path.join('CustomCard.kv')][1]]
    DEBUG = True

    # app-internals
    dialog = None
    show_line = BooleanProperty(False)
    fit_display_source = StringProperty("segno_custom_qr_code.png")
    #
    icon_brush_color = ListProperty([0,1,.2, 1])
    footer_brush_color = ListProperty([0,1,.2, 1])
    qr_code_data = StringProperty("fudemy.me")
    qr_code_description = StringProperty("fudemy.me")
    qr_code_icon = StringProperty("qrcode")
    qr_code_color = ListProperty([0,1,.2, 1])
    qr_code_micro = BooleanProperty(False)
    qr_save_dir = StringProperty("src/qr")

    def build_app(self):  # hotreload-build
    # def build(self):
        global color_picker
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.set_color_to = "icon_brush_color"
        # color_picker.open()
        color_picker.bind(
            # on_select_color=get_color,
            on_release=self.get_selected_color,
        )
        self._init_loading_widget()
        # return Builder.load_file(self.KV_FILES[0])
        self.theme_cls.theme_style = "Dark"
        return Factory.MainScreen()
    
    def _init_loading_widget(self):
        ''' Initialize the loading widget '''
        # init the modal view
        from kivy.uix.modalview import ModalView
        from kivymd.uix.spinner import MDSpinner
        global _modal
        _modal  =   ModalView(size_hint=(.8, .8), auto_dismiss=False, background='', background_color=[0, 0, 0, 0])
        _modal.add_widget(MDSpinner(line_width=dp(5.25), size_hint=(None, None), size=(120, 120), pos_hint={'center_x': .5, 'center_y': .5}, active=True))  # Load and play the GIF
    

    def open_color_picker(self,set_color_to):
        color_picker.set_color_to = set_color_to
        color_picker.open()

    def update_color(self, color: list) -> None: ...
        # self.root.ids.toolbar.md_bg_color = color

    def get_selected_color(
        self,
        instance_color_picker: MDColorPicker,
        type_color: str,
        selected_color: Union[list, str],
    ):
        '''Return selected color.'''
        print(color_picker,color_picker.get_rgb(selected_color))
        # set color to icon_brush_color
        print(selected_color , instance_color_picker.set_color_to)
        _ = selected_color  
        # _ = color_picker.get_rgb(selected_color)
        # TODO: pass it to qr code generator method

        if instance_color_picker.set_color_to == "icon_brush_color":
            app.icon_brush_color = _
        elif instance_color_picker.set_color_to == "footer_brush_color":
            app.footer_brush_color = _
            print(app.icon_brush_color)
        # dissmiss color picker
        instance_color_picker.dismiss()
        
    def get_rgb(self, color: list) -> tuple:
        """Returns an ``RGB`` list of values from 0 to 255."""

        return tuple([
            int(value * 255)
            for value in (color[:-1] if len(color) == 4 else color)
        ])

    def on_select_color(self, instance_gradient_tab, color: list) -> None:
        '''Called when a gradient image is clicked.'''

    def generate_qr_code(self):
        _modal.open()
        def _gen():
            import  test2 as t2# generate_custom_qr_icon
            import time
            time.sleep(1)
            t2.generate_custom_qr_icon(
                self.qr_code_data,
                self.qr_code_description,
                output='src/qr/qr_code.png',
                scale=10,
                light=(255, 255, 255),
                dark=tuple(self.qr_code_color),
                border=1,
                icon_name=self.qr_code_icon,
                info_text_color=self.get_rgb(self.footer_brush_color),
                # info_text_back_color="WHITE",
                icon_color=self.get_rgb(self.icon_brush_color),
                micro=self.qr_code_micro
            )
            print("QR Code Generated",'micro',self.qr_code_micro)
            self.fit_display_source = "qr_code.png"
            _modal.dismiss()
        # Clock.schedule_once(lambda x: threading.Thread(target=_gen).start(), 0.1)
        threading.Thread(target=_gen).start()

# global color_picker
# def get_color(color_picker_instance, selected_color):
    
#     print(color_picker,color_picker.get_rgb(selected_color))
#     # set color to icon_brush_color
#     print(selected_color)
#     _ = selected_color  
#     # _ = color_picker.get_rgb(selected_color)
#     # TODO: pass it to qr code generator method
#     app.icon_brush_color = _
#     print(app.icon_brush_color)
#     # print(selected_color)
#     # print(_)
#     # print(app.icon_brush_color,_.append(1))
#     # color_picker.dismiss()


app = MainApp()
app.run()