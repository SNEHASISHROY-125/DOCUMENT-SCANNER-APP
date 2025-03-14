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
from kivy.core.window import Window
from kivy.properties import BooleanProperty, StringProperty , ListProperty
from kivymd.uix.pickers import MDColorPicker
from typing import Union
import threading 
from datetime import datetime
#

from kivy.animation import Animation
# from kivymd.uix.button.button
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.utils import platform, get_color_from_hex , get_hex_from_color
from kivymd.toast import toast as tst
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.config import Config
Config.set('kivy', 'pause_on_minimize', '1')
Window.softinput_mode = "below_target"

# font
# from kivy.core.text import LabelBase

# LabelBase.register(name="Default", fn_regular="fonts/Marigny-Bold.ttf")

# test
if platform != 'android':
    Window.size = (360, 1080) 
# ADs
# if platform == 'android':
    # from kivmoblite import Admob

import codegen

if platform == 'android':
    import unityads  as UnityAds
    # from android import mActivity
    from androidstorage4kivymod import SharedStorage, Chooser, ShareSheet

# create ./src folder
if not os.path.exists('./src'):
    os.makedirs('./src')
    os.makedirs('./src/qr')
    os.makedirs('./src/pdf')
    os.makedirs('./src/_cache')    # _cache | temp files to be deleted on_pre_leave
# create ./tmp_cache folder
if not os.path.exists('./tmp_cache'):
    os.makedirs('./tmp_cache')    # tmp_cache | temp files to be deleted on_pre_leave

# create ./svg folder
if not os.path.exists('./svg'):
    os.makedirs('./svg')    # svg | temp files to be deleted on_pre_leave

ad_ids = {
        "appId": "ca-app-pub-2987282397801743~7612741649",
        "banId": "ca-app-pub-2987282397801743/6842585450",
        "intId": "ca-app-pub-2987282397801743/7168106242",
        "testD": []
        }

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

# Animated Button
class AnimatedProgressButton(MDCard):
    spinner = None
    label = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (80, 50)
        self.pos_hint = {"center_x": .5, "center_y": .5}
        self.radius = [10,]
        self.md_bg_color = [0, 1, .2, 1]
        self.text = "Animate"
        self.text_color = [0, 0, 0, 1]
        self.on_release = self.animate

    def on_animation_start(self, widget):
        Clock.schedule_once(lambda x : setattr(self.label,"text",  "") , 0.3)
    def on_animation_complete(self, widget):
        print("Animation complete", widget , self.spinner)
        self.disabled = True
        self.spinner.opacity = 0.4
        self.spinner.active = True

    def animate(self):
        # Create an animation object
        animation = Animation(duration=0.4, t="in_out_circ",size=(dp(100), dp(50)))     # https://kivy.org/doc/stable/api-kivy.animation.html#kivy.animation.AnimationTransition
        animation.on_start = self.on_animation_start
        animation.on_complete = self.on_animation_complete
        # Start the animation
        print("Animation started")
        animation.start(self)
        global ref # reference to self for outside access
        ref = self
    def animate_back(self): 
        # Create an animation object
        animation = Animation(duration=0.4, t='out_bounce',size=(dp(200), dp(50)))      # https://kivy.org/doc/stable/api-kivy.animation.html#kivy.animation.AnimationTransition
        # animation.on_start = self.on_animation_start
        # animation.on_complete = self.on_animation_complete
        Clock.schedule_once(lambda x: setattr(self.spinner,"active" , False), 0.1)
        # # Start the animation
        print("Animation started")
        animation.start(self)
        Clock.schedule_once(lambda x : setattr(self.label,"text",  "Generate QR") , 0.3)
        Clock.schedule_once(lambda x: setattr(self , "disabled" , False), 0.5)

class mMDColorPicker(MDColorPicker):

    def update_color_slider_item_bottom_navigation(self, color: list) -> None:
        """
        Updates the color of the slider that sets the transparency value of the
        selected color and the color of bottom navigation items.
        """
        if "select_alpha_channel_widget" in self._current_tab.ids:
            self._current_tab.ids.select_alpha_channel_widget.ids.slider.color = (
                color
            )
        # Comment out the line that updates the bottom navigation color
        # self.ids.bottom_navigation.text_color_active = color              # bug fix

import qrcode
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty
from kivy.metrics import dp

class QRWidget(Widget):
    light_color = ListProperty([1, 1, 1, 1])  # Default light color (white)
    dark_color = ListProperty([0, 0, 0, 1])   # Default dark color (black)
    data = StringProperty('fudemy.me')

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.matrix = self.generate_matrix(self.data)
        self.bind(size=self.update_canvas)
        self.bind(pos=self.update_canvas)
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
        x_offset = self.x + (self.width - (cols * module_width)) / 2
        y_offset = self.y + (self.height - (rows * module_height)) / 2

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

# from kivy.graphics.svg import Svg
# from kivy.uix.widget import Widget

# class MyWidget(Widget):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         with self.canvas:
#             self.box = MDBoxLayout()
#             self.svg = Svg("barcode/assets/svg.svg")  # Add SVG to canvas
#             self.box.add_widget(self.svg)
#             self.box.size = self.size

class MyApp(MDApp):

    uris = []

    # fonts
    font = "fonts/SupriaSans.otf"
    font_italic = "fonts/SupriaSans-Italic.otf"

    # app-internals
    dialog = None
    del_dialog = None
    animated_info_dialog = None
    micro_info_dialog = None
    permissions_grant_dialog = None
    file_to_delete = StringProperty("")
    show_line = BooleanProperty(False)
    fit_display_source = StringProperty("assets/color-picker-qr.png")
    # ads
    ad_loaded = BooleanProperty(False)
    show_ad_dialog = None
    # prices | coins | nornal qr = 10 | animated qr = 20
    PRICE_NORMAL_QR = 10
    PRICE_ANIMATED_QR = 20
    ### features | animated qr
    gen_btn = BooleanProperty(False)
    web_sync_btn = ... # IconButton TODO to be added
    file_picker_card  = ... # instance of MDCard TODO to be added
    generate_qr_btn = ... # instance of MDIconButton TODO to be added
    tempUrlFile = StringProperty()
    tempUrlFile_ext = StringProperty()
    Preview_modal_source = StringProperty("src/qr/Ranimated_qr_code_20250120122818.gif")
    # features | icon_qr
    icon_brush_color = ListProperty([1,.4,.2, 1])
    footer_brush_color = ListProperty([1,.4,.2, 1])
    qr_bg_dark_color = ListProperty([0, 0, 0, 1])
    qr_bg_light_color = ListProperty([1, 1, 1, 1])
    qr_code_data = StringProperty("fudemy.me")
    qr_code_description = StringProperty("fudemy.me")
    qr_code_icon = StringProperty("qrcode")
    qr_code_color = ListProperty([0, 0, 0, 1])
    qr_frame_ids = ListProperty([])
    qr_code_micro = BooleanProperty(False)
    qr_code_frame = BooleanProperty(False)      # if frame is selected in selectableImage
    qr_code_frame_path = StringProperty("")
    qr_save_dir = StringProperty("src/qr")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Barcode"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = 'Dark'
        # Override the primary color directly
        # Define the custom color palette
        # custom_palette = {
        #     "50": "E0F2F1",
        #     "100": "B2DFDB",
        #     "200": "80CBC4",
        #     "300": "4DB6AC",
        #     "400": "26A69A",
        #     "500": "00796B",  # Replace with your custom color
        #     "600": "00897B",
        #     "700": "00796B",
        #     "800": "00695C",
        #     "900": "004D40",
        #     "A100": get_hex_from_color([0.15, 0.35, 0.8, 0.35]),
        #     "A200": "64FFDA",
        #     "A400": "1DE9B6",
        #     "A700": "00BFA5",
        # }

        # Add the custom palette to the theme manager
        print('jfjjfjf: ',self.theme_cls.primary_hue)
        # self.theme_cls.theme_bg_color["Custom"] = custom_palette
        self.theme_cls.primary_hue = "A200"

        #
        # for root, dirs, files in os.walk('./src'):
        #     for file in files:
        #         file_list.append(os.path.join(root, file))

        print(file_list)
    
    def set_bars_colors(self):
            set_bars_colors(
                [0.15, 0.35, 0.8, 0.35],  # status bar color
                [0.13, 0.13, 0.13, 1],  # navigation bar color
                "Dark",  # icons color of status bar
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
                size_hint=(0.8, 0.4),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        font_name=self.font_italic,
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="ADD",
                        font_name=self.font_italic,
                        on_release=lambda x: self.generate_barcode(self.dialog.content_cls.ids.barcode_textfield.text) if not self.dialog.content_cls.ids.dialog_switch.active else self.generate_qr_code(self.dialog.content_cls.ids.barcode_textfield.text)
                    ),
                ],
            )
            self.dialog.children[0].children[-1].font_name=self.font_italic
        self.dialog.open()

    def on_switch_active(self, instance, value):
        # dialog.title = self.dialog.children[0].children[-1].text
        # set 
        # self.dialog.children[0].children[-1].text = "Create QR code" if value else "Create Barcode"
        print(f"Switch is now {'on' if value else 'off'}")
        # print(self.dialog.children[0].children[-1].text)

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
    
    def _show_baner(self): ...
        # if platform == 'android':
        #     self.ads.banner_pos("top")
            # self.ads.show_banner()
        # else:
        #     print('Not supported on this platform')
    def _hide_baner(self):...
        # if platform == 'android':
        #     self.ads.hide_banner()
        # else:
        #     print('Not supported on this platform')
    def _show_rewarded_ad(self):
        if platform == 'android':
            self.ad_manager.show_ad()
        else:
            print('Not supported on this platform')
    def build(self):
        
        #
        self.theme_cls.theme_style = 'Dark' 
        self.set_bars_colors()
        return Builder.load_file('kv/app.kv')
    
    def on_start(self):
        if platform == 'android': ...
            # self.ads.banner_pos("top")
            # self.ads.new_interstitial()  # Initialize interstitial
            # self.ads.request_interstitial()
            # self.ads.show_interstitial()
        # self.fps_monitor_start()
        #
        Clock.schedule_once(lambda dt: self._init_loading_widget(),1)
        #
        
        self._on_start_lazy_load()
        # self.db:dict = db_.fetch_data()
        # if platform == 'android':
        #     from android.permissions import request_permissions, Permission
        #     request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
    
    def _on_start_lazy_load(self):
        #
        # self.refresh_files()
        import db
        self.db_:db.DB = db.DB()
        #
        self.coin_label =  self.root.get_screen("home").ids.top_app_bar_coins_label
        Clock.schedule_once(lambda dt: setattr(self.coin_label,"text",str(self.db_.fetch_data()["coins"])), 4)
        #
        # ADs
        if platform == 'android':
            # self.ads = Admob(ad_ids)
            # self.ads.new_banner(position = [0,0], color = "#ffffff", margin = 0) # Adaptive banner
            # self.ads.request_banner()
            # self.ads.hide_banner()
            self.ad_manager = UnityAds.UnityAdManager(test_mode=False)
            self.ad_manager.set_ad_manager(self.ad_manager)  # Set the ad manager
            self.ad_manager.set_reward_callback(self.reward_user)  # Set reward callback
            self.ad_manager.set_load_state_callback(self.on_ad_loaded)

            self.ad_manager.load_ad()

    def reward_user(self):
        print("🎉 Rewarding user with 10 coins!")

        _ = self.db_.fetch_data()
        self.db_.update_db(
            user_id=_[0],
            theme=_[1],
            coins=_[2]+10,
            email=_[3],
        )
        _ = None
        self.coin_label.text = str(self.db_.fetch_data()["coins"])
    
    def on_ad_loaded(self, state):
        # print("Ad loaded")
        self.ad_loaded = state
    
    def on_pause(self):
        return True
    
    def on_resume(self):
        # Restore any data or state when the app resumes.
        # Force a redraw
        self.root.canvas.ask_update()

    def on_stop(self):
        pass

    def on_pre_leave(self, *args):
        # 
        self.db_.close_db()

    def Abtn_reverse(self):
        try:
            ref.animate_back() 
        except NameError:
            print("NameError: name 'ref' is not defined")
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
        _modal.add_widget(MDSpinner(line_width=dp(5.25), size_hint=(None, None), size=(Window.width * 0.6, Window.width * 0.6), pos_hint={'center_x': .5, 'center_y': .5}, active=True))  # Load and play the GIF
        _modal.add_widget(MDLabel(text="Please Wait",font_size='20sp', halign='center', pos_hint={'center_x': .5, 'center_y': .4}))
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
        color_picker = mMDColorPicker(size_hint=(0.45, 0.85),type_color='RGBA')
        color_picker.set_color_to = "icon_brush_color"
        # color_picker.open()
        color_picker.bind(
            # on_select_color=get_color,
            on_release=self.get_selected_color,
        ) 
        # #
        # self.web_sync_btn = self.root.get_screen('advanced_qr').ids.web_sync
        self.file_picker_card = self.root.get_screen('advanced_qr').ids.file_picker_card
        self.generate_qr_btn = self.root.get_screen('advanced_qr').ids.generate_qr_btn
    
    def show_permissions_grant_dialog(self):
        if not self.permissions_grant_dialog:
            def req_():
                if platform == 'android':
                    self.permissions_grant_dialog.dismiss()
                    #
                    from android.permissions import request_permissions, Permission , check_permission
                    if not check_permission(Permission.READ_EXTERNAL_STORAGE) or not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

            self.permissions_grant_dialog = MDDialog(
                title="Please allow Permissions",
                # text="Please Grant Permissions to access your files",
                type="custom",
                size_hint=(0.8, 0.4),
                auto_dismiss=False,
                # width_offset=dp(30),
                content_cls=Builder.load_file('kv/grant_permissions.kv'),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda x: self.permissions_grant_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="GRANT",
                        on_release=lambda x: req_()
                    ),
                ],
            )
            self.permissions_grant_dialog.children[0].children[-1].halign="center"
        self.permissions_grant_dialog.content_cls.ids.grant_permissions_label.text = "QR Genie needs to access your files, in order to share QR Codes with other apps."
        self.permissions_grant_dialog.open()

    def show_info_micro(self):
        if not self.micro_info_dialog:
            self.micro_info_dialog = MDDialog(
                    title="What are Micro QR Codes ?",
                    type="custom",
                    size_hint=(0.8, 0.4),
                    # width_offset=dp(30),
                    content_cls=Builder.load_file('kv/micro_qr.kv'),
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda x: self.micro_info_dialog.dismiss()
                        ),
                    ],
                )
            self.micro_info_dialog.children[0].children[-1].halign="center"
            self.micro_info_dialog.children[0].children[-1].font_size="15sp"
            self.micro_info_dialog.children[0].children[-1].theme_text_color = "Custom"
            self.micro_info_dialog.children[0].children[-1].text_color = [130/255, 247/255, 27/255, 0.8]  # Red color
        self.micro_info_dialog.open()
        
    
    def show_info_animated(self):
        if not self.animated_info_dialog:
            self.animated_info_dialog = MDDialog(
                title="",
                type="custom",
                size_hint= (0.8, 0.4),
                # width_offset=dp(30),
                content_cls=Builder.load_file('kv/animated_qr.kv'),
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.animated_info_dialog.dismiss()
                    ),
                ],
                on_dismiss=lambda x: setattr(self.animated_info_dialog.content_cls.children[-1] , "source" , "assets/image_placeholder.png"),
            )
            
        self.animated_info_dialog.open()
        Clock.schedule_once(lambda dt: setattr(self.animated_info_dialog.content_cls.children[-1] , "source" , "assets/animated_qr.gif"), 0.5)

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

        
    def _del(self):
        def _():
            try:
                os.remove(self.file_to_delete)
            except Exception as e:
                print(e)
                Clock.schedule_once(lambda dt: self.toast("❌ Couldn't delete file"),0.1)
                return
            Clock.schedule_once(lambda dt :self.toast("🗑️ File deleted"), 0.2)
            Clock.schedule_once(lambda dt : self.refresh_files() ,0.3)
        Clock.schedule_once(lambda dt: self.del_dialog.dismiss(), 0.1)
        Thread(target=_).start()

    def delete_file(self, file):
        self.file_to_delete = file
        
        if not self.del_dialog:
            self.del_dialog = MDDialog(
                    title="Do You Want to Delete this File?",
                    type="custom",
                    width_offset=dp(30),
                    content_cls=Builder.load_file('kv/delete.kv'),
                    buttons=[
                        MDFlatButton(
                            text="DELETE",
                            on_release=lambda x: self._del()
                        ),
                        MDFlatButton(
                            text="CANCEL",
                            on_release=lambda x: self.del_dialog.dismiss()
                        ),
                    ],
                )
        
        self.del_dialog.open()

    def share_file(self, file:str):
        if not os.path.exists(file):
            self.toast("❌ File not found")
            return
        def get_time() -> str:
            return datetime.now().strftime("%Y%m%d%H%M%S")
        # open _modal
        # self.show_permissions_grant_dialog()
        if platform == 'android':
            from android.permissions import request_permissions, Permission , check_permission
            if not check_permission(Permission.READ_EXTERNAL_STORAGE) or not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                # request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
                Clock.schedule_once(lambda dt: self.toast("Please Grant Pemitions\nto share a file"),0.3)
                self.show_permissions_grant_dialog()
                return
        _modal.open()
        def _share():
            try:

                ## create a file in Private storage
                # new_file_name = file
                # # copy the file to a new name , then share it
                with open(file, 'rb') as f:
                    new_file_name = os.path.join('src/_cache',get_time()+"_"+os.path.basename(file))
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
                print('file shared',file)
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
        
    def check_coin_balance(self , price:int=10):
        '''
        if the user has enough coins to generate a QR code return True
        '''
        if int(self.coin_label.text) - price  >=10:
            return True
        else:
            False
    
    def show_ad(self):
        def _diss(args):
            self.show_ad_dialog.dismiss()
            Clock.schedule_once(lambda dt: self.Abtn_reverse(), 1)
        if not self.show_ad_dialog:
                self.show_ad_dialog = MDDialog(
                    title="You ran out of credits",
                    type="custom",
                    width_offset=dp(30),
                    content_cls=Builder.load_file('kv/watchAd.kv'),
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            on_release= _diss
                        ),
                    ],
                )
                self.show_ad_dialog.bind(on_dismiss=lambda *args: self.Abtn_reverse())
        self.show_ad_dialog.open()

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
        # check price
        if self.check_coin_balance(price=self.PRICE_NORMAL_QR):
            Thread(target=_gen).start()
            # deduct coins
            _ = self.db_.fetch_data()
            self.db_.update_db(
                user_id=_["user_id"],
                theme=_["theme"],
                coins=_["coins"] - self.PRICE_NORMAL_QR,
                email=_["email"], 
            )
            _ = None
            self.coin_label.text = str(self.db_.fetch_data()["coins"])
        else:
            Clock.schedule_once(lambda dt :self.toast("Not enough coins to generate QR code"),.2)
            Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
            # show dialog | watch an Ad
            self.show_ad()

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
                Clock.schedule_once(lambda dt: self.toast("Something went wrong ! ❌"),.2)

            
        threading.Thread(target=_,args=(url,)).start()

    def generate_animated_qr_code(self):
        # _modal.open()
        # check if code is valid
        if not self.qr_code_data:
            self.toast("QR code data cannot be empty \nPlease enter something")
            Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
            Clock.schedule_once(lambda dt : self.Abtn_reverse(), 1)
            return
        def _gen():
            # create qr first

            try:
                _ = codegen.generate_animated_qr_code(self.qr_code_data,self.tempUrlFile,)
                if _:
                    Clock.schedule_once(lambda  dt :self.toast("QR code generated Sucessfuly"),.2)
                    Clock.schedule_once(lambda x: setattr(self,"fit_display_source" , _), 0.1)
                    Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
                    Clock.schedule_once(lambda dt : self.Abtn_reverse(), 1)
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
                    Clock.schedule_once(lambda dt: self.toast("Something went wrong ! ❌"),.2)
                    Clock.schedule_once(lambda dt : self.Abtn_reverse(), 1)
            except Exception as e:
                print('The file is not a valid image.\n' "error" , e)
                Clock.schedule_once(lambda dt: self.toast("Something went wrong ! ❌"),.2)
                Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
                Clock.schedule_once(lambda dt : self.Abtn_reverse(), 1)
            finally:
                Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
                Clock.schedule_once(lambda dt : self.Abtn_reverse(), 1)
        
        # check price
        if self.check_coin_balance(price=self.PRICE_ANIMATED_QR):
            Thread(target=_gen).start()
            # deduct coins
            _ = self.db_.fetch_data()
            self.db_.update_db(
                user_id=_["user_id"],
                theme=_["theme"],
                coins=_["coins"] - self.PRICE_ANIMATED_QR,
                email=_["email"], 
            )
            _ = None
            self.coin_label.text = str(self.db_.fetch_data()["coins"])
        else:
            Clock.schedule_once(lambda dt :self.toast("Not enough coins to generate QR code"),.2)
            Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
            # show dialog | watch an Ad
            self.show_ad()
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
            Clock.schedule_once(lambda dt: self.toast("Barcode generated Sucessfuly"),.2)
        #
        # check price
        if self.check_coin_balance(price=self.PRICE_NORMAL_QR):
            Thread(target=_gen).start()
            # deduct coins
            _ = self.db_.fetch_data()
            self.db_.update_db(
                user_id=_["user_id"],
                theme=_["theme"],
                coins=_["coins"] - self.PRICE_NORMAL_QR,
                email=_["email"], 
            )
            _ = None
            self.coin_label.text = str(self.db_.fetch_data()["coins"])
        else:
            Clock.schedule_once(lambda dt :self.toast("Not enough coins to generate QR code"),.2)
            Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
            # show dialog | watch an Ad
            self.show_ad()

    def Pick_A_File(self):
        try:
            if platform == 'android':
                    from android.permissions import request_permissions, Permission , check_permission
                    if not check_permission(Permission.READ_EXTERNAL_STORAGE) or not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                        Clock.schedule_once(lambda dt: self.toast("Please Grant Pemitions\nto pick a file from Internal\nstorage"),0.3)
                        # request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
                        if not self.permissions_grant_dialog:
                            def req_():
                                if platform == 'android':
                                    self.permissions_grant_dialog.dismiss()
                                    #
                                    from android.permissions import request_permissions, Permission , check_permission
                                    if not check_permission(Permission.READ_EXTERNAL_STORAGE) or not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                                        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
                            self.permissions_grant_dialog = MDDialog(
                            title="Please allow Permissions",
                            # text="Please Grant Permissions to access your files",
                            type="custom",
                            size_hint=(0.8, 0.4),
                            auto_dismiss=False,
                            # width_offset=dp(30),
                            content_cls=Builder.load_file('kv/grant_permissions.kv'),
                            buttons=[
                                MDFlatButton(
                                    text="CANCEL",
                                    on_release=lambda x: self.permissions_grant_dialog.dismiss()
                                ),
                                MDFlatButton(
                                    text="GRANT",
                                    on_release=lambda x: req_()
                                ),
                            ],
                        )
                        self.permissions_grant_dialog.children[0].children[-1].halign="center"
                        self.permissions_grant_dialog.content_cls.ids.grant_permissions_label.text = "QR Genie needs to access your files, in order to pick images for QR Code generation like logos,background image, etc."
                        self.permissions_grant_dialog.open()
                        return
            if platform == 'android':
                if not hasattr(self, 'chooser'):
                    self.chooser = Chooser(self._chooser_callback)
                else: print('Chooser already exists')
                # let the user choose a file
                self.chooser.choose_content('image/*') 

            else: 
                print('Not supported on this platform')

                if not self.permissions_grant_dialog:
                    def req_():
                        if platform == 'android':
                            self.permissions_grant_dialog.dismiss()
                            #
                            from android.permissions import request_permissions, Permission , check_permission
                            if not check_permission(Permission.READ_EXTERNAL_STORAGE) or not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
                    self.permissions_grant_dialog = MDDialog(
                    title="Please allow Permissions",
                    # text="Please Grant Permissions to access your files",
                    type="custom",
                    size_hint=(0.8, 0.4),
                    auto_dismiss=False,
                    # width_offset=dp(30),
                    content_cls=Builder.load_file('kv/grant_permissions.kv'),
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            on_release=lambda x: self.permissions_grant_dialog.dismiss()
                        ),
                        MDFlatButton(
                            text="GRANT",
                            on_release=lambda x: req_()
                        ),
                    ],
                )
                self.permissions_grant_dialog.children[0].children[-1].halign="center"
                self.permissions_grant_dialog.content_cls.ids.grant_permissions_label.text = "QR Genie needs to access your files, in order to pick images for QR Code generation like logos,background image, etc."
                self.permissions_grant_dialog.open()
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
                    tmp_fit = shutil.copy(_file, os.path.join('tmp_cache', os.path.basename(_file)))
                    Clock.schedule_once(lambda x: setattr(self,"fit_display_source" , tmp_fit), 0.2)
                except Exception as e:
                    print(e,"\nCould not copy file to cache")
                    Clock.schedule_once(lambda x: setattr(self,"fit_display_source" , _file), 0.2)
                # self.fit_display_source = _file
                # del self.chooser
                def _d(): del self.chooser
                Clock.schedule_once(lambda dt: _d, 0.3)#setattr(self, 'chooser', None), 0.3)

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
            # print(_app.icon_brush_color)
        elif instance_color_picker.set_color_to == "qr_bg_dark_color":
            _app.qr_bg_dark_color = _
        elif instance_color_picker.set_color_to == "qr_bg_light_color":
            _app.qr_bg_light_color = _
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
    def _transition_to(self, screen_name,t):
        Clock.schedule_once(lambda x: setattr(self.root,"current" , screen_name),t)
    def generate_qr_code_icon(self):
        # _modal.open()
        def _gen():
            # import  test2 as t2# generate_custom_qr_icon
            import time
            time.sleep(1)
            if not self.qr_code_frame:
                _ = codegen.generate_custom_qr_icon(
                    self.qr_code_data,
                    self.qr_code_description,
                    output='',
                    scale=10,
                    light= self.get_rgb(self.qr_bg_light_color), #(255, 255, 255),
                    dark= self.get_rgb(self.qr_bg_dark_color) , #tuple(self.qr_code_color),
                    border=1,
                    icon_name=self.qr_code_icon,
                    info_text_color=self.get_rgb(self.footer_brush_color),
                    # info_text_back_color="WHITE",
                    icon_color=self.get_rgb(self.icon_brush_color),
                    micro=self.qr_code_micro
                )
            else:
                print(self.qr_code_frame_path)
                # Clock.schedule_once(lambda dt : self.Abtn_reverse(), 1)
                # return
                _ = codegen.generate_qr_with_frame(data=self.qr_code_data,original_svg_frame_path=os.path.splitext(self.qr_code_frame_path)[0] + ".svg")
            if not _:
                Clock.schedule_once(lambda dt: self.toast("❌ Couldn't generate QR code"),0.2)
                Clock.schedule_once(lambda dt: _modal.dismiss(),0.2)
                Clock.schedule_once(lambda dt : self.Abtn_reverse(), 1)
                return
            print("QR Code Generated",'micro',self.qr_code_micro)
            # self.fit_display_source = "qr_code.png"
            Clock.schedule_once(lambda dt : _modal.dismiss() ,0.1)
            Clock.schedule_once(lambda dt: self.toast("QRcode generated Sucessfuly"),0.2)
            Clock.schedule_once(lambda dt : self.Abtn_reverse(), 1)
            # refresh the files
            self.root.get_screen('home').ids.rv.data.insert(
                0,
                {
                'image_source': _ if isinstance(_,str) else _[1],
                }
            )
            _ = None
        # Clock.schedule_once(lambda x: threading.Thread(target=_gen).start(), 0.1)
        print(self.qr_code_frame,'\n',self.qr_code_frame_path)
        # check micro and data len <11
        if not self.qr_code_data:
            self.toast("QR code data cannot be empty")
            Clock.schedule_once(lambda dt : self.Abtn_reverse(), 1)
            return
        elif self.qr_code_micro and len(self.qr_code_data) > 11:
            print(self.qr_code_data)
            self.toast("Micro QR code can only contain 10 characters")
            Clock.schedule_once(lambda dt : self.Abtn_reverse(), 1)
            return
        elif self.qr_code_frame and not self.qr_code_frame_path:
            self.toast("Please select a frame image")
            Clock.schedule_once(lambda dt : self.Abtn_reverse(), 1)
            return
       # check price
        if self.check_coin_balance(price=self.PRICE_ANIMATED_QR):
            Thread(target=_gen).start()
            # deduct coins
            _ = self.db_.fetch_data()
            self.db_.update_db(
                user_id=_["user_id"],
                theme=_["theme"],
                coins=_["coins"] - self.PRICE_ANIMATED_QR,
                email=_["email"], 
            )
            _ = None
            self.coin_label.text = str(self.db_.fetch_data()["coins"])
        else:
            Clock.schedule_once(lambda dt :self.toast("Not enough coins to generate QR code"),.2)
            Clock.schedule_once(lambda dt : _modal.dismiss() ,.2)
            # show dialog | watch an Ad
            self.show_ad()


_app = MyApp()
_app.run()