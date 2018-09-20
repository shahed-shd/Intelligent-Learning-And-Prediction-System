from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout


from model import database
from .miscellaneous import represent_estimator_in_rv


class RBL(RecycleBoxLayout):
    def __init__(self, **kwargs):
        super(RBL, self).__init__(**kwargs)

        self.default_size_hint = (1, None)
        self.default_size = (None, 100)
        self.size_hint_y = None
        self.bind(minimum_height=lambda a, b: setattr(self, 'height', b))
        self.orientation = 'vertical'


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.add_widget(RBL())
        self.viewclass = 'Button'
        # self.data = [{'text': str(x) + '\n' + 'Hello', 'on_release': lambda *args: print("Hello kivy")} for x in range(100)]


class EstimatorsLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(EstimatorsLayout, self).__init__(**kwargs)

        self.rv = RV()

        db = database.DB()
        estimator_list = db.get_estimators()
        L = [{'text': 'Add new'}]
        L += [{'text': represent_estimator_in_rv(e)} for e in estimator_list]

        self.rv.data = L

        self.add_widget(self.rv)