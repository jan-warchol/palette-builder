from __future__ import division
from jinja2 import Template
from pprint import pprint
import sys
import importlib
import palette_builder as builder
import token_styling


def expand_pycharm(color, style):
    attributes = set(style.split())
    result = ['<option name="FOREGROUND" value="{}" />'.format(color)]

    if "bold" in attributes and "italic" in attributes:
        result.append('<option name="FONT_TYPE" value="3" />')
    elif "bold" in attributes:
        result.append('<option name="FONT_TYPE" value="1" />')
    elif "italic" in attributes:
        result.append('<option name="FONT_TYPE" value="2" />')

    if "underline" in attributes:
        result.append('<option name="EFFECT_COLOR" value="{}" />'.format(color))
        result.append('<option name="EFFECT_TYPE" value="1" />')

    return '\n        '.join(result)


if len(sys.argv) < 2:
    print("Missing argument: palette module name")
    sys.exit()

palette = builder.Palette.load_from_module(sys.argv[1])

pycharm_styling = {
    token: expand_pycharm(palette.rgb_values()[color_name], style)
    for token, (color_name, style) in token_styling.rules.items()
}

values = {"name": palette.name}
values.update(palette.rgb_values())
values.update(pycharm_styling)

with open("pycharm.j2", "r") as f:
    template = Template(f.read())

with open("pycharm.icls", "w") as f:
    f.write(template.render(**values))
