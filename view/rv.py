from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout


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