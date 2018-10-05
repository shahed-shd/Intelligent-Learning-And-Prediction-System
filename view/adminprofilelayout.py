from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from model.persistentdata import PersistentData
from model.globalvalues import GlobalValues


class AdminProfileLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(AdminProfileLayout, self).__init__(**kwargs)

        n = 15
        idx = 14

        self.label_dialogue = Label(text='', bold=True, italic=True, size_hint=(1, 1/n), pos_hint={'x': 0.1, 'y': 1/n*idx})
        self.add_widget(self.label_dialogue)

        idx -= 3
        self.add_widget(Label(text='Change admin username:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.10, 'y': 1/n*idx}))
        self.text_input_admin_username = TextInput(text='', hint_text='To change admin username, enter new admin username', write_tab=False, size_hint=(0.70, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_admin_username)
        idx -= 1
        self.text_input_confirm_admin_username = TextInput(text='', hint_text='Confirm admin username', write_tab=False, size_hint=(0.70, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_confirm_admin_username)

        idx -= 2
        self.add_widget(Label(text='Change password:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.10, 'y': 1/n*idx}))
        self.text_input_password = TextInput(text='', hint_text='To change password, enter new password', password=True, write_tab=False, size_hint=(0.70, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_password)
        idx -= 1
        self.text_input_confirm_password = TextInput(text='', hint_text='Confirm password', password=True, write_tab=False, size_hint=(0.70, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_confirm_password)

        idx -= 2
        self.add_widget(Button(text='Reset', italic=True, on_release=self.btn_reset_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.35, 'y': 1/n*idx}))
        self.add_widget(Button(text='Done', italic=True, on_release=self.btn_done_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.55, 'y': 1/n*idx}))
        self.add_widget(Button(text='Log out', italic=True, on_release=self.btn_logout_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.75, 'y': 1/n*idx}))


    def btn_reset_do(self, *args):
        self.label_dialogue.text = ''

        self.text_input_admin_username.text = ''
        self.text_input_confirm_admin_username.text = ''

        self.text_input_password.text = ''
        self.text_input_confirm_password.text = ''


    def btn_done_do(self, *args):
        # Username section
        un1 = self.text_input_admin_username.text
        un2 = self.text_input_confirm_admin_username.text

        if len(un1) > 0:
            if un1 == un2:
                path = GlobalValues().get_persistent_data_file_path()
                persistent_data = PersistentData(path)

                persistent_data.change_admin_username(un1)
                self.btn_reset_do()
                self.label_dialogue.text = 'Admin username changed.'
            else:
                self.label_dialogue.text = "Admin username doesn't match!"

        # Password section
        pw1 = self.text_input_password.text
        pw2 = self.text_input_confirm_password.text

        if len(pw1) > 0:
            if pw1 == pw2:
                path = GlobalValues().get_persistent_data_file_path()
                persistent_data = PersistentData(path)

                persistent_data.change_admin_password(pw1)
                self.btn_reset_do()
                self.label_dialogue.text = 'Password changed.'
            else:
                self.label_dialogue.text = "Password doesn't match!"


    def btn_logout_do(self, *args):
        self.btn_reset_do()
        scr_mngr = self.parent.parent.parent.parent
        scr_mngr.go_to_login_screen()
