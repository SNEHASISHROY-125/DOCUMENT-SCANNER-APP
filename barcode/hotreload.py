from kivymd.tools.hotreload.app import MDApp
from kivy.lang import Builder
from kivy.factory import Factory
import os
from kivy.properties import BooleanProperty, StringProperty , ListProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.pickers import MDColorPicker
from typing import Union

KV_DIR = os.path.join(os.path.dirname(__file__), "kv")



class MainApp(MDApp):
    # KV_FILES = [os.path.join(KV_DIR, kv_file) for kv_file in os.listdir(KV_DIR) if kv_file.endswith(".kv")]
    KV_FILES = [os.path.join(KV_DIR, "main.kv")]
    DEBUG = True

    dialog = None
    show_line = BooleanProperty(False)
    fit_display_source = StringProperty("segno_custom_qr_code.png")
    #
    icon_brush_color = ListProperty([0,1,.2, 1])
    footer_brush_color = ListProperty([0,1,.2, 1])

    def build_app(self):
        global color_picker
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.set_color_to = "icon_brush_color"
        # color_picker.open()
        color_picker.bind(
            # on_select_color=get_color,
            on_release=self.get_selected_color,
        )
        return Factory.MainScreen()
    
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
        

    def on_select_color(self, instance_gradient_tab, color: list) -> None:
        '''Called when a gradient image is clicked.'''

global color_picker
def get_color(color_picker_instance, selected_color):
    
    print(color_picker,color_picker.get_rgb(selected_color))
    # set color to icon_brush_color
    print(selected_color)
    _ = selected_color  
    # _ = color_picker.get_rgb(selected_color)
    # TODO: pass it to qr code generator method
    app.icon_brush_color = _
    print(app.icon_brush_color)
    # print(selected_color)
    # print(_)
    # print(app.icon_brush_color,_.append(1))
    # color_picker.dismiss()


app = MainApp()
app.run()