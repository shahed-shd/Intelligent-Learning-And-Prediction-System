from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

from model import database
from model.miscellaneous import get_sha256_hex_digest


class UserOwnProfileLayout(RelativeLayout):
    user = ObjectProperty(None, allownone=True)

    def __init__(self, db, **kwargs):
        super(UserOwnProfileLayout, self).__init__(**kwargs)

        self.db = db

        n = 15
        idx = 14
        self.label_dialogue = Label(text='', bold=True, italic=True, size_hint=(1, 1/n), pos_hint={'x': 0.1, 'y': 1/n*idx})
        self.add_widget(self.label_dialogue)

        idx -= 2
        self.add_widget(Label(text='Username:', bold=True, italic=True, size_hint=(0.1, 1/n), pos_hint={'x': 0.1, 'y': 1/n*idx}))
        self.text_input_username = TextInput(text='', readonly=True, size_hint=(0.70, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_username)

        idx -= 1
        self.add_widget(Label(text='Full name:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.10, 'y': 1/n*idx}))
        self.text_input_fullname = TextInput(text='', size_hint=(0.70, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_fullname)

        idx -= 1
        self.add_widget(Label(text='Short bio:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.10, 'y': 1/n*idx}))
        self.text_input_short_bio = TextInput(text='', multiline=True, size_hint=(0.70, 1/n*3), pos_hint={'x': 0.25, 'y': 1/n*(idx-2)})
        self.add_widget(self.text_input_short_bio)

        # idx -= 3
        # self.add_widget(Label(text='Activity logs:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.10, 'y': 1/n*idx}))
        # self.text_input_activity_logs = TextInput(text='', multiline=True, readonly=True, size_hint=(0.70, 1/n*3), pos_hint={'x': 0.25, 'y': 1/n*(idx-2)})
        # self.add_widget(self.text_input_activity_logs)

        idx -= 4
        self.add_widget(Label(text='Change password:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.10, 'y': 1/n*idx}))
        self.text_input_password = TextInput(text='', hint_text='To change password, enter new password', password=True, write_tab=False, size_hint=(0.70, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_password)
        idx -= 1
        self.text_input_confirm_password = TextInput(text='', hint_text='Confirm password', password=True, write_tab=False, size_hint=(0.70, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_confirm_password)

        idx -= 2
        self.btn_reset_info = Button(text='Reset info', italic=True, on_release=self.btn_reset_info_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.35, 'y': 1/n*idx})
        self.add_widget(self.btn_reset_info)
        self.add_widget(Button(text='Done', italic=True, on_release=self.btn_done_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.55, 'y': 1/n*idx}))
        self.add_widget(Button(text='Log out', italic=True, on_release=self.btn_logout_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.75, 'y': 1/n*idx}))

        self.text_input_fullname.bind(text=self.text_input_fullname_text_bind)
        self.text_input_short_bio.bind(text=self.text_input_short_bio_text_bind)
        self.btn_reset_info.disabled = True

        self.bind(user=self.bind_user)


    def btn_logout_do(self, *args):
        scr_mngr = self.parent.parent.parent.manager
        scr_mngr.go_to_login_screen()


    def is_any_change(self):
        val = (self.user and (self.text_input_fullname.text != self.user.fullname or self.text_input_short_bio.text != self.user.short_bio))
        return val


    def text_input_fullname_text_bind(self, *args):
        self.btn_reset_info.disabled = not self.is_any_change()


    def text_input_short_bio_text_bind(self, *args):
        self.btn_reset_info.disabled = not self.is_any_change()


    def bind_user(self, *args):
        if self.user:
            user = self.user
            self.text_input_username.text = user.username
            self.text_input_fullname.text = user.fullname
            self.text_input_short_bio.text = user.short_bio


    def assign_user(self, user):
        self.user = user


    def btn_reset_info_do(self, *args):
        if self.is_any_change():
            self.text_input_fullname.text = self.user.fullname
            self.text_input_short_bio.text = self.user.short_bio
            self.label_dialogue.text = ''


    def btn_done_do(self, *args):
        if self.is_any_change():
            self.user.fullname = self.text_input_fullname.text
            self.user.short_bio = self.text_input_short_bio.text
            self.db.session.commit()

        pw1 = self.text_input_password.text
        pw2 = self.text_input_confirm_password.text

        if len(pw1) > 0:
            if pw1 == pw2:
                self.user.password_hash = get_sha256_hex_digest(pw1)
                self.db.session.commit()
                self.label_dialogue.text = 'Password changed.'
            else:
                self.label_dialogue.text = "Password doesn't match!"
