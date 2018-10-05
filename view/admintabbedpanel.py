from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader

from .estimatorslayout import EstimatorsLayout
from .userslayout import UsersLayout
from .usersvsestimatorslayout import UsersVSEstimatorsLayout
from .activitylogslayout import ActivityLogsLayout
from .adminprofilelayout import AdminProfileLayout


class AdminTabbedPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super(AdminTabbedPanel, self).__init__(**kwargs)

        self.do_default_tab = False
        self.tab_pos = 'top_mid'

        # Layouts in tabs
        self.estimators_layout = EstimatorsLayout()
        self.users_layout = UsersLayout()
        self.users_vs_estimators_layout = UsersVSEstimatorsLayout()
        # self.activity_logs_layout = ActivityLogsLayout()
        self.admin_profile_layout = AdminProfileLayout()

        # Adding tabbed panel headers
        self.add_widget(TabbedPanelHeader(text='Estimators', content=self.estimators_layout))
        self.add_widget(TabbedPanelHeader(text='Users', content=self.users_layout))
        self.add_widget(TabbedPanelHeader(text='Users VS\nEstimators', content=self.users_vs_estimators_layout))
        # self.add_widget(TabbedPanelHeader(text='Activity logs', content=self.activity_logs_layout))
        self.add_widget(TabbedPanelHeader(text='Profile', content=self.admin_profile_layout))
