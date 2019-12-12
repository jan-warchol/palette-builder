from __future__ import division
from jinja2 import Template
from pprint import pprint
from os import path
import sys
import importlib
import palette_builder as builder
import token_styling
import argparse


ABOUT = "Generate editor theme file from palette, styling and config template."


def calc_output_path(palette, input_path):
    dir = path.dirname(input_path)
    extension = path.basename(input_path)\
        .replace("template-", "")\
        .replace(".j2", "")
    filename = palette.slug + "." + extension
    return path.join(dir, filename)


def build_pycharm_snippet(color, style):
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


def build_templating_values(palette, styling_rules):
    """Create a dict with all attributes that can be used in a template"""
    mapping = {"name": palette.name}
    for token, (color_name, style) in styling_rules.items():
        rgb_color = palette.rgb_values()[color_name]
        mapping[token] = {
            "color": rgb_color,
            "style": style,
            "pycharm": build_pycharm_snippet(rgb_color, style)
        }
    mapping.update(palette.rgb_values())
    return mapping


parser = argparse.ArgumentParser(description=ABOUT)
parser.add_argument("--palette", "-p", required=True)
parser.add_argument("--template", "-t", required=True)
args = parser.parse_args()

palette = builder.Palette.load_from_module(args.palette)
styling = build_templating_values(palette, token_styling.rules)

with open(args.template, "r") as f:
    template = Template(f.read())

file = calc_output_path(palette, args.template)
with open(file, "w") as f:
    f.write(template.render(**styling))
    print("Output written to {}".format(file))
