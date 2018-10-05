import functools

from kivy.uix.relativelayout import RelativeLayout
# from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

from model import database
from .miscellaneous import represent_estimator_in_rv
from .rv import RV
from .userestimatorshowlayout import UserEstimatorShowLayout


class UserEstimatorsLayout(RelativeLayout):
    user = ObjectProperty(None, allownone=True)

    def __init__(self, db, **kwargs):
        super(UserEstimatorsLayout, self).__init__(**kwargs)

        self.db = db

        n = 18
        idx = 16
        self.add_widget(Label(text='Search bar:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.45, 'y': 1/n*idx}))
        self.text_input_search_title = TextInput(text='', hint_text='title like', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.20, 1/n), pos_hint={'x': 0.55, 'y': 1/n*idx})
        self.add_widget(self.text_input_search_title)
        self.text_input_search_type = TextInput(text='', hint_text='type like', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.20, 1/n), pos_hint={'x': 0.77, 'y': 1/n*idx})
        self.add_widget(self.text_input_search_type)

        idx -= 1
        self.rv = RV(size_hint=(1, 1/n*idx), pos_hint={'x': 0, 'y': 0})

        # db = database.DB()
        # estimator_list = db.get_estimators_by_user_id(self.user.id)
        # L = [{'text': represent_estimator_in_rv(e), 'on_release': functools.partial(self.show_estimator_on_release, est_id=e.id)} for e in estimator_list]

        # if self.user:
        #     estimator_list = self.db.get_estimators_by_user_id(self.user.id)
        #     L = [{'text': represent_estimator_in_rv(e), 'on_release': functools.partial(self.show_estimator_on_release, est_id=e.id)} for e in estimator_list]
        # else:
        #     L = []

        self.rv.data = []
        self.add_widget(self.rv)

        self.text_input_search_title.bind(text=self.search_bind)
        self.text_input_search_type.bind(text=self.search_bind)

        self.popup_user_estimator_show = Popup(title='Estimator show', title_align='center', content=UserEstimatorShowLayout(), auto_dismiss=False, on_dismiss=self.reload_rv_data, size_hint=(0.95, 0.95), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.popup_user_estimator_show.content.db = self.db

        self.bind(user=self.user_bind)


    def user_bind(self, *args):
        self.reload_rv_data()


    def show_estimator_on_release(self, *args, **kwargs):
        est_id = kwargs['est_id']
        est = self.db.get_estimator_by_id(est_id)
        layout = self.popup_user_estimator_show.content
        layout.assign_estimator(est)
        self.popup_user_estimator_show.open()


    def update_rv_data(self, estimator_list, *args):
        L = [{'text': represent_estimator_in_rv(e), 'on_release': functools.partial(self.show_estimator_on_release, est_id=e.id)} for e in estimator_list]
        # L = [{'text': represent_estimator_in_rv(e)} for e in estimator_list]
        self.rv.data = L


    def reload_rv_data(self, *args):
        self.text_input_search_title.text = ''
        self.text_input_search_type.text = ''

        self.db.create_new_session()

        estimator_list = self.db.get_estimators_by_user_id(self.user.id)
        self.update_rv_data(estimator_list)


    def search_bind(self, *args):
        if not self.user:
            return

        titlelike = '%' + self.text_input_search_title.text + '%'
        typelike = '%' + self.text_input_search_type.text + '%'

        qry = self.db.get_query_estimators_by_user_id(self.user.id)

        if len(titlelike) > 2:
            qry = qry.filter(database.Estimator.title.like(titlelike))
        if len(typelike) > 2:
            qry = qry.filter(database.Estimator.type.like(typelike))

        user_list = qry.all()
        self.update_rv_data(user_list)
