from __future__ import division
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color


class SimpleLab(object):
    def __init__(self, coords):
        self.l = coords[0]
        self.a = coords[1]
        self.b = coords[2]


class Palette(object):
    def __init__(self, name, background, foreground, shade_specs):
        self.name = name
        self.bg = SimpleLab(background)
        self.fg = SimpleLab(foreground)
        self.contrast = self.fg.l - self.bg.l

        self.colors = {}
        self.colors["fg_0"] = foreground
        self.colors["bg_0"] = background

        self.build_shades(shade_specs)

    @classmethod
    def load_from_module(cls, module_name):
        import importlib
        config = importlib.import_module(module_name)
        return cls(config.name,
                   config.background,
                   config.foreground,
                   config.shades)

    def build_shades(self, shade_specs):
        for name, lightness in shade_specs.items():
            if name.startswith("bg"):
                self.colors[name] = self.background_shade(lightness)
            elif name.startswith("fg"):
                self.colors[name] = self.foreground_shade(lightness)
            else:
                self.colors[name] = self.secondary_shade(lightness)

    def secondary_shade(self, relative_lightness):
        lightness = self.bg.l + relative_lightness * self.contrast
        fg_weight = relative_lightness
        bg_weight = 1 - relative_lightness
        a = fg_weight * self.fg.a + bg_weight * self.bg.a
        b = fg_weight * self.fg.b + bg_weight * self.bg.b
        return (lightness, a, b)

    def foreground_shade(self, relative_lightness):
        lightness = self.bg.l + relative_lightness * self.contrast
        return (lightness, self.fg.a, self.fg.b)

    def background_shade(self, relative_lightness):
        lightness = self.bg.l + relative_lightness * self.contrast
        return (lightness, self.bg.a, self.bg.b)

    def lab_colors(self):
        return {
            name: LabColor(*coords, illuminant='d50')
            for name, coords in self.colors.items()
        }

    def rgb_values(self):
        return {
            name: convert_color(lab, sRGBColor).get_rgb_hex().replace('#', '')
            for name, lab in self.lab_colors().items()
        }


if __name__ == "__main__":
    import sys
    import pprint

    if len(sys.argv) < 2:
        print("Missing argument: palette module name")
        sys.exit()

    p = Palette.load_from_module(sys.argv[1])
    pprint.pprint(p.colors)



