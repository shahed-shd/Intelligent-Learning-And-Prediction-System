import kivy
kivy.require('1.10.0')


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from model.persistentdata import PersistentData
from view.loginscreenlayout import LoginScreenLayout
from view.adminpanelscreenlayout import AdminPanelScreenLayout

class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainScreenManager, self).__init__(**kwargs)

        # Screens
        login_scr = Screen(name='login_screen')
        admin_panel_scr = Screen(name='admin_panel_screen')

        # Screen layouts
        self.login_screen_layout = LoginScreenLayout()
        self.admin_panel_screen_layout = AdminPanelScreenLayout()

        # Adding layouts
        login_scr.add_widget(self.login_screen_layout)
        admin_panel_scr.add_widget(self.admin_panel_screen_layout)

        # Adding screens
        self.add_widget(login_scr)
        self.add_widget(admin_panel_scr)

        self.current = 'login_screen' # 'admin_panel_screen'


    def go_to_admin_panel(self):
        self.transition.direction = 'left'
        self.current = 'admin_panel_screen'


class ILPS(App):
    def __init__(self, **kwargs):
        super(ILPS, self).__init__(**kwargs)


    def build(self):
        return MainScreenManager()


def start():
    persistent_data = PersistentData('data/persistent_data.json')

    app = ILPS()
    app.run()