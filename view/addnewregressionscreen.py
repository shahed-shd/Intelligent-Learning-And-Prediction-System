from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import numpy as np

from model.database import DB
from controller.miscellaneous import prepare_regression_estimator
from .filechooserpopup import FileChooserPopup


class AddNewRegressionScreen(Screen):
    def __init__(self, **kwargs):
        super(AddNewRegressionScreen, self).__init__(**kwargs)

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
        self.add_widget(Button(text='Reset', italic=True, on_release=self.reset_input_fields, size_hint=(0.15, 1/n), pos_hint={'x': 0.30, 'y': 1/n*idx}))
        self.add_widget(Button(text='Add', italic=True, on_release=self.btn_add_do, size_hint=(0.15, 1/n), pos_hint={'x': 0.45, 'y': 1/n*idx}))

        self.popup_progress_bar = PopupProgressBar(title='Please wait . . .', title_align='center', auto_dismiss=False, size_hint=(0.95, 0.95), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.db = DB()


    def reset_input_fields(self, *args):
        self.dialogue = ''
        self.text_input_title.text = ''
        self.text_input_n_features.text = ''
        self.text_input_n_targets.text = ''
        self.text_input_feature_file_choose.text = ''
        self.text_input_target_file_choose.text = ''


    def btn_add_do(self, *args):
        print("btn add do pressed.")

        dialogue = ''

        if len(self.text_input_title.text) == 0:
            dialogue = 'Please enter title.'
        elif self.db.does_estimator_title_exist(self.text_input_title.text):
            dialogue = 'Title already exists. Try another.'
        elif len(self.text_input_n_features.text) == 0:
            dialogue = 'Please enter number of features.'
        elif len(self.text_input_n_targets.text) == 0:
            dialogue = 'Please enter number of targets.'
        elif len(self.text_input_feature_file_choose.text) == 0:
            dialogue = 'Please choose a feature file.'
        elif len(self.text_input_target_file_choose.text) == 0:
            dialogue = 'Please choose a target file.'
        else:
            try:
                X = np.loadtxt(self.text_input_feature_file_choose.text)
                X = X.reshape(-1, int(self.text_input_n_features.text))
                y = np.loadtxt(self.text_input_target_file_choose.text)
            except Exception as e:
                dialogue = str(e)

        if len(dialogue) == 0:
                fc = int(self.text_input_n_features.text)
                tc = int(self.text_input_n_targets.text)

                if X.shape[0] != y.shape[0]:
                    dialogue = "Number of rows in Feature file and target file mismatch !"
                elif X.shape[1] != fc:
                    dialogue = "Feature file doesn't contain {} columns !".format(fc)
                elif tc == 1:
                    if y.ndim != 1:
                        dialogue = "Target file doesn't contain {} columns !".format(tc)
                elif tc > 1:
                    if tc != y.shape[1]:
                        dialogue = "Target file doesn't contain {} columns !".format(tc)

        self.label_dialogue.text = dialogue

        if dialogue != '':
            return

        self.label_dialogue.text = 'Please wait . . .'
        prepare_regression_estimator(X, y, title=self.text_input_title.text, features_file_path=self.text_input_feature_file_choose.text, targets_file_path=self.text_input_target_file_choose.text)
        self.reset_input_fields()
        self.label_dialogue.text = 'Estimator added.'
