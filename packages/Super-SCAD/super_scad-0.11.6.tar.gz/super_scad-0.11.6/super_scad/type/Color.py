import re
from typing import List, Tuple


class Color:
    """
    Class for representing colors.
    """
    __colors = {  # Available color names are taken from the World Wide Web Consortium's SVG color list.
        # https://www.w3.org/TR/css-color-3/
        'black':                (0.0, 0.0, 0.0),
        'navy':                 (0.0, 0.0, 128 / 255),
        'darkblue':             (0.0, 0.0, 139 / 255),
        'mediumblue':           (0.0, 0.0, 205 / 255),
        'blue':                 (0.0, 0.0, 1.0),
        'darkgreen':            (0.0, 100 / 255, 0.0),
        'green':                (0.0, 128 / 255, 0.0),
        'teal':                 (0.0, 128 / 255, 128 / 255),
        'darkcyan':             (0.0, 139 / 255, 139 / 255),
        'deepskyblue':          (0.0, 191 / 255, 1.0),
        'darkturquoise':        (0.0, 206 / 255, 209 / 255),
        'mediumspringgreen':    (0.0, 250 / 255, 154 / 255),
        'lime':                 (0.0, 1.0, 0.0),
        'springgreen':          (0.0, 1.0, 127 / 255),
        'cyan':                 (0.0, 1.0, 1.0),
        'aqua':                 (0.0, 1.0, 1.0),
        'midnightblue':         (25 / 255, 25 / 255, 112 / 255),
        'dodgerblue':           (30 / 255, 144 / 255, 1.0),
        'lightseagreen':        (32 / 255, 178 / 255, 170 / 255),
        'forestgreen':          (34 / 255, 139 / 255, 34 / 255),
        'seagreen':             (46 / 255, 139 / 255, 87 / 255),
        'darkslategray':        (47 / 255, 79 / 255, 79 / 255),
        'darkslategrey':        (47 / 255, 79 / 255, 79 / 255),
        'limegreen':            (50 / 255, 205 / 255, 50 / 255),
        'mediumseagreen':       (60 / 255, 179 / 255, 113 / 255),
        'turquoise':            (64 / 255, 224 / 255, 208 / 255),
        'royalblue':            (65 / 255, 105 / 255, 225 / 255),
        'steelblue':            (70 / 255, 130 / 255, 180 / 255),
        'darkslateblue':        (72 / 255, 61 / 255, 139 / 255),
        'mediumturquoise':      (72 / 255, 209 / 255, 204 / 255),
        'indigo':               (75 / 255, 0.0, 130 / 255),
        'darkolivegreen':       (85 / 255, 107 / 255, 47 / 255),
        'cadetblue':            (95 / 255, 158 / 255, 160 / 255),
        'cornflowerblue':       (100 / 255, 149 / 255, 237 / 255),
        'mediumaquamarine':     (102 / 255, 205 / 255, 170 / 255),
        'dimgray':              (105 / 255, 105 / 255, 105 / 255),
        'dimgrey':              (105 / 255, 105 / 255, 105 / 255),
        'slateblue':            (106 / 255, 90 / 255, 205 / 255),
        'olivedrab':            (107 / 255, 142 / 255, 35 / 255),
        'slategray':            (112 / 255, 128 / 255, 144 / 255),
        'slategrey':            (112 / 255, 128 / 255, 144 / 255),
        'lightslategray':       (119 / 255, 136 / 255, 153 / 255),
        'lightslategrey':       (119 / 255, 136 / 255, 153 / 255),
        'mediumslateblue':      (123 / 255, 104 / 255, 238 / 255),
        'lawngreen':            (124 / 255, 252 / 255, 0.0),
        'chartreuse':           (127 / 255, 1.0, 0.0),
        'aquamarine':           (127 / 255, 1.0, 212 / 255),
        'maroon':               (128 / 255, 0.0, 0.0),
        'purple':               (128 / 255, 0.0, 128 / 255),
        'olive':                (128 / 255, 128 / 255, 0.0),
        'gray':                 (128 / 255, 128 / 255, 128 / 255),
        'grey':                 (128 / 255, 128 / 255, 128 / 255),
        'skyblue':              (135 / 255, 206 / 255, 235 / 255),
        'lightskyblue':         (135 / 255, 206 / 255, 250 / 255),
        'blueviolet':           (138 / 255, 43 / 255, 226 / 255),
        'darkred':              (139 / 255, 0.0, 0.0),
        'darkmagenta':          (139 / 255, 0.0, 139 / 255),
        'saddlebrown':          (139 / 255, 69 / 255, 19 / 255),
        'darkseagreen':         (143 / 255, 188 / 255, 143 / 255),
        'lightgreen':           (144 / 255, 238 / 255, 144 / 255),
        'mediumpurple':         (147 / 255, 112 / 255, 219 / 255),
        'darkviolet':           (148 / 255, 0.0, 211 / 255),
        'palegreen':            (152 / 255, 251 / 255, 152 / 255),
        'darkorchid':           (153 / 255, 50 / 255, 204 / 255),
        'yellowgreen':          (154 / 255, 205 / 255, 50 / 255),
        'sienna':               (160 / 255, 82 / 255, 45 / 255),
        'brown':                (165 / 255, 42 / 255, 42 / 255),
        'darkgray':             (169 / 255, 169 / 255, 169 / 255),
        'darkgrey':             (169 / 255, 169 / 255, 169 / 255),
        'lightblue':            (173 / 255, 216 / 255, 230 / 255),
        'greenyellow':          (173 / 255, 1.0, 47 / 255),
        'paleturquoise':        (175 / 255, 238 / 255, 238 / 255),
        'lightsteelblue':       (176 / 255, 196 / 255, 222 / 255),
        'powderblue':           (176 / 255, 224 / 255, 230 / 255),
        'firebrick':            (178 / 255, 34 / 255, 34 / 255),
        'darkgoldenrod':        (184 / 255, 134 / 255, 11 / 255),
        'mediumorchid':         (186 / 255, 85 / 255, 211 / 255),
        'rosybrown':            (188 / 255, 143 / 255, 143 / 255),
        'darkkhaki':            (189 / 255, 183 / 255, 107 / 255),
        'silver':               (192 / 255, 192 / 255, 192 / 255),
        'mediumvioletred':      (199 / 255, 21 / 255, 133 / 255),
        'indianred':            (205 / 255, 92 / 255, 92 / 255),
        'peru':                 (205 / 255, 133 / 255, 63 / 255),
        'chocolate':            (210 / 255, 105 / 255, 30 / 255),
        'tan':                  (210 / 255, 180 / 255, 140 / 255),
        'lightgray':            (211 / 255, 211 / 255, 211 / 255),
        'lightgrey':            (211 / 255, 211 / 255, 211 / 255),
        'thistle':              (216 / 255, 191 / 255, 216 / 255),
        'orchid':               (218 / 255, 112 / 255, 214 / 255),
        'goldenrod':            (218 / 255, 165 / 255, 32 / 255),
        'palevioletred':        (219 / 255, 112 / 255, 147 / 255),
        'crimson':              (220 / 255, 20 / 255, 60 / 255),
        'gainsboro':            (220 / 255, 220 / 255, 220 / 255),
        'plum':                 (221 / 255, 160 / 255, 221 / 255),
        'burlywood':            (222 / 255, 184 / 255, 135 / 255),
        'lightcyan':            (224 / 255, 1.0, 1.0),
        'lavender':             (230 / 255, 230 / 255, 250 / 255),
        'darksalmon':           (233 / 255, 150 / 255, 122 / 255),
        'violet':               (238 / 255, 130 / 255, 238 / 255),
        'palegoldenrod':        (238 / 255, 232 / 255, 170 / 255),
        'lightcoral':           (240 / 255, 128 / 255, 128 / 255),
        'khaki':                (240 / 255, 230 / 255, 140 / 255),
        'aliceblue':            (240 / 255, 248 / 255, 1.0),
        'honeydew':             (240 / 255, 1.0, 240 / 255),
        'azure':                (240 / 255, 1.0, 1.0),
        'sandybrown':           (244 / 255, 164 / 255, 96 / 255),
        'wheat':                (245 / 255, 222 / 255, 179 / 255),
        'beige':                (245 / 255, 245 / 255, 220 / 255),
        'whitesmoke':           (245 / 255, 245 / 255, 245 / 255),
        'mintcream':            (245 / 255, 1.0, 250 / 255),
        'ghostwhite':           (248 / 255, 248 / 255, 1.0),
        'salmon':               (250 / 255, 128 / 255, 114 / 255),
        'antiquewhite':         (250 / 255, 235 / 255, 215 / 255),
        'linen':                (250 / 255, 240 / 255, 230 / 255),
        'lightgoldenrodyellow': (250 / 255, 250 / 255, 210 / 255),
        'oldlace':              (253 / 255, 245 / 255, 230 / 255),
        'red':                  (1.0, 0.0, 0.0),
        'magenta':              (1.0, 0.0, 1.0),
        'fuchsia':              (1.0, 0.0, 1.0),
        'deeppink':             (1.0, 20 / 255, 147 / 255),
        'orangered':            (1.0, 69 / 255, 0.0),
        'tomato':               (1.0, 99 / 255, 71 / 255),
        'hotpink':              (1.0, 105 / 255, 180 / 255),
        'coral':                (1.0, 127 / 255, 80 / 255),
        'darkorange':           (1.0, 140 / 255, 0.0),
        'lightsalmon':          (1.0, 160 / 255, 122 / 255),
        'orange':               (1.0, 165 / 255, 0.0),
        'lightpink':            (1.0, 182 / 255, 193 / 255),
        'pink':                 (1.0, 192 / 255, 203 / 255),
        'gold':                 (1.0, 215 / 255, 0.0),
        'peachpuff':            (1.0, 218 / 255, 185 / 255),
        'navajowhite':          (1.0, 222 / 255, 173 / 255),
        'moccasin':             (1.0, 228 / 255, 181 / 255),
        'bisque':               (1.0, 228 / 255, 196 / 255),
        'mistyrose':            (1.0, 228 / 255, 225 / 255),
        'blanchedalmond':       (1.0, 235 / 255, 205 / 255),
        'papayawhip':           (1.0, 239 / 255, 213 / 255),
        'lavenderblush':        (1.0, 240 / 255, 245 / 255),
        'seashell':             (1.0, 245 / 255, 238 / 255),
        'cornsilk':             (1.0, 248 / 255, 220 / 255),
        'lemonchiffon':         (1.0, 250 / 255, 205 / 255),
        'floralwhite':          (1.0, 250 / 255, 240 / 255),
        'snow':                 (1.0, 250 / 255, 250 / 255),
        'yellow':               (1.0, 1.0, 0.0),
        'lightyellow':          (1.0, 1.0, 224 / 255),
        'ivory':                (1.0, 1.0, 240 / 255),
        'white':                (1.0, 1.0, 1.0),

        # Metals
        # 'silver':
        # 'gold:
        'aluminium':            (165 / 255, 167 / 255, 173 / 255),
        'aluminum':             (165 / 255, 167 / 255, 173 / 255),
        'brass':                (1.0, 220 / 255, 100 / 255),
        'bronze':               (205 / 255, 127 / 255, 50 / 255),
        'chrome':               (219 / 255, 226 / 255, 233 / 255),
        'copper':               (230 / 255, 140 / 255, 51 / 255),
        'iron':                 (165 / 255, 156 / 255, 148 / 255),
        'lead':                 (67 / 255, 78 / 255, 82 / 255),
        'nickel':               (114 / 255, 116 / 255, 114 / 255),
        'platinum':             (229 / 255, 225 / 255, 230 / 255),
        'stainless steel':      (207 / 255, 212 / 255, 217 / 255),
        'titanium':             (135 / 255, 134 / 255, 129 / 255),
        'zinc':                 (186 / 255, 196 / 255, 200 / 255)}

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, color: any = None, *, alpha: float | None = None):
        """
        Object constructor.

        :param color: The color specification in one of the following formats:
        - (int, int, int)
        - [int, int, int]
        - (int, int, int, float)
        - [int, int, int, float]
        - (float, float, float)
        - [float, float, float]
        - (float, float, float, float)
        - [float, float, float, float]
        - #rgb
        - #rgba
        - #rrggbb
        - #rrggbbaa
        - color name
        - Color(...)
        For example, the following values result in the same color:
        - (119, 136, 153)
        - [119, 136, 153]
        - (119, 136, 153 , 1.0)
        - [119, 136, 153 , 1.0]
        - (0.467, 0.533, 0.6)
        - [0.467, 0.533, 0.6]
        - (0.467, 0.533, 0.6, 1.0)
        - [0.467, 0.533, 0.6, 1.0]
        - '#789'
        - '#789F'
        - '#789f'
        - '#778899'
        - '#778899FF'
        - '#778899ff'
        - 'lightslategray'
        - 'lightslategrey'
        - 'LightSlateGray'
        - 'LightSlateGrey'
        - 'LIGHTSLATEGRAY'
        - 'LIGHTSLATEGREY'
        - Color('#778899FF')
        :param alpha: The transparency of the color between 0.0 fully (transparent) and 1.0 (opaque). If the alpha
        value is given in both the color parameter and in the alpha parameter, the alpha parameter takes
        precedence.
        """
        if (isinstance(color, Tuple) or isinstance(color, List)) and len(color) == 3:
            if isinstance(color[0], int) and isinstance(color[1], int) and isinstance(color[2], int):
                self.__red = Color.__normalize(color[0] / 255.0)
                self.__green = Color.__normalize(color[1] / 255.0)
                self.__blue = Color.__normalize(color[2] / 255.0)
                self.__alpha = 1.0
            elif isinstance(color[0], float) and isinstance(color[1], float) and isinstance(color[2], float):
                self.__red = Color.__normalize(color[0])
                self.__green = Color.__normalize(color[1])
                self.__blue = Color.__normalize(color[2])
                self.__alpha = 1.0
            else:
                self.__alpha = None

        elif (isinstance(color, Tuple) or isinstance(color, List)) and len(color) == 4:
            if isinstance(color[0], int) and isinstance(color[1], int) and isinstance(color[2], int) and (
                    isinstance(color[3], float) or isinstance(color[3], int)):
                self.__red = Color.__normalize(color[0] / 255.0)
                self.__green = Color.__normalize(color[1] / 255.0)
                self.__blue = Color.__normalize(color[2] / 255.0)
                self.__alpha = Color.__normalize(color[3])

            elif isinstance(color[0], float) and isinstance(color[1], float) and isinstance(color[2], float) and (
                    isinstance(color[3], float) or isinstance(color[3], int)):
                self.__red = Color.__normalize(color[0])
                self.__green = Color.__normalize(color[1])
                self.__blue = Color.__normalize(color[2])
                self.__alpha = Color.__normalize(color[3])
            else:
                self.__alpha = None

        elif isinstance(color, str):
            if color.lower() in Color.__colors:
                (self.__red, self.__green, self.__blue) = Color.__colors[color.lower()]
                self.__alpha = 1.0

            elif re.fullmatch('#[0-9a-fA-F]{3}', color) is not None:
                self.__red = int(color[1], 16) / 15.0
                self.__green = int(color[2], 16) / 15.0
                self.__blue = int(color[3], 16) / 15.0
                self.__alpha = 1.0

            elif re.fullmatch('#[0-9a-fA-F]{4}', color) is not None:
                self.__red = int(color[1], 16) / 15.0
                self.__green = int(color[2], 16) / 15.0
                self.__blue = int(color[3], 16) / 15.0
                self.__alpha = int(color[4], 16) / 15.0

            elif re.fullmatch('#[0-9a-fA-F]{6}', color) is not None:
                self.__red = int(color[1:3], 16) / 255.0
                self.__green = int(color[3:5], 16) / 255.0
                self.__blue = int(color[5:7], 16) / 255.0
                self.__alpha = 1.0

            elif re.fullmatch('#[0-9a-fA-F]{8}', color) is not None:
                self.__red = int(color[1:3], 16) / 255.0
                self.__green = int(color[3:5], 16) / 255.0
                self.__blue = int(color[5:7], 16) / 255.0
                self.__alpha = int(color[7:9], 16) / 255.0
            else:
                self.__alpha = None

        elif isinstance(color, Color):
            self.__red = color.red
            self.__green = color.green
            self.__blue = color.blue
            self.__alpha = color.alpha

        else:
            self.__alpha = None

        if self.__alpha is None:
            raise ValueError('Not a valid color: {}'.format(str(color)))

        if isinstance(alpha, float) or isinstance(alpha, int):
            self.__alpha = Color.__normalize(alpha)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def red(self) -> float:
        """
        Returns the intensity of the color red as a float between (inclusive) 0.0 and 1.0.
        """
        return self.__red

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def green(self) -> float:
        """
        Returns the intensity of the color green as a float between (inclusive) 0.0 and 1.0.
        """
        return self.__green

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def blue(self) -> float:
        """
        Returns the intensity of the color blue as a float between (inclusive) 0.0 and 1.0.
        """
        return self.__blue

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def alpha(self) -> float:
        """
        Returns the transparency as a float between (inclusive) 0.0 (fully transparent) and 1.0 (opaque).
        """
        return self.__alpha

    # ------------------------------------------------------------------------------------------------------------------
    def __mul__(self, factor: float):
        return Color((self.__red * factor, self.__green * factor, self.__blue * factor, self.__alpha))

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return "[{}, {}, {}, {}]".format(round(self.__red, 3),
                                         round(self.__green, 3),
                                         round(self.__blue, 3),
                                         round(self.__alpha, 3))

    # ------------------------------------------------------------------------------------------------------------------
    def __truediv__(self, fraction: float):
        return Color((self.__red / fraction, self.__green / fraction, self.__blue / fraction, self.__alpha))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __normalize(intensity: float) -> float:
        """
        Returns a normalized color intensity between 0.0 and 1.0.

        :param intensity: The color intensiveness to be normalized.
        """
        return max(min(intensity, 1.0), 0.0)

# ----------------------------------------------------------------------------------------------------------------------
