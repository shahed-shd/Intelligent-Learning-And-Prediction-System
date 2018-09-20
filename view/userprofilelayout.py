from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput




class UserProfileLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(UserProfileLayout, self).__init__(**kwargs)

        self.user = None
        self.db = None
        self.rv_data = None

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

        idx -= 3
        self.add_widget(Label(text='Activity logs:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.10, 'y': 1/n*idx}))
        self.text_input_activity_logs = TextInput(text='', multiline=True, readonly=True, size_hint=(0.70, 1/n*3), pos_hint={'x': 0.25, 'y': 1/n*(idx-2)})
        self.add_widget(self.text_input_activity_logs)

        idx -= 5
        self.btn_reset_info = Button(text='Reset info', italic=True, on_release=self.btn_reset_info_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.35, 'y': 1/n*idx})
        self.add_widget(self.btn_reset_info)
        self.add_widget(Button(text='Remove user', italic=True, on_release=self.btn_remove_user_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.55, 'y': 1/n*idx}))
        self.add_widget(Button(text='Done', italic=True, on_release=self.btn_done_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.75, 'y': 1/n*idx}))

        self.text_input_fullname.bind(text=self.text_input_fullname_text_bind)
        self.text_input_short_bio.bind(text=self.text_input_short_bio_text_bind)
        self.btn_reset_info.disabled = True


    def dismiss_popup(self, *args):
        self.parent.parent.parent.dismiss()
        self.btn_reset_info.disabled = True
        self.label_dialogue.text = ''


    def is_any_change(self):
        val = (self.user and (self.text_input_fullname.text != self.user.fullname or self.text_input_short_bio.text != self.user.short_bio))
        return val


    def text_input_fullname_text_bind(self, *args):
        self.btn_reset_info.disabled = not self.is_any_change()


    def text_input_short_bio_text_bind(self, *args):
        self.btn_reset_info.disabled = not self.is_any_change()


    def assign_user(self, user):
        self.user = user
        self.text_input_username.text = user.username
        self.text_input_fullname.text = user.fullname
        self.text_input_short_bio.text = user.short_bio


    def btn_reset_info_do(self, *args):
        if self.is_any_change():
            self.text_input_fullname.text = self.user.fullname
            self.text_input_short_bio.text = self.user.short_bio
            self.label_dialogue.text = ''


    def btn_remove_user_do(self, *args):
        self.db.delete_user(self.user)
        self.dismiss_popup()


    def btn_done_do(self, *args):
        if self.is_any_change():
            fname = self.text_input_fullname.text
            user2 = self.db.get_user_by_fullname(fname)
            if user2 and user2.id != self.user.id:
                self.label_dialogue.text = "This Full Name belongs to another user, please try another."
                return

            self.db.update_user(self.user, {'fullname': self.text_input_fullname.text, 'short_bio': self.text_input_short_bio.text})
        self.dismiss_popup()