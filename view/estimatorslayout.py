from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from model import database
from .miscellaneous import represent_estimator_in_rv
from .rv import RV
from .addnewestimatorlayout import AddNewEstimatorLayout


class EstimatorsLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(EstimatorsLayout, self).__init__(**kwargs)

        n = 18
        idx = 16
        self.btn_add_new = Button(text='Add new estimator', italic=True, on_release=self.btn_add_new_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.05, 'y': 1/n*idx})
        self.add_widget(self.btn_add_new)
        self.add_widget(Label(text='Search bar:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.45, 'y': 1/n*idx}))
        self.text_input_search_title = TextInput(text='', hint_text='title like', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.20, 1/n), pos_hint={'x': 0.55, 'y': 1/n*idx})
        self.add_widget(self.text_input_search_title)
        self.text_input_search_type = TextInput(text='', hint_text='type like', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.20, 1/n), pos_hint={'x': 0.77, 'y': 1/n*idx})
        self.add_widget(self.text_input_search_type)

        idx -= 1
        self.rv = RV(size_hint=(1, 1/n*idx), pos_hint={'x': 0, 'y': 0})

        db = database.DB()
        estimator_list = db.get_estimators()
        L = [{'text': represent_estimator_in_rv(e)} for e in estimator_list]

        self.db = db
        self.rv.data = L
        self.add_widget(self.rv)

        self.text_input_search_title.bind(text=self.search_bind)
        self.text_input_search_type.bind(text=self.search_bind)

        self.popup_add_new_estimator = Popup(title='Add new estimator', title_align='center', content=AddNewEstimatorLayout(), auto_dismiss=False, on_dismiss=self.reload_rv_data, size_hint=(0.95, 0.95), pos_hint={'center_x': 0.5, 'center_y': 0.5})


    def btn_add_new_do(self, *args):
        self.popup_add_new_estimator.open()


    def update_rv_data(self, estimator_list, *args):
        L = [{'text': represent_estimator_in_rv(e)} for e in estimator_list]
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
