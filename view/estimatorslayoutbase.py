from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from model import database
from .miscellaneous import represent_estimator_in_rv
from .rv import RV


class EstimatorsLayoutBase(RelativeLayout):
    def __init__(self, **kwargs):
        super(EstimatorsLayoutBase, self).__init__(**kwargs)

        n = 18
        idx = 16
        self.add_widget(Label(text='Search bar:', bold=True, italic=True, size_hint=(0.15, 1/n), pos_hint={'x': 0, 'y': 1/n*idx}))
        self.text_input_search_title = TextInput(text='', hint_text='title like', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.40, 1/n), pos_hint={'x': 0.15, 'y': 1/n*idx})
        self.add_widget(self.text_input_search_title)
        self.text_input_search_type = TextInput(text='', hint_text='type like', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.40, 1/n), pos_hint={'x': 0.57, 'y': 1/n*idx})
        self.add_widget(self.text_input_search_type)

        idx -= 1
        self.rv = RV(size_hint=(1, 1/n*idx), pos_hint={'x': 0, 'y': 0})

        db = database.DB()
        estimator_list = db.get_estimators()
        L = [{'text': 'Add new'}]
        L += [{'text': represent_estimator_in_rv(e)} for e in estimator_list]

        self.db = db
        self.rv.data = L
        self.add_widget(self.rv)

        self.text_input_search_title.bind(text=self.search_bind)
        self.text_input_search_type.bind(text=self.search_bind)


    def update_rv_data(self, estimator_list, *args):
        L = [{'text': 'Add new'}]
        L += [{'text': represent_estimator_in_rv(e)} for e in estimator_list]
        self.rv.data = L

    def reload_rv_data(self, *args):
        self.text_input_search_title.text = ''
        self.text_input_search_type.text = ''

        self.db.create_new_session()
        estimator_list = self.db.get_estimators()
        self.update_rv_data(estimator_list)


    def search_bind(self, *args):
        titlelike = '%' + self.text_input_search_title.text + '%'
        typelike = '%' + self.text_input_search_type.text + '%'

        qry = self.db.session.query(database.Estimator)

        if len(titlelike) > 2:
            qry = qry.filter(database.Estimator.title.like(titlelike))
        if len(typelike) > 2:
            qry = qry.filter(database.Estimator.type.like(typelike))

        user_list = qry.all()
        self.update_rv_data(user_list)
