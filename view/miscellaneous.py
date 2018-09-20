# Miscellaneous functions are defined here.

from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.graphics import Color, Rectangle


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


def layout_color(layout_instance, color_tpl):
    '''Changes the color of `layout_instance`.
    `color_tpl` is a tuple of size 3 or 4, such as (red, green, blue, alpha) wher alpha is optional.'''

    with layout_instance.canvas.before:
        Color(*color_tpl)
        layout_instance.rect = Rectangle(size=layout_instance.size, pos=layout_instance.pos)
    layout_instance.bind(size=lambda *a: setattr(layout_instance.rect, 'size', layout_instance.size), pos=lambda *a: setattr(layout_instance.rect, 'pos', layout_instance.pos))


def represent_estimator_in_rv(estimator_ob):
    e = estimator_ob
    return "Title: {title}\nType: {type}\nFeatures: {n_features}, Targets: {n_targets}\nBuild time: {buildtime}".format(title=e.title, type=e.type, n_features=e.n_features, n_targets=e.n_targets, buildtime=e.build_datetime)


def represent_user_in_rv(user_ob):
    u = user_ob
    return "Username: {username}\nFull name: {fullname}".format(username=u.username, fullname=u.fullname)
