from kivy.uix.relativelayout import RelativeLayout
import functools

from model import database
from .miscellaneous import RV, represent_user_in_rv


class UsersLayoutBase(RelativeLayout):
    def __init__(self, **kwargs):
        super(UsersLayoutBase, self).__init__(**kwargs)

        self.rv = RV()

        db = database.DB()
        user_list = db.get_users()
        L = [{'text': 'Add new'}]
        L += [{'text': represent_user_in_rv(u), 'on_release': functools.partial(self.show_user_profile_on_release, user_id=u.id)} for u in user_list]

        self.db = db
        self.rv.data = L
        self.add_widget(self.rv)


    def reload_rv_data(self, *args):
        self.db.create_new_session()
        user_list = self.db.get_users()
        L = [{'text': 'Add new'}]
        L += [{'text': represent_user_in_rv(u), 'on_release': functools.partial(self.show_user_profile_on_release, user_id=u.id)} for u in user_list]
        self.rv.data = L
