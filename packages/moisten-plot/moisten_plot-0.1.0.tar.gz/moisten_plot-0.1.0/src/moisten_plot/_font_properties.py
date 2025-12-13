from matplotlib.font_manager import FontProperties
from pathlib import Path
from typing import Literal
from .length_unit import LengthOrNumber, Length
import os


class FontStyle(FontProperties):
    """ 对 FontProperties 的封装拓展

    配置一个字体样式，供 text() 或类似方法中作为 `font` 参数使用。

    Example
    -------

        >>> import moisten_plot as mplt
        >>> fig = mplt.figure()
        >>> #配置一个 10 mm 大小的 Times New Roman 字体
        >>> my_font = mplt.FontStyle('Times New Roman', size=fig.units.mm * 10)
        >>> # 使用样式
        >>> plt.text(0.5, 0.5, "Hello World", font=my_font)

    """

    def __init__(self, family_or_file: str | Path,
            style: Literal['normal', 'italic', 'oblique'] = None,
            variant: Literal['normal', 'small-caps'] = None,
            weight: Literal['ultralight', 'light', 'normal', 'regular',
                            'book', 'medium', 'roman', 'semibold',
                            'demibold', 'demi', 'bold', 'heavy',
                            'extra bold', 'black'] | int = None,
            stretch: Literal['ultra-condensed', 'extra-condensed', 'condensed',
                             'semi-condensed', 'normal', 'semi-expanded',
                             'expanded', 'extra-expanded','ultra-expanded'
                             ] = None,
            size: Literal['xx-small', 'x-small', 'small', 'medium',
                        'large', 'x-large', 'xx-large'] | LengthOrNumber = None,
            math_fontfamily: Literal['dejavusans', 'dejavuserif', 'cm', 'stix',
                                      'stixsans', 'custom'] = None
            ):
        """配置一个字体样式，供 text() 或类似方法中作为 `font` 参数使用。

        Example
        -------

            >>> import moisten_plot as mplt
            >>> fig = mplt.figure()
            >>> #配置一个 10 mm 大小的 Times New Roman 字体
            >>> my_font = mplt.FontStyle('Times New Roman', size=fig.units.mm * 10)
            >>> # 使用样式
            >>> plt.text(0.5, 0.5, "Hello World", font=my_font)


        Parameters
        ----------
        family_or_file : str | Path
            字体名称，或字体文件路径
        style : Literal['normal', 'italic', 'oblique'], optional
            字体样式, by default None
        variant : Literal['normal', 'small, optional
            字体变化, by default None
        weight : Literal['ultralight', 'light', 'normal', 'regular', 'book',
            'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy',
            'extra bold', 'black'] | int, optional
            字重，可以是0-1000的数值, by default None
        stretch : Literal['ultra-condensed', 'extra-condensed', 'condensed',
            'semi-condensed', 'normal', 'semi-expanded', 'expanded',
            'extra-expanded','ultra-expanded'], optional
            横向拉伸, by default None
        size : Literal['xx, optional
            字体大小，可以是长度单位，默认为 pt, by default None
        math_fontfamily : Literal['dejavusans', 'dejavuserif', 'cm', 'stix',
            'stixsans', 'custom'], optional
            Latex数学公式里的字体，如果想用当前字体，则设置 'custom'
            by default None
        """

        if isinstance(size, Length):
            size = size.to_pt()

        if isinstance(family_or_file, Path) or \
            Path(family_or_file).is_file() or \
            Path(os.getcwd(), family_or_file).is_file():
            super().__init__(fname=str(family_or_file.absolute()),
                             style=style,
                             variant=variant,
                             weight=weight,
                             stretch=stretch,
                             size=size,
                             math_fontfamily=math_fontfamily)
        else:
            super().__init__(family=family_or_file,
                             style=style,
                             variant=variant,
                             weight=weight,
                             stretch=stretch,
                             size=size,
                             math_fontfamily=math_fontfamily)



