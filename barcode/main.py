import os , shutil
from threading import Thread
from kivy.lang import Builder
from kivy.clock import Clock , mainthread
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivy.uix.image import Image, AsyncImage
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
from datetime import datetime
#
from kivy.animation import Animation
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.utils import platform
from kivymd.toast import toast as tst
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.config import Config
Config.set('kivy', 'pause_on_minimize', '1')

import codegen

if platform == 'android':
    from android import mActivity
    from androidstorage4kivymod import SharedStorage, Chooser, ShareSheet

# create ./src folder
if not os.path.exists('./src'):
    os.makedirs('./src')
    os.makedirs('./src/qr')
    os.makedirs('./src/pdf')
    os.makedirs('./src/_cache')    # _cache | temp files to be deleted on_pre_leave



class HomeScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ScanerScreen(Screen):
    pass

class AdvancedQRScreen(Screen):
    pass

class CustomCard(MDCard,ButtonBehavior):
    # icon = StringProperty()
    image_source = StringProperty()      



file_list = []

Preview_modal = None

class CustomRecycleView(MDRecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [
            {
                'image_source': x,
            } for x in file_list
        ]


class MyApp(MDApp):

    uris = []

    # app-internals
    dialog = None
    show_line = BooleanProperty(False)
    fit_display_source = StringProperty("src/qr/9Ranimated_qr_code_20250120122818.gif")
    ### features | animated qr
    web_sync_btn = ... # IconButton TODO to be added
    file_picker_card  = ... # instance of MDCard TODO to be added
    generate_qr_btn = ... # instance of MDIconButton TODO to be added
    tempUrlFile = StringProperty()
    tempUrlFile_ext = StringProperty()
    Preview_modal_source = StringProperty("src/qr/Ranimated_qr_code_20250120122818.gif")
    #
    icon_brush_color = ListProperty([1,.4,.2, 1])
    footer_brush_color = ListProperty([1,.4,.2, 1])
    qr_code_data = StringProperty("fudemy.me")
    qr_code_description = StringProperty("fudemy.me")
    qr_code_icon = StringProperty("qrcode")
    qr_code_color = ListProperty([0, 0, 0, 1])
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
                self.theme_cls.primary_color,  # navigation bar color
                "Dark",                       # icons color of status bar
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
                width_offset=dp(30),
                content_cls=Builder.load_file('kv/quick_create.kv'),
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
            screen.ids.top_app_bar_label.text = "Scan Codes"
        elif instance_tab.name == 'home_tab':
            screen.ids.top_app_bar_label.text = "Create Codes"
        elif instance_tab.name == 'document_tab':
            screen.ids.top_app_bar_label.text = "Scan Documents"
        else:
            screen.ids.top_app_bar_label.text = "All Services"
        print(instance_tab.name)

    def build(self):
        #
        self.theme_cls.theme_style = 'Dark' 
        self.set_bars_colors()
        return Builder.load_file('kv/app.kv')
    
    def on_start(self):
        self.refresh_files()
        self.fps_monitor_start()
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

    # def on_pre_enter(self, *args):
    #     # bind back button
    #     self.bind(on_keyboard=self.quit_app)

    # def on_pre_leave(self, *args):
    #     # unbind back button
    #     self.unbind(on_keyboard=self.quit_app)
    #     # delete files-shared
    #     [SharedStorage().delete_shared(uri) for uri in self.uris]

    # def quit_app(self,window,key,*args):
    #     # back button/gesture quits app
    #     if key == 27:
    #         if self.test_uri:
    #             # SharedStorage().delete_file(self.test_uri)
    #             [SharedStorage().delete_shared(uri) for uri in self.uris]
    #         mActivity.finishAndRemoveTask() 
    #         return True   
    #     else:
    #         return False

    def _init_loading_widget(self):
        ''' Initialize the loading widget '''
        # init the modal view
        from kivy.uix.modalview import ModalView
        from kivymd.uix.spinner import MDSpinner
        global _modal
        _modal  =   ModalView(size_hint=(.8, .8), auto_dismiss=False, background='', background_color=[0, 0, 0, 0])
        _modal.add_widget(MDSpinner(line_width=dp(5.25), size_hint=(None, None), size=(120, 120), pos_hint={'center_x': .5, 'center_y': .5}, active=True))  # Load and play the GIF
        #
        global Preview_modal
        if not Preview_modal:
            Preview_modal = ModalView(size_hint=(.7, .7), auto_dismiss=True, background='', background_color=[0, 0, 0, 0],)
            self.image_widget = AsyncImage(source=self.Preview_modal_source, anim_delay=0.03,allow_stretch=True,keep_ratio=True)  # Load and play the GIF
            Preview_modal.add_widget(self.image_widget)
            Preview_modal.bind(on_open=self.preview_modal_open, on_dismiss=self.preview_modal_dismiss,on_touch_up=Preview_modal.dismiss)
        #
        # hotreload ->
        global color_picker
        color_picker = MDColorPicker(size_hint=(0.45, 0.85),type_color='RGBA')
        color_picker.set_color_to = "icon_brush_color"
        # color_picker.open()
        color_picker.bind(
            # on_select_color=get_color,
            on_release=self.get_selected_color,
        ) 
        # #
        self.web_sync_btn = self.root.get_screen('advanced_qr').ids.web_sync
        self.file_picker_card = self.root.get_screen('advanced_qr').ids.file_picker_card
        self.generate_qr_btn = self.root.get_screen('advanced_qr').ids.generate_qr_btn
    

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
        def get_time() -> str:
            return datetime.now().strftime("%Y%m%d%H%M%S")
        # open _modal
        _modal.open()
        def _share():
            try:
                if platform == 'android':
                    from android.permissions import request_permissions, Permission , check_permission
                    if not check_permission(Permission.READ_EXTERNAL_STORAGE) or not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

                ## create a file in Private storage

                # copy the file to a new name , then share it
                with open(file, 'rb') as f:
                    new_file_name = os.path.join('src/_cache',f'{get_time()}.png')
                    with open(new_file_name, 'wb') as nf:
                        nf.write(f.read())
                        nf.close()
                    f.close()
                # copy to shared storage and get the uri
                if platform == 'android':
                    filename = SharedStorage().copy_to_shared(new_file_name)
                    self.uris.append(filename)
                # add to uris list
                # print('uri',': ',filename,)
                # try:
                #     print('exists: ',os.path.exists(filename))
                # except Exception as e: print(e)
                if platform == 'android':
                    ShareSheet().share_file(filename)
                elif platform != 'android':
                    Clock.schedule_once(lambda dt :self.toast("❌ Only works on Android\nCouldn't share file"),.2)
            except Exception as e:
                print(e)
                Clock.schedule_once(lambda dt :self.toast("❌ Couldn't share file"),.2)
                Clock.schedule_once(lambda x : _modal.dismiss(),.2)
            finally:
                os.remove(new_file_name)
                Clock.schedule_once(lambda x : _modal.dismiss(),.2)
        #
        Thread(target=_share).start()

    def open_image_preview(self, file:str):
        #
        global Preview_modal
        Preview_modal.children[0].source = file
        # self.Preview_modal_source = file
        # print('before opening',file,modal.children[0].source)
        Preview_modal.open()

    def preview_modal_open(self, instance):
        # modal._is_open = True
        # print(instance.children)
        # instance.opacity = 0
        Animation(opacity=1, duration=0.5).start(instance)

    def preview_modal_dismiss(self, instance):
        # modal._is_open = False
        instance.opacity = 0
        Animation(opacity=0, duration=0.1).start(instance)
        

    def generate_qr_code(self , code:str):
        #
        _modal.open()
        if not code:
            self.toast("QRcode data cannot be empty \nPlease enter something")
            Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
            return
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
            Clock.schedule_once(lambda  dt :self.toast("QR code generated Sucessfuly"),.2)
            print('qr',code)
        #
        Thread(target=_gen).start()

    def _verify_and_fetch_from_url(self, url:str):

        def _(url):
            # Download the image from the URL
            # url = 'https://ci3.googleusercontent.com/meips/ADKq_Nb8AgH6eOB3xeD5UFQEwsIuzmY8x9ngEA63u62xOr82ptFtVfPSz7Nb6UmgBJ8YXbvmEhhKKevYWSFL4gj2MCjlSaV66UiZtkbCv2y4RqcDyUkWeBmxnDWygWmckGwaJ-bF5z2nDIWXpAIIZRtCzL1cty_7uK6vZKXb=s0-d-e1-ft#https://m.media-amazon.com/images/G/01/outbound/OutboundTemplates/Amazon_logo_US._BG255,255,255_.png'
            try:
                _ = codegen._verify_and_fetch_from_url(url)
                if not _: 
                    print('The URL is not valid.')
                    Clock.schedule_once(lambda  dt :self.toast("The URL is not valid.\ntry a different file Url"),.2)
                    Clock.schedule_once(lambda x: setattr(self.web_sync_btn,"disabled" , False), 0.1)
                    Clock.schedule_once(lambda x: setattr(self.file_picker_card,"disabled" , False), 0.1)
                    Clock.schedule_once(lambda x: setattr(self.generate_qr_btn,"disabled" , False), 0.1)
                    return
                else:
                    # self.fit_display_source = _[0]
                    Clock.schedule_once(lambda x: setattr(self,"fit_display_source" , _[0]), 0.1)
                    self.tempUrlFile = _[1]
                    Clock.schedule_once(lambda x: setattr(self.web_sync_btn,"disabled" , False), 0.1)
                    Clock.schedule_once(lambda x: setattr(self.file_picker_card,"disabled" , False), 0.1)
                    Clock.schedule_once(lambda x: setattr(self.generate_qr_btn,"disabled" , False), 0.1)
            except Exception as e: 
                Clock.schedule_once(self.toast("Something went wrong ! ❌"),.2)

            
        threading.Thread(target=_,args=(url,)).start()

    def generate_animated_qr_code(self):
        _modal.open()
        # check if code is valid
        if not self.qr_code_data:
            self.toast("Barcode data cannot be empty \nPlease enter something")
            Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
            return
        def _gen():
            # create qr first

            try:
                _ = codegen.generate_animated_qr_code(self.qr_code_data,self.tempUrlFile,)
                if _:
                    Clock.schedule_once(lambda  dt :self.toast("QR code generated Sucessfuly"),.2)
                    Clock.schedule_once(lambda x: setattr(self,"fit_display_source" , _), 0.1)
                    Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
                    # refresh the files
                    self.root.get_screen('home').ids.rv.data.insert(
                        0,
                        {
                        'image_source': _,
                        }
                    )
                    # save_as = None

                else:
                    print('Could not generate QR\ngot not qr file from callback see logs.')
            except Exception as e:
                print('The file is not a valid image.\n' "error" , e)
                Clock.schedule_once(self.toast("Something went wrong ! ❌"),.2)
                Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
        Thread(target=_gen).start()
        print(self.tempUrlFile,os.path.isfile(self.tempUrlFile))

    def generate_barcode(self,code:str):
        _modal.open()
        # check if code is valid
        if not code:
            self.toast("Barcode data cannot be empty \nPlease enter something")
            Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
            return
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
            Clock.schedule_once(self.toast("Barcode generated Sucessfuly"),.2)
        #
        Thread(target=_gen).start()

    def Pick_A_File(self):
        try:
            if platform == 'android':
                    from android.permissions import request_permissions, Permission , check_permission
                    if not check_permission(Permission.READ_EXTERNAL_STORAGE) or not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                        Clock.schedule_once(lambda dt: self.toast("Please Grant Pemitions\nto pick a file from Internal\nstorage"),0.3)
                        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
                        return
            if platform == 'android':
                if not hasattr(self, 'chooser'):
                    self.chooser = Chooser(self._chooser_callback)
                # let the user choose a file
                self.chooser.choose_content('image/*') 

            else: print('Not supported on this platform')
                # self._chooser_callback([])
        except Exception as e:
            print(e)
            return
    # callback is called when the user selects a file
    def _chooser_callback(self,uri_list):
    # ShareSheet().share_file_list(uri_list, self.target)
        def _call(uri_list):
            try:
                Clock.schedule_once(lambda dt : _modal.open() ,.1)
                # print(uri_list,'type:',type(uri_list[0]))
                #self._source = uri_list[0]
                _file = SharedStorage().copy_from_shared(uri_list[0])
                # set the tempUrlFile
                # self.tempUrlFile = _file
                Clock.schedule_once(lambda x: setattr(self,"tempUrlFile" , _file), 0.1)
                # make a copy for fit_display_source at "src/_cache"
                try:
                    tmp_fit = shutil.copy(_file, os.path.join('src', '_cache', os.path.basename(_file)))
                    Clock.schedule_once(lambda x: setattr(self,"fit_display_source" , tmp_fit), 0.2)
                except Exception as e:
                    print(e,"\nCould not copy file to cache")
                    Clock.schedule_once(lambda x: setattr(self,"fit_display_source" , _file), 0.2)
                # self.fit_display_source = _file
                # del self.chooser
                Clock.schedule_once(lambda dt: setattr(self, 'chooser', None), 0.3)

                base = os.path.basename(_file)
                Clock.schedule_once(lambda dt: self.toast(f"{base}"),0.5)
                Clock.schedule_once(lambda dt : _modal.dismiss() ,0.2)
                #
                # with open('freehost', 'r') as f:
                #     api_key = f.read()
                #     f.close()
                # url = 'https://freeimage.host/api/1/upload'
                # with open(_file, 'rb') as f:
                #     response = requests.post(url, data={'key': api_key}, files={'source': f})
                #     if response.status_code == 200:
                #             data = response.json()
                #             if 'link' in data:
                #                 f.close()
                #                 print(data['link'])
                #                 return data['link']
                #             else: return 
                #     else:
                #         print(f"Failed to upload file: {response.status_code}")
                #         f.close()
                #         return None
            except Exception as e:
                print(e,"\nSomething went wrong ,while _chooser_callback")
                Clock.schedule_once(lambda dt : _modal.dismiss() ,0.2)
        threading.Thread(target=_call,args=(uri_list,)).start()

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

    # def on_select_color(self, instance_gradient_tab, color: list) -> None:
    #     '''Called when a gradient image is clicked.'''

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
            Clock.schedule_once(self.toast("QRcode generated Sucessfuly"),.2)
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