from kivy.uix.popup import Popup

from .userprofilelayout import UserProfileLayout
from .userslayoutbase import UsersLayoutBase


class UsersLayout(UsersLayoutBase):
    def __init__(self, **kwargs):
        super(UsersLayout, self).__init__(**kwargs)

        self.popup_user_profile = Popup(title='User profile', title_align='center', content=UserProfileLayout(), auto_dismiss=False, on_dismiss=self.reload_rv_data, size_hint=(0.95, 0.95), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.popup_user_profile.content.db = self.db


    def show_user_profile_on_release(self, *args, **kwargs):
        user_id = kwargs['user_id']
        user = self.db.get_user_by_id(user_id)
        layout = self.popup_user_profile.content
        layout.assign_user(user)
        self.popup_user_profile.open()
