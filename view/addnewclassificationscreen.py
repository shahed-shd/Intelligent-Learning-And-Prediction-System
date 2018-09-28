from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from .filechooserpopup import FileChooserPopup


class AddNewClassificationScreen(Screen):
    def __init__(self, **kwargs):
        super(AddNewClassificationScreen, self).__init__(**kwargs)

        n = 11
        idx = 10
        self.label_dialogue = Label(text='', bold=True, italic=True, size_hint=(0.90, 1/n), pos_hint={'x': 0.05, 'y': 1/n*idx})
        self.add_widget(self.label_dialogue)

        idx -= 1
        self.add_widget(Label(text='Title :', bold=True, italic=True, size_hint=(0.20, 1/n), pos_hint={'x': 0.05, 'y': 1/n*idx}))
        self.text_input_title = TextInput(text='', hint_text='Estimator title', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.60, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_title)

        idx -= 2
        self.add_widget(Label(text='Number of features:', bold=True, italic=True, size_hint=(0.20, 1/n), pos_hint={'x': 0.05, 'y': 1/n*idx}))
        self.text_input_n_features = TextInput(text='', hint_text='number of features', password=False, input_filter='int', multiline=False, write_tab=False, focus=False, size_hint=(0.60, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_n_features)

        idx -= 1
        self.add_widget(Label(text='Number of targets:', bold=True, italic=True, size_hint=(0.20, 1/n), pos_hint={'x': 0.05, 'y': 1/n*idx}))
        self.text_input_n_targets = TextInput(text='', hint_text='number of targets', password=False, input_filter='int', multiline=False, write_tab=False, focus=False, size_hint=(0.60, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_n_targets)

        idx -= 2
        self.add_widget(Label(text='Select feature file:', bold=True, italic=True, size_hint=(0.20, 1/n), pos_hint={'x': 0.05, 'y': 1/n*idx}))
        self.text_input_feature_file_choose = TextInput(text='', hint_text='No file selected', readonly=True, size_hint=(0.6, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_feature_file_choose)
        self.feature_file_chooser_popup = FileChooserPopup(size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.feature_file_chooser_popup.bind(on_dismiss=lambda popup_instance, *a: setattr(self.text_input_feature_file_choose, 'text', popup_instance.text_input.text))
        self.add_widget(Button(text='Choose', italic=True, on_release=self.feature_file_chooser_popup.open, size_hint=(0.14, 1/n), pos_hint={'x': 0.85, 'y': 1/n*idx}))

        idx -= 1
        self.add_widget(Label(text='Select target file:', bold=True, italic=True, size_hint=(0.20, 1/n), pos_hint={'x': 0.05, 'y': 1/n*idx}))
        self.text_input_target_file_choose = TextInput(text='', hint_text='No file selected', readonly=True, size_hint=(0.6, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_target_file_choose)
        self.target_file_chooser_popup = FileChooserPopup(size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.target_file_chooser_popup.bind(on_dismiss=lambda popup_instance, *a: setattr(self.text_input_target_file_choose, 'text', popup_instance.text_input.text))
        self.add_widget(Button(text='Choose', italic=True, on_release=self.target_file_chooser_popup.open, size_hint=(0.14, 1/n), pos_hint={'x': 0.85, 'y': 1/n*idx}))

        idx -= 2
        self.add_widget(Button(text='Add', italic=True, on_release=self.btn_add_do, size_hint=(0.15, 1/n), pos_hint={'x': 0.45, 'y': 1/n*idx}))


    def btn_add_do(self, *args):
        print("btn add do pressed.")
        dialogue = ''

        if len(self.text_input_title.text) == 0:
            dialogue = 'Please enter title.'
        elif len(self.text_input_n_features.text) == 0:
            dialogue = 'Please enter number of features.'
        elif len(self.text_input_n_targets.text) == 0:
            dialogue = 'Please enter number of targets.'
        elif len(self.text_input_feature_file_choose.text) == 0:
            dialogue = 'Please choose a feature file.'
        elif len(self.text_input_target_file_choose.text) == 0:
            dialogue = 'Please choose a target file.'

        self.label_dialogue.text = dialogue