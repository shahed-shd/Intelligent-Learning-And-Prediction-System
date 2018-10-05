from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.properties import ObjectProperty

from .userestimatorslayout import UserEstimatorsLayout
from .userownprofilelayout import UserOwnProfileLayout


class UserTabbedPanel(TabbedPanel):
    user = ObjectProperty(None, allownone=True)

    def __init__(self, db, **kwargs):
        super(UserTabbedPanel, self).__init__(**kwargs)

        self.db = db
        self.do_default_tab = False
        self.tab_pos = 'top_mid'

        # Layouts in tabs
        self.user_estimators_layout = UserEstimatorsLayout(db=self.db)
        self.user_own_profile_layout = UserOwnProfileLayout(db=self.db)

        # Adding tabbed panel headers
        self.add_widget(TabbedPanelHeader(text='Estimators', content=self.user_estimators_layout))
        self.add_widget(TabbedPanelHeader(text='Profile', content=self.user_own_profile_layout))

        self.bind(user=self.bind_user)


    def bind_user(self, *args):
        if self.user:
            self.user_estimators_layout.db = self.db
            self.user_estimators_layout.user = self.user

            self.user_own_profile_layout.db = self.db
            self.user_own_profile_layout.user = self.user