from kivy.uix.screenmanager import ScreenManager, Screen

from .addnewregressionscreen import AddNewRegressionScreen
from .addnewclassificationscreen import AddNewClassificationScreen
from .miscellaneous import layout_color


class AddNewEstimatorScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(AddNewEstimatorScreenManager, self).__init__(**kwargs)

        layout_color(self, (0, 0, 1, 1))

        # screens
        regression_scr = AddNewRegressionScreen(name="regression_screen")
        classification_scr = AddNewClassificationScreen(name="classification_screen")

        # Adding screens
        self.add_widget(regression_scr)
        self.add_widget(classification_scr)

        self.current = "regression_screen"


    def go_to_regression_screen(self, *args):
        self.current = 'regression_screen'


    def go_to_classification_screen(self, *args):
        self.current = 'classification_screen'