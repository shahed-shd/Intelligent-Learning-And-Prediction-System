from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput


class FileChooserPopup(Popup):
    def __init__(self, **kwargs):
        super(FileChooserPopup, self).__init__(**kwargs)

        self.title = 'Select features file'

        layout = RelativeLayout()

        file_chooser_list_view = FileChooserListView(filters=['*.txt', '*.data'], size_hint=(1, 0.8), pos_hint={'x': 0, 'y': 0.2})
        file_chooser_list_view.bind(selection=self.file_chooser_selection_do)
        self.text_input = TextInput(text='', readonly=True, size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.1})

        layout.add_widget(file_chooser_list_view)
        layout.add_widget(self.text_input)
        layout.add_widget(Button(text='Select', italic=True, on_release=self.dismiss, size_hint=(0.25, 0.1), pos_hint={'x': 0.25, 'y': 0}))
        layout.add_widget(Button(text='Cancel', italic=True, on_release=self.cancel_btn_do, size_hint=(0.25, 0.1), pos_hint={'x': 0.5, 'y': 0}))

        self.content = layout


    def file_chooser_selection_do(self, fc, selection, *a):
        self.text_input.text = selection[0] if selection else ''


    def cancel_btn_do(self, *a):
        self.text_input.text = ''
        self.dismiss()