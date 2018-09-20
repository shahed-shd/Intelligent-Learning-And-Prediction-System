from kivy.uix.relativelayout import RelativeLayout

from model import database
from .miscellaneous import RV, represent_estimator_in_rv


class EstimatorsLayoutBase(RelativeLayout):
    def __init__(self, **kwargs):
        super(EstimatorsLayoutBase, self).__init__(**kwargs)

        self.rv = RV()

        db = database.DB()
        estimator_list = db.get_estimators()
        L = [{'text': 'Add new'}]
        L += [{'text': represent_estimator_in_rv(e)} for e in estimator_list]

        self.db = db
        self.rv.data = L
        self.add_widget(self.rv)


    def reload_rv_data(self, *args):
        self.db.create_new_session()
        estimator_list = db.get_estimators()
        L = [{'text': 'Add new'}]
        L += [{'text': represent_estimator_in_rv(e)} for e in estimator_list]
        self.rv.data = L