from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from .addnewestimatorscreenmanager import AddNewEstimatorScreenManager


class AddNewEstimatorLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(AddNewEstimatorLayout, self).__init__(**kwargs)

        n = 16
        idx = 14

        self.add_widget(Label(text='Select type :', bold=True, italic=True, size_hint=(0.20, 1/n), pos_hint={'x': 0.30, 'y': 1/n*idx}))
        self.spinner_estimator_type = Spinner(text='Regression', values=('Regression', 'Classification'), size_hint=(0.20, 1/n), pos_hint={'x': 0.50, 'y': 1/n*idx})
        self.add_widget(self.spinner_estimator_type)

        idx -= 1
        self.add_new_estimator_screen_manager = AddNewEstimatorScreenManager(size_hint=(1, 1/n*11), pos_hint={'x': 0, 'y': 1/n*(idx-11)})
        self.add_widget(self.add_new_estimator_screen_manager)

        idx -= 10
        self.add_widget(Button(text='Cancel', italic=True, on_release=self.btn_cancel_do, size_hint=(0.15, 1/n), pos_hint={'x': 0.02, 'y': 1/n*idx}))

        self.spinner_estimator_type.bind(text=self.spinner_estimator_type_bind)


    def spinner_estimator_type_bind(self, *args):
        t = self.spinner_estimator_type.text
        if t == 'Regression':
            self.add_new_estimator_screen_manager.go_to_regression_screen()
        elif t == 'Classification':
            self.add_new_estimator_screen_manager.go_to_classification_screen()


    def btn_cancel_do(self, *args):
        self.parent.parent.parent.dismiss()
