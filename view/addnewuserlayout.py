from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class AddNewUserLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(AddNewUserLayout, self).__init__(**kwargs)

        self.userslayout_instance = None

        n = 15
        idx = 14
        self.label_dialogue = Label(text='', bold=True, italic=True, size_hint=(1, 1/n), pos_hint={'x': 0.1, 'y': 1/n*idx})
        self.add_widget(self.label_dialogue)

        idx -= 2
        self.add_widget(Label(text='Username:', bold=True, italic=True, size_hint=(0.1, 1/n), pos_hint={'x': 0.1, 'y': 1/n*idx}))
        self.text_input_username = TextInput(text='', write_tab=False, focus=False, size_hint=(0.70, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_username)

        idx -= 1
        self.add_widget(Label(text='Full name:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.10, 'y': 1/n*idx}))
        self.text_input_fullname = TextInput(text='', write_tab=False, focus=False, size_hint=(0.70, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_fullname)

        idx -= 1
        self.add_widget(Label(text='Short bio:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.10, 'y': 1/n*idx}))
        self.text_input_short_bio = TextInput(text='', multiline=True, write_tab=False, focus=False, size_hint=(0.70, 1/n*3), pos_hint={'x': 0.25, 'y': 1/n*(idx-2)})
        self.add_widget(self.text_input_short_bio)

        idx -= 3
        self.add_widget(Label(text='Password:', bold=True, italic=True, size_hint=(0.1, 1/n), pos_hint={'x': 0.1, 'y': 1/n*idx}))
        self.text_input_password = TextInput(text='', write_tab=False, focus=False, size_hint=(0.70, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.text_input_password)

        idx -= 3
        self.add_widget(Button(text='Cancel', italic=True, on_release=self.btn_cancel_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.55, 'y': 1/n*idx}))
        self.add_widget(Button(text='Add', italic=True, on_release=self.btn_add_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.75, 'y': 1/n*idx}))


    def reset(self, *args):
        self.label_dialogue.text = ''
        self.text_input_username.text = ''
        self.text_input_fullname.text = ''
        self.text_input_password.text = ''


    def btn_add_do(self, *args):
        new_username = self.text_input_username.text
        new_fullname = self.text_input_fullname.text
        new_password = self.text_input_password.text

        db = self.userslayout_instance.db

        if len(new_username) == 0:
            self.label_dialogue.text = 'Enter username.'
        elif len(new_username) > 0 and db.get_user_by_username(new_username):
            self.label_dialogue.text = "Username already exists, please try another."
        elif len(new_fullname) == 0:
            self.label_dialogue.text = 'Enter full name.'
        elif len(new_password) == 0:
            self.label_dialogue.text = 'Enter password.'
        else:
            db.add_user_by_attributes(user_id=None, username=new_username, fullname=new_fullname, short_bio=self.text_input_short_bio.text, raw_password=new_password)

            u = db.get_user_by_username(new_username)
            self.userslayout_instance.rv_data_append(u)

            self.reset()
            self.label_dialogue.text = 'User added.'


    def btn_cancel_do(self, *args):
        self.parent.parent.parent.dismiss()