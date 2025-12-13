"""
用于直接面向用户使用的接口函数。
"""

import matplotlib.pyplot as plt
from .moi_figure import MoiFigure

def figure(**kwargs) -> MoiFigure:
    """像 plt.figure() 一样，创建一个 MoiFigure 实例。
    等价于 `plt.figure(FigureClass=MoiFigure, **kwargs)`。

    Parameters
    ----------
    kwargs : dict
        传递给 matplotlib.figure.Figure 的参数

    Returns
    -------
    MoiFigure
        创建的 MoiFigure 实例

    """
    # 确保使用 MoiFigure 作为 FigureClass
    kwargs.update({"FigureClass": MoiFigure})

    return plt.figure(**kwargs)
