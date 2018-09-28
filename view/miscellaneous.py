# Miscellaneous functions are defined here.

import functools

from kivy.graphics import Color, Rectangle


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
