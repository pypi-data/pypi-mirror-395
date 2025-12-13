from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib import font_manager
from matplotlib.transforms import Bbox, BboxTransform
from matplotlib.gridspec import GridSpec, SubplotSpec
from .length_unit import (MoiFigureUnits, LengthOrNumber, as_unit,
                          LengthUnit, Pt, Inch, Length)
from .length_unit import LengthOrNumber as LenNum
from ._font_properties import FontStyle
from ._core import MoiRcParams
from .axes_tools import SubplotParams
from typing import Literal
import numpy as np
import os
from typing import Callable, TypeVar

class BreakLoopException(Exception):
    """用于中断循环的异常"""
    pass

class MoiFigure(Figure):

    _used_custom_font = False
    """是否使用了自定义字体"""

    FONT_ROBOTO: FontStyle | None = None
    FONT_ROBOTO_ITALIC: FontStyle | None = None
    FONT_ROBOTO_CONDENSED: FontStyle | None = None

    def __init__(self, moi_config: bool=True, **kwargs):
        """创建一个 MoiFigure 实例。

        Create an instance of MoiFigure.

        Parameters
        ----------
        moi_config : bool, optional
            是否使用 Moisten 默认的配置，包括字体、边框粗细等，默认为 True

            Whether to use the default configuration of Moisten, including
            font, border thickness, etc., by default True
        """
        self._use_a4_size = False
        super().__init__(**kwargs)

        if moi_config:
            MoiRcParams().apply()
            self.use_std_font()

        self.units = MoiFigureUnits(self)
        """获取长度单位，例如：

            >>> import moisten_plot as mplt
            >>> fig = mplt.figure()
            >>> pt = fig.units.pt  # 1 point
        """


    @staticmethod
    def get_font_names() -> list[str]:
        """
        获取 Matplotlib 中可用的字体名称列表。
        可以用 set_font_family() 方法，传入字体名设置默认字体。

        Get the list of available font names in Matplotlib.
        You can use the set_font_family() method to set the default font
        by passing in the font name.
        """
        return font_manager.get_font_names()


    @staticmethod
    def use_std_font():
        """
        设置 MoiFigure 标准字体，将使用 assets/fonts 中的字体文件。
        使用开源的 Roboto 作为默认字体，包含了两款字体与多种变体。
        同时，可以使用几个预设的类变量单独设置字体（见例子）。


        Set the MoiFigure standard font,
        which will use the font files in assets/fonts.
        Use the open-source Roboto font as the default font,
        including two fonts and multiple variants.
        At the same time, several preset class variables can be used
        to set the font separately (see example).

        Example
        -------

            >>> import moisten_plot as mplt
            >>> fig = mplt.figure()
            >>>
            >>> plt.text(0.5, 0.3, "Roboto", font=fig.FONT_ROBOTO)
            >>> plt.text(0.5, 0.4, "Roboto Italic",
            ...          font=fig.FONT_ROBOTO_ITALIC, size=18)
            >>> plt.text(0.5, 0.5, "Roboto Condense",
            ...          font=fig.FONT_ROBOTO_CONDENSED)


        included fonts:

        - Roboto
            - Roboto Light
            - Roboto
            - Roboto Bold
            - Roboto Italic Light
            - Roboto Italic
            - Roboto Italic Bold
        - Roboto Condensed
            - Roboto Condensed Regular
            - Roboto Condensed Italic

        """
        font_dir = os.path.dirname(os.path.realpath(__file__))
        font_dir = font_dir + "/assets/fonts"

        font_files = font_manager.findSystemFonts(fontpaths=font_dir)

        for font_file in font_files:
            font_manager.fontManager.addfont(font_file)

        MoiFigure.set_font_family('Roboto Condensed')
        MoiFigure.set_font_family('Roboto')

        MoiFigure.FONT_ROBOTO = FontStyle('Roboto')
        MoiFigure.FONT_ROBOTO_ITALIC = FontStyle('Roboto', style='italic')
        MoiFigure.FONT_ROBOTO_CONDENSED = FontStyle('Roboto Condensed')



    @staticmethod
    def set_font_family(font_name: str | list[str]):
        """插入字体到 rcParams['font.family'] 的数组前面，即设置默认优先字体，
        要查看 Matplotlib 支持的字体名称，可以使用 get_font_list() 方法。

        Insert font(s) to the front of rcParams['font.family'],
        i.e., set the default priority font(s).
        To see the font names supported by Matplotlib,
        you can use the get_font_list() method.

        Parameters
        ----------
        font_name : str
            字体名称
        """
        ff = plt.rcParams['font.family']
        if isinstance(ff, str):
            plt.rcParams['font.family'] = [font_name, ff]
        else:
            plt.rcParams['font.family'] = [font_name] + ff



    @staticmethod
    def use_custom_font(font_file_path: str, font_name: str=None,
                        as_math_font: bool=False):
        """
        使用自定义的字体。此字体将会被插入到 rcParams['font.family'] 最前。
        如果不指定 font_name，将会自动识别字体的名称。
        此方法可以在实例化 MoiFigure 之前调用，这样的话 MoiFigure 就不会设置默认的字体。

        Use a custom font. This font will be inserted at the front of
        rcParams['font.family'].
        If `font_name` is not specified, the name of the font will be
        automatically recognized.
        This method can be called before instantiating `MoiFigure`, so that
        `MoiFigure` will not set the default font.

        Parameters
        ----------
        font_file_path : str
            字体文件的路径

            The path to the font file
        font_name : str
            字体的名称

            The name of the font
        as_math_font : bool, optional
            是否将此字体也作为数学公式的字体，默认为 False

            Whether to use this font as the font for mathematical formulas,
            by default False
        """


        if font_name is None:
            ttf_len = len(self.mpl_font_manager.ttflist)
            afm_len = len(self.mpl_font_manager.afmlist)

        font_manager.fontManager.addfont(font_file_path)

        if font_name is None:
            if len(font_manager.fontManager.ttflist) > ttf_len:
                font_name = font_manager.fontManager.ttflist[-1].name
            elif len(font_manager.fontManager.afmlist) > afm_len:
                font_name = font_manager.fontManager.afmlist[-1].name
            else:
                raise ValueError("Cannot recognize the font name from the "
                                 "given font file. Please specify the font_name.")

        MoiFigure.set_font_family(font_name)

        if as_math_font:
            plt.rcParams['mathtext.default'] = 'regular'

        MoiFigure._used_custom_font = True


    @staticmethod
    def set_math_font(font_name: Literal['dejavusans', 'dejavuserif', 'cm',
                                         'stix', 'stixsans']=None,
                      use_text_font: bool=False):
        """
        设置数学公式显示的字体，如果想使用正常文字的字体作为数学公式的字体，
        可以设置 `use_text_font=True` 。

        Set the font for displaying latex formulas.
        If you want to use the font of normal text as the font of latex formulas,
        you can set `use_text_font=True`.

        Parameters
        ----------
        font_name : Literal['dejavusans', 'dejavuserif', 'cm', 'stix',
            'stixsans'], optional
            公式字体名称

            The name of the font for latex formulas
        use_text_font : bool, optional
            使用正常字体作为公式字体, 默认为 False

            Use the font of normal text as the font of latex formulas,
            by default False
        """

        if use_text_font:
            plt.rcParams['mathtext.default'] = 'regular'
        elif font_name is not None:
            plt.rcParams['mathtext.fontset'] = font_name


    def extend(self, left: LengthOrNumber=0, bottom: LengthOrNumber=0,
                right: LengthOrNumber=0, top: LengthOrNumber=0) -> None:
        """拓展画幅的大小，同时不改变子图的绝对大小。默认以英寸为单位。

        Extend the size of the figure without changing the absolute size of
        the subplots. The default unit is inch.

        Parameters
        ----------
        left, right, bottom, top : LenType, optional
            画幅的四边的拓展大小，可以使用 MoiFigure 的长度单位或者直接使用 float。

            The extension size of the four sides of the figure, you can use the
            length unit of MoiFigure or directly use float.
        """

        left, bottom, right, top = as_unit(left, bottom, right, top, fig=self,
                                           unit=LengthUnit.INCH,
                                           return_value=True)

        extend = np.array([[left, bottom], [right, top]], dtype=np.float64)

        origin_bbox = self.bbox_inches

        new_bbox = Bbox.from_extents(0, 0,
            origin_bbox.width + extend[:, 0].sum(),
            origin_bbox.height + extend[:, 1].sum()
        )

        offset = extend[0] / np.array([new_bbox.width, new_bbox.height])

        trans = BboxTransform(new_bbox, origin_bbox)
        for ax in self.axes:
            points = ax.get_position().get_points()
            points = trans.transform(points)
            points += offset[None, :]
            ax.set_position(
                Bbox.from_extents(*points.flatten())
            )

        self.set_size_inches(new_bbox.width, new_bbox.height)


    def aspect_gridspec(self, nrows: int, ncols: int,
            aspect_ratio: float|tuple[float, float]|tuple[float,float,float,float],
            subplot_width: LenNum=None,
            gridspec_width: LenNum=None,
            margin: LenNum |tuple[LenNum, LenNum] |
                    tuple[LenNum, LenNum, LenNum, LenNum]=
                    (Pt(20), Pt(20), Pt(30), Pt(40)),
            margin_left: LenNum=None, margin_right: LenNum=None,
            margin_top: LenNum=None, margin_bottom: LenNum=None,
            hspace: LenNum=Pt(40), wspace: LenNum=Pt(20),
            extend_fig: bool=True) -> GridSpec:
        """每个子图都是相同固定比例的网格布局（邮票图），
        网格布局整体的位置将以 `margin_left`、`margin_top`
        相对于画幅(figure)左上角来定位。
        如果布局的大小超出画幅，且 `extend_fig=True`(默认)，将会根据布局修改画幅大小。

        需要指定子图宽度 `subplot_width` 或整体网格宽度 `gridspec_width` 来设置大小。

        边距 margin 与 CSS 类似，参数 `margin` 可以为以下几种形式：

        - 单个值：同时指定四边相同的边距
        - 两个值：第一个值指定左右边距，第二个值指定上下边距，如 (0.3, 0.5)
        - 四个值：分别指定上、右、下、左四边的边距，如 (0.2, 0.3, 0.4, 0.5)

        同时，还有各个边的单独参数 `margin_left`、`margin_right`、`margin_top`、
        `margin_bottom`，这些参数如果被指定，将会覆盖 `margin` 中对应的边距设置。

        所有与长度相关的参数都可以使用 MoiFigure 的长度单位，或者直接使用数值。

        Create a grid layout where each subplot has the same fixed aspect ratio
        (stamp plot).
        The position of the overall grid layout will be positioned relative to
        the upper left corner of the figure with `margin_left` and `margin_top`.
        If the size of the layout exceeds the figure, and `extend_fig=True`
        (default), the figure size will be modified according to the layout.

        You need to specify the subplot width `subplot_width` or the overall
        grid width `gridspec_width` to set the size.

        The margin is similar to CSS. The `margin` parameter can take the
        following forms:

        - A single value: specifies the same margin for all four sides
        - Two values: the first value specifies the left and right margins,
          and the second value specifies the top and bottom margins, e.g., (0.3, 0.5)
        - Four values: specify the margins of the top, right, bottom, and left sides,
          e.g., (0.2, 0.3, 0.4, 0.5)

        In addition, there are individual parameters for each side:
        `margin_left`, `margin_right`, `margin_top`, and `margin_bottom`.
        If these parameters are specified, they will override
        the corresponding margin settings in `margin`.

        All length-related parameters can use the length units of MoiFigure,
        or directly use numerical values.

        Parameters
        ----------
        nrows, ncols : int
            子图的行数和列数

            The number of rows and columns of the subplots
        aspect_ratio : float|tuple[float, float]|tuple[float,float,float,float]
            子图的宽高比例，可以是一个浮点数，二元组或四元组。
            当为二元组时，表示宽度与高度，比例为 `aspect_ratio[0] / aspect_ratio[1]`；
            当为四元组时，表示左、右、上、下的坐标， 比例为
            `(aspect_ratio[1]-aspect_ratio[0]) / (aspect_ratio[3]-aspect_ratio[2])`。

            The width-to-height ratio of the subplots, which can be a float,
            a tuple of two or four elements.
            When it is a tuple of two elements, it represents width and height,
            and the ratio is `aspect_ratio[0] / aspect_ratio[1]`;
            when it is a tuple of four elements, it represents the left, right,
            top, and bottom coordinates, and the ratio is
            `(aspect_ratio[1]-aspect_ratio[0]) / (aspect_ratio[3]-aspect_ratio[2])`.
        subplot_width : Length | float | int, optional
            子图的宽度，如果是数值则单位为英寸。

            The width of the subplots, if it is a number, the unit is inch.
        gridspec_width : Length | float | int, optional
            gridspec 组图整体的宽度，如果是数值则单位为英寸。

            The width of the gridspec group plot as a whole, if it is a number,
            the unit is inch.
        margin : LengthOrNum | tuple(horizontal, vertical) | tuple (top, right, bottom, left), optional
            设置布局到画幅四边边距，类似 CSS，可以是单个值、二元组或四元组，
            如果是数值则单位为pt。 具体见函数说明。

            The margin of the four sides of the figure, similar to CSS,
            which can be a single value, a tuple of two or four elements.
            If it is a number, the unit is pt. See the function description
            for details.
        margin_left, margin_right, margin_top, margin_bottom : Length |
            float | int, optional

            设置布局到画幅的四边边距，如果是数值则单位为pt。

            The margin of the four sides of the figure, if it is a number, the
            unit is pt.
        hspace, wspace : Length| float | int, optional
            子图之间的水平和垂直间距，如果是数值则单位为pt。

            The horizontal and vertical spacing between subplots, if it is a
            number, the unit is pt.
        extend_fig : bool, optional
            如果画幅大小超出，是否调整画幅大小

            If the size of the figure exceeds, whether to adjust the
            size of the figure.
        """

        # 获取子图比例
        if not isinstance(aspect_ratio, (float, int)):
            if len(aspect_ratio) == 2:
                ratio = aspect_ratio[0] / aspect_ratio[1]
            elif len(aspect_ratio) == 4:
                ratio = (aspect_ratio[1] - aspect_ratio[0]) / \
                    (aspect_ratio[3] - aspect_ratio[2])
            else:
                raise ValueError("The length of aspect_ratio must be 2 or 4.")
        else:
            ratio = aspect_ratio

        if subplot_width is None and gridspec_width is None:
            raise ValueError("You must specify either `subplot_width` or "
                             "`gridspec_width` to set width.")

        if subplot_width is not None and gridspec_width is not None:
            raise ValueError("You can't specify both `subplot_width` and "
                             "`gridspec_width`.")

        wspace, hspace = as_unit(wspace, hspace, fig=self, unit=LengthUnit.PT)
        wspace = wspace.to_inch()
        hspace = hspace.to_inch()

        # 处理边距
        _left_margin = _right_margin = _top_margin = _bottom_margin = 0
        if isinstance(margin, (int, float)):
            _left_margin = _right_margin = _top_margin = _bottom_margin = \
                as_unit(margin, fig=self, unit=LengthUnit.PT)
        elif isinstance(margin, Length):
            _left_margin = _right_margin = _top_margin = _bottom_margin = margin
        elif hasattr(margin, "__len__"):
            if len(margin) == 2:
                _left_margin, _right_margin = margin[0]
                _top_margin = _bottom_margin = margin[1]
            elif len(margin) == 4:
                _top_margin, _right_margin, _bottom_margin, _left_margin = margin
            else:
                raise ValueError("The length of margin must be 2 or 4.")

        margin_left   = margin_left   if margin_left   is not None else _left_margin
        margin_right  = margin_right  if margin_right  is not None else _right_margin
        margin_top    = margin_top    if margin_top    is not None else _top_margin
        margin_bottom = margin_bottom if margin_bottom is not None else _bottom_margin

        margin_left, margin_right, margin_top, margin_bottom = \
            as_unit(margin_left, margin_right, margin_top, margin_bottom,
                    fig=self, unit=LengthUnit.PT)

        # 计算子图、gridspec、画幅大小
        if subplot_width is not None:
            subplot_width = as_unit(subplot_width, fig=self, unit=LengthUnit.INCH)
            subplot_height = subplot_width / ratio
            gridspec_width = subplot_width * ncols + wspace * (ncols - 1)

        elif gridspec_width is not None:
            gridspec_width = as_inch(self, gridspec_width)
            subplot_width = (gridspec_width - wspace * (ncols - 1)) / ncols
            subplot_height = subplot_width / ratio

        gridspec_height = subplot_height * nrows + hspace * (nrows - 1)
        fig_width = gridspec_width + margin_left + margin_right
        fig_height = gridspec_height + margin_top + margin_bottom

        # 如果画幅大小超出，调整画幅大小
        if extend_fig:
            dx, dy = 0, 0
            if fig_width.to_inch().value > self.get_figwidth():
                dx = fig_width.to_inch().value - self.get_figwidth()
            if fig_height.to_inch().value > self.get_figheight():
                dy = fig_height.to_inch().value - self.get_figheight()
            if dx + dy > 0:
                self.set_size_inches(self.get_figwidth() + dx,
                                    self.get_figheight() + dy)

        gs = GridSpec(nrows, ncols, self,
                      left=margin_left.to_fig_x().value,
                      top=1 - margin_top.to_fig_y().value,
                      right=(margin_left+gridspec_width).to_fig_x().value,
                      bottom=1 - (margin_top + gridspec_height).to_fig_y().value,
                      hspace=hspace.value/subplot_height.value,
                      wspace=wspace.value/subplot_width.value)

        return gs


    def gridspec_by_size(self, nrows: int, ncols: int,
                        width: LenNum | tuple[LenNum],
                        height: LenNum | list[LenNum],
                        margin: LenNum |tuple[LenNum, LenNum] |
                                tuple[LenNum, LenNum, LenNum, LenNum]=
                                (Pt(20), Pt(20), Pt(30), Pt(40)),
                        margin_left: LenNum=None, margin_right: LenNum=None,
                        margin_top: LenNum=None, margin_bottom: LenNum=None,
                        hspace: LenNum=Pt(40), wspace: LenNum=Pt(20),
                        extend_fig: bool=True) -> GridSpec:
        """
        指定不同行、列的具体大小来创建 gridspec。
        宽度和高度参数可以使用列表或数组来分别指定不同行、列的大小。

        网格布局整体的位置将以 `margin_left`、`margin_top`
        相对于画幅(figure)左上角来定位。
        如果布局的大小超出画幅，且 `extend_fig=True`(默认)，将会根据布局修改画幅大小。

        边距 margin 与 CSS 类似，参数 `margin` 可以为以下几种形式：

        - 单个值：同时指定四边相同的边距
        - 两个值：第一个值指定左右边距，第二个值指定上下边距，如 (0.3, 0.5)
        - 四个值：分别指定上、右、下、左四边的边距，如 (0.2, 0.3, 0.4, 0.5)

        同时，还有各个边的单独参数 `margin_left`、`margin_right`、`margin_top`、
        `margin_bottom`，这些参数如果被指定，将会覆盖 `margin` 中对应的边距设置。

        所有与长度相关的参数都可以使用 MoiFigure 的长度单位，或者直接使用数值。

        Create a gridspec by specifying the specific size of different rows
        and columns.
        The width and height parameters can use lists or arrays to specify
        the size of different rows and columns respectively.
        The position of the overall grid layout will be positioned relative to
        the upper left corner of the figure with `margin_left` and `margin_top`.
        If the size of the layout exceeds the figure, and `extend_fig=True`
        (default), the figure size will be modified according to the layout.

        The margin is similar to CSS. The `margin` parameter can take the
        following forms:

        - A single value: specifies the same margin for all four sides
        - Two values: the first value specifies the left and right margins,
          and the second value specifies the top and bottom margins, e.g., (0.3, 0.5)
        - Four values: specify the margins of the top, right, bottom, and left sides,
          e.g., (0.2, 0.3, 0.4, 0.5)

        In addition, there are individual parameters for each side:
        `margin_left`, `margin_right`, `margin_top`, and `margin_bottom`.
        If these parameters are specified, they will override
        the corresponding margin settings in `margin`.

        All length-related parameters can use the length units of MoiFigure,
        or directly use numerical values.

        Parameters
        ----------
        nrows, ncols : int
            子图布局的行数和列数

            The number of rows and columns of the subplot layout
        width, height : LengthOrNum | list[LengthOrNum]
            每列的宽度与每行的高度。如果是单值，则所有行/列相同；
            如果是列表或数组，则每列/行的宽/高度分别为列表中的值。
            如果参数是数值，则以英寸为单位。

            The width of each column and the height of each row.
            If it is a single value, all rows/columns are the same;
            if it is a list or array, the width/height of each column/row
            is the value in the list.
            If the parameter is a number, it is in inches.
        margin : LengthOrNum | tuple(horizontal, vertical) | tuple (top, right, bottom, left), optional

            设置布局到画幅四边边距，类似 CSS，可以是单个值、二元组或四元组，
            如果是数值则单位为pt。 具体见函数说明。

            The margin of the four sides of the figure, similar to CSS,
            which can be a single value, a tuple of two or four elements.
            If it is a number, the unit is pt. See the function description
            for details.
        margin_left, margin_right, margin_top, margin_bottom : LengthOrNum, optional
            设置布局到画幅的四边边距，如果是数值则单位为pt。

            The margin of the four sides of the figure, if it is a number, the
            unit is pt.
        wspace, hspace : LenType, optional
            子图之间的水平和垂直间距，如果是数值则单位为pt。

            The horizontal and vertical spacing between subplots, if it is a
            number, the unit is pt.
        extend_fig : bool, optional
            如果 Gridspec 大小超出画幅，是否调整画幅大小，默认为 True。

            If the size of the Gridspec exceeds the figure, whether to adjust
            the size of the figure, by default True.

        Returns
        -------
        GridSpec
            返回 GridSpec 对象

            return GridSpec object
        """

        # 根据子图大小创建 gridspec
        if hasattr(width, '__len__'):
            if len(width) == ncols:
                width = [as_unit(w, fig=self, unit=LengthUnit.INCH)
                         for w in width]
            else:
                raise ValueError(f"The length of width list: {len(width)} must "
                                 f"be equal to the number of cols: {ncols}.")
        elif isinstance(width, (int, float)):
            width = [as_unit(width, fig=self, unit=LengthUnit.INCH)] * ncols
        else:
            raise ValueError("Unknown type for width parameter.")

        if hasattr(height, '__len__'):
            if len(height) == nrows:
                height = [as_unit(h, fig=self, unit=LengthUnit.INCH)
                         for h in height]
            else:
                raise ValueError(f"The length of height list: {len(height)} must "
                                 f"be equal to the number of rows: {nrows}.")
        elif isinstance(height, (int, float)):
            height = [as_unit(height, fig=self, unit=LengthUnit.INCH)] * nrows
        else:
            raise ValueError("Unknown type for height parameter.")

        # 处理边距
        _left_margin = _right_margin = _top_margin = _bottom_margin = 0
        if isinstance(margin, (int, float)):
            _left_margin = _right_margin = _top_margin = _bottom_margin = \
                as_unit(margin, fig=self, unit=LengthUnit.PT)
        elif isinstance(margin, Length):
            _left_margin = _right_margin = _top_margin = _bottom_margin = margin
        elif hasattr(margin, "__len__"):
            if len(margin) == 2:
                _left_margin, _right_margin = margin[0]
                _top_margin = _bottom_margin = margin[1]
            elif len(margin) == 4:
                _top_margin, _right_margin, _bottom_margin, _left_margin = margin
            else:
                raise ValueError("The length of margin must be 2 or 4.")

        margin_left   = margin_left   if margin_left   is not None else _left_margin
        margin_right  = margin_right  if margin_right  is not None else _right_margin
        margin_top    = margin_top    if margin_top    is not None else _top_margin
        margin_bottom = margin_bottom if margin_bottom is not None else _bottom_margin

        margin_left, margin_right, margin_top, margin_bottom = \
            as_unit(margin_left, margin_right, margin_top, margin_bottom,
                    fig=self, unit=LengthUnit.PT)

        wspace, hspace = as_unit(wspace, hspace, fig=self, unit=LengthUnit.PT)

        grid_width = sum(width) + wspace * (ncols - 1)
        grid_height = sum(height) + hspace * (nrows - 1)

        width_ratio = [w.to_inch().value for w in width]
        width_mean = np.mean(width_ratio)
        height_ratio = [h.to_inch().value for h in height]
        height_mean = np.mean(height_ratio)

        fig_width = margin_left + grid_width + margin_right
        fig_height = margin_top + grid_height + margin_bottom

        # 如果画幅大小超出，调整画幅大小
        if extend_fig:
            dx, dy = 0, 0
            if fig_width.to_inch().value > self.get_figwidth():
                dx = fig_width.to_inch().value - self.get_figwidth()
            if fig_height.to_inch().value > self.get_figheight():
                dy = fig_height.to_inch().value - self.get_figheight()
            if dx + dy > 0:
                self.set_size_inches(self.get_figwidth() + dx,
                                    self.get_figheight() + dy)

        gs = GridSpec(nrows, ncols, self,
                      left=margin_left.to_fig_x().value,
                      top=1 - margin_top.to_fig_y().value,
                      right=(margin_left + grid_width).to_fig_x().value,
                      bottom=1 - (margin_top + grid_height).to_fig_y().value,
                      hspace=hspace.to_inch().value/height_mean,
                      wspace=wspace.to_inch().value/width_mean,
                      width_ratios=width_ratio, height_ratios=height_ratio)

        return gs


    def fig_title(self, title: str, margin_top: LengthOrNumber=Pt(5),
                  va='top', **kwargs) -> plt.Text:
        """
        添加一个总标题到画幅的上方，为 `Figure.suptitle()` 的封装方法，可控制标题位置。
        通过 `margin_top` 来设置标题距离画幅上边框的距离。

        Add a main title above the figure, which is a wrapper method for
        `Figure.suptitle()`, and can control the position of the title.
        Use `margin_top` to set the distance of the title from the top border
        of the figure.

        Parameters
        ----------
        title : str
            标题内容  title content
        margin_top : LengthOrNumber, optional
            到画幅顶部距离, 如果是数字，则以 pt 为单位。by default Pt(5)

            The distance to the top of the figure, if it is a number,
            the unit is pt. by default Pt(5)
        va : str, optional
            垂直对齐方式，默认为 'top'

            The vertical alignment, by default 'top'

        **kwargs
            其他参数，传递给 `Figure.suptitle()` 方法

            Other parameters, passed to the `Figure.suptitle()` method
        """
        margin_top = as_unit(margin_top, fig=self, unit=LengthUnit.PT)
        y = 1 - margin_top.to_fig_y()
        kwargs.setdefault('y', y)
        kwargs.setdefault('va', va)
        return self.suptitle(title, **kwargs)


    def subplots_adjust(self, left:LengthOrNumber | None=None,
                        bottom:LengthOrNumber | None=None,
                        right:LengthOrNumber | None=None,
                        top:LengthOrNumber | None=None,
                        wspace:LengthOrNumber | None=None,
                        hspace:LengthOrNumber | None=None) -> None:
        # 添加单位支持
        left = as_unit(left, fig=self, unit=LengthUnit.FIG_X)
        right = as_unit(right, fig=self, unit=LengthUnit.FIG_X)
        bottom = as_unit(bottom, fig=self, unit=LengthUnit.FIG_Y)
        top = as_unit(top, fig=self, unit=LengthUnit.FIG_Y)

        if wspace is not None and isinstance(wspace, Length):
            if len(self.axes) > 0:
                ax_width = [ax.get_position().width for ax in self.axes]
                ax_width = np.mean(ax_width) * self.get_figwidth()
                wspace = wspace.to_inch().value / ax_width
            else:
                Warning("Setting a specific `wspace` length with no axes, "
                        "the value of `wspace` will be directly used.",
                        UserWarning)
                wspace = wspace.value

        if hspace is not None and isinstance(hspace, Length):
            if len(self.axes) > 0:
                ax_height = [ax.get_position().height for ax in self.axes]
                ax_height = np.mean(ax_height) * self.get_figheight()
                hspace = hspace.to_inch().value / ax_height
            else:
                Warning("Setting a specific `hspace` length with no axes, "
                        "the value of `hspace` will be directly used.",
                        UserWarning)
                hspace = hspace.value

        super().subplots_adjust(left=left, bottom=bottom, right=right, top=top,
                                wspace=wspace, hspace=hspace)


    def add_axes(self, *args, **kwargs):
        # 添加单位支持
        if kwargs.get('rect') is not None:
            rect = kwargs.pop('rect')
        elif len(args) > 0 and hasattr(args[0], '__len__'):
            rect = args[0]
        else:
            return super().add_axes(*args, **kwargs)

        new_rect = []
        for i, v in enumerate(rect):
            if isinstance(v, Length):
                if i % 2 == 0:
                    new_rect.append(float(v.to_fig_x()))
                else:
                    new_rect.append(float(v.to_fig_y()))
            else:
                new_rect.append(v)

        return super().add_axes(new_rect, *args[1:], **kwargs)


    def _progress_bar(self, title: str, show_progress: bool=True):
        from rich.progress import (Progress, TextColumn, BarColumn,
        TimeRemainingColumn, MofNCompleteColumn, SpinnerColumn)
        progress = Progress(
            TextColumn(title),
            SpinnerColumn('moon', finished_text="✓"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeRemainingColumn(True, True),
            disable=not show_progress)
        return progress


    def loop_gridspec[T](self, gridspec: GridSpec,
                         function: Callable[[SubplotParams, tuple[any, ...]], T],
                         show_progress: bool = True,
                         break_at: int = None,
                         func_args: dict | None = None,
                         **subplot_kwargs) -> list[T]:
        """遍历每个 GridSpec 的子图并执行指定的函数画图，适用于邮票图。
        你需要传入一个函数，该函数的第一个参数为 `SubplotParams` 对象，
        其余参数可自己设置。对每个子图都会调用此函数一次来画图，
        与子图相关的信息在 `SubplotParams` 中。
        在 SubplotParams.ax 使用前，Axes 不会被创建，
        这样可以用于跳过一些子图（如 Example），
        也可以先用 `SubplotParams.set_subplot_kwargs()` 先单独设置参数再创建。

        Example
        -------
            >>> import moisten_plot as mplt
            >>> from cartopy import crs as ccrs
            >>>
            >>> fig = mplt.figure()
            >>> gs = fig.aspect_gridspec(3, 4, aspect_ratio=1,
            ...                          subplot_width=fig.units.inch(1))
            >>>
            >>> data = get_my_data()
            >>>
            >>> def plot_func(sp: mplt.SubplotParams):
            >>>     if sp.row == 1:
            >>>         # 第2行不画，不创建 Axes
            >>>         return
            >>>     ax = sp.ax
            >>>     ax.plot(data[sp.row_index])
            >>>     ... # 其他绘图内容
            ...
            >>> # 遍历 gridspec 并绘图，每个子图设置 projection 参数。
            >>> fig.loop_gridspec(gs, plot_func, projection=ccrs.PlateCarree())


        Parameters
        ----------
        gridspec : GridSpec
            要遍历的 GridSpec 对象
        function : Callable[[SubplotParams, tuple[any, ...]], T]
            用于绘图的函数，第一个参数为 SubplotParams 对象，其余参数可自己设置，
            在 `func_args` 中传入，函数返回值会被收集到一个列表中返回。
        show_progress : bool, optional
            是否显示进度条，默认为 True
        break_at : int, optional
            在第几个子图后中断（从0开始计数，行优先），默认不中断，可用于调试。
        func_args : dict | None, optional
            传递给绘图函数的其他参数字典，默认为 None
        **subplot_kwargs
            传递给 Figure.add_subplot() 方法的参数，用于指定每一个子图创建时的参数，
            例如 projection 等。

        Returns
        -------
        list[T]
            返回绘图函数的返回值列表

        """
        prog = self._progress_bar("Setting subplots", show_progress)
        prog.start()
        total = (break_at+1) if break_at is not None else\
            gridspec.nrows * gridspec.ncols
        task = prog.add_task("Drawing subplots...", total=total)
        results = []

        try:
            for i in range(gridspec.nrows):
                for j in range(gridspec.ncols):
                    result = function(SubplotParams(self, gridspec[i, j], i, j,
                                        gridspec.nrows, gridspec.ncols,
                                        subplot_kwargs),
                                        **(func_args or {}))
                    results.append(result)
                    prog.update(task, advance=1)
                    row_index = i * gridspec.ncols + j
                    if break_at is not None and row_index >= break_at:
                        raise BreakLoopException

        except BreakLoopException:
            pass
        finally:
            prog.stop()

        return results


    def shift_axes(self, axes: plt.Axes | list[plt.Axes],
                   dx: LengthOrNumber=0, dy: LengthOrNumber=0) -> None:
        """平移指定的单个或多个 Axes 位置。
        dx 和 dy 可以使用 MoiFigure 的长度单位，或者直接使用数字（单位为 pt）。
        dx 为正时向右平移，dy 为正时向上平移。

        Parameters
        ----------
        axes : plt.Axes | list[plt.Axes]
            要平移的 Axes 对象或列表

        dx, dy : LengthOrNumber, optional
            平移的距离，如果是数字则以pt为单位。

        """

        dx, dy = as_unit(dx, dy, fig=self, unit=LengthUnit.PT)

        if isinstance(axes, plt.Axes):
            axes = [axes]

        for ax in axes:
            pos = ax.get_position()
            new_pos = Bbox.from_extents(
                pos.x0 + dx.to_fig_x().value,
                pos.y0 + dy.to_fig_y().value,
                pos.x1 + dx.to_fig_x().value,
                pos.y1 + dy.to_fig_y().value,
            )
            ax.set_position(new_pos)


    def _get_merge_bbox(self, bbox_list: list[Bbox]) -> Bbox:
        """获取多个 Bbox 的合并边界框"""
        x0 = min([bbox.x0 for bbox in bbox_list])
        y0 = min([bbox.y0 for bbox in bbox_list])
        x1 = max([bbox.x1 for bbox in bbox_list])
        y1 = max([bbox.y1 for bbox in bbox_list])
        return Bbox.from_extents(x0, y0, x1, y1)


    def append_axes(self, target_ax: plt.Axes | list[plt.Axes],
                    ha: Literal['left', 'right', 'center']='right',
                    va: Literal['top', 'bottom', 'center']='center',
                    width: LengthOrNumber | None=None,
                    height: LengthOrNumber | None=None,
                    margin: LengthOrNumber | tuple[LengthOrNumber,
                                                   LengthOrNumber]=Pt(20),
                    extend_fig: bool=True,
                    extend_fig_padding: LengthOrNumber | tuple[LengthOrNumber,
                                                    LengthOrNumber]=Pt(20),
                    **kwargs) -> plt.Axes:
        """在已有的 Axes 旁边添加一个新的 Axes。
        新的 Axes 会根据已有 Axes 的位置进行定位，可以通过 `ha` 和 `va` 参数
        来控制新 Axes 相对于已有 Axes 的位置，类似 Text 的对齐方式。
        通过 `margin` 参数来设置新 Axes 与已有 Axes 之间的距离。
        如果新 Axes 超出画幅范围，且 `extend_fig=True` (默认)，
        则会自动扩展画幅大小以容纳新的 Axes。
        如果不指定新 Axes 的宽度和高度，则会使用已有 Axes 的总边界框的宽度和高度。

        Parameters
        ----------
        target_ax : plt.Axes | list[plt.Axes]
            作为参考位置的目标 Axes 对象或列表
        ha : Literal['left', 'right', 'center'], optional
            水平对齐位置, by default 'right'
        va : Literal['top', 'bottom', 'center'], optional
            垂直对齐位置, by default 'center'
        width : LengthOrNumber | None, optional
            新 axes 的宽度, by default None
        height : LengthOrNumber | None, optional
            新 axes 的高度, by default None
        margin : LengthOrNumber | tuple[LengthOrNumber, LengthOrNumber], optional
            距离参考目标的距离，可以设置一个值，或两个值分别为x和y方向。
            如果是数字则认为单位是Pt, by default Pt(20)
        extend_fig : bool, optional
            如果新 axes 超出 figure，是否拓展 figure, by default True
        extend_fig_padding : LengthOrNumber | tuple[LengthOrNumber, LengthOrNumber], optional
            如果拓展 figure，新 axes 与 figure 之间的边距大小, by default Pt(20)
        **kwargs
            其他参数，传递给 Figure.add_axes() 方法

        Returns
        -------
        plt.Axes
            返回新创建的 Axes 对象
        """

        if isinstance(target_ax, plt.Axes):
            target_ax = [target_ax]

        # 计算总的边界位置
        merge_bbox = self._get_merge_bbox(
            [ax.get_position() for ax in target_ax]
        )

        if width is None:
            width = merge_bbox.width * self.get_figwidth()
        if height is None:
            height = merge_bbox.height * self.get_figheight()

        width = as_unit(width, fig=self, unit=LengthUnit.INCH)
        height = as_unit(height, fig=self, unit=LengthUnit.INCH)

        if hasattr(margin, '__len__') and len(margin) == 2:
            margin_x, margin_y = margin
        elif isinstance(margin, (int, float, Length)):
            margin_x = margin_y = margin
        else:
            raise ValueError("Unknown type for margin parameter.")

        if hasattr(extend_fig_padding, '__len__') and \
            len(extend_fig_padding) == 2:
            extend_padding_x, extend_padding_y = extend_fig_padding
        elif isinstance(extend_fig_padding, (int, float, Length)):
            extend_padding_x = extend_padding_y = extend_fig_padding
        else:
            raise ValueError("Unknown type for extend_fig_padding parameter.")

        margin_x = as_unit(margin_x, fig=self, unit=LengthUnit.PT)
        margin_y = as_unit(margin_y, fig=self, unit=LengthUnit.PT)
        margin_x = margin_x.to_fig_x().value
        margin_y = margin_y.to_fig_y().value
        extend_padding_x = as_unit(extend_padding_x, fig=self, unit=LengthUnit.PT)
        extend_padding_y = as_unit(extend_padding_y, fig=self, unit=LengthUnit.PT)
        extend_padding_x = extend_padding_x.to_fig_x().value
        extend_padding_y = extend_padding_y.to_fig_y().value
        height = height.to_fig_y().value
        width = width.to_fig_x().value

        ax_bbox = [0, 0, width, height]  # x0, y0, width, height
        match ha:
            case 'left':
                ax_bbox[0] = merge_bbox.x1 + margin_x
            case 'center':
                ax_bbox[0] = merge_bbox.x0 + (merge_bbox.width - width) / 2
            case 'right':
                ax_bbox[0] = merge_bbox.x0 - margin_x - width
        match va:
            case 'top':
                ax_bbox[1] = merge_bbox.y0 - height - margin_y
            case 'center':
                ax_bbox[1] = merge_bbox.y0 + (merge_bbox.height - height) / 2
            case 'bottom':
                ax_bbox[1] = merge_bbox.y1 + margin_y

        ax = self.add_axes(ax_bbox, **kwargs)

        if extend_fig:
            # 检查是否超出画幅，超出则扩展画幅
            extend_left = extend_right = extend_top = extend_bottom = 0
            if ax_bbox[0] < 0:
                extend_left = (-ax_bbox[0] + extend_padding_x) * self.get_figwidth()
            if ax_bbox[0] + ax_bbox[2] > 1:
                extend_right = (ax_bbox[0] + ax_bbox[2] - 1 + extend_padding_x) \
                    * self.get_figwidth()
            if ax_bbox[1] < 0:
                extend_bottom = (-ax_bbox[1] + extend_padding_y) * self.get_figheight()
            if ax_bbox[1] + ax_bbox[3] > 1:
                extend_top = (ax_bbox[1] + ax_bbox[3] - 1 + extend_padding_y)\
                    * self.get_figheight()

            if extend_left + extend_right + extend_top + extend_bottom > 0:
                self.extend(extend_left, extend_bottom,
                            extend_right, extend_top)

        return ax


    def append_colorbar(self,  mappable: any,
                    ax: plt.Axes | list[plt.Axes] | SubplotSpec=None,
                    loc: Literal['right', 'bottom', 'left', 'top']='right',
                    margin: LengthOrNumber=Pt(10),
                    width: LengthOrNumber=Pt(10),
                    padding: LengthOrNumber=Pt(0),
                    extend_fig: bool=True,
                    extend_fig_padding: LengthOrNumber=Pt(6), **kwargs
                    ):
        """在 axes 的旁边添加一个颜色条(colorbar)。
        颜色条的位置由 `loc` 参数控制，可以是 'right'、'left'、'top' 或 'bottom'。
        通过 `margin` 参数来设置颜色条与参考 Axes 之间的距离。
        通过 `width` 参数来设置颜色条的宽度(如果是水平放置则为高度)。
        通过 `padding` 参数来设置颜色条长度收缩的距离。
        如果颜色条超出画幅范围，且 `extend_fig=True` (默认)，
        则会自动扩展画幅大小以容纳颜色条。

        Parameters
        ----------
        mappable : any
            用于创建颜色条的 mappable 对象，通常是一个 image、contourf 等
        ax : plt.Axes | list[plt.Axes] | SubplotSpec, optional
            作为参考位置的目标 Axes 对象、列表或 SubplotSpec，
            如果为 None 则使用当前 Axes， by default None
        loc : Literal['right', 'bottom', 'left', 'top'], optional
            颜色条放置的位置, by default 'right'
        margin : LengthOrNumber, optional
            颜色条与参考目标的距离，如果是数字则认为单位是Pt, by default Pt(10)
        width : LengthOrNumber, optional
            颜色条的宽度(如果是水平放置则为高度)，如果是数字则认为单位是Pt,
            by default Pt(10)
        padding : LengthOrNumber, optional
            颜色条长度收缩的距离，如果是数字则认为单位是Pt, by default Pt(0)
        extend_fig : bool, optional
            如果颜色条超出 figure，是否拓展 figure, by default True
        extend_fig_padding : LengthOrNumber, optional
            如果拓展 figure，颜色条与 figure 之间的边距大小, by default Pt(20)

        Returns
        -------
        Colorbar
            返回新创建的颜色条对象
        """

        if ax is None:
            ax = self.gca()
        if isinstance(ax, plt.Axes):
            ax = [ax]
            ax_bbox = [i.get_position() for i in ax]
        elif isinstance(ax, SubplotSpec):
            ax_bbox = [ax.get_position(self)]

        merge_bbox = self._get_merge_bbox(ax_bbox)

        width = as_unit(width, fig=self, unit=LengthUnit.PT)
        margin = as_unit(margin, fig=self, unit=LengthUnit.PT)
        padding = as_unit(padding, fig=self, unit=LengthUnit.PT)


        ha = {'right': 'left', 'left': 'right',
              'top': 'center', 'bottom': 'center'}[loc]
        va = {'right': 'center', 'left': 'center',
              'top': 'bottom', 'bottom': 'top'}[loc]
        orientation = {'right': 'vertical', 'left': 'vertical',
                       'top': 'horizontal', 'bottom': 'horizontal'}[loc]

        if loc in ['right', 'left']:
            cax_width = width
            cax_height = merge_bbox.height * self.get_figheight() - \
                (2 * padding).to_inch()
        else:
            cax_width = merge_bbox.width * self.get_figwidth() - \
                (2 * padding).to_inch()
            cax_height = width

        cax = self.append_axes(ax, ha=ha, va=va,
                                width=cax_width,
                                height=cax_height,
                                margin=margin,
                                extend_fig=False,)

        kwargs.setdefault('orientation', orientation)

        cbar = self.colorbar(mappable, cax=cax, **kwargs)

        if extend_fig:
            cb_bbox = cax.get_tightbbox(self.canvas.get_renderer())
            x0, y0 = self.transFigure.inverted().transform((cb_bbox.x0, cb_bbox.y0))
            x1, y1 = self.transFigure.inverted().transform((cb_bbox.x1, cb_bbox.y1))
            extend_left = extend_right = extend_top = extend_bottom = 0
            if x0 < 0:
                extend_left = (-x0 + extend_fig_padding.to_fig_x().value) * \
                    self.get_figwidth()
            if x1 > self.get_figwidth():
                extend_right = (x1 - self.get_figwidth() +
                    extend_fig_padding.to_fig_x().value) * self.get_figwidth()
            if y0 < 0:
                extend_bottom = (-y0 + extend_fig_padding.to_fig_y().value) * \
                    self.get_figheight()
            if y1 > self.get_figheight():
                extend_top = (y1 - self.get_figheight() +
                    extend_fig_padding.to_fig_y().value) * self.get_figheight()
            if extend_left + extend_right + extend_top + extend_bottom > 0:
                self.extend(extend_left, extend_bottom,
                            extend_right, extend_top)

        return cbar