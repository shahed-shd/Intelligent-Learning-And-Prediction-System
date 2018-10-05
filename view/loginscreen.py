from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from .miscellaneous import layout_color
from model.persistentdata import PersistentData
from model.globalvalues import GlobalValues
from model.database import DB
# from model.miscellaneous import get_sha256_hex_digest


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Canvas color
        layout_color(self, (0.25, 0, 0, 1))

        self.db = None

        # Widgets
        n = 15
        idx = 12
        self.dialogue = Label(text='', bold=True, italic=True, size_hint=(0.50, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
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
            path = GlobalValues().get_persistent_data_file_path()
            persistent_data = PersistentData(path)

            username = self.text_input_username.text
            password = self.text_input_password.text

            is_valid = persistent_data.validate_admin_login(username, password)

            if is_valid:
                self.btn_reset_do()
                self.manager.go_to_admin_panel()
            else:
                self.dialogue.text = 'Wrong admin username and password !!!'

        else:
            username = self.text_input_username.text
            password = self.text_input_password.text

            db = self.db
            does_match = db.does_user_password_match(username, password)

            if does_match:
                self.btn_reset_do()
                user = db.get_user_by_username(username)
                self.manager.go_to_user_panel(user=user, db=db)
            else:
                self.dialogue.text = "Username and password mismatch !"



    def btn_reset_do(self, *args):
        self.dialogue.text = ''
        self.text_input_username.text = ''
        self.text_input_password.text = ''
        if not self.text_input_password.password:
            self.show_hide_password()
        self.spinner_admin_or_user.text = 'Admin'
