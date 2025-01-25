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

from kivy.uix.screenmanager import Screen ###
class HomeScreen(Screen):...   
file_list = []

Preview_modal = None
from kivymd.uix.recycleview import MDRecycleView

class CustomRecycleView(MDRecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [
            {
                'image_source': x,
            } for x in file_list
        ]


class MainApp(MDApp):
    # KV_FILES = [os.path.join(KV_DIR, kv_file) for kv_file in os.listdir(KV_DIR) if kv_file.endswith(".kv")]
    KV_FILES = [[os.path.join(KV_DIR, "app.kv"),os.path.join(KV_DIR, "main.kv"),os.path.join('quick_create.kv'),os.path.join('CustomCard.kv')][1]]
    DEBUG = True

    # app-internals
    dialog = None
    animated_info_dialog = None
    micro_info_dialog = None
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
    ### features | animated qr
    gen_btn = BooleanProperty(False)
    web_sync_btn = ... # IconButton
    file_picker_card  = ... # instance of MDCard
    tempUrlFile = StringProperty()
    tempUrlFile_ext = StringProperty()

    def build_app(self):  # hotreload-build
    # def build(self):
        global color_picker
        color_picker = MDColorPicker(size_hint=(None, None), size=(150, 200))
        color_picker.set_color_to = "icon_brush_color"
        # color_picker.open()
        color_picker.bind(
            # on_select_color=get_color,
            on_release=self.get_selected_color,
        )
        self._init_loading_widget()
        # return Builder.load_file(self.KV_FILES[0])
        self.theme_cls.theme_style = "Dark"
        ###
        for root, dirs, files in os.walk('./src'):
            for file in files:
                file_list.append(os.path.join(root, file))

        print(file_list)
        return Factory.AdvancedQRScreen()
    def generate_qr_code_icon(self):
        import time as t
        def _():
            Clock.schedule_once(lambda x: setattr(self ,'gen_btn' ,True), 0.1)
            t.sleep(5)
            Clock.schedule_once(lambda x: setattr(self ,'gen_btn' ,False), 0.1)
        threading.Thread(target=_).start()
    def _verify_and_fetch_from_url(self, url:str):
        # def _validate(url:str):
        from urllib.request import urlopen
        from PIL import Image
        import tempfile
        def _(url):
            # Download the image from the URL
            # url = 'https://ci3.googleusercontent.com/meips/ADKq_Nb8AgH6eOB3xeD5UFQEwsIuzmY8x9ngEA63u62xOr82ptFtVfPSz7Nb6UmgBJ8YXbvmEhhKKevYWSFL4gj2MCjlSaV66UiZtkbCv2y4RqcDyUkWeBmxnDWygWmckGwaJ-bF5z2nDIWXpAIIZRtCzL1cty_7uK6vZKXb=s0-d-e1-ft#https://m.media-amazon.com/images/G/01/outbound/OutboundTemplates/Amazon_logo_US._BG255,255,255_.png'
            try:
                response = urlopen(url)
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(response.read())
                    bg_file_path = tmp_file.name
            except Exception as e:
                print('The URL is not valid.')
                # toast('The URL is not valid.')
                return

            # Check if the file exists
            if os.path.isfile(bg_file_path):
                print('yes a file', bg_file_path)
                
                # Determine the file type using Pillow
                try:
                    with Image.open(bg_file_path) as img:
                        image_format = img.format.lower()
                        if image_format in ['gif', 'png', 'jpg', 'jpeg']:
                            print(f'The file is a valid image of type: {image_format}')
                            # set the image temp property
                            self.tempUrlFile = bg_file_path
                            self.tempUrlFile_ext = image_format
                            # change Imge source
                            Clock.schedule_once(lambda x: setattr(self,"fit_display_source" , bg_file_path), 0.1)
                            # change button state | web_sync | file_picker_card
                            Clock.schedule_once(lambda x: setattr(self.web_sync_btn,"disabled" , False), 0.1)
                            Clock.schedule_once(lambda x: setattr(self.file_picker_card,"disabled" , False), 0.1)
                        else:
                            print('The file is not a valid image.')
                except (IOError, SyntaxError) as e:
                    print('The file is not a valid image.')
                    # change Imge source
                    # Clock.schedule_once(lambda x: setattr(self,"fit_display_source" , bg_file_path), 0.1)
                    # change button state | web_sync | file_picker_card
                    Clock.schedule_once(lambda x: setattr(self.web_sync_btn,"disabled" , False), 0.1)
                    Clock.schedule_once(lambda x: setattr(self.file_picker_card,"disabled" , False), 0.1)
            else:
                print('no a file')
        threading.Thread(target=_,args=(url,)).start()
    
    def _init_loading_widget(self):
        ''' Initialize the loading widget '''
        # init the modal view
        from kivy.uix.modalview import ModalView
        from kivymd.uix.spinner import MDSpinner
        global _modal
        _modal  =   ModalView(size_hint=(.8, .8), auto_dismiss=False, background='', background_color=[0, 0, 0, 0])
        _modal.add_widget(MDSpinner(line_width=dp(5.25), size_hint=(None, None), size=(120, 120), pos_hint={'center_x': .5, 'center_y': .5}, active=True))  # Load and play the GIF

    def show_info_micro(self):
        if 7==7: #not self.micro_info_dialog:
            self.micro_info_dialog = MDDialog(
                    title="What are Micro QR Codes ?",
                    # halign="center",
                    type="custom",
                    width_offset=dp(30),
                    content_cls=Builder.load_file('kv/micro_qr.kv'),
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda x: self.micro_info_dialog.dismiss()
                        ),
                    ],
                )
        self.micro_info_dialog.children[0].children[-1].halign="center"
        self.micro_info_dialog.open()
        
    def show_info_animated(self):
        if 6==6: #not self.animated_info_dialog:
            self.animated_info_dialog = MDDialog(
                    title="",
                    type="custom",
                    width_offset=dp(30),
                    content_cls=Builder.load_file('kv/animated_qr.kv'),
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda x: self.animated_info_dialog.dismiss()
                        ),
                    ],
                )
        self.animated_info_dialog.open()

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