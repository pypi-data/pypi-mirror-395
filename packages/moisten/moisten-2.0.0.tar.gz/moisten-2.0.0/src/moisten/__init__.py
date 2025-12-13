from .utils.viewer import Viewer

pp = Viewer()
"""
与 print() 类似，打印任意内容，支持美化 numpy 和 xarray 的打印输出。

Print any content, supports beautifying the print output of
numpy and xarray.

Usage
-----
    >>> from moisten import pp
    >>> pp(your_data)
    >>> # or
    >>> import moisten as moi
    >>> moi.pp(your_data)

Parameters
----------
*args : any
需要打印的内容，可以是任意数量的变量。

style : ViewerStyle, optional
打印内容的样式，默认为 ViewerStyle()。

lineno : bool, optional
是否显示文件与行号，默认为 True。
"""

from .utils.timer import Timer
import moisten_ew as ew
import moisten_plot as plot

__version__ = "2.0.0"