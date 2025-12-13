"""
控制 Colormap 的工具
"""

from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.colors import Colormap
import numpy as np
from typing import Union, Literal
from matplotlib import colormaps as mcolormaps
from matplotlib import colors as mcolors

Color = Union[str, tuple[float, float, float], tuple[float, float, float, float]]
ColormapDef = Union[Colormap, str, list[Color], tuple[Color, Color]]


class MoiCmap(Colormap):
    """
    MoiCmap 是一个方便编辑的 colormap 对象，继承自 matplotlib.colors.Colormap。

    使用介绍
    --------
    可以使用已有的 colormap 名称、颜色或颜色列表来创建一个 MoiCmap 对象。

    >>> my_cmap = MoiCmap('gray')  # 一个纯灰色的 colormap
    >>> my_cmap = MoiCmap('RdBu')  # Matplotlib 内置的 colormap
    >>> my_cmap = MoiCmap(['r', 'g', 'b'])  # 使用颜色列表定义

    `print` 一个 `MoiCmap` 对象时，会在终端显示一个彩色的 colorbar
    （需要终端支持显示彩色），如果你想查看所有注册的 colormaps，
    可以使用 `print_all_cmaps()` 方法。
    >>> MoiCmap.print_all_cmaps()  # 打印所有注册的 colormaps

    编辑方法 
    -----------------

    MoiCmap 提供了多种对操作 colormap 的方法，如裁剪、替换、拼接等。

    **裁剪**, 只保留一部分的 colormap
    >>> # 可以使用 clip() 方法
    >>> my_cmap = my_cmap.clip(0.2, 0.5)  # 0~1，保留 0.2 到 0.5 的部分
    >>> # 又或者直接切片
    >>> my_cmap = my_cmap[0.2:0.5]

    **去除**, 去掉一部分的 colormap，中间合并
    >>> # 可以使用 sub() 方法
    >>> my_cmap = my_cmap.sub(0.2, 0.5)  # 去掉 0.2 到 0.5 的部分
    >>> # 又或者直接用减号
    >>> my_cmap = my_cmap - (0.2, 0.5)  # 去掉 0.2 到 0.5 的部分

    **拼接**, 将两个 colormap 拼接在一起
    >>> # 可以使用 concat() 方法，并且可以指定比例与过渡范围
    >>> # 将 ”Blues" 和 "Reds" 拼接在一起，中间有 0.1 宽的过渡范围
    >>> cmap1 = MoiCmap('Blues')
    >>> my_cmap = cmap1.concat('Reds', 0.5, 0.1)
    >>> # 也可以直接用加号
    >>> my_cmap = cmap1 + 'Reds'  # 等比例拼接

    **替换**, 替换 colormap 中间的颜色
    >>> # 使用设置切片的值的方法来替换
    >>> my_cmap[0.2:0.5] = 'Reds'  # 替换 0.2 到 0.5 的部分为 "Reds"
    >>> # replace_center() 方法可以替换中间的颜色
    >>> my_cmap = my_cmap.replace_center('red', 0.2)  # 替换中间 0.2 宽为红色

    **反转**, 反转 colormap 颜色的顺序
    >>> my_cmap = -my_cmap  # 可以直接加上负号
    >>> my_cmap = my_cmap.reversed()  # 或者使用 reversed() 方法

    同时， MoiCmap 还提供了一些调色的方法：
     - `resampled()`：重新采样 colormap 的颜色数
     - `hue()`：调整色相
     - `brightness()`：调整亮度
     - `saturation()`：调整饱和度
     - `gamma()`：调整伽马值
     - `contrast()`：调整对比度

    """
    def __init__(self, cmap: ColormapDef,
                 cmap_type: Literal['linear', 'list'] = 'linear',
                 N=256, name=""):
        """创建一个方便编辑的 colormap 对象，
        该类继承自 matplotlib.colors.Colormap，画图时可以作为 `cmap` 参数使用。

        参数 `cmap` 可接收以下类型来定义 colormap 对象：

         - *str*：已注册的 colormap 名称，如 'gray'、'jet' 等
         - 一个颜色的值，生成一个纯色的 colormap，有效值为:
            - 颜色名称，如 'red'、'blue'
            - 十六进制颜色值，如 '#ff0000'、'#00ff00'
            - RGB/RGBA 元组/列表，如 (1, 0, 0) 或 (0, 1, 0)

         - *list*：颜色列表，有效值同上，组成的列表可以任意组合类型，
         如 ['red', '#00ff00', (0, 0, 1)]
         - 一个 Colormap 对象，直接复制该对象的属性


        Create a MoiCmap object, a convenient colormap object for editing,
        inheriting from matplotlib.colors.Colormap.

        Parameters
        ----------
        cmap : ColormapDef
            一个定义 colormap 的对象。

            An object that defines the colormap.
        cmap_type : Literal['linear', 'list'], optional
            colormap 的类型，仅当 `cmap` 是一个颜色列表时有效，有效值为
            'linear' 和 'list'，表示这些颜色是线性插值还是作为列表颜色。
            默认是 'linear'。

            The type of colormap, only valid when `cmap` is a list of colors.
            Valid values are 'linear' and 'list', indicating whether these
            colors are linearly interpolated or treated as a list of colors.
            Default is 'linear'.
        N : int, optional
            colormap 的颜色数, by default 256

            The number of colors in the colormap, by default 256.
        name : str, optional
            colormap 的名称，默认将自动识别

            The name of the colormap, default is auto-detected.

        """

        super().__init__(name=name, N=N)
        self._copy_to_self(self._parse_colormap_def(cmap, cmap_type, name, N))


    @staticmethod
    def _parse_colormap_def(cmap: ColormapDef,
                            cmap_type: Literal['linear', 'list']='linear',
                            name: str="", N: int=256) -> Colormap:
        """解析 colormap 定义，返回一个 Colormap 对象"""
        if isinstance(cmap, Colormap):
            return cmap
        elif isinstance(cmap, str):
            # 尝试解析为已注册的 colormap
            try:
                return mcolormaps.get_cmap(cmap)
            except ValueError:
                # 尝试解析为颜色
                if mcolors.is_color_like(cmap):
                    if name == "":
                        name = cmap
                    return ListedColormap([cmap], name=name, N=N)
                else:
                    raise ValueError(f"'{cmap}' is not a valid colormap"
                                     " name or color.")
        elif isinstance(cmap, (list, tuple, np.ndarray)):
            if mcolors.is_color_like(cmap):
                return ListedColormap(cmap, name=name, N=N)
            else:
                if cmap_type == 'linear':
                    return LinearSegmentedColormap.from_list(name, cmap, N)
                elif cmap_type == 'list':
                    return ListedColormap(cmap, name=name, N=N)
                else:
                    raise ValueError(f"'{cmap_type}' is not a valid colormap "
                                     "type.")
        elif mcolors.is_color_like(cmap):
            return ListedColormap([cmap], name=name, N=N)
        else:
            raise ValueError(f"'{cmap}' is not a valid colormap name or color.")


    def _copy_to_self(self, colormap: Colormap) -> None:
        self.__dict__.update(colormap.__dict__)
        if not colormap._isinit:
            colormap._init()
        self._lut = colormap._lut
        self._isinit = True
        if hasattr(colormap, "monochrome"):
            self.monochrome = colormap.monochrome
        else:
            self.monochrome = False


    @staticmethod
    def _to_colorbar_ascii(cmap: ColormapDef, str_len: int=30) -> str:
        """将 colormap 转换为能在终端显示的彩色 colorbar"""
        colors = cmap(np.linspace(0.0, 1.0, str_len*2))
        colors *= 255
        colors = colors.astype(int)

        result = ""
        for i in range(len(colors) // 2):
            c1 = colors[2*i]
            c2 = colors[2*i+1]
            fg_color = f"\033[38;2;{c1[0]};{c1[1]};{c1[2]}m"
            bg_color = f"\033[48;2;{c2[0]};{c2[1]};{c2[2]}m"
            result += f"{fg_color}{bg_color}▌\033[0m"

        return result


    @staticmethod
    def _to_colorbar_rich(cmap: ColormapDef, str_len: int=30) -> str:
        """将 colormap 转换为能在终端显示的彩色 colorbar"""

        colors = cmap(np.linspace(0.0, 1.0, str_len*2))
        colors *= 255
        colors = colors.astype(int)

        result = ""
        for i in range(len(colors) // 2):
            c1 = colors[2*i]
            c2 = colors[2*i+1]
            fg_color = f"rgb({c1[0]},{c1[1]},{c1[2]})"
            bg_color = f"rgb({c2[0]},{c2[1]},{c2[2]})"
            result += f"[{fg_color} on {bg_color}]▌[/]"

        return result


    def __repr__(self):
        return f"<MoiCmap> {self._to_colorbar_ascii(self)} {self.name}"


    @staticmethod
    def _resample_array(arr: np.ndarray, N:int) -> np.ndarray:
        """将数组重新采样到 N 个点"""
        if N < arr.shape[0]:
            idx = np.linspace(0, arr.shape[0]-1, N, dtype=int)
            return arr[idx]
        elif N > arr.shape[0]:
            ori_idx = np.arange(arr.shape[0])
            new_idx = np.linspace(0, arr.shape[0]-1, N)
            new_result = np.zeros((N, arr.shape[1]), dtype=arr.dtype)
            for i in range(arr.shape[1]):
                new_result[:, i] = np.interp(new_idx, ori_idx, arr[:, i])
            return new_result
        else:
            return arr


    def resampled(self, lutsize):
        """返回一个重新采样为 lutsize 个颜色的 colormap 对象"""
        if not self._isinit:
            self._init()
        if lutsize == self.N:
            return self
        else:
            lut = self._resample_array(self._lut[:self.N], lutsize)
            lut = np.concatenate((lut, self._lut[self.N:]), axis=0)
            return MoiCmap.from_lut(lut, name=self.name, N=lutsize)


    def reversed(self) -> "MoiCmap":
        """返回一个顺序反转的 colormap 对象，也可以直接加上负号。"""
        if not self._isinit:
            self._init()
        lut = np.flip(self._lut[:self.N], axis=0)
        lut = np.concatenate((lut, [self._lut[-2], 
                                    self._lut[-3], self._lut[-1]]), axis=0)
        return MoiCmap.from_lut(lut, name=f"{self.name}_r", N=self.N)


    def __neg__(self) -> "MoiCmap":
        return self.reversed()


    @staticmethod
    def from_lut(lut: np.ndarray, name: str = "", N: int = 256, 
                 monochrome=False) -> "MoiCmap":
        """根据 LUT 创建一个 MoiCmap 对象"""
        c = Colormap(name=name, N=N)
        # 如果 lut 不包含 bad、under、over 的值，则添加
        if lut.shape[0] == N:
            lut = np.concatenate((lut, [lut[0], lut[-1], [1,1,1,0]]), axis=0)
        elif lut.shape[0] == N + 3:
            pass
        else:
            raise ValueError(f"LUT must be of size {N} or {N + 3}, "
                             f"but got {lut.shape[0]}")
        c._lut = lut
        c._isinit = True
        return MoiCmap(c)


    @staticmethod
    def _concat(a: Colormap, b: Colormap, ratio: float, N: float,
                blur: float=0) -> "MoiCmap":
        """按照比例拼接两个 colormap, a 在前，b 在后"""
        if not a._isinit:
            a._init()
        if not b._isinit:
            b._init()

        ratio = np.clip(ratio, 0, 1)
        blur = np.clip(np.abs(blur), 0, 1)
        if blur / 2 > ratio or blur / 2 > (1-ratio):
            raise ValueError("blur range must be less than ratio")

        a_lut = MoiCmap._resample_array(a._lut[:a.N], int(a.N * (ratio-blur/2)))
        b_lut = MoiCmap._resample_array(b._lut[:b.N],
                                        N - int(a.N * (ratio+blur/2)))
        if blur > 0:
            blur_lut = LinearSegmentedColormap.from_list("",
                [a_lut[-1], b_lut[0]], N=int(a.N * blur))
            blur_lut._init()
            blur_lut = blur_lut._lut[:blur_lut.N]
        else:
            blur_lut = np.empty((0, 4), dtype=float)
        lut = np.concatenate((a_lut, blur_lut, b_lut), axis=0)
        under = a._lut[a._i_under]
        over = b._lut[b._i_over]
        bad = a._lut[a._i_bad]
        lut = np.concatenate((lut, [under], [over], [bad]), axis=0)
        return MoiCmap.from_lut(lut, name=f"{a.name}-{b.name}", N=N)


    def __add__(self, other: ColormapDef):
        """相加，等比例拼接"""
        other = MoiCmap._parse_colormap_def(other)
        return MoiCmap(self._concat(self, other, 0.5, self.N))


    def __radd__(self, other: ColormapDef):
        """相加，等比例拼接"""
        return self.__add__(other)


    def concat(self, other: ColormapDef, ratio: float = 0.5, 
               blur: float=0) -> "MoiCmap":
        """在当前 colormap 后面拼上另一个 colormap。

        Concatenate two colormaps with a ratio.

        Parameters
        ----------
        other : ColormapDef
            另一个 colormap

            Another colormap to concatenate.
        ratio : float, optional
            当前 colormap 占比，范围 [0, 1]，默认 0.5

            The ratio of the current colormap, in the range [0, 1],
            default is 0.5.
        blur : float, optional
            拼接时的模糊宽度，使拼接处的颜色平滑过渡。若为 0（默认），则无过渡。
            此模糊宽度相当于在两个 colormap 之间插入一个渐变的 colormap。

            The blur width when concatenating, to make the color
            transition smoothly. If 0 (default), there is no transition.
            This blur width is equivalent to inserting a gradient
            colormap between the two colormaps.

        Returns
        -------
        MoiCmap
            拼接后的 colormap 对象

            The concatenated colormap object.
        """
        other = MoiCmap._parse_colormap_def(other)
        return MoiCmap(self._concat(self, other, ratio, self.N, blur))


    def _clip(self, start: float, end: float) -> "MoiCmap":
        start = np.clip(start, 0, 1)
        end = np.clip(end, 0, 1)
        if start >= end:
            raise ValueError("start must be less than end")

        if not self._isinit:
            self._init()

        start_idx = int(start * self.N)
        end_idx = int(end * self.N)
        lut = self._lut[start_idx:end_idx]
        lut = self._resample_array(lut, self.N)
        return MoiCmap.from_lut(lut, name=self.name, N=self.N,
                                monochrome=self.monochrome)


    def clip(self, start: float=0, end: float=1) -> "MoiCmap":
        """裁剪 colormap 的范围，保留裁剪的部分。与 `sub()` 相反。

        >>> cmap = MoiCmap('Blues')
        >>> cmap1 = cmap.clip(0.2, 0.5)  # 保留 0.2 到 0.5 的部分
        >>> cmap2 = cmap[0.2:0.5]        # 或者使用切片

        Clip the colormap to a range.

        Parameters
        ----------
        start : float, optional
            开始位置，范围 [0, 1]，默认 0

            The start position, in the range [0, 1], default is 0.
        end : float, optional
            结束位置，范围 [0, 1]，默认 1

            The end position, in the range [0, 1], default is 1.
        Returns
        -------
        MoiCmap
            裁剪后的 colormap 对象

            The clipped colormap object.
        """
        return self._clip(start, end)


    def __sub__(self, other: list[float]|tuple[float]|np.ndarray[float]
                ) -> "MoiCmap":
        """剪去 colormap 的一部分"""
        if not isinstance(other, (list, tuple, np.ndarray)):
            raise ValueError("other must be a list, tuple or ndarray")
        if not len(other) == 2:
            raise ValueError("length of other must be 2")
        if other[0] >= other[1]:
            raise ValueError("start must be less than end")
        other = [np.clip(i, 0, 1) for i in other]
        if other[0] == 0 and other[1] == 1:
            raise ValueError("you cannot remove the whole colormap")

        if not self._isinit:
            self._init()
        start_idx = int(other[0] * self.N)
        end_idx = int(other[1] * self.N)
        lut = np.concatenate((self._lut[:start_idx], self._lut[end_idx:self.N]),
                              axis=0)
        lut = self._resample_array(lut, self.N)
        return MoiCmap.from_lut(lut, name=self.name, N=self.N, 
                                monochrome=self.monochrome)


    def sub(self, start: float=0, end: float=1) -> "MoiCmap":
        """剪去 colormap 的一部分，与 `clip()` 相反。

        >>> cmap = MoiCmap('Blues')
        >>> cmap1 = cmap.sub(0.2, 0.5)  # 去掉 0.2 到 0.5 的部分
        >>> cmap2 = cmap - (0.2, 0.5)     # 或者直接用减号

        Subtract a part of the colormap, opposite to `clip()`.

        Parameters
        ----------
        other : list[float] | tuple[float] | np.ndarray[float]
            要剪去的范围，是一个长度为 2 的列表、元组或数组，
            数值范围在 [0, 1] 之间

            The range to subtract, a list, tuple or array of length 2,
            with values in the range [0, 1].
        Returns
        -------
        MoiCmap
            _description_
        """
        return self.__sub__([start, end])


    def __getitem__(self, key: int | slice):
        """获取某个颜色，或者裁剪"""
        if isinstance(key, int):
            return self._lut[key]
        elif isinstance(key, slice):
            start = key.start
            stop = key.stop
            return self.clip(start, stop)
        else:
            raise TypeError("key must be an int or a slice")


    def _replace(self, start: float, end: float, cmap: ColormapDef
                 ) -> "MoiCmap":
        """替换 colormap 的一部分 """
        if not self._isinit:
            self._init()
        start = np.clip(start, 0, 1)
        end = np.clip(end, 0, 1)
        if start >= end:
            raise ValueError("start must be less than end")
        if start == 0 and end == 1:
            raise ValueError("you cannot replace the whole colormap")

        start_idx = int(start * self.N)
        end_idx = int(end * self.N)
        lut = np.copy(self._lut[:self.N])
        cmap = self._parse_colormap_def(cmap)
        cmap = cmap.resampled(end_idx - start_idx)
        if not cmap._isinit:
            cmap._init()
        lut = np.concatenate((lut[:start_idx], cmap._lut[:cmap.N],
                                lut[end_idx:self.N]), axis=0)
        lut = self._resample_array(lut, self.N)
        return self.from_lut(lut, name=self.name, N=self.N, monochrome=False)


    def replace_center(self, color: Color="white", width:float=0.1) -> "MoiCmap":
        """替换 colormap 中心的颜色

        Replace the center color of the colormap.

        Parameters
        ----------
        color : Color, optional
            替换的颜色，默认是白色

            The color to replace, default is white.
        width : float, optional
            替换的宽度，默认是 0.1

            The width of the replacement, default is 0.1.
        Returns
        -------
        MoiCmap
            替换后的 colormap 对象

            The replaced colormap object.
        """
        return self._replace(0.5 - width / 2, 0.5 + width / 2, color)


    def __setitem__(self, key: int | slice, value: ColormapDef) -> None:
        """设置某个颜色，或者裁剪"""
        if isinstance(key, int):
            self._lut[key] = value
        elif isinstance(key, slice):
            start = key.start
            stop = key.stop
            cmp = self._replace(start, stop, value)
            self._copy_to_self(cmp)
        else:
            raise TypeError("key must be an int or a slice")


    @staticmethod
    def print_all_cmaps(cols: int=None) -> None:
        """打印所有注册的 colormaps 的名称和预览图，需要终端支持显示8bit颜色。

        Print all registered colormaps with their names and previews.
        Requires terminal support for 8-bit colors.

        Parameters
        ----------
        cols : int, optional
            列数，默认自动计算
            The number of columns, default is auto-calculated.
        """
        from rich.console import Console
        from rich.table import Table
        console = Console()
        console_width = console.width
        if cols is None:
            cols = console_width // 60 + 1

        table = Table(title="Matplotlib Registered Colormaps")
        for i in range(cols):
            table.add_column("Name", justify="right", style="cyan")
            table.add_column("Preview", justify="left", style="magenta")

        cmap_names = list(mcolormaps)
        cmap_width = (console_width - 2 - (2*cols - 1)*3 - 16 * cols) // cols - 1

        cmap_list = []
        for cmap_name in cmap_names:
            if cmap_name.endswith("_r"):
                continue
            cmap = mcolormaps.get_cmap(cmap_name)
            cmap_list.append([cmap_name, 
                              MoiCmap._to_colorbar_rich(cmap, cmap_width)])

        for i in range(0, len(cmap_list), cols):
            row = []
            for j in range(cols):
                if i + j < len(cmap_list):
                    row += cmap_list[i + j]
                else:
                    row += [""] * 2
            table.add_row(*row)

        console.print(table)


    # ------------- Color Processing -----------------
    @staticmethod
    def _lut_to_hsv(cmap) -> np.ndarray:
        """将 LUT 转换为 HSV 颜色空间，不保留特殊值"""
        if not cmap._isinit:
            cmap._init()
        lut = np.copy(cmap._lut[:cmap.N])
        lut[:, :3] = mcolors.rgb_to_hsv(lut[:, :3])
        return lut

    def brightness(self, value: float) -> "MoiCmap":
        """调整 colormap 的亮度

        Adjust the brightness of the colormap.

        Parameters
        ----------
        value : float
            亮度值倍数，原始的亮度将乘上此值，大于1变亮，小于1变暗

            The brightness value multiplier, the original brightness
            will be multiplied by this value, greater than 1 will
            brighten, less than 1 will darken.

        Returns
        -------
        MoiCmap
            调整后的 colormap 对象

            The adjusted colormap object.
        """
        lut = self._lut_to_hsv(self)
        lut[:, 2] = np.clip(lut[:, 2] * value, 0, 1)
        lut[:, :3] = mcolors.hsv_to_rgb(lut[:, :3])
        return MoiCmap.from_lut(lut, name=self.name, N=self.N,
                                monochrome=self.monochrome)


    def saturation(self, value: float) -> "MoiCmap":
        """调整 colormap 的饱和度

        Adjust the saturation of the colormap.

        Parameters
        ----------
        value : float
            饱和度值倍数，原始的饱和度将乘上此值，大于1变饱和，小于1变淡

            The saturation value multiplier, the original saturation
            will be multiplied by this value, greater than 1 will
            saturate, less than 1 will desaturate.

        Returns
        -------
        MoiCmap
            调整后的 colormap 对象

            The adjusted colormap object.
        """
        lut = self._lut_to_hsv(self)
        lut[:, 1] = np.clip(lut[:, 1] * value, 0, 1)
        lut[:, :3] = mcolors.hsv_to_rgb(lut[:, :3])
        return MoiCmap.from_lut(lut, name=self.name, N=self.N,
                                monochrome=self.monochrome)


    def hue(self, value: float) -> "MoiCmap":
        """调整 colormap 的色相

        Adjust the hue of the colormap.

        Parameters
        ----------
        value : float
            色相值偏移量，原始色相为 [0, 1]，将加上此值。

            The hue value offset, the original hue is [0, 1], and
            will be added to this value.

        Returns
        -------
        MoiCmap
            调整后的 colormap 对象

            The adjusted colormap object.
        """
        lut = self._lut_to_hsv(self)
        lut[:, 0] += value
        lut[:, 0] = lut[:, 0] % 1
        lut[:, :3] = mcolors.hsv_to_rgb(lut[:, :3])
        return MoiCmap.from_lut(lut, name=self.name, N=self.N, 
                                monochrome=self.monochrome)


    def gamma(self, value: float) -> "MoiCmap":
        """调整 colormap 的 gamma 值，即 brightness=brightness ^ (1/gamma)

        Adjust the gamma of the colormap.

        Parameters
        ----------
        value : float
            gamma 值。 The gamma value.

        Returns
        -------
        MoiCmap
            调整后的 colormap 对象

            The adjusted colormap object.
        """
        lut = self._lut_to_hsv(self)
        lut[:, 2] = np.clip(lut[:, 2] ** (1 / value), 0, 1)
        lut[:, :3] = mcolors.hsv_to_rgb(lut[:, :3])
        return MoiCmap.from_lut(lut, name=self.name, N=self.N,
                                monochrome=self.monochrome)


    def contrast(self, value: float) -> "MoiCmap":
        """调整 colormap 的对比度

        Adjust the contrast of the colormap.

        Parameters
        ----------
        value : float
            对比度强度，大于1增强对比度，小于1减弱对比度

            The contrast strength, greater than 1 will enhance the
            contrast, less than 1 will weaken the contrast.

        Returns
        -------
        MoiCmap
            调整后的 colormap 对象

            The adjusted colormap object.
        """
        lut = self._lut_to_hsv(self)
        lut[:, 2] = np.clip(lut[:, 2]**value/\
                            (lut[:, 2]**value+(1-lut[:, 2])**value), 0, 1)
        lut[:, :3] = mcolors.hsv_to_rgb(lut[:, :3])
        return MoiCmap.from_lut(lut, name=self.name, N=self.N,
                                monochrome=self.monochrome)


    @classmethod
    def register_moi_cmap(self, prefix="m_"):
        """注册 MoiCmap 中的 colormap 到 matplotlib 中

        Register the colormaps in MoiCmap to matplotlib.

        Parameters
        ----------
        prefix : str, optional
            前缀，默认是 "m_"，即注册的 colormap 名称为 "m_<name>"。

            The prefix, default is "m_", i.e. the registered colormap
            name is "m_<name>".
        """
        # 获取已有的 colormap
        cmaps = list(mcolormaps)
        from ._colormap import MOI_CMAP

        for name, colors in MOI_CMAP.items():
            if prefix + name in cmaps:
                continue

            cm = LinearSegmentedColormap.from_list(prefix + name, colors)
            mcolormaps.register(cm)
            mcolormaps.register(cm.reversed(), name=prefix + name + "_r")
