from matplotlib.axes import Axes
from matplotlib.gridspec import SubplotSpec
from typing import Literal, Union
from matplotlib.quiver import Quiver
import numpy as np
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from dataclasses import dataclass, field
from cartopy.mpl.geoaxes import GeoAxes
from .length_unit import Length, LengthUnit, LengthOrNumber, Pt, Em, as_unit
from matplotlib import rcParams
from cartopy import crs as ccrs


LocType = Literal['upper right', 'upper left', 'lower right',
                    'lower left', 'right', 'center left', 'center right',
                    'lower center', 'upper center', 'center', 1, 2, 3, 4,
                    5, 6, 7, 8, 9, 10]


class AxesTools:

    def __init__(self, ax: Axes):
        self.ax: Axes | GeoAxes = ax
        self._figure = ax.figure
        self._is_geo_axes = isinstance(ax, GeoAxes)

        self._bbox = None
        self.ax_width = None
        self.ax_height = None
        self._update_bbox()


    def _update_bbox(self):
        """更新 Axes 的边界信息"""
        self._bbox = self.ax.get_position()
        self.ax_width = Length(self._figure, LengthUnit.FIG_X, self._bbox.width)
        self.ax_height = Length(self._figure, LengthUnit.FIG_Y, self._bbox.height)


    def label(self, text: str, loc: Literal['lt', 'lb', 'rt', 'rb']='lt',
              margin_x: LengthOrNumber=0, margin_y: LengthOrNumber=0,
              background_color: bool | str | tuple = 'white',
              padding: LengthOrNumber = Em(0.3), zorder=100,
              **kwargs):
        """为 Axes 添加一个在角落的标签，可用于给子图编号。
        文本框将紧贴 Axes 的边框，当边框线条宽度较小时，可能会重叠。

        Add a label to the corner of the Axes, which can be used to number
        the subplots.
        The text box will be close to the edge of the Axes, and may overlap
        when the border line width is small.

        Parameters
        ----------
        text : str
            标签内容
        loc : Literal['lt', 'lb', 'rt', 'rb']
            标签位置，lt 左上，lb 左下，rt 右上，rb 右下

            label position combination of: left/right, top/bottom
        margin_x : LengthOrNumber, optional
            x方向上距离 Axes 边框的边距, 默认单位为pt。

            x direction offset from the edge of the Axes, the default unit is inch.
        margin_y : LenType, optional
            y方向上距离 Axes 边框的边距, 默认单位为pt。

            y direction offset from the edge of the Axes, the default unit is inch.
        background_color : bool | str | tuple, optional
            标签的背景颜色，如果不需要背景，设置为 False，
            接受 Matpltlib 能识别的颜色格式，默认为白色。

            the background color of the label, and if you don't need a background,
            set it to False.
        background_pad : LengthOrNumber, optional
            背景的内边距，即背景的边缘到文字的距离, 默认为 0.3 em。

            the padding of the background border to the text, by default 0.3 em
        zorder : int, optional
            图层位置, by default 100

            zorder of the label, by default 100

        **kwargs :
            其他传递给 ax.text 的参数

            other parameters passed to ax.text

        Returns
        -------
        text : matplotlib.text.Text
            返回创建的文本对象

        """

        # 转为 Axes 的相对单位
        # offset_x, offset_y = as_inch(self._figure, offset_x, offset_y)
        # offset_x = offset_x / self.ax_width
        # offset_y = offset_y / self.ax_height

        margin_x = as_unit(margin_x, fig=self._figure, unit=LengthUnit.PT)
        margin_y = as_unit(margin_y, fig=self._figure, unit=LengthUnit.PT)
        padding = as_unit(padding, fig=self._figure, unit=LengthUnit.PT)

        match loc:
            case "lt":
                left_border = Pt(self.ax.spines['left'].get_linewidth() / 2)
                top_border = Pt(self.ax.spines['top'].get_linewidth() / 2)
                x = (left_border + margin_x).to_ax_x(self.ax)
                y = 1 - (top_border + margin_y).to_ax_y(self.ax)
                ha = 'left'
                va = 'top'
            case "lb":
                left_border = Pt(self.ax.spines['left'].get_linewidth() / 2)
                bottom_border = Pt(self.ax.spines['bottom'].get_linewidth() / 2)
                x = (left_border + margin_x).to_ax_x(self.ax)
                y = (bottom_border + margin_y).to_ax_y(self.ax)
                ha = 'left'
                va = 'bottom'
            case "rt":
                right_border = Pt(self.ax.spines['right'].get_linewidth() / 2)
                top_border = Pt(self.ax.spines['top'].get_linewidth() / 2)
                x = 1 - (right_border + margin_x).to_ax_x(self.ax)
                y = 1 - (top_border + margin_y).to_ax_y(self.ax)
                ha = 'right'
                va = 'top'
            case "rb":
                right_border = Pt(self.ax.spines['right'].get_linewidth() / 2)
                bottom_border = Pt(self.ax.spines['bottom'].get_linewidth() / 2)
                x = 1 - (right_border + margin_x).to_ax_x(self.ax)
                y = (bottom_border + margin_y).to_ax_y(self.ax)
                ha = 'right'
                va = 'bottom'
            case _:
                raise ValueError(f"Unknown loc: {loc}")

        if background_color:
            if kwargs.get('size') is not None:
                fontsize = kwargs['size']
            elif kwargs.get('fontsize') is not None:
                fontsize = kwargs['fontsize']
            else:
                fontsize = rcParams['font.size']
            if isinstance(fontsize, str):
                from matplotlib.font_manager import font_scalings
                fontsize = rcParams['font.size'] * font_scalings.get(fontsize, 1.0)

            padding = padding.to_pt(fontsize_pt=fontsize)

            match loc:
                case "lt":
                    x += padding.to_ax_x(self.ax)
                    y -= padding.to_ax_y(self.ax)
                case "lb":
                    x += padding.to_ax_x(self.ax)
                    y += padding.to_ax_y(self.ax)
                case "rt":
                    x -= padding.to_ax_x(self.ax)
                    y -= padding.to_ax_y(self.ax)
                case "rb":
                    x -= padding.to_ax_x(self.ax)
                    y += padding.to_ax_y(self.ax)

            return self.ax.text(x, y, text, ha=ha, va=va, transform=self.ax.transAxes,
                    bbox=dict(facecolor=background_color, edgecolor='none',
                              pad=padding.value),
                    zorder=zorder, **kwargs)
        else:
            return self.ax.text(x, y, text, ha=ha, va=va,
                                transform=self.ax.transAxes, zorder=zorder,
                                **kwargs)


    def quiver_by_size(self, *args, length_pre_unit: LengthOrNumber=Pt(10),
                       width: LengthOrNumber=Pt(1), **kwargs) -> Quiver:
        """
        使用指定的长度单位来绘制箭头图，例如设置 1 m/s 的风矢量长多少像素。
        可以使用 `length_pre_unit` 设置数据每单位对应的实际长度。
        例如数据 u=1, v=1，矢量长度为 sqrt(2)，如果设置 `length_pre_unit=Pt(10)`，
        则箭头实际长度为 10*sqrt(2) pt，且不随画幅、Axes而变化，
        适用于需要在不同的子图中画出相同的矢量箭头。

        Draw a quiver plot by using the specified length unit. You can use
        `length_pre_unit` to set the actual length of each unit of data.
        For example, if u=1, v=1, the vector length is sqrt(2), and let
        `length_pre_unit=Pt(10)`, then the actual length of the arrow is
        10*sqrt(2) pt, and it does not change with the figure or Axes.
        It is a convenient way to draw the same vector arrows in different subplots.

        Parameters
        ----------
        *args
            plt.quiver() 原始的位置参数, 例如 X, Y, U, V,

            the original positional arguments of plt.quiver(), such as X, Y, U, V,
        length_pre_unit : LenType, optional
            数据每单位对应的实际长度, 默认为 Pt(10)

            the actual length of each unit of data, by default Pt(10)
        width : LenType, optional
            箭头的宽度, 默认为 Pt(1)

            the width of the arrow, by default Pt(1)

        Returns
        -------
        Quiver
            Quiver 对象

            Quiver object
        """

        length_pre_unit, width = as_unit(length_pre_unit, width,
                                          fig=self._figure,
                                          unit=LengthUnit.INCH)

        q = self.ax.quiver(*args, scale_units='inches',
                           scale=1/length_pre_unit.to_inch().value,
                           units="inches", width=width.to_inch().value,
                           **kwargs)

        return q


    def draw_rectangle(self, left: float, right: float, bottom: float, top: float,
                segments: int = 20, transform=None, **kwargs) -> PathPatch:
        """画一个可以设置边分段数的矩形，在有地图投影的情况下会很有用。
        需要传入左、右、下、上的坐标值，还可以设置所有 Patch 的属性，例如
        edgecolor、facecolor、linewidth 等。

        Draw a rectangle with a specified number of segments. This is useful
        when there is a map projection. You need to pass in the left, right,
        bottom, and top coordinates, and you can also set all Patch properties,
        such as edgecolor, facecolor, linewidth, etc.

        Parameters
        ----------
        left : float
            左边的x值
        right : float
            右边的x值
        bottom : float
            下边的y值
        top : float
            上边的y值
        segments : int, optional
            每个边的分段数, by default 20
        transform : _type_, optional
            转换投影，如果没有设置此参数且 Ax 设置了地图投影，会自动设置。

        Returns
        -------
        PathPatch
            返回矩形的 PathPatch 对象
        """

        if transform is None and self._is_geo_axes:
            transform = ccrs.PlateCarree()._as_mpl_transform(self.ax)

        _left = [np.full(segments, left), np.linspace(top, bottom, segments)]
        _right = [np.full(segments, right), np.linspace(bottom, top, segments)]
        _bottom = [np.linspace(left, right, segments), np.full(segments, bottom)]
        _top = [np.linspace(right, left, segments), np.full(segments, top)]
        v = np.concatenate([_left, _bottom, _right, _top], axis=1)
        v = v.T

        path = Path(v, closed=True)
        path_patch = PathPatch(path, **kwargs)

        if transform is not None:
            path_patch.set_transform(transform)

        return self.ax.add_patch(path_patch)


    def quiver_legend(self, Q: Quiver, U: float, label: str, angle: float=0,
                coordinate: Literal['axes', 'figure', 'data', 'inches'] = 'axes',
                labelpos: Literal['N', 'E', 'S', 'W'] = 'E',
                labelsep: LengthOrNumber=Pt(4),
                loc: LocType = 'upper right',
                bbox_to_anchor: tuple = None, color: any=None,
                pad: LengthOrNumber=Pt(5), borderpad: LengthOrNumber=Pt(5),
                frameon: bool=True, fontproperties=None,
                style: Literal['default', 'legend'] = 'default',
                **kwargs):
        """
        添加一个 Quiver 箭头图例，与 quiverkey 不同的是，像 legend 一样有边框
        且可以设置对齐方式。需要注意的是，使用此图例，需要在创建 Figure 时设置
        与保存时的 DPI 一致，否则图例的大小会不一致。
        参数融合了 quiverkey 和 legend 的参数。

        Parameters
        ----------
        Q : Quiver
            `~.quiver()` 返回的对象。

            the return object of `~.quiver()`
        U : float, optional
            图例中箭头的长度，默认为 1。

            The length of the arrow in the legend, default is 1.
        label : str, optional
            图例中的文字说明。 The text in the legend.
        angle : float, optional
            箭头的角度，默认为 0。

            The angle of the arrow, default is 0.
        coordinate : Literal['axes', 'figure', 'data', 'inches'], optional
            图例所在的坐标系，默认为 'axes'。

            The coordinate system of the legend, default is 'axes'.
        labelpos : Literal['N', 'E', 'S', 'W'], optional
            文字在箭头的哪个方向，与 quiverkey 一致，默认为 'E'。

            The position of the text relative to the arrow, default is 'E'.
        labelsep : LenType, optional
            文字与箭头之间的间隔，单位为 pt，默认为 4 pt。

            The distance between the text and the arrow, default is 4 pt.
        loc : LocType, optional
            图例的位置，默认为 'upper right'。

            The location of the legend, default is 'upper right'.
        bbox_to_anchor : tuple, optional
            图例的锚点位置，默认为 None。

            The anchor point of the legend, default is None.
        color : any, optional
            箭头的颜色，默认跟随 quiver 的颜色。

            The color of the arrow, default is the same as the quiver.
        pad : LenType, optional
            图例的内边距，单位为字体大小，默认为 5 pt。

            The padding of the legend, default is 5 pt.
        borderpad : LenType, optional
            图例与锚点之间的间距，单位为字体大小，默认为 5 pt。

            The padding between the legend and the anchor point, default is 5 pt.
        frameon : bool, optional
            是否显示边框，默认为 True。

            Whether to show the border, default is True.
        fontproperties : any, optional
            字体属性，默认为 None。

            Font properties, default is None.
        style : Literal['default', 'legend'], optional
            预设样式，默认为白底无边框，可以设置为 'legend'，类似图例的样式。

            Preset style, default is 'default', can be set to 'legend' for a 
            legend-like style.

        **kwargs : any, optional
            其他设置边框的参数，传递给 `FancyBboxPatch`。

            Other parameters for the border, passed to `FancyBboxPatch`.

        """
        from ._quiver import QuiverLegend
        qk = QuiverLegend(Q, U, label, angle, coordinate, labelpos, labelsep,
                            loc, bbox_to_anchor, color, pad, borderpad, frameon,
                            fontproperties, style, **kwargs)
        self.ax.add_artist(qk)
        return qk


    def barbs(self, x: any, y: any, u: any, v: any,
              low_res: int=1, barb_increments: dict=None, 
              transform=ccrs.PlateCarree(), length: LengthOrNumber=Pt(5.5),
              linewidth: LengthOrNumber=Pt(0.5), color: any='black',
              hide_empty: bool=True, **kwargs):
        """绘制风羽，默认配置好了短杆为 2，长杆为 4，三角为 20。支持降采样和
        隐藏空的风羽。

        Parameters
        ----------
        x, y, u, v : np.ndarray | DataArray
            风羽的坐标和风速，与 `plt.barbs()` 一致。

            The coordinates and wind speed of the barbs, consistent with `plt.barbs()`.
        low_res : int, optional
            降采样间隔，1为不降采样。

            The downsampling interval, 1 means no downsampling.
        barb_increments : dict, optional
            自定义风羽长短杆的值，与 `plt.barbs()` 一致。

            Custom values for the short and long barbs, consistent with `plt.barbs()`.
        transform : _type_, optional
            地图投影，默认为 PlateCarree。

            The map projection, default is PlateCarree.
        length, linewidth: LenType, optional
            风羽的长度和线宽，单位为 pt。

            The length and line width of the barbs, in pt.
        color : str, optional
            风羽的颜色，默认为黑色。

            The color of the barbs, default is black.
        hide_empty : bool, optional
            是否隐藏空的风羽，默认为 True。

            Whether to hide empty barbs, default is True.

        Returns
        -------
        Barbs
            返回 `plt.barbs()` 的返回对象。

        """

        x = np.asarray(x)
        y = np.asarray(y)
        u = np.asarray(u)
        v = np.asarray(v)

        length, linewidth = as_unit(length, linewidth, fig=self._figure,
                                    unit=LengthUnit.PT, return_value=True)

        def _low_res(v: np.ndarray, low_res: int):
            if len(v.shape) == 1:
                return v[::low_res]
            elif len(v.shape) == 2:
                return v[::low_res, ::low_res]
            else:
                raise ValueError("arrays must be 1D or 2D")

        if barb_increments is None:
            barb_increments = dict(half=2, full=4, flag=20)

        if hide_empty:
            sizes = {"emptybarb": 0}
        else:
            if sizes is None:
                sizes = {"emptybarb": 0.5}

        if "sizes" in kwargs:
            sizes.update(kwargs.pop("sizes"))

        return self.ax.barbs(
                    _low_res(x, low_res), _low_res(y, low_res),
                    _low_res(u, low_res), _low_res(v, low_res),
                    barb_increments=barb_increments, transform=transform,
                    length=length, linewidth=linewidth, color=color,
                    sizes=sizes, **kwargs)


    def fill_land(self, color: str | tuple | None = None,
                  scale: Literal['110m', '50m', '10m', 'auto']='auto',):
        """填充陆地颜色，仅适用于 GeoAxes。

        Fill land color, only applicable to GeoAxes.

        Parameters
        ----------
        color : str | tuple | None, optional
            陆地颜色, by default None

            Land color, by default None
        scale : Literal['110m', '50m', '10m', 'auto'], optional
            陆地数据的分辨率, 默认为 'auto'

            The scale of the land features, by default 'auto'
        """

        if not self._is_geo_axes:
            Warning("`fill_land` only works for GeoAxes.")
            return

        from cartopy.feature import NaturalEarthFeature, auto_scaler, COLORS

        if scale == 'auto':
            scale = auto_scaler
        if color is None:
            color = COLORS['land']

        land = NaturalEarthFeature(
            'physical', 'land', scale,
            edgecolor='none', facecolor=color, zorder=-1)

        self.ax.add_feature(land)


    def fill_water(self, color: str | tuple | None = None,
                   lake: bool = False, river: bool = False,
                   river_width: LengthOrNumber=Pt(0.8),
                   scale: Literal['110m', '50m', '10m', 'auto']='auto',):
        """填充水体颜色（海、湖、河），仅适用于 GeoAxes。

        Fill water color (ocean, lakes, rivers), only applicable to GeoAxes.

        Parameters
        ----------
        color : str | tuple | None, optional
            水体颜色, by default None

            Water color, by default None
        lake : bool, optional
            是否填充湖泊, 默认为 False

            Whether to fill lakes, by default False
        river : bool, optional
            是否绘制河流线条, 默认为 False

            Whether to draw river lines, by default False
        river_width : LenType, optional
            河流线条宽度, 默认为 0.8 pt

            The line width of rivers, by default 0.8 pt
        scale : Literal['110m', '50m', '10m', 'auto'], optional
            水体数据的分辨率, 默认为 'auto'

            The scale of the water features, by default 'auto'
        """

        if not self._is_geo_axes:
            Warning("`fill_water` only works for GeoAxes.")
            return

        from cartopy.feature import NaturalEarthFeature, auto_scaler, COLORS

        if scale == 'auto':
            scale = auto_scaler
        if color is None:
            color = COLORS['water']

        ocean = NaturalEarthFeature(
            'physical', 'ocean', scale,
            edgecolor='none', facecolor=color, zorder=-1)
        self.ax.add_feature(ocean)

        if lake:
            lake = NaturalEarthFeature(
                'physical', 'lakes', scale,
                edgecolor='none', facecolor=color, zorder=-1)
            self.ax.add_feature(lake)

        if river:
            river = NaturalEarthFeature(
                'physical', 'rivers_lake_centerlines', scale,
                edgecolor=color, facecolor='none', zorder=-1)

            river_width = as_unit(river_width, fig=self._figure,
                                unit=LengthUnit.PT, return_value=True)
            self.ax.add_feature(river, linewidth=river_width)


    def coastlines(self, linewidth: LengthOrNumber=Pt(0.5),color: str = 'black',
                   scale: Literal['110m', '50m', '10m', 'auto']='auto',
                   **kwargs):
        """绘制海岸线，仅适用于 GeoAxes。`GeoAxes.coastlines()` 的封装。

        Draw coastlines, only applicable to GeoAxes.

        Parameters
        ----------
        linewidth : LenType, optional
            海岸线宽度, 默认为 0.5 pt

            Coastline width, by default 1 pt
        color : str, optional
            海岸线颜色, by default 'black'

            Coastline color, by default 'black'
        scale : Literal['110m', '50m', '10m', 'auto'], optional
            海岸线数据的分辨率, 默认为 'auto'

            The scale of the coastline features, by default 'auto'
        **kwargs : any, optional
            其他传递给 `GeoAxes.coastlines()` 的参数。
        """

        if not self._is_geo_axes:
            Warning("`coastlines` only works for GeoAxes.")
            return

        linewidth = as_unit(linewidth, fig=self._figure,
                            unit=LengthUnit.PT, return_value=True)

        self.ax.coastlines(color=color, linewidth=linewidth,
                           resolution=scale, **kwargs)


    def map_ticks_and_gridlines(self,
                                lon_ticks: list | np.ndarray | None = None,
                                lat_ticks: list | np.ndarray | None = None,
                                lon_major_interval: float | None = None,
                                lon_minor_interval: float | None = None,
                                lat_major_interval: float | None = None,
                                lat_minor_interval: float | None = None,
                                use_axes_ticks: bool = True,
                                hide_lon_ticklables: bool = False,
                                hide_lat_ticklables: bool = False,
                                draw_gridlines: bool = True,
                                gridline_linestyle: str = '--',
                                gridline_linewidth: LengthOrNumber = Pt(0.5),
                                gridline_color: str = 'gray',
                                gridline_kwargs: dict = None,
                                ):
        """为地图 Axes 添加经纬度刻度和网格线。
        如果 `use_axes_ticks` 为 True (默认)，
        则使用 Axes 的刻度和标签(需要是矩形的投影)，否则使用 cartopy.Gridliner
        来绘制标签，且 `draw_gridline` 需为 True。

        传入 `lon_ticks` 和 `lat_ticks` 可以直接设置经纬度刻度的位置，
        也可以传入 `lon_major_interval` 和 `lat_major_interval` 来设置主刻度间隔，
        如果两者都没有传入，则使用自动刻度定位器来生成刻度位置。
        还可以传入 `lon_minor_interval` 和 `lat_minor_interval` 来设置次刻度间隔。

        `hide_lon_ticklables` 和 `hide_lat_ticklables` 可以用来隐藏经纬度标签。

        Parameters
        ----------
        lon_ticks, lat_ticks : list | np.ndarray | None, optional
            指定经纬度刻度的值，默认自动生成, by default None
        lon_major_interval, lat_major_interval : float | None, optional
            指定经纬度刻度的间隔自动生成刻度, by default None
        lon_minor_interval, lat_minor_interval : float | None, optional
            指定经纬度刻度的次间隔, by default None
        use_axes_ticks : bool, optional
            使用 Axes 的刻度和刻度标签，否则使用 Gridliner 的, by default True
        hide_lon_ticklables, hide_lat_ticklabels : bool, optional
            是否隐藏经纬度刻度标签，在多子图排版时有用, by default False
        draw_gridlines : bool, optional
            是否画网格线, by default True
        gridline_linestyle, gridline_linewidth, gridline_color : str, optional
            网格线的样式, by default '--', Pt(0.5), 'gray'
        gridline_kwargs : dict, optional
            其他传递给 Gridliner 的参数, by default None
        """

        from matplotlib.ticker import MultipleLocator
        from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
        from cartopy.mpl.ticker import LongitudeLocator, LatitudeLocator

        ax_extent = self.ax.get_extent(crs=ccrs.PlateCarree())

        if lon_ticks is None:
            if lon_major_interval is None:
                lon_ticks = LongitudeLocator().tick_values(ax_extent[0], ax_extent[1])
            else:
                lon_ticks = MultipleLocator(lon_major_interval).tick_values(
                    ax_extent[0], ax_extent[1])
        lon_ticks = np.array(lon_ticks)
        lon_ticks = lon_ticks[(lon_ticks >= ax_extent[0]) &
                              (lon_ticks <= ax_extent[1])]

        if lat_ticks is None:
            if lat_major_interval is None:
                lat_ticks = LatitudeLocator().tick_values(ax_extent[2], ax_extent[3])
            else:
                lat_ticks = MultipleLocator(lat_major_interval).tick_values(
                    ax_extent[2], ax_extent[3])
        lat_ticks = np.array(lat_ticks)
        lat_ticks = lat_ticks[(lat_ticks >= ax_extent[2]) &
                              (lat_ticks <= ax_extent[3])]

        if use_axes_ticks:
            self.ax.set_xticks(lon_ticks, crs=ccrs.PlateCarree())
            self.ax.set_yticks(lat_ticks, crs=ccrs.PlateCarree())
            self.ax.set_xticklabels([LONGITUDE_FORMATTER(lon) for lon in lon_ticks])
            self.ax.set_yticklabels([LATITUDE_FORMATTER(lat) for lat in lat_ticks])

            if lon_minor_interval is not None:
                lon_minor_ticks = MultipleLocator(lon_minor_interval).tick_values(
                    ax_extent[0], ax_extent[1])
                lon_minor_ticks = lon_minor_ticks[
                        (lon_minor_ticks >= ax_extent[0]) &
                        (lon_minor_ticks <= ax_extent[1])]
                self.ax.set_xticks(lon_minor_ticks,
                                   crs=ccrs.PlateCarree(), minor=True)
            if lat_minor_interval is not None:
                lat_minor_ticks = MultipleLocator(lat_minor_interval).tick_values(
                    ax_extent[2], ax_extent[3])
                lat_minor_ticks = lat_minor_ticks[
                        (lat_minor_ticks >= ax_extent[2]) &
                        (lat_minor_ticks <= ax_extent[3])]
                self.ax.set_yticks(lat_minor_ticks,
                                   crs=ccrs.PlateCarree(), minor=True)

            if hide_lon_ticklables:
                self.ax.set_xticklabels([])
            if hide_lat_ticklables:
                self.ax.set_yticklabels([])

        if draw_gridlines:
            gridline_linewidth = as_unit(gridline_linewidth, fig=self._figure,
                                         unit=LengthUnit.PT, return_value=True)
            gl = self.ax.gridlines(draw_labels=not use_axes_ticks,
                                   xlocs=lon_ticks, ylocs=lat_ticks,
                                   linestyle=gridline_linestyle,
                                   color=gridline_color,
                                   linewidth=gridline_linewidth,
                                   x_inline=False, y_inline=False,
                                   **(gridline_kwargs or {}))
            if not use_axes_ticks:
                gl.right_labels = False
                gl.top_labels = False
                if hide_lon_ticklables:
                    gl.bottom_labels = False
                if hide_lat_ticklables:
                    gl.left_labels = False


    def ignore_first_x_tick_labels(self, number_from_left: int=1):
        """隐藏 x 轴最左边的若干个刻度标签，适用于密集排版时避免重叠。

        Parameters
        ----------
        number_from_left : int, optional
            隐藏数量, by default 1
        """
        tl = self.ax.get_xticklabels()
        for label in tl[:number_from_left]:
            label.set_visible(False)


    def format_ticklabels_to_lon(self, which: Literal['x', 'y']='x'):
        """将横/纵刻度标签格式化为经度格式"""
        from cartopy.mpl.gridliner import LONGITUDE_FORMATTER
        if which == 'x':
            self.ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
        elif which == 'y':
            self.ax.yaxis.set_major_formatter(LONGITUDE_FORMATTER)
        else:
            raise ValueError(f"Unknown which: {which}")


    def format_ticklabels_to_lat(self, which: Literal['x', 'y']='y'):
        """将横/纵刻度标签格式化为纬度格式"""
        from cartopy.mpl.gridliner import LATITUDE_FORMATTER
        if which == 'x':
            self.ax.xaxis.set_major_formatter(LATITUDE_FORMATTER)
        elif which == 'y':
            self.ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
        else:
            raise ValueError(f"Unknown which: {which}")


    def set_tick_interval(self, x_major: float=None, x_minor: float=None,
                         y_major: float=None, y_minor: float=None,
                        ) -> None:
        """一个方便设置主副刻度间隔的方法，等价于：

        ```python
        from matplotlib.ticker import MultipleLocator
        ax.xaxis.set_major_locator(MultipleLocator(x_major))
        ax.yaxis.set_major_locator(MultipleLocator(y_major))
        ax.xaxis.set_minor_locator(MultipleLocator(x_minor))
        ax.yaxis.set_minor_locator(MultipleLocator(y_minor))
        ```

        A convenient method to set the major and minor tick intervals, which
        is equivalent to above code.

        Parameters
        ----------
        x_major, y_major, x_minor, y_minor : float, optional
            主刻度和次刻度的间隔，默认为 None，即不设置。
        """
        from matplotlib.ticker import MultipleLocator
        if x_major is not None:
            self.ax.xaxis.set_major_locator(MultipleLocator(x_major))
        if y_major is not None:
            self.ax.yaxis.set_major_locator(MultipleLocator(y_major))
        if x_minor is not None:
            self.ax.xaxis.set_minor_locator(MultipleLocator(x_minor))
        if y_minor is not None:
            self.ax.yaxis.set_minor_locator(MultipleLocator(y_minor))


    def set_time_ticks(self, which: Literal['major', 'minor'],
                       axis: Literal['x', 'y'],
                       interval: int | list[int] | None = None,
                       unit: Literal['year', 'month', 'days_of_month',
                                     'weekday', 'hour', 'minute', 'second',
                                     'ms'] = 'hour',
                       format: str='%Y-%m-%d %H:%M:%S', tz:str=None):
        """设置时间刻度的位置和格式，是不同 DateLocator 的封装。
        刻度具体设置可参考 https://matplotlib.org/stable/api/dates_api.html。

        时间格式化符号列表：

        - %y 两位数的年份表示（00-99）
        - %Y 四位数的年份表示（000-9999）
        - %m 月份（01-12）
        - %d 月内中的一天（0-31）
        - %H 24小时制小时数（0-23）
        - %I 12小时制小时数（01-12）
        - %M 分钟数（00-59）
        - %S 秒（00-59）
        - %a 本地简化星期名称
        - %A 本地完整星期名称
        - %b 本地简化的月份名称
        - %B 本地完整的月份名称
        - %c 本地相应的日期表示和时间表示
        - %j 年内的一天（001-366）
        - %p 本地A.M.或P.M.的等价符
        - %U 一年中的星期数（00-53）星期天为星期的开始
        - %w 星期（0-6），星期天为星期的开始
        - %W 一年中的星期数（00-53）星期一为星期的开始
        - %x 本地相应的日期表示
        - %X 本地相应的时间表示
        - %Z 当前时区的名称

        Parameters
        ----------
        which : Literal['major', 'minor']
            设置主刻度还是次刻度
        axis : Literal['x', 'y']
            设置 x 轴还是 y 轴
        interval : int | list[int] | None, optional
            刻度的值或间隔，默认为 None。
            使用默认的间隔，一般为全部，例如 `unit='hour'` 时，
            `interval=None` 则表示每小时一个刻度。
        unit : Literal['year', 'month', 'days_of_month',
                       'weekday', 'hour', 'minute', 'second',
                       'ms'], optional
            刻度的单位, by default 'hour'
        format : _type_, optional
            时间的格式, by default '%Y-%m-%d %H:%M:%S'
        tz : str, optional
            时区, by default None

        """

        match unit:
            case 'year':
                from matplotlib.dates import YearLocator as Locator
            case 'month':
                from matplotlib.dates import MonthLocator as Locator
            case 'days_of_month':
                from matplotlib.dates import DayLocator as Locator
            case 'weekday':
                from matplotlib.dates import WeekdayLocator as Locator
            case 'hour':
                from matplotlib.dates import HourLocator as Locator
            case 'minute':
                from matplotlib.dates import MinuteLocator as Locator
            case 'second':
                from matplotlib.dates import SecondLocator as Locator
            case 'ms':
                from matplotlib.dates import MicrosecondLocator as Locator
            case _:
                raise ValueError(f"Unknown unit: {unit}")

        from matplotlib.dates import DateFormatter

        if axis == 'x':
            ax = self.ax.xaxis
        elif axis == 'y':
            ax = self.ax.yaxis
        else:
            raise ValueError(f"Unknown axis: {axis}")

        if which == 'major':
            ax.set_major_locator(Locator(interval, tz=tz))
            ax.set_major_formatter(DateFormatter(format, tz))
        elif which == 'minor':
            ax.set_minor_locator(Locator(interval, tz=tz))
        else:
            raise ValueError(f"Unknown which: {which}")

    
    def quiver_legend(self, Q: Quiver, U: float, label: str, angle: float=0,
                    coordinate: Literal['axes', 'figure', 'data', 'inches'] = 'axes',
                    labelpos: Literal['N', 'E', 'S', 'W'] = 'E',
                    labelsep: LengthOrNumber=Pt(4),
                    loc: LocType = 'upper right',
                    bbox_to_anchor: tuple = None, color: any=None,
                    pad: LengthOrNumber=Pt(5), borderpad: LengthOrNumber=Pt(5),
                    frameon: bool=True, fontproperties=None,
                    style: Literal['default', 'legend'] = 'default',
                    **kwargs):
        """
        添加一个 Quiver 箭头图例，与 quiverkey 不同的是，像 legend 一样有边框
        且可以设置对齐方式。需要注意的是，使用此图例，需要在创建 Figure 时设置
        与保存时的 DPI 一致，否则图例的大小会不一致。
        参数融合了 quiverkey 和 legend 的参数。

        Parameters
        ----------
        Q : Quiver
            `~.quiver()` 返回的对象。

            the return object of `~.quiver()`
        U : float, optional
            图例中箭头的长度，默认为 1。

            The length of the arrow in the legend, default is 1.
        label : str, optional
            图例中的文字说明。 The text in the legend.
        angle : float, optional
            箭头的角度，默认为 0。

            The angle of the arrow, default is 0.
        coordinate : Literal['axes', 'figure', 'data', 'inches'], optional
            图例所在的坐标系，默认为 'axes'。

            The coordinate system of the legend, default is 'axes'.
        labelpos : Literal['N', 'E', 'S', 'W'], optional
            文字在箭头的哪个方向，与 quiverkey 一致，默认为 'E'。

            The position of the text relative to the arrow, default is 'E'.
        labelsep : LenType, optional
            文字与箭头之间的间隔，单位为 pt，默认为 4 pt。

            The distance between the text and the arrow, default is 4 pt.
        loc : LocType, optional
            图例的位置，默认为 'upper right'。

            The location of the legend, default is 'upper right'.
        bbox_to_anchor : tuple, optional
            图例的锚点位置，默认为 None。

            The anchor point of the legend, default is None.
        color : any, optional
            箭头的颜色，默认跟随 quiver 的颜色。

            The color of the arrow, default is the same as the quiver.
        pad : LenType, optional
            图例的内边距，单位为字体大小，默认为 5 pt。

            The padding of the legend, default is 5 pt.
        borderpad : LenType, optional
            图例与锚点之间的间距，单位为字体大小，默认为 5 pt。

            The padding between the legend and the anchor point, default is 5 pt.
        frameon : bool, optional
            是否显示边框，默认为 True。

            Whether to show the border, default is True.
        fontproperties : any, optional
            字体属性，默认为 None。

            Font properties, default is None.
        style : Literal['default', 'legend'], optional
            预设样式，默认为白底无边框，可以设置为 'legend'，类似图例的样式。

            Preset style, default is 'default', can be set to 'legend' for a 
            legend-like style.

        **kwargs : any, optional
            其他设置边框的参数，传递给 `FancyBboxPatch`。

            Other parameters for the border, passed to `FancyBboxPatch`.

        """
        from ._quiver import QuiverLegend
        qk = QuiverLegend(Q, U, label, angle, coordinate, labelpos, labelsep,
                            loc, bbox_to_anchor, color, pad, borderpad, frameon,
                            fontproperties, style, **kwargs)
        self.ax.add_artist(qk)
        return qk



    def stream_quiver(self, X: any, Y: any, U: any, V: any,
                    scale: float=1, grid_num: int | tuple[int, int]=20,
                    head_length: float = 0.3, arrow_angle: float = 30,
                    head_mode: Literal['data', 'screen']='data',
                    screen_head_length: LengthOrNumber=Pt(5),
                    color: any='black', linewidth: LengthOrNumber=Pt(1),
                    **kwargs):
        """绘制流线箭头图，类似于 plt.quiver()，但箭头是沿着流场积分的流线，
        所有箭头积分时间相同，越长表示流速越大。

        因为不同的情况下， Axes 与 数据范围的长宽不是 1:1 的，因此箭头的头部需要
        一定的变形以使得显示出来的效果更好。
        此方法提供了两种头部绘制模式：`data` 和 `screen`。
        大部分情况下（不使用弯曲地图投影时），两种模式区别不大。
        使用地图投影时，如果效果不佳，可以试试切换另一种模式。

        此外，返回的 `StreamQuiver` 对象还提供了 `quiverkey` 方法可以添加对应图例。

        Parameters
        ----------
        X, Y, U, V : any
            如同 plt.quiver() 的位置、速度参数。
        scale : float, optional
            箭头的大小缩放，实际控制积分的时长, by default 1
        grid_num : int | tuple[int, int], optional
            箭头的数量，如果是整数，则表示在 x 和 y 方向的数量相同，
            如果是两个值，则分别表示在 x 和 y 方向的数量, by default
        head_length : float, optional
            箭头头部的长度，此参数在 `head_mode='data'` 时生效，
            为箭头间间隔长度的比例, by default 0.3
        arrow_angle : float, optional
            箭头头部长开的夹角, by default 30
        head_mode : Literal['data', 'screen'], optional
            箭头的绘制模式,`data` 基于数据绘制，会根据当前 Axes 计算与数据的比例，
            保持箭头在当前画面下保持正确比例，
            此模式箭头长度使用 `head_length` 参数控制；
            `screen` 基于屏幕像素位置绘制，保持箭头在屏幕上长度不变，
            此模式箭头长度使用 `screen_head_length` 参数控制, by default 'data'
        screen_head_length : LengthOrNumber, optional
            箭头头部的长度，当 `head_mode='screen'`时有效, by default Pt(5)
        color : any, optional
            箭头颜色, by default 'black'
        linewidth : LengthOrNumber, optional
            箭头线宽度, by default Pt(1)
        **kwargs : any
            其他传递给 `LineCollection` 的参数，可以调整箭头线条的样式。

        Returns
        -------
        StreamQuiver
            StreamQuiver 对象
        """
        from ._quiver import StreamQuiver
        sq = StreamQuiver(self.ax, X, Y, U, V, scale=scale, grid_num=grid_num,
                          head_length=head_length, arrow_angle=arrow_angle,
                          head_mode=head_mode, color=color, linewidth=linewidth,
                          screen_head_length=screen_head_length, **kwargs)
        return sq


    def pressure_log_y(self, 
                       major_ticks: any = None,
                       minor_ticks: any = None,
                       major_ticks_interval: float | None = None,
                       minor_ticks_interval: float | None = None,
                       hide_minor_ticklabels: bool = False):
        """将 Y 轴设置为气压对数坐标轴，并将 Y 轴反转，画剖面或廓线时很有用。
        调整了刻度的显示格式，使其为普通数字格式，而不是 5x10^2 的指数。
        同时，你也可以传入刻度值或刻度间隔来设置刻度位置，或隐藏副刻度的标签。

        Parameters
        ----------
        major_ticks : any | None, optional
            设置主刻度的值, by default None
        minor_ticks : any | None, optional
            设置副刻度的值, by default None
        major_ticks_interval : float | None, optional
            设置主刻度的间隔, by default None
        minor_ticks_interval : float | None, optional
            设置副刻度的间隔, by default None
        hide_minor_ticklabels : bool, optional
            是否隐藏副刻度的标签, by default False
        """
        from matplotlib.ticker import ScalarFormatter
        from matplotlib.ticker import MultipleLocator
        self.ax.set_yscale('log')
        self.ax.invert_yaxis()
        self.ax.yaxis.set_major_formatter(ScalarFormatter())
        self.ax.yaxis.set_minor_formatter(ScalarFormatter())
        if major_ticks_interval is not None:
            self.ax.yaxis.set_major_locator(MultipleLocator(major_ticks_interval))
        if minor_ticks_interval is not None:
            self.ax.yaxis.set_minor_locator(MultipleLocator(minor_ticks_interval))
        if major_ticks is not None:
            self.ax.set_yticks(major_ticks)
        if minor_ticks is not None:
            self.ax.set_yticks(minor_ticks, minor=True)
        if hide_minor_ticklabels:
            from matplotlib.ticker import NullFormatter
            self.ax.yaxis.set_minor_formatter(NullFormatter())

from matplotlib.gridspec import SubplotSpec
from matplotlib.figure import Figure
class SubplotParams(AxesTools):

    def __init__(self, fig: Figure, subplot_spec: SubplotSpec, row: int,
                 col: int, nrows: int, ncols: int, subplot_kwargs: dict):
        self._figure = fig
        self._subplot_spec = subplot_spec
        self._subplot_kwargs = subplot_kwargs

        self.nrows = nrows
        """子图总行数"""

        self.ncols = ncols
        """子图总列数"""

        self.row = row
        """当前子图所在的行索引，从 0 开始"""

        self.col = col
        """当前子图所在的列索引，从 0 开始"""

        self.is_left = subplot_spec.is_first_col()
        """当前子图是否是最左侧的子图（第一列）"""

        self.is_right = subplot_spec.is_last_col()
        """当前子图是否是最右侧的子图（最后一列）"""

        self.is_top = subplot_spec.is_first_row()
        """当前子图是否是最上方的子图（第一行）"""

        self.is_bottom = subplot_spec.is_last_row()
        """当前子图是否是最下方的子图（最后一行）"""

        self.row_index = col + row * ncols
        """以行优先的方式计算当前子图的索引，从 0 开始"""

        self.col_index = row + col * nrows
        """以列优先的方式计算当前子图的索引，从 0 开始"""

        self._ax = None

    @property
    def ax(self):
        """获取当前子图的 Axes 对象，如果不使用此属性，则不会实际添加 Axes 。"""
        if self._ax is None:
            ax = self._figure.add_subplot(self._subplot_spec,
                                          **self._subplot_kwargs)
            super().__init__(ax)
        return self._ax

    @ax.setter
    def ax(self, value):
        self._ax = value

    def set_subplot_kwargs(self, **kwargs):
        """设置子图的参数，这些参数会在创建子图时传递给 `fig.add_subplot()`。
        注意需要在使用 SubplotParams.ax 创建子图之前调用此方法。

        Parameters
        ----------
        **kwargs : any
            传递给 `fig.add_subplot()` 的参数。
        """
        self._subplot_kwargs.update(kwargs)