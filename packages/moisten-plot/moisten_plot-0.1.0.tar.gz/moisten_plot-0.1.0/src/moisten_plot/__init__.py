"""
moisten-plot: A module to improve matplotlib plot and make it easier to use. This is a part of moisten package series.
"""
from ._interface import *
from ._font_properties import FontStyle
from .axes_tools import AxesTools, SubplotParams
from .moiCmap import MoiCmap

MoiCmap.register_moi_cmap()