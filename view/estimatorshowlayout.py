import io

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

import numpy as np

from controller.miscellaneous import get_prediction


class EstimatorShowLayout(RelativeLayout):
    est = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super(EstimatorShowLayout, self).__init__(**kwargs)

        self.db = None

        n = 15
        idx = 14
        self.label_dialogue = Label(text='', bold=True, italic=True, size_hint=(1, 1/n), pos_hint={'x': 0.1, 'y': 1/n*idx})
        self.add_widget(self.label_dialogue)

        idx -= 2
        self.label_features = Label(text='Features:', bold=True, italic=True, size_hint=(0.1, 1/n), pos_hint={'x': 0.1, 'y': 1/n*idx})
        self.add_widget(self.label_features)
        self.text_input_features = TextInput(text='', multiline=True, size_hint=(0.70, 1/n*5), pos_hint={'x': 0.25, 'y': 1/n*(idx-4)})
        self.add_widget(self.text_input_features)

        idx -= 5
        self.label_targets = Label(text='Targets:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.10, 'y': 1/n*idx})
        self.add_widget(self.label_targets)
        self.text_input_targets = TextInput(text='', readonly=True, multiline=True, size_hint=(0.70, 1/n*5), pos_hint={'x': 0.25, 'y': 1/n*(idx-4)})
        self.add_widget(self.text_input_targets)

        idx -= 6
        self.add_widget(Button(text='Back', italic=True, on_release=self.btn_back_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.15, 'y': 1/n*idx}))
        self.add_widget(Button(text='Reset inputs', italic=True, on_release=self.btn_reset_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.35, 'y': 1/n*idx}))
        self.add_widget(Button(text='Remove estimator', italic=True, on_release=self.btn_remove_estimator_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.55, 'y': 1/n*idx}))
        self.add_widget(Button(text='Predict', italic=True, on_release=self.btn_predict_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.75, 'y': 1/n*idx}))

        self.bind(est=self.bind_est)


    def bind_est(self, *args):
        if self.est:
            est = self.est
            self.label_features.text = "Features ({}):".format(est.n_features)
            self.label_targets.text = "Targets ({}):".format(est.n_targets)


    def assign_estimator(self, est):
        self.est = est


    def btn_reset_do(self, *args):
        self.text_input_features.text = ''
        self.text_input_targets.text = ''
        self.label_dialogue.text = ''


    def btn_back_do(self, *args):
        self.btn_reset_do()
        self.dismiss_popup()


    def dismiss_popup(self, *args):
        self.parent.parent.parent.dismiss()
        self.btn_reset_do()


    def btn_remove_estimator_do(self, *args):
        self.db.delete_estimator(self.est)
        self.dismiss_popup()


    def btn_predict_do(self, *args):
        feat_str = self.text_input_features.text

        if len(feat_str) == 0:
            self.label_dialogue.text = "Enter features to get prediction."
            return

        try:
            X = np.fromstring(feat_str, sep=' ')
        except Exception as e:
            self.label_dialogue.text = str(e)
            return

        est = self.est
        fc = est.n_features
        try:
            X = X.reshape(-1, fc)
        except:
            self.label_dialogue.text = "Please input in proper format."
            return

        if X.shape[0] < 1:
            self.label_dialogue.text = "Please input in proper format."
            return

        y = get_prediction(X, est.id)

        self.text_input_targets.text = str(y.reshape(-1, est.n_targets))
