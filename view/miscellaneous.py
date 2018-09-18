# Miscellaneous functions are defined here.

from kivy.graphics import Color, Rectangle


def layout_color(layout_instance, color_tpl):
    '''Changes the color of `layout_instance`.
    `color_tpl` is a tuple of size 3 or 4, such as (red, green, blue, alpha) wher alpha is optional.'''

    with layout_instance.canvas.before:
        Color(*color_tpl)
        layout_instance.rect = Rectangle(size=layout_instance.size, pos=layout_instance.pos)
    layout_instance.bind(size=lambda *a: setattr(layout_instance.rect, 'size', layout_instance.size), pos=lambda *a: setattr(layout_instance.rect, 'pos', layout_instance.pos))
