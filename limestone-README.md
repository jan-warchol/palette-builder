Limestone colors
----------------

Limestone will be a family of monochrome color palettes and color schemes for
IDEs and text editors. It's currently in early phase of development, no stable
version has been released yet. See `devel` branch for current state of work.

Features
--------

- restrained, minimalistic feel, resulting in professional appearance
- moderate contrast: very readable but not tiring to the eyes
- lightness optimized for maximum shade legibility
- carefully crafted highlighting rules make important information easy to find

Design
------

- based on precise lightness relationships in CIE Lab colorspace
- fully parameterized: foreground and background hues, as well as contrast, can
  be adjusted, with all shades generated from these properties
- token types have shades assigned based on importance, length and frequency
- font attributes (bold, italic, underline) are used to convey additional
  meaning and information about token type

Monochome syntax highlighting
-----------------------------

This is an experiment to see whether it's possible to design a syntax
highlighting theme that uses only shades of grey (and bold/italic/underline),
but still makes the code readable.

Design principles
-----------------

- less important elements should be dimmer:
    - comments should be clearly secondary to the code
    - boilerplate/metadata, for example variable types
- rare and important tokens (e.g. exceptions) shoud be strong, drawing
  attention
- "heading-like" elements that structure the code (e.g. class/function names)
  should be easy to spot from distance, to make navigation easy
- special/language-defined words should have some formatting distinguishing
  them from user-defined values
    - e.g. if you make a typo (like `false` instead of `False` in Python) it
      should be clear from the formatting
