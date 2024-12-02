import os
from kivy.lang import Builder
from kivy.clock import Clock , mainthread
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivymd.uix.button import MDRaisedButton, MDIconButton
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

class CustomRecycleView(MDRecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [
            {
                'image_source': x,
            } for x in file_list
        ]


class MyApp(MDApp):
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


_app = MyApp()
_app.run()