from dataclasses import dataclass, asdict
from matplotlib import pyplot as plt

@dataclass
class SetRcParams:
    """
    rcParams 的配置类型。继承此类，使用下划线命名法来填写 rcParams 的配置，
    然后使用 apply() 方法应用到 plt.rcParams 中。

    例如设置 rcParams['font.size'] = 10.5，可令 font_size = 10.5
    """
    def _underscore_to_dot(self, name: str) -> str:
        """驼峰命名转换为点分割命名"""
        return name.replace('_', '.')

    def apply(self):
        """将对象中的属性应用到plt.rcParams中
        """
        for key, value in asdict(self).items():
            key = self._underscore_to_dot(key)
            plt.rcParams[key] = value


@dataclass
class MoiRcParams(SetRcParams):
    """Moisten 的默认配置，适用于A4印刷"""
    font_size: float = 10.5

    # 边框线宽
    axes_linewidth: float = 0.8

    # 刻度线宽
    xtick_major_width: float = 0.8
    ytick_major_width: float = 0.8
    xtick_minor_width: float = 0.6
    ytick_minor_width: float = 0.6

    # 刻度线长度
    xtick_major_size: float = 4
    ytick_major_size: float = 4
    xtick_minor_size: float = 2.5
    ytick_minor_size: float = 2.5

    # 刻度线标签间隔
    xtick_major_pad: float = 3
    ytick_major_pad: float = 3

    # 刻度线标签大小
    xtick_labelsize: float = font_size
    ytick_labelsize: float = font_size


