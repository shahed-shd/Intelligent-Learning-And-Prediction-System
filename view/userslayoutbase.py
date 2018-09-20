import functools

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from model import database

from .miscellaneous import RV, represent_user_in_rv


class UsersLayoutBase(RelativeLayout):
    def __init__(self, **kwargs):
        super(UsersLayoutBase, self).__init__(**kwargs)

        n = 18
        idx = 16
        self.add_widget(Label(text='Search bar:', bold=True, italic=True, size_hint=(0.15, 1/n), pos_hint={'x': 0, 'y': 1/n*idx}))
        self.text_input_search_username = TextInput(text='', hint_text='user name like', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.40, 1/n), pos_hint={'x': 0.15, 'y': 1/n*idx})
        self.add_widget(self.text_input_search_username)
        self.text_input_search_fullname = TextInput(text='', hint_text='full name like', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.40, 1/n), pos_hint={'x': 0.57, 'y': 1/n*idx})
        self.add_widget(self.text_input_search_fullname)

        idx -= 1
        self.rv = RV(size_hint=(1, 1/n*idx), pos_hint={'x': 0, 'y': 0})

        db = database.DB()
        user_list = db.get_users()
        L = [{'text': 'Add new'}]
        L += [{'text': represent_user_in_rv(u), 'on_release': functools.partial(self.show_user_profile_on_release, user_id=u.id)} for u in user_list]

        self.db = db
        self.rv.data = L
        self.add_widget(self.rv)

        self.text_input_search_username.bind(text=self.search_bind)
        self.text_input_search_fullname.bind(text=self.search_bind)


    def update_rv_data(self, user_list, *args):
        L = [{'text': 'Add new'}]
        L += [{'text': represent_user_in_rv(u), 'on_release': functools.partial(self.show_user_profile_on_release, user_id=u.id)} for u in user_list]
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