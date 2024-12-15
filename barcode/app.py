import os
from threading import Thread
from kivy.lang import Builder
from kivy.clock import Clock , mainthread
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.properties import StringProperty
# hotreload ->
from kivy.properties import BooleanProperty, StringProperty , ListProperty
from kivymd.uix.pickers import MDColorPicker
from typing import Union
import threading
#
from kivy.metrics import dp
from kivy.utils import platform
from kivymd.toast import toast as tst
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.config import Config
Config.set('kivy', 'pause_on_minimize', '1')

import codegen

if platform == 'android':
    from android import mActivity
    from androidstorage4kivy import SharedStorage, Chooser, ShareSheet

# create ./src folder
if not os.path.exists('./src'):
    os.makedirs('./src')
    os.makedirs('./src/qr')
    os.makedirs('./src/pdf')



class HomeScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ScanerScreen(Screen):
    pass

class AdvancedQRScreen(Screen):
    pass

class CustomCard(MDCard):
    # icon = StringProperty()
    image_source = StringProperty()        

file_list = []

DIALOG_KV = '''
MDBoxLayout:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)
    adaptive_height: True  # This ensures dynamic height adjustment

    MDTextField:
        id: barcode_textfield
        hint_text: "AACB1978432" if not dialog_switch.active else "https://www.cb28.com/"

    MDBoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: self.minimum_height
        spacing: dp(10)
        md_bg_color: 0, 1, .4, .4

        MDLabel:
            text: "Advanced Options"
            size_hint_x: 0.8
            halign: "left"

        MDSwitch:
            id: dialog_switch
            size_hint_x: 0.2
            pos_hint: {"center_y": 0.33} 
            on_active: 
                app.root.get_screen('advanced_qr').manager.current = 'advanced_qr' if self.active else 'home'
                # app.on_switch_active(self, self.active)

            

    MDBoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: self.minimum_height
        spacing: dp(10)
        md_bg_color: 0, 1, .4, .4

        MDLabel:
            text: "Create QR code"
            size_hint_x: 0.8
            halign: "left"

        MDSwitch:
            id: dialog_switch
            size_hint_x: 0.2
            pos_hint: {"center_y": 0.33} 
            on_active: app.on_switch_active(self, self.active)
'''


class CustomRecycleView(MDRecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [
            {
                'image_source': x,
            } for x in file_list
        ]


class MyApp(MDApp):
    dialog = None
    uris = []

    # app-internals
    dialog = None
    show_line = BooleanProperty(False)
    fit_display_source = StringProperty("kv/color-picker-qr.png")
    #
    icon_brush_color = ListProperty([0,1,.2, 1])
    footer_brush_color = ListProperty([0,1,.2, 1])
    qr_code_data = StringProperty("fudemy.me")
    qr_code_description = StringProperty("fudemy.me")
    qr_code_icon = StringProperty("qrcode")
    qr_code_color = ListProperty([0,1,.2, 1])
    qr_code_micro = BooleanProperty(False)
    qr_save_dir = StringProperty("src/qr")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Barcode"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = 'Dark'
        #
        for root, dirs, files in os.walk('./src'):
            for file in files:
                file_list.append(os.path.join(root, file))

        print(file_list)
    
    def set_bars_colors(self):
        set_bars_colors(
            self.theme_cls.primary_color,  # status bar color
            #self.theme_cls.primary_color,  # navigation bar color
            "Light",                       # icons color of status bar
        )

    def toast(self,text:str, duration=1.0):
        if platform == 'android':
            tst(text, duration)
        else:
            tst(text, duration=duration) 

    def generate_codes(self):
        # dialog
        if not self.dialog:
            self.dialog = MDDialog(
                title="  Quick Create",
                type="custom",
                content_cls=Builder.load_file('quick_create.kv'),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="ADD",
                        on_release=lambda x: self.generate_barcode(self.dialog.content_cls.ids.barcode_textfield.text) if not self.dialog.content_cls.ids.dialog_switch.active else self.generate_qr_code(self.dialog.content_cls.ids.barcode_textfield.text)
                    ),
                ],
            )
        self.dialog.open()

    def on_switch_active(self, instance, value):
        # dialog.title = self.dialog.children[0].children[-1].text
        # set 
        # self.dialog.children[0].children[-1].text = "Create QR code" if value else "Create Barcode"
        print(f"Switch is now {'on' if value else 'off'}")
        print(self.dialog.children[0].children)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label,):
        screen = self.root.get_screen('home')
        if instance_tab.name == 'scaner_tab':
            screen.ids.top_app_bar.title = "Scan Codes"
        elif instance_tab.name == 'home_tab':
            screen.ids.top_app_bar.title = "Create Codes"
        else:
            screen.ids.top_app_bar.title = "All Services"
        print(instance_tab.name)

    def build(self):
        # hotreload ->
        global color_picker
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.set_color_to = "icon_brush_color"
        # color_picker.open()
        color_picker.bind(
            # on_select_color=get_color,
            on_release=self.get_selected_color,
        ) 
        #
        self.theme_cls.theme_style = 'Dark' 
        return Builder.load_file('app.kv')
    
    def on_start(self):
        self.refresh_files()
        #
        self._init_loading_widget()
        #
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

    def on_pause(self):
        return True
    
    def on_resume(self):
        # Restore any data or state when the app resumes.
        # Force a redraw
        self.root.canvas.ask_update()

    def on_stop(self):
        pass

    def on_pre_enter(self, *args):
        # bind back button
        self.bind(on_keyboard=self.quit_app)

    def on_pre_leave(self, *args):
        # unbind back button
        self.unbind(on_keyboard=self.quit_app)
        # delete files-shared
        [SharedStorage().delete_shared(uri) for uri in self.uris]

    def quit_app(self,window,key,*args):
        # back button/gesture quits app
        if key == 27:
            if self.test_uri:
                # SharedStorage().delete_file(self.test_uri)
                [SharedStorage().delete_shared(uri) for uri in self.uris]
            mActivity.finishAndRemoveTask() 
            return True   
        else:
            return False

    def _init_loading_widget(self):
        ''' Initialize the loading widget '''
        # init the modal view
        from kivy.uix.modalview import ModalView
        from kivymd.uix.spinner import MDSpinner
        global _modal
        _modal  =   ModalView(size_hint=(.8, .8), auto_dismiss=False, background='', background_color=[0, 0, 0, 0])
        _modal.add_widget(MDSpinner(line_width=dp(5.25), size_hint=(None, None), size=(120, 120), pos_hint={'center_x': .5, 'center_y': .5}, active=True))  # Load and play the GIF
    

    def refresh_files(self) -> list:
        file_list = []
        for root, dirs, files in os.walk('./src'):
            for file in files:
                file_list.append(os.path.join(root, file))
        print(file_list)
        self.root.get_screen('home').ids.rv.data = [
            {
                'image_source': x,
            } for x in file_list
        ]
        return file_list

    def delete_file(self, file):
        def _del():
            try:
                os.remove(file)
            except Exception as e:
                print(e)
                self.toast("❌ Couldn't delete file")
            Clock.schedule_once(lambda dt :self.toast("🗑️ File deleted"), 0.2)
            Clock.schedule_once(lambda dt : self.refresh_files() ,0.2)
        #
        Thread(target=_del).start()

    def share_file(self, file:str):
        if not os.path.exists(file):
            self.toast("❌ File not found")
            return
        # open _modal
        _modal.open()
        def _share():
            try:
                if platform == 'android':
                    from android.permissions import request_permissions, Permission , check_permission
                    if not check_permission(Permission.READ_EXTERNAL_STORAGE) or not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

                # create a file in Private storage
                # filename = join(SharedStorage().get_cache_dir(),'ico.png')
                filename = SharedStorage().copy_to_shared(file)
                # add to uris list
                self.uris.append(filename)
                Clock.schedule_once(lambda x : _modal.dismiss(),.2)
                ShareSheet().share_file(filename)
            except Exception as e:
                print(e)
                Clock.schedule_once(lambda dt :self.toast("❌ Couldn't share file"),.2)
                Clock.schedule_once(lambda x : _modal.dismiss(),.2)
        #
        Thread(target=_share).start()

    def generate_qr_code(self , code:str):
        #
        _modal.open()
        def _gen():
            _ = codegen.generate_qr_code(code)
            # refresh the files
            self.root.get_screen('home').ids.rv.data.insert(
                0,
                {
                'image_source': _,
                }
            )
            _ = None
            Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
            print('qr',code)
        #
        Thread(target=_gen).start()

    def generate_barcode(self,code:str):
        _modal.open()
        def _gen():
            # check if code is valid
            if len(code) ==12 and code.isdigit():
                _=codegen.generate_ean13_barcode(code)
            elif len(code) ==11 and code.isdigit():
                _=codegen.generate_upc_barcode(code)
            else:
                _=codegen.generate_code128_barcode(code)
            print(code)
            # refresh the files
            self.root.get_screen('home').ids.rv.data.insert(
                0,
                {
                'image_source': _,
                }
            )
            _ = None
            Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
        #
        Thread(target=_gen).start()

    # hotreload ->
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
            _app.icon_brush_color = _
        elif instance_color_picker.set_color_to == "footer_brush_color":
            _app.footer_brush_color = _
            print(_app.icon_brush_color)
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

    def generate_qr_code_icon(self):
        # check micro and data len <11
        if not self.qr_code_data:
            self.toast("QR code data cannot be empty")
            return
        elif self.qr_code_micro and len(self.qr_code_data) > 11:
            print(self.qr_code_data)
            self.toast("Micro QR code can only contain 10 characters")
            return
        _modal.open()
        def _gen():
            # import  test2 as t2# generate_custom_qr_icon
            import time
            time.sleep(1)
            _ = codegen.generate_custom_qr_icon(
                self.qr_code_data,
                self.qr_code_description,
                output='',
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
            # self.fit_display_source = "qr_code.png"
             # refresh the files
            self.root.get_screen('home').ids.rv.data.insert(
                0,
                {
                'image_source': _,
                }
            )
            _ = None
            Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
        # Clock.schedule_once(lambda x: threading.Thread(target=_gen).start(), 0.1)
        threading.Thread(target=_gen).start()


_app = MyApp()
_app.run()