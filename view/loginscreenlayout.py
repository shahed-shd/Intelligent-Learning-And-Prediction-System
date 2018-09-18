from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from .miscellaneous import layout_color


class LoginScreenLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(LoginScreenLayout, self).__init__(**kwargs)

        # Canvas color
        layout_color(self, (0.25, 0, 0, 1))

        # Widgets
        n = 15
        idx = 12
        self.dialogue = Label(text='dialogue text goes here', bold=True, italic=True, size_hint=(0.50, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.dialogue)

        idx -= 1
        self.add_widget(Label(text='Username:', bold=True, italic=True, size_hint=(0.25, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx}))
        self.text_input_username = TextInput(text='', hint_text='User name', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.25, 1/n), pos_hint={'x': 0.50, 'y': 1/n*idx})
        self.add_widget(self.text_input_username)

        idx -= 1
        self.add_widget(Label(text='Password:', bold=True, italic=True, size_hint=(0.25, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx}))
        self.text_input_password = TextInput(text='', hint_text='password', password=True, multiline=False, write_tab=False, focus=False, size_hint=(0.25, 1/n), pos_hint={'x': 0.50, 'y': 1/n*idx})
        self.add_widget(self.text_input_password)
        self.btn_show_hide_password = Button(text='Show', italic=True, on_release=self.show_hide_password, size_hint=(0.05, 1/n), pos_hint={'x': 0.75, 'y': 1/n*idx})
        self.add_widget(self.btn_show_hide_password)

        idx -= 1
        self.add_widget(Label(text='Log in as:', bold=True, italic=True, size_hint=(0.25, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx}))
        self.spinner_admin_or_user = Spinner(text='Admin', values=('Admin', 'User'), size_hint=(0.10, 1/n), pos_hint={'x': 0.50, 'y': 1/n*idx})
        self.add_widget(self.spinner_admin_or_user)

        idx -= 2
        self.add_widget(Button(text='Submit', italic=True, on_release=self.btn_submit_do, size_hint=(0.15, 1/n), pos_hint={'x': 0.45, 'y': 1/n*idx}))
        self.add_widget(Button(text='Reset', italic=True, on_release=self.btn_reset_do, size_hint=(0.15, 1/n), pos_hint={'x': 0.60, 'y': 1/n*idx}))


    def show_hide_password(self, *args):
        if self.text_input_password.password:
            self.text_input_password.password = False
            self.btn_show_hide_password.text = 'Hide'
        else:
            self.text_input_password.password = True
            self.btn_show_hide_password.text = 'Show'


    def btn_submit_do(self, *args):
        if self.spinner_admin_or_user.text.lower() == 'admin':
            print("logged in as admin")
        else:
            print("logged in as user")


    def btn_reset_do(self, *args):
        self.text_input_username.text = ''
        self.text_input_password.text = ''
        if not self.text_input_password.password:
            self.show_hide_password()
        self.spinner_admin_or_user.text = 'Admin'
