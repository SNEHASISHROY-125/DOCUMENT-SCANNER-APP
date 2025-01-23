'''
kivmoblite
'''

from kivmoblite import Admob
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


# Test ad

test = {
        "appId": "ca-app-pub-2987282397801743~7612741649",
        "banId": "ca-app-pub-2987282397801743/6842585450",
        "intId": "ca-app-pub-3940256099942544/1033173712",
        "testD": []
        }

class KivMobTest(App):
    
    def build(self):
        self.ads = Admob(test)
        self.ads.new_banner(position = "bottom", color = "#ffffff", margin = 0) # Adaptive banner
        self.ads.request_banner()
        self.ads.show_banner()
        # Interstetial
        self.ads.new_interstitial()
        #self.ads.request_interstitial()
        #self.ads.show_interstitial()
        b1 = Button(text='Place banner at 0,40',
                      on_release=lambda a:self.ads.banner_pos([0,120]))
        b2 = Button(text='Show Interstitial',
                      on_release=lambda a:self.show_int())
        box = BoxLayout(orientation="vertical")
        box.add_widget(b1)
        box.add_widget(b2)

        return box
    def show_int(self):
        self.ads.request_interstitial()
        self.ads.show_interstitial()
                      
    def on_resume(self):
        # self.ads.request_interstitial()
        ...

KivMobTest().run()

