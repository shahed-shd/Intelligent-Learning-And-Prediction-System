import kivy
kivy.require('1.10.0')


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from model import database
from model.persistentdata import PersistentData
from view.loginscreen import LoginScreen
from view.admintabbedpanel import AdminTabbedPanel
from view.usertabbedpanel import UserTabbedPanel


class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainScreenManager, self).__init__(**kwargs)

        self.db = database.DB()

        # Screens
        login_scr = LoginScreen(name='login_screen')
        admin_panel_scr = Screen(name='admin_panel_screen')
        user_panel_scr = Screen(name='user_panel_screen')

        login_scr.db = self.db

        # Screen layouts
        self.admin_tabbed_panel = AdminTabbedPanel()
        self.user_tabbed_panel = UserTabbedPanel(db=self.db)

        # Adding layouts
        admin_panel_scr.add_widget(self.admin_tabbed_panel)
        user_panel_scr.add_widget(self.user_tabbed_panel)

        # Adding screens
        self.add_widget(login_scr)
        self.add_widget(admin_panel_scr)
        self.add_widget(user_panel_scr)

        self.current = 'login_screen'
        # self.current = 'admin_panel_screen'
        # self.current = 'user_panel_screen'


    def go_to_admin_panel(self, *args):
        self.transition.direction = 'left'
        self.current = 'admin_panel_screen'


    def go_to_user_panel(self, user, db):
        self.transition.direction = 'left'
        self.user_tabbed_panel.db = db
        self.user_tabbed_panel.user = user
        self.current = 'user_panel_screen'


    def go_to_login_screen(self, *args):
        self.transition.direction = 'right'
        self.current = 'login_screen'


class ILPS(App):
    def __init__(self, **kwargs):
        super(ILPS, self).__init__(**kwargs)


    def build(self):
        return MainScreenManager()


def start():
    persistent_data = PersistentData('data/persistent_data.json')

    app = ILPS()
    app.run()