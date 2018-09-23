import functools

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from model import database
from .miscellaneous import represent_user_in_rv
from .rv import RV
from .userprofilelayout import UserProfileLayout


class UsersLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(UsersLayout, self).__init__(**kwargs)

        n = 18
        idx = 16
        self.btn_add_new = Button(text='Add new user', italic=True, on_release=self.btn_add_new_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.05, 'y': 1/n*idx})
        self.add_widget(self.btn_add_new)
        self.add_widget(Label(text='Search bar:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.45, 'y': 1/n*idx}))
        self.text_input_search_username = TextInput(text='', hint_text='user name like', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.20, 1/n), pos_hint={'x': 0.55, 'y': 1/n*idx})
        self.add_widget(self.text_input_search_username)
        self.text_input_search_fullname = TextInput(text='', hint_text='full name like', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.20, 1/n), pos_hint={'x': 0.77, 'y': 1/n*idx})
        self.add_widget(self.text_input_search_fullname)

        idx -= 1
        self.rv = RV(size_hint=(1, 1/n*idx), pos_hint={'x': 0, 'y': 0})

        db = database.DB()
        user_list = db.get_users()
        # L = [{'text': 'Add new'}]
        L = [{'text': represent_user_in_rv(u), 'on_release': functools.partial(self.show_user_profile_on_release, user_id=u.id)} for u in user_list]

        self.db = db
        self.rv.data = L
        self.add_widget(self.rv)

        self.text_input_search_username.bind(text=self.search_bind)
        self.text_input_search_fullname.bind(text=self.search_bind)

        self.popup_user_profile = Popup(title='User profile', title_align='center', content=UserProfileLayout(), auto_dismiss=False, on_dismiss=self.reload_rv_data, size_hint=(0.95, 0.95), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.popup_user_profile.content.db = self.db


    def btn_add_new_do(self, *args):
        pass


    def show_user_profile_on_release(self, *args, **kwargs):
        user_id = kwargs['user_id']
        user = self.db.get_user_by_id(user_id)
        layout = self.popup_user_profile.content
        layout.assign_user(user)
        self.popup_user_profile.open()


    def update_rv_data(self, user_list, *args):
        # L = [{'text': 'Add new'}]
        L = [{'text': represent_user_in_rv(u), 'on_release': functools.partial(self.show_user_profile_on_release, user_id=u.id)} for u in user_list]
        self.rv.data = L


    def reload_rv_data(self, *args):
        self.text_input_search_username.text = ''
        self.text_input_search_fullname.text = ''

        self.db.create_new_session()
        user_list = self.db.get_users()
        self.update_rv_data(user_list)


    def search_bind(self, *args):
        usernamelike = '%' + self.text_input_search_username.text + '%'
        fullnamelike = '%' + self.text_input_search_fullname.text + '%'

        qry = self.db.session.query(database.User)

        if len(usernamelike) > 2:
            qry = qry.filter(database.User.username.like(usernamelike))
        if len(fullnamelike) > 2:
            qry = qry.filter(database.User.fullname.like(fullnamelike))

        user_list = qry.all()
        self.update_rv_data(user_list)
