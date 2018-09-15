import kivy
kivy.require('1.10.0')


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen


from view.screenlayouts import LoginScreenLayout

class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainScreenManager, self).__init__(**kwargs)

        # Screens
        login_scr = Screen(name='login_screen')

        # Screen layouts
        self.login_screen_layout = LoginScreenLayout()

        # Adding layouts
        login_scr.add_widget(self.login_screen_layout)

        # Adding screens
        self.add_widget(login_scr)


class ILPS(App):
    def __init__(self, **kwargs):
        super(ILPS, self).__init__(**kwargs)


    def build(self):
        return MainScreenManager()


def main():
    app = ILPS()
    app.run()


if __name__ == '__main__':
    main()