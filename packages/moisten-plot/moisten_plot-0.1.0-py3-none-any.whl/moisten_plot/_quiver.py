from matplotlib.quiver import QuiverKey, Quiver
from matplotlib.offsetbox import DrawingArea, AnchoredOffsetbox
from matplotlib.transforms import Bbox
import numpy as np
from .length_unit import LengthOrNumber, Pt, as_unit, LengthUnit
from typing import Literal
from matplotlib import text as mtext
from matplotlib import collections as mcollections
from matplotlib.pyplot import rcParams
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes

LocType = Literal['upper right', 'upper left', 'lower right',
                    'lower left', 'right', 'center left', 'center right',
                    'lower center', 'upper center', 'center', 1, 2, 3, 4,
                    5, 6, 7, 8, 9, 10]


class QuiverLegend(AnchoredOffsetbox):
    halign = {'N': 'center', 'S': 'center', 'E': 'left', 'W': 'right'}
    valign = {'N': 'bottom', 'S': 'top', 'E': 'center', 'W': 'center'}

    def __init__(self, Q: Quiver, U: float=1, label: str="", angle: float=0,
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
        添加一个 Quiver 箭头图例，与 quiverkey 不同的是，像 legend 一样有边框且
        可以设置对齐方式。
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

        self.fig = Q.figure

        # 使用原来的 QuiverKey 类来创建箭头，为了保证适应不同的 MPL 版本
        self.qk = QuiverKey(Q, 0, 0, U, label, angle=angle, labelpos=labelpos,
                            coordinates=coordinate,)
        self.qk._init()
        qkwargs = Q.polykw
        self.vector = mcollections.PolyCollection(self.qk.verts, **qkwargs)
        self.vector.set_transform(Q.get_transform())
        self.vector.set_figure(self.fig)
        if color is not None:
            self.vector.set_color(color)

        # 设置文字
        self.text = mtext.Text( text=label, 
                               horizontalalignment=self.halign[labelpos],
                               verticalalignment=self.valign[labelpos],
                               fontproperties=fontproperties)
        self.text.set_figure(self.fig)

        labelsep = as_unit(labelsep, fig=self.fig, unit=LengthUnit.PT).value
        text_offset = {"N": (0, labelsep),
                        "S": (0, -labelsep),
                        "E": (labelsep, 0),
                        "W": (-labelsep, 0)}[labelpos]
        self.text.set_position(np.array(text_offset)*self.dpi_cor)
        text_bbox = self._get_text_bbox()
        self.text.set_position(np.array(self.text.get_position())/self.dpi_cor)

        # 设置 Bbox
        vector_bbox = self._get_vector_bbox()
        legend_bbox = text_bbox.union([vector_bbox, text_bbox])

        self._da = DrawingArea(legend_bbox.width, legend_bbox.height,
                               max(-legend_bbox.x0, 0), max(-legend_bbox.y0, 0), clip=False)
        self.vector.set_offsets((0, 0))
        self.vector.set_offset_transform(self._da.get_transform())
        self._da.add_artist(self.vector)
        self._da.add_artist(self.text)

        zorder = kwargs.get('zorder', Q.get_zorder()+0.1)
        pad, borderpad = as_unit(pad, borderpad, fig=self.fig,
                                 unit=LengthUnit.EM, return_value=True)
        super().__init__(loc, child=self._da, pad=pad,
                         borderpad=borderpad, frameon=frameon,
                         bbox_to_anchor=bbox_to_anchor,
                         bbox_transform=self.qk.get_transform(), zorder=zorder)

        if style == 'legend':
            kwargs.setdefault('facecolor', self.fig.get_facecolor())
            kwargs.setdefault('edgecolor', '#666666')
            kwargs.setdefault('boxstyle', 'round, pad=0.3')
            kwargs.setdefault('alpha', rcParams['legend.framealpha'])
        elif style == 'default':
            kwargs.setdefault('facecolor', self.fig.get_facecolor())
            kwargs.setdefault('edgecolor', 'none')
        else:
            raise ValueError(f"Unknown style: {style}")
        self.patch.set(**kwargs)

    @property
    def dpi_cor(self):
        return self.fig.canvas.get_renderer().points_to_pixels(1.)

    def _get_vector_bbox(self) -> Bbox:
        vector_path = self.vector.get_paths()[0]
        xy_min = vector_path.vertices.min(axis=0)
        xy_max = vector_path.vertices.max(axis=0)
        xy_min = self.vector.get_transform().transform(xy_min)
        xy_max = self.vector.get_transform().transform(xy_max)
        return Bbox([xy_min/self.dpi_cor, xy_max/self.dpi_cor])

    def _get_text_bbox(self) -> Bbox:
        bbox = self.text.get_tightbbox(self.fig.canvas.get_renderer())
        return Bbox(bbox.get_points() / self.dpi_cor)



from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from scipy.interpolate import RegularGridInterpolator

class StreamQuiver():
    def __init__(self, ax:Axes, X: any, Y: any, U: any, V: any,
                 grid_num: int | tuple[int, int]=20, arrow_angle: float=30,
                 scale: float = 1, stagger: bool=True, head_length: float=0.3,
                 head_mode: Literal['data', 'screen']='data',
                 screen_head_length: LengthOrNumber=Pt(5),
                 color: any='black', linewidth: LengthOrNumber=Pt(1), **kwargs):
        self.ax = ax

        # 检查维度
        X = np.asarray(X)
        Y = np.asarray(Y)
        U = np.asarray(U)
        V = np.asarray(V)

        if X.ndim != 1 or Y.ndim != 1:
            raise ValueError("X and Y must be 1D arrays.")
        if U.ndim != 2 or V.ndim != 2:
            raise ValueError("U and V must be 2D arrays.")

        self.X = X
        self.Y = Y
        self.U = U
        self.V = V

        if isinstance(grid_num, int):
            self.grid_num_x = grid_num
            self.grid_num_y = grid_num
        elif isinstance(grid_num, (tuple, list)) and len(grid_num) == 2:
            self.grid_num_x = grid_num[0]
            self.grid_num_y = grid_num[1]

        self.x_range = (X.min(), X.max())
        self.y_range = (Y.min(), Y.max())

        self.dx = (self.x_range[1] - self.x_range[0]) / (self.grid_num_x + 1)
        self.dy = (self.y_range[1] - self.y_range[0]) / (self.grid_num_y + 1)

        # 网格中心点位置
        grid_x = np.linspace(self.x_range[0], self.x_range[1], self.grid_num_x)
        grid_y = np.linspace(self.y_range[0], self.y_range[1], self.grid_num_y)
        self.grid_x, self.grid_y = np.meshgrid(grid_x, grid_y, indexing='ij')
        if stagger:
            # 奇数行错开
            self.grid_x += 0.1547 * (self.grid_x - self.x_range[0])
            self.grid_x[:, 1::2] += self.dx / 2
            valid = self.grid_x < self.x_range[1]
            self.grid_x = self.grid_x[valid]
            self.grid_y = self.grid_y[valid]

        self.kwargs = kwargs
        self.arrow_angle = np.deg2rad(arrow_angle)
        self.steps = 5
        self.dt = scale
        self.head_length = head_length
        self.screen_head_length = as_unit(screen_head_length, fig=self.ax.figure, 
                                          unit=LengthUnit.PX).value
        self.color = color
        self.linewidth = as_unit(linewidth, fig=None, unit=LengthUnit.PT).value
        self.head_mode = head_mode
        self.lines = self.generate_lines()

    def rk2(self, x, y, interp_u, interp_v, inverse=False):
        """RK2 流线积分"""
        dt = -self.dt if inverse else self.dt
        k1u = dt * interp_u((y, x))
        k1v = dt * interp_v((y, x))
        k2u = dt * interp_u((y + k1v, x + k1u))
        k2v = dt * interp_v((y + k1v, x + k1u))
        x_new = x + 0.5 * (k1u + k2u)
        y_new = y + 0.5 * (k1v + k2v)
        return x_new, y_new

    def _cal_line_length(self, coord: np.ndarray, ratio: float):
        """计算线段长度， coord shape = (N, 2)"""
        if ratio > 1:
            coord[:, 0] /= ratio
        elif ratio < 1:
            coord[:, 1] *= ratio
        diffs = np.diff(coord, axis=0)
        seg_lengths = np.sqrt((diffs ** 2).sum(axis=1))
        return np.sum(seg_lengths)


    def generate_lines(self):
        #  每个格点都积分流线
        interp_u = RegularGridInterpolator((self.Y, self.X), self.U,
                                           bounds_error=False, fill_value=np.nan)
        interp_v = RegularGridInterpolator((self.Y, self.X), self.V,
                                           bounds_error=False, fill_value=np.nan)
        x = self.grid_x.flatten()
        y = self.grid_y.flatten()
        line_x = np.zeros((len(x), self.steps*2+1))
        line_y = np.zeros((len(y), self.steps*2+1))
        line_x[:, self.steps] = x
        line_y[:, self.steps] = y

        grid_u = interp_u((y, x))
        grid_v = interp_v((y, x))
        grid_speed = np.sqrt(grid_u**2 + grid_v**2)

        # 向前积分
        for k in range(self.steps):
            x_new, y_new = self.rk2(x, y, interp_u, interp_v, inverse=False)
            line_x[:, self.steps + k + 1] = x_new
            line_y[:, self.steps + k + 1] = y_new
            x_new[np.isnan(x_new)] = x[np.isnan(x_new)]
            y_new[np.isnan(y_new)] = y[np.isnan(y_new)]
            x, y = x_new, y_new

        # 向后积分
        x = self.grid_x.flatten()
        y = self.grid_y.flatten()
        for k in range(self.steps):
            x_new, y_new = self.rk2(x, y, interp_u, interp_v, inverse=True)
            line_x[:, self.steps - k - 1] = x_new
            line_y[:, self.steps - k - 1] = y_new
            x_new[np.isnan(x_new)] = x[np.isnan(x_new)]
            y_new[np.isnan(y_new)] = y[np.isnan(y_new)]
            x, y = x_new, y_new

        # 画箭头身
        lines = []
        for i in range(len(line_x)):
            x = line_x[i]
            y = line_y[i]
            x = x[~np.isnan(x)]
            y = y[~np.isnan(y)]
            if len(x) < 2:
                continue
            line_coords = np.array([x, y]).T
            lines.append(line_coords)

        arrow_lines = LineCollection(lines, linewidth=self.linewidth, color=self.color,
                         **self.kwargs)
        self.ax.add_collection(arrow_lines)
        self.ax.autoscale_view()

        # 画箭头
        lines2 = []
        if self.head_mode == 'data':
            # 使用 y/x 为比例标准
            data_ratio = (self.y_range[1] - self.y_range[0]) /\
                (self.x_range[1] - self.x_range[0])
            ax_pos = self.ax.get_position()
            ax_ratio = (ax_pos.height * self.ax.figure.get_size_inches()[1]) /\
                    (ax_pos.width * self.ax.figure.get_size_inches()[0])

            ratio =  ax_ratio / data_ratio
            if ratio >= 1:
                head_length = self.head_length * min(self.dx, self.dy / ratio)
            else:
                head_length = self.head_length * min(self.dx * ratio, self.dy)

            for i in range(len(line_x)):
                x = line_x[i][~np.isnan(line_x[i])]
                y = line_y[i][~np.isnan(line_y[i])]
                line_length = self._cal_line_length(np.array([x, y]).T, ratio)
                if len(x) < 2:
                    continue
                if ratio >= 1: # y > x
                    angle = np.arctan2((y[-1] - y[-2]), (x[-1] - x[-2]) / ratio)
                    hl = min(head_length*ratio, line_length)

                    head_loc = np.array([[0, 0], [x[-1], y[-1]], [0, 0]])
                    head_loc[0, 0] = x[-1] - hl * \
                        np.cos(angle - self.arrow_angle) * ratio
                    head_loc[0, 1] = y[-1] - hl * \
                        np.sin(angle - self.arrow_angle)
                    head_loc[2, 0] = x[-1] - hl * \
                        np.cos(angle + self.arrow_angle) * ratio
                    head_loc[2, 1] = y[-1] - hl * \
                        np.sin(angle + self.arrow_angle)
                    lines2.append(head_loc)
                else: # x >= y
                    angle = np.arctan2((y[-1] - y[-2]) * ratio, (x[-1] - x[-2]))
                    hl = min(head_length/ratio, line_length)

                    head_loc = np.array([[0, 0], [x[-1], y[-1]], [0, 0]])
                    head_loc[0, 0] = x[-1] - hl * \
                        np.cos(angle - self.arrow_angle)
                    head_loc[0, 1] = y[-1] - hl * \
                        np.sin(angle - self.arrow_angle) / ratio
                    head_loc[2, 0] = x[-1] - hl * \
                        np.cos(angle + self.arrow_angle)
                    head_loc[2, 1] = y[-1] - hl * \
                        np.sin(angle + self.arrow_angle) / ratio
                    lines2.append(head_loc)
        else:  # screen
            for i in range(len(line_x)):
                x = line_x[i][~np.isnan(line_x[i])]
                y = line_y[i][~np.isnan(line_y[i])]
                if len(x) < 2:
                    continue
                line_coord_px = self.ax.transData.transform(np.array([x, y]).T)
                line_length_px = self._cal_line_length(line_coord_px, 1)

                angle = np.arctan2((line_coord_px[-1, 1] - line_coord_px[-2, 1]),
                                   (line_coord_px[-1, 0] - line_coord_px[-2, 0]))
                hl = min(self.screen_head_length, line_length_px)
                head_loc_px = np.array([[0, 0], [line_coord_px[-1, 0], 
                                                 line_coord_px[-1, 1]], [0, 0]])
                head_loc_px[0, 0] = line_coord_px[-1, 0] - hl *\
                      np.cos(angle - self.arrow_angle)
                head_loc_px[0, 1] = line_coord_px[-1, 1] - hl *\
                      np.sin(angle - self.arrow_angle)
                head_loc_px[2, 0] = line_coord_px[-1, 0] - hl *\
                      np.cos(angle + self.arrow_angle)
                head_loc_px[2, 1] = line_coord_px[-1, 1] - hl *\
                      np.sin(angle + self.arrow_angle)
                head_loc = self.ax.transData.inverted().transform(head_loc_px)
                lines2.append(head_loc)

        arrow_heads = LineCollection(lines2, linewidth=self.linewidth, 
                                     color=self.color, **self.kwargs)
        self.ax.add_collection(arrow_heads)
        return arrow_lines, arrow_heads


    def quiverkey(self, ax: Axes, X=0.8, Y=1.05, U: float=1,
                  label: str="",
                  labelpos: Literal['N', 'E', 'S', 'W'] = 'E',
                  pad:LengthOrNumber=Pt(5),
                  **kwargs):
        """在 Axes 上添加一个箭头图例，类似于 `QuiverKey`。
        注意如果使用非矩形地图投影，此方法可能无法正确显示箭头图例。

        Parameters
        ----------
        ax : Axes
            需要添加图例的 Axes。
        X, Y : float, optional
            箭头根部的位置，为 Axes 的相对坐标, by default 0.8, 1.05
        U : float, optional
            箭头的长度, by default 1
        label : str, optional
            箭头图例的文字, by default ""
        labelpos : Literal['N', 'E', 'S', 'W'], optional
            文字在箭头的哪个方向, by default 'E'
        pad : LengthOrNumber, optional
            箭头与文字之间的间隔大小, by default Pt(5)

        Returns
        -------
        Text
            返回添加图例的文字对象。
        """
        # 箭身
        arrow_length = self.dt * U * (self.steps * 2)
        arrow = np.array([[0, 0], [arrow_length, 0]])

        # 画箭头
        ax_pos = self.ax.get_position()
        ax_ratio = (ax_pos.height * self.ax.figure.get_size_inches()[1]) /\
                (ax_pos.width * self.ax.figure.get_size_inches()[0])
        ang = 0
        head_x = [0, arrow_length, 0]
        head_y = [0, 0, 0]
        head_length = self.head_length * self.dx
        if arrow_length < head_length:
            head_length = arrow_length

        if ax_ratio >= 1:
            head_x[0] = arrow_length - head_length *\
                  np.cos(ang - self.arrow_angle) * ax_ratio
            head_y[0] = 0 - head_length * np.sin(ang - self.arrow_angle )
            head_x[2] = arrow_length - head_length *\
                  np.cos(ang + self.arrow_angle) * ax_ratio
            head_y[2] = 0 - head_length * np.sin(ang + self.arrow_angle)
        else:
            head_x[0] = arrow_length - head_length * np.cos(ang - self.arrow_angle)
            head_y[0] = 0 - head_length * np.sin(ang - self.arrow_angle) / ax_ratio
            head_x[2] = arrow_length - head_length * np.cos(ang + self.arrow_angle)
            head_y[2] = 0 - head_length * np.sin(ang + self.arrow_angle) / ax_ratio
        arrow_head = np.array([head_x, head_y]).T

        # 转为 Axes 坐标
        arrow = ax.transData.transform(arrow)
        arrow = ax.transAxes.inverted().transform(arrow)
        arrow_head = ax.transData.transform(arrow_head)
        arrow_head = ax.transAxes.inverted().transform(arrow_head)
        origin = arrow[0]
        arrow_head -= origin
        arrow -= origin
        arrow[:, 0] += X
        arrow[:, 1] += Y
        arrow_head[:, 0] += X
        arrow_head[:, 1] += Y

        args = self.kwargs.copy()
        args.update(transform=ax.transAxes, clip_on=False, color=self.color,
                    linewidth=self.linewidth)
        line1 = Line2D(arrow[:, 0], arrow[:, 1], **args)
        line2 = Line2D(arrow_head[:, 0], arrow_head[:, 1], **args)
        ax.add_artist(line1)
        ax.add_artist(line2)

        # 文字
        halign = {'N': 'center', 'S': 'center', 'E': 'left', 'W': 'right'}
        valign = {'N': 'bottom', 'S': 'top', 'E': 'center', 'W': 'center'}
        if labelpos in ['E', 'W']:
            pad = as_unit(pad, fig=ax.figure, unit=LengthUnit.FIG_X).value
        else:
            pad = as_unit(pad, fig=ax.figure, unit=LengthUnit.FIG_Y).value
        arrow_center = (arrow[0] + arrow[-1]) / 2
        text_anchor = {
            "N": (arrow_center[0], arrow_center[1] + pad),
            "S": (arrow_center[0], arrow_center[1] - pad),
            "E": (arrow[1, 0] + pad, arrow[1, 1]),
            "W": (arrow[0, 0] - pad, arrow[1, 1]),
        }
        return ax.text(x=text_anchor[labelpos][0],
                          y=text_anchor[labelpos][1],
                          s=label,
                          horizontalalignment=halign[labelpos],
                          verticalalignment=valign[labelpos],
                          transform=ax.transAxes, clip_on=False,
                          **kwargs)