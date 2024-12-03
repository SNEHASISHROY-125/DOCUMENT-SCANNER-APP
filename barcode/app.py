import os
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

# from androidstorage4kivy import SharedStorage, Chooser, ShareSheet

# create ./src folder
if not os.path.exists('./src'):
    os.makedirs('./src')
    os.makedirs('./src/qr')
    os.makedirs('./src/pdf')



class HomeScreen(Screen):
    pass

class SettingsScreen(Screen):
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
        hint_text: "AACB1978432" if not dialog_switch.active else "https://www.cb28.com/cp=9?d=1"

    MDBoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: self.minimum_height
        spacing: dp(10)

        MDLabel:
            text: "Create QR code"
            adaptive_height: True

        MDSwitch:
            id: dialog_switch
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

    def generate_codes(self):
        # dialog
        if not self.dialog:
            self.dialog = MDDialog(
                title="Create Barcode",
                type="custom",
                content_cls=Builder.load_string(DIALOG_KV),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="ADD",
                        on_release=lambda x: generate_barcode(self.dialog.content_cls.ids.barcode_textfield.text) if not self.dialog.content_cls.ids.dialog_switch.active else generate_qr_code(self.dialog.content_cls.ids.barcode_textfield.text)
                    ),
                ],
            )
        self.dialog.open()

    def on_switch_active(self, instance, value):
        # dialog.title = self.dialog.children[0].children[-1].text
        # set 
        self.dialog.children[0].children[-1].text = "Create QR code" if value else "Create Barcode"
        print(f"Switch is now {'on' if value else 'off'}")

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
        self.theme_cls.theme_style = 'Dark' 
        return Builder.load_file('app.kv')
    
    def on_start(self):
        self.refresh_files()

    def refresh_files(self):
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

    def delete_file(self, file):
        os.remove(file)
        Clock.schedule_once(lambda dt : self.refresh_files() ,0.2)

def generate_qr_code(code:any):
    print('qr',code)

def generate_barcode(code:any):
    print(code)


_app = MyApp()
_app.run()