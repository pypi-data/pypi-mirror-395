"""
一个统一、方便的单位转换模块。
一共有以下的长度单位：
 - inch = 25.4 mm
 - mm
 - pt = 1/72 inch
 - px = inch / dpi
 - fig_x, fig_y = relative length of figure size, from 0 to 1
 - ax_x, ax_y = relative length of axis size, from 0 to 1
"""

from enum import Enum
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import warnings
from matplotlib import pyplot as plt

type Number = int | float
"""数字类型，int 或 float"""

type LengthOrNumber = Length | Number
"""长度或数字类型，Length 或 int 或 float"""

class LengthUnit(Enum):
    """各个长度单位的枚举类型。"""
    INCH = "inch"
    MM = "mm"
    PT = "pt"
    PX = "px"
    FIG_X = "fig_x"
    FIG_Y = "fig_y"
    AX_X = "ax_x"
    AX_Y = "ax_y"
    EM = "em"

class Length():
    """一段实际的长度，可以用不同的单位表示。"""
    def __init__(self,fig: Figure=None, unit: LengthUnit=LengthUnit.INCH,
                 value: int | float = 1.0) :
        self.fig = fig
        self.fig_dpi = fig.dpi if fig is not None else None

        self.unit = unit
        """长度的单位"""

        self.value = value
        """长度在当前单位下的数值"""

    def __float__(self) -> float:
        return float(self.value)

    def __int__(self) -> int:
        return int(self.value)

    def __repr__(self) -> str:
        return f"Length({self.value:.4g} {self.unit.value})"

    def _handle_input(self, other: LengthOrNumber) -> Number:
        if isinstance(other, Length):
            return other._to_unit(self.unit).value
        elif isinstance(other, (int, float)):
            return other
        else:
            raise TypeError(f"Length can only operate / compare with another Length"
                            f"or a number, not {type(other)}.")

    def _copy_with_value(self, value: Number) -> "Length":
        """复制当前 Length 实例，但使用新的值。"""
        return Length(self.fig, self.unit, value)

    def _get_plt_figure(self):
        """获取 figure 示例给 fig_x, fig_y, ax_x, ax_y 单位使用。"""
        if self.fig is not None:
            return
        if len(plt.get_fignums()) > 0:
            self.fig = plt.gcf()
            self.fig_dpi = self.fig.dpi
        else:
            raise ValueError("No figure available in pyplot.")

    # operations
    def __add__(self, other: LengthOrNumber) -> "Length":
        if isinstance(other, Length):
            return self._copy_with_value(self.value +
                                         other._to_unit(self.unit).value)
        elif isinstance(other, (int, float)):
            return self._copy_with_value(self.value + other)
        else:
            try:
                return self.value + other
            except Exception:
                raise TypeError(f"Length can only be added to another Length"
                                f"or a number, not {type(other)}.")

    def __radd__(self, other: LengthOrNumber) -> "Length":
        return self.__add__(other)

    def __sub__(self, other: LengthOrNumber) -> "Length":
        if isinstance(other, Length):
            return self._copy_with_value(self.value -
                                         other._to_unit(self.unit).value)
        elif isinstance(other, (int, float)):
            return self._copy_with_value(self.value - other)
        else:
            try:
                return self.value - other
            except Exception:
                raise TypeError(f"Length can only be subtracted by another Length"
                                f"or a number, not {type(other)}.")

    def __rsub__(self, other: LengthOrNumber) -> "Length":
        if isinstance(other, Length):
            return other._copy_with_value(
                other.value - self._to_unit(other.unit).value)
        elif isinstance(other, (int, float)):
            return self._copy_with_value(other - self.value)
        else:
            try:
                return other - self.value
            except Exception:
                raise TypeError(f"Length can only be subtract another Length"
                                f"or a number, not {type(other)}.")

    def __mul__(self, other: Number) -> "Length":
        if isinstance(other, (int, float)):
            return Length(self.fig, self.unit, self.value * other)
        elif isinstance(other, Length):
            raise TypeError("Length can only be multiplied by a number, "
                            f"not Length.")
        else:
            try:
                return self.value * other
            except Exception:
                raise TypeError("Length can only be multiplied by a number, "
                                f"not {type(other)}.")

    def __rmul__(self, other: Number) -> "Length":
        return self.__mul__(other)

    def __truediv__(self, other: LengthOrNumber) -> "Length":
        if isinstance(other, Length):
            warnings.warn(
                "Dividing Length by Length will return a dimensionless float "
                "number, not a Length instance.", UserWarning
            )
            other_converted = other._to_unit(self.unit)
            return self.value / other_converted.value
        elif isinstance(other, (int, float)):
            return self._copy_with_value(self.value / other)
        else:
            try:
                return self.value / other
            except Exception:
                raise TypeError(f"Length can only be divided by another Length "
                                f"or a number, not {type(other)}.")

    def __rturediv__(self, other: Number) -> "Length":
        if isinstance(other, (int, float)):
            warnings.warn(
                "Dividing a number by Length will return a dimensionless float "
                "number, not a Length instance.", UserWarning
            )
            return other / self.value
        else:
            try:
                return other / self.value
            except Exception:
                raise TypeError(f"Type {type(other)} cannot be divided by Length.")

    def __neg__(self) -> "Length":
        return self._copy_with_value(-self.value)

    def __abs__(self) -> "Length":
        return self._copy_with_value(abs(self.value))

    # compare methods
    def __lt__(self, other: LengthOrNumber) -> bool:
        return self.value < self._handle_input(other)

    def __le__(self, other: LengthOrNumber) -> bool:
        return self.value <= self._handle_input(other)

    def __gt__(self, other: LengthOrNumber) -> bool:
        return self.value > self._handle_input(other)

    def __ge__(self, other: LengthOrNumber) -> bool:
        return self.value >= self._handle_input(other)

    def __eq__(self, other: LengthOrNumber) -> bool:
        return self.value == self._handle_input(other)

    def __ne__(self, other: LengthOrNumber) -> bool:
        return self.value != self._handle_input(other)


    def __call__(self, value: Number) -> "Length":
        """设置长度在当前单位下的值。

        Parameters
        ----------
        value : Number
            新的长度值

        Returns
        -------
        Length
            新的相同单位、新的长度值的 Length 实例
        """
        return self._copy_with_value(value)


    @property
    def _fig_size_inch(self) -> tuple[float, float]:
        """获取当前 Figure 的尺寸，单位为英寸。"""
        self._get_plt_figure()
        return self.fig.get_size_inches()

    def _axes_size_inch(self, axes: Axes = None) -> tuple[float, float]:
        """获取当前 Axes 的尺寸，单位为英寸。"""
        self._get_plt_figure()
        if axes is None:
            axes = self.fig.gca()
        bbox = axes.get_position()
        fig_width_inch, fig_height_inch = self._fig_size_inch
        ax_width_inch = bbox.width * fig_width_inch
        ax_height_inch = bbox.height * fig_height_inch
        return (ax_width_inch, ax_height_inch)


    def _as_inch(self, axes: Axes = None, fontsize_pt: float = None) -> float:
        """将当前长度转换为英寸时的数值。"""
        match self.unit:
            case LengthUnit.INCH:
                return self.value
            case LengthUnit.MM:
                return self.value / 25.4
            case LengthUnit.PT:
                return self.value / 72.0
            case LengthUnit.PX:
                self._get_plt_figure()
                return self.value / self.fig_dpi
            case LengthUnit.FIG_X:
                self._get_plt_figure()
                return self.value * self._fig_size_inch[0]
            case LengthUnit.FIG_Y:
                self._get_plt_figure()
                return self.value * self._fig_size_inch[1]
            case LengthUnit.AX_X:
                self._get_plt_figure()
                return self.value * self._axes_size_inch(axes)[0]
            case LengthUnit.AX_Y:
                self._get_plt_figure()
                return self.value * self._axes_size_inch(axes)[1]
            case LengthUnit.EM:
                if fontsize_pt is None:
                    fontsize_pt = plt.rcParams['font.size']
                return self.value * fontsize_pt / 72.0
            case _:
                raise ValueError(f"Unsupported length unit: {self.unit}")

    def _to_unit(self, target_unit: LengthUnit, axes: Axes = None,
                 fontsize_pt: float = None) -> "Length":
        """将当前长度转换为指定单位的长度。"""
        inch_value = self._as_inch(axes, fontsize_pt)
        match target_unit:
            case LengthUnit.INCH:
                return Length(self.fig, LengthUnit.INCH, inch_value)
            case LengthUnit.MM:
                mm_value = inch_value * 25.4
                return Length(self.fig, LengthUnit.MM, mm_value)
            case LengthUnit.PT:
                pt_value = inch_value * 72.0
                return Length(self.fig, LengthUnit.PT, pt_value)
            case LengthUnit.PX:
                self._get_plt_figure()
                px_value = inch_value * self.fig_dpi
                return Length(self.fig, LengthUnit.PX, px_value)
            case LengthUnit.FIG_X:
                self._get_plt_figure()
                fig_width_inch = self._fig_size_inch[0]
                fig_x_value = inch_value / fig_width_inch
                return Length(self.fig, LengthUnit.FIG_X, fig_x_value)
            case LengthUnit.FIG_Y:
                self._get_plt_figure()
                fig_height_inch = self._fig_size_inch[1]
                fig_y_value = inch_value / fig_height_inch
                return Length(self.fig, LengthUnit.FIG_Y, fig_y_value)
            case LengthUnit.AX_X:
                self._get_plt_figure()
                ax_width_inch = self._axes_size_inch(axes)[0]
                ax_x_value = inch_value / ax_width_inch
                return Length(self.fig, LengthUnit.AX_X, ax_x_value)
            case LengthUnit.AX_Y:
                self._get_plt_figure()
                ax_height_inch = self._axes_size_inch(axes)[1]
                ax_y_value = inch_value / ax_height_inch
                return Length(self.fig, LengthUnit.AX_Y, ax_y_value)
            case LengthUnit.EM:
                if fontsize_pt is None:
                    fontsize_pt = plt.rcParams['font.size']
                em_value = inch_value * 72.0 / fontsize_pt
                return Length(self.fig, LengthUnit.EM, em_value)
            case _:
                raise ValueError(f"Unsupported target length unit: {target_unit}")

    def to_inch(self, fontsize_pt: float = None) -> "Length":
        """转换为英寸单位的长度。"""
        return self._to_unit(LengthUnit.INCH, fontsize_pt=fontsize_pt)

    def to_mm(self, fontsize_pt: float = None) -> "Length":
        """转换为毫米单位的长度。"""
        return self._to_unit(LengthUnit.MM, fontsize_pt=fontsize_pt)

    def to_pt(self, fontsize_pt: float = None) -> "Length":
        """转换为磅(pt)单位的长度。"""
        return self._to_unit(LengthUnit.PT, fontsize_pt=fontsize_pt)

    def to_px(self, fontsize_pt: float = None) -> "Length":
        """转换为像素(px)单位的长度。"""
        return self._to_unit(LengthUnit.PX, fontsize_pt=fontsize_pt)

    def to_fig_x(self, fontsize_pt: float = None) -> "Length":
        """转换为相对于 Figure 宽度的长度。"""
        return self._to_unit(LengthUnit.FIG_X, fontsize_pt=fontsize_pt)

    def to_fig_y(self, fontsize_pt: float = None) -> "Length":
        """转换为相对于 Figure 高度的长度。"""
        return self._to_unit(LengthUnit.FIG_Y, fontsize_pt=fontsize_pt)

    def to_ax_x(self, axes: Axes = None, fontsize_pt: float = None) -> "Length":
        """转换为相对于 Axes 宽度的长度。"""
        return self._to_unit(LengthUnit.AX_X, axes, fontsize_pt=fontsize_pt)

    def to_ax_y(self, axes: Axes = None, fontsize_pt: float = None) -> "Length":
        """转换为相对于 Axes 高度的长度。"""
        return self._to_unit(LengthUnit.AX_Y, axes, fontsize_pt=fontsize_pt)

    def to_em(self, fontsize_pt: float=None) -> "Length":
        """转换为 em 单位的长度。"""
        return self._to_unit(LengthUnit.EM, fontsize_pt=fontsize_pt)



class MoiFigureUnits:
    def __init__(self, fig: Figure):
        self.fig = fig

    @property
    def inch(self):
        """获取一个英寸单位的长度。"""
        return Length(self.fig, LengthUnit.INCH, 1.0)

    @property
    def mm(self):
        """获取一个毫米单位的长度。"""
        return Length(self.fig, LengthUnit.MM, 1.0)

    @property
    def pt(self):
        """获取一个磅(pt)单位的长度。"""
        return Length(self.fig, LengthUnit.PT, 1.0)

    @property
    def px(self):
        """获取一个像素(px)单位的长度。"""
        return Length(self.fig, LengthUnit.PX, 1.0)

    @property
    def fig_x(self):
        """获取一个相对于 Figure 宽度的长度。"""
        return Length(self.fig, LengthUnit.FIG_X, 1.0)

    @property
    def fig_y(self):
        """获取一个相对于 Figure 高度的长度。"""
        return Length(self.fig, LengthUnit.FIG_Y, 1.0)

    @property
    def ax_x(self):
        """获取一个相对于 Axes 宽度的长度。"""
        return Length(self.fig, LengthUnit.AX_X, 1.0)

    @property
    def ax_y(self):
        """获取一个相对于 Axes 高度的长度。"""
        return Length(self.fig, LengthUnit.AX_Y, 1.0)

    @property
    def em(self):
        """获取一个字体大小(em)的长度，使用 plt.rcParams['font.size'] 的值为 1em。"""
        return Length(self.fig, LengthUnit.EM, 1.0)


def as_unit(*lengths: LengthOrNumber | None, fig: Figure, unit: LengthUnit | Length,
            return_value: bool = False
            ) -> list[Length] | Length | list[float] | float | None:
    """将多个长度/数字转换为指定单位的长度，如果是数字则视为当前单位下的长度值。

    Parameters
    ----------
    *lengths : LengthOrNumber
        要转换的长度，可以是 Length 实例或数字
    fig : Figure
        所属的 Figure 实例
    unit : LengthUnit | Length
        目标单位，如果是一个 Length 实例，则使用其单位
    return_value : bool, optional
        是否返回长度的数值而不是 Length 实例, by default False

    Returns
    -------
    list[Length] | Length | list[float] | float
        转换后的长度或长度列表
    """
    converted_lengths = []
    if isinstance(unit, Length):
        unit = unit.unit

    for length in lengths:
        if length is None:
            converted_lengths.append(None)
        elif isinstance(length, Length):
            converted_length = length._to_unit(unit)
            if return_value:
                converted_length = converted_length.value
            converted_lengths.append(converted_length)
        elif isinstance(length, (int, float)):
            if return_value:
                converted_lengths.append(length)
            else:
                converted_lengths.append(Length(fig, unit, length))
        else:
            raise TypeError(f"Unsupported type for length conversion: "
                            f"{type(length)}.")

    if len(converted_lengths) == 1:
        return converted_lengths[0]
    else:
        return converted_lengths


class Inch(Length):
    """英寸单位的长度。"""
    def __init__(self, value: Number, fig: Figure = None):
        super().__init__(fig, LengthUnit.INCH, value)


class Pt(Length):
    """磅(pt)单位的长度。"""
    def __init__(self, value: Number, fig: Figure = None):
        super().__init__(fig, LengthUnit.PT, value)

class Mm(Length):
    """毫米单位的长度。"""
    def __init__(self, value: Number, fig: Figure = None):
        super().__init__(fig, LengthUnit.MM, value)

class Px(Length):
    """像素(px)单位的长度。"""
    def __init__(self, value: Number, fig: Figure = None):
        super().__init__(fig, LengthUnit.PX, value)

class Em(Length):
    """em单位的长度。"""
    def __init__(self, value: Number, fig: Figure = None):
        super().__init__(fig, LengthUnit.EM, value)
