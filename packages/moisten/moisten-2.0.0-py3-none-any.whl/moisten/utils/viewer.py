from rich.console import Console, Group
from rich.panel import Panel
from rich.columns import Columns
import numpy as np
from dataclasses import dataclass
import inspect
from xarray import DataArray, Dataset
from xarray.core.coordinates import DataArrayCoordinates
from rich.table import Table
from rich.padding import Padding
from rich.tree import Tree
from pathlib import Path
from matplotlib.colors import Colormap

TB = "│"
CONSOLE = Console()

def format_datetime(dt: np.datetime64) -> str:
    """格式化 datetime64"""
    if dt is None:
        return "None"
    elif isinstance(dt, np.datetime64):
        return dt.astype('datetime64[ms]').item().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return str(dt)

@dataclass
class ViewerStyle:
    keyword: str = "bright_cyan"
    type: str = "magenta"
    value: str = "default"
    number: str = "green not bold"
    title: str = "blue"
    warning: str = "orange1"
    url: str = "not bold not italic underline bright_blue"

    def __call__(self, style: str, text: str, bold: bool = False) -> str:
        """根据样式名称返回对应的样式
        """
        # 获取自身的属性
        attr = getattr(self, style, None)
        if attr is None:
            raise ValueError(f"Invalid style: {style}")

        if bold:
            return f"[bold {attr}]{text}[/bold {attr}]"
        else:
            return f"[{attr}]{text}[/{attr}]"


class Viewer:
    """
    美化 Numpy 与 Xarray 的打印输出的包装器。

    A warapping class for beautifying the print output of Numpy and Xarray.
    """

    def __init__(self, *args, style: ViewerStyle = ViewerStyle(),
                 lineno: bool = True):
        """
        打印任意内容，支持美化 numpy 和 xarray 的打印输出。

        Print any content, supports beautifying the print output of
        numpy and xarray.

        Usage
        -----
        ``` python
        data = np.array([1, 2, 3])

        # 直接使用
        Viewer(data)

        # 或实例化
        v = Viewer()
        v(data)
        ```

        Parameters
        ----------
        *args : any
            需要打印的内容，可以是任意数量的参数。

            The content to be printed, can be any number of parameters.
        style : ViewerStyle, optional
            打印内容的样式，默认为 ViewerStyle()。

            The style to be used for printing, by default ViewerStyle()
        lineno : bool, optional
            是否显示文件与行号，默认为 True。

            Whether to display the file and line number, by default True.
        """

        self.s = style
        self.lineno = lineno
        self.call_frame = inspect.currentframe().f_back
        self.xr_viewer = XrViewer(style)
        self.np_viewer = NpViewer(style)

        for arg in args:
            CONSOLE.print(self._print(arg))


    def view(self, *args):
        self.call_frame = inspect.currentframe().f_back
        for arg in args:
            CONSOLE.print(self._print(arg))


    def __call__(self, *args):
        self.call_frame = inspect.currentframe().f_back
        for arg in args:
            CONSOLE.print(self._print(arg))


    def _get_var_name(self, arg) -> str | None:
        """获取变量名"""
        var_name = None
        local_vars = self.call_frame.f_locals
        for name, value in local_vars.items():
            if value is arg:
                var_name = name
                break
        return var_name


    def _get_line_number(self) -> int:
        """获取调用行号"""
        info = inspect.getframeinfo(self.call_frame)
        file_name = Path(info.filename).name
        return f"{file_name}:{info.lineno}"


    def _print(self, v: any):
        """打印信息"""
        name = self._get_var_name(v)
        var_title = ""
        if self.lineno:
            var_title += f"{self.s('number', self._get_line_number())} "
        var_title += f"{self.s('type', f'<{type(v).__name__}>')}"

        if name is not None:
            var_title += f" {self.s('keyword', self._get_var_name(v), True)}:"

        if isinstance(v, np.ndarray):
            var_info, array = self.np_viewer.print_ndarray(v)
            return Group(f"{var_title} {var_info}", Padding(array, (0,0,0,2)))
        elif isinstance(v, DataArray):
            return self.xr_viewer.print_dataarray(v, var_title.strip(":"))
        elif isinstance(v, Dataset):
            return self.xr_viewer.print_dataset(v, var_title.strip(":"))
        else:
            var_info = str(v)
            return Columns([var_title, var_info])


    def _insert_str(origin: str, insertList: list[str],
                    insertIndexList: list[int]) -> str:
        """插入字符串
        """
        for i in range(len(insertList)):
            strLen = len(insertList[i])
            if insertIndexList[i] == 0:
                origin = insertList[i] + origin[strLen:]
            elif insertIndexList[i] == len(origin) - 1:
                origin = origin[:-strLen] + insertList[i]
            else:
                halfLen = strLen // 2
                if strLen % 2 == 0:
                    origin = origin[:insertIndexList[i]-halfLen] + \
                        insertList[i] + origin[insertIndexList[i]+halfLen:]
                else:
                    origin = origin[:insertIndexList[i]-halfLen] + \
                        insertList[i] + origin[insertIndexList[i]+halfLen+1:]
        return origin


    @staticmethod
    def pcolor(data: np.ndarray | DataArray,
                x: np.ndarray | DataArray | str = None,
                y: np.ndarray | DataArray | str = None,
                cmap: str | Colormap=None, tick_num=5,
                colorbar_tick_num=5, zero_center=None):
        """在终端中显示2D数据的伪彩色图，类似 matplotlib 的 pcolor。

        Parameters
        ----------
        data : np.ndarray | DataArray
            2D的数据，支持 numpy ndarray 和 xarray DataArray。
        x, y : np.ndarray | DataArray | str, optional
            数据的 x, y 坐标，如果数据是 DataArray，
            可以自动识别或使用字符串指定坐标名称。
        cmap : str | Colormap, optional
            填色使用的 matplotlib 的 colormap，可以使用字符串指定 colormap 名称。
            默认自动选择。
        tick_num : int, optional
            坐标刻度的数量，默认为 5
        colorbar_tick_num : int, optional
            colorbar 刻度的数量，默认为 5
        zero_center : _type_, optional
            填色是否以 0 为中心正负对称，默认为 None，
            如果为 None，则根据数据自动判断是否需要。

        """

        PColorViewer.pcolor(data, x=x, y=y, cmap=cmap,
                            tick_num=tick_num,
                            colorbar_tick_num=colorbar_tick_num,
                            zero_center=zero_center)



class XrViewer:
    """xarray head info viewer"""

    def __init__(self, style: ViewerStyle):
        self.s = style


    @staticmethod
    def _format_bytes(size: int) -> str:
        """格式化字节数
        """
        if size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size/1024:.2f} KB"
        elif size < 1024**3:
            return f"{size/1024**2:.2f} MB"
        else:
            return f"{size/1024**3:.2f} GB"


    @staticmethod
    def _datetime64_format(t: np.datetime64) -> str:
        """格式化datetime64
        """
        if t is None:
            return "None"
        elif isinstance(t, np.datetime64):
            return t.astype('datetime64[ms]').item().strftime("%Y-%m-%d %H:%M:%S")
        else:
            return str(t)


    def _xr_coords(self, coord: DataArrayCoordinates, title=True) -> Table:
        """打印xarray的维度信息"""
        table = Table(show_edge=False, show_lines=False,
                      show_header=False, show_footer=False,
                      title_justify='left', title_style=self.s.title)
        table.add_column("index", style=self.s.number + " i")
        table.add_column("name", style=self.s.keyword)
        table.add_column("type", style=self.s.type)
        table.add_column("size", style=self.s.number)
        table.add_column("values",)

        if title:
            table.title = ":compass: Coordinates (index, name, type, size, values)"

        for index, key in enumerate(coord.dims):
            c = coord[key]
            table.add_row(
                str(index), str(key), str(c.dtype), str(c.size),
                np.array2string(c.values, precision=2, suppress_small=True,
                                threshold=4, edgeitems=2, max_line_width=50,
                                formatter={"datetime": self._datetime64_format}
                                ).strip("[]")
            )
        return table

    def _xr_attrs(self, attrs: dict) -> Table:
        """打印属性信息"""
        attrsTable = Table(title= ":memo: Attributes (name, value)",
                            show_edge=False, show_lines=False,
                            show_header=False, show_footer=False,
                            title_style=self.s.title, title_justify="left")

        attrsTable.add_column("name", style=self.s.keyword, justify='right')
        attrsTable.add_column("value", justify='left')

        for key in attrs.keys():
            attrsTable.add_row(key, str(attrs[key]))
        return attrsTable


    def _xr_variable(self, data: DataArray) -> Table:
        """打印xarray变量信息"""
        coords = data.coords
        coords_text = []

        for key in coords.keys():
            coords_text.append(f"{key}: {self.s('number', coords[key].size)}")
        if len(coords_text) > 0:
            coords_text = " (" + ", ".join(coords_text) + ")"
        else:
            coords_text = ""

        tree = Tree(f":package: {self.s('keyword', data.name, True)}{coords_text}",)

        long_name = data.attrs.get("long_name", False)
        std_name = data.attrs.get("standard_name", False)
        description = data.attrs.get("description", False)
        desc = long_name or std_name or description
        unit = data.attrs.get("units", False)
        if desc and unit:
            desc = f"{desc} ({unit})"
        elif desc:
            desc = f"{desc}"
        elif unit:
            desc = f"units: {unit}"
        if desc:
            tree.add(self.s('title', desc))

        size = data.size * data.dtype.itemsize
        compress = data.encoding.get("complevel", 0)
        tree.add(
            f"Mem:{self.s('type', data.dtype)} {self._format_bytes(size)} "
            f"| Encoding: {self.s('type', data.encoding.get('dtype', ''))} "
            f"(complevel: {compress})"
        )
        return tree


    def print_dataarray(self, data: DataArray, title: str) -> Group:
        """美化打印 xarray DataArray 的信息"""
        source = data.encoding.get("source", "")
        coords = data.coords
        coords_text = []

        for key in coords.keys():
            coords_text.append(f"{key}: {self.s('number', coords[key].size)}")
        if len(coords_text) > 0:
            coords_text = " (" + ", ".join(coords_text) + ")"
        else:
            coords_text = ""

        tree = Tree(f":package: {self.s('keyword', data.name, True)}{coords_text}",)

        size = data.size * data.dtype.itemsize
        compress = data.encoding.get("complevel", 0)
        info = Tree(":information: Information", style=self.s.title)
        info.add(
            f"[default]Mem:{self.s('type', data.dtype)} {self._format_bytes(size)} "
            f"| Encoding: {self.s('type', data.encoding.get('dtype', ''))} "
            f"(complevel: {compress})" +
            (f"\nSource: {self.s('url', source)}" if source else "") + "[/default]"
        )
        tree.add(Padding(info, (0, 0, 1, 0)))
        tree.add(Padding(self._xr_coords(data.coords), (0, 0, 1, 0)))
        tree.add(self._xr_attrs(data.attrs))
        panel = Panel( tree, title=title, style="on black", title_align="left",)
        return panel


    def print_dataset(self, data: Dataset, title: str, subtitle="") -> Group:
        """美化打印 xarray Dataset 的信息"""
        source = data.encoding.get("source", "")
        if source != "":
            try:
                file_size = Path(source).stat().st_size
                source = f"{self.s('url', source)} ({self._format_bytes(file_size)})"
            except FileNotFoundError:
                source = f"{self.s('url', source)}"
        else:
            source = "<unknown source or in memory>"
        tree = Tree(f":truck: {source}\n{TB}")

        # variables
        for key in data.data_vars.keys():
            tree.add(Padding(self._xr_variable(data[key]), (0, 0, 1, 0)))

        # dimensions
        tree.add(Padding(self._xr_coords(data.coords), (0, 0, 1, 0)))

        # attributes
        tree.add(self._xr_attrs(data.attrs))

        panel = Panel(
            tree, title=title, style="on black",
            subtitle=subtitle, title_align="left",
        )
        return panel


class NpViewer:
    """numpy info viewer"""

    def __init__(self, style: ViewerStyle):
        self.s = style

    @staticmethod
    def _format_bytes(size: int) -> str:
        """格式化字节数
        """
        if size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size/1024:.2f} KB"
        elif size < 1024**3:
            return f"{size/1024**2:.2f} MB"
        else:
            return f"{size/1024**3:.2f} GB"


    def print_ndarray(self, data: np.ndarray):
        """打印ndarray的简要信息
        """
        info = f"{self.s('warning', data.shape)} " + \
                f"{self.s('type', data.dtype)} " + \
                f"({self._format_bytes(data.itemsize * data.size)})"
        edgeitems = 3 if data.ndim < 3 else 2
        array = np.array2string(data, max_line_width=CONSOLE.width-2,
                                edgeitems=edgeitems,
                                formatter={'float': '{:<9.4g}'.format})
        return info, array



class PColorViewer:

    @staticmethod
    def pcolor(data: np.ndarray | DataArray,
                x: np.ndarray | DataArray | str = None,
                y: np.ndarray | DataArray | str = None,
                cmap: str | Colormap=None, tick_num=5,
                colorbar_tick_num=5, zero_center=None):
        """在终端中显示2D数据的伪彩色图，类似 matplotlib 的 pcolor。

        Parameters
        ----------
        data : np.ndarray | DataArray
            2D的数据，支持 numpy ndarray 和 xarray DataArray。
        x, y : np.ndarray | DataArray | str, optional
            数据的 x, y 坐标，如果数据是 DataArray，
            可以自动识别或使用字符串指定坐标名称。
        cmap : str | Colormap, optional
            填色使用的 matplotlib 的 colormap，可以使用字符串指定 colormap 名称。
            默认自动选择。
        tick_num : int, optional
            坐标刻度的数量，默认为 5
        colorbar_tick_num : int, optional
            colorbar 刻度的数量，默认为 5
        zero_center : _type_, optional
            填色是否以 0 为中心正负对称，默认为 None，
            如果为 None，则根据数据自动判断是否需要。

        """

        if not isinstance(data, (np.ndarray, DataArray)):
            try:
                data = np.array(data)
            except Exception as e:
                raise TypeError("failed to convert data to ndarray") from e

        # 检查数据是否为2D
        if len(data.shape) != 2:
            raise ValueError(f"pcolor only supports 2D data, "
                             f"but got {len(data.shape)}D data")

        # 处理 x 和 y 坐标
        if isinstance(x, str):
            if not isinstance(data, DataArray):
                raise TypeError("if x is str, data must be DataArray")
            if x in data.coords:
                x = data.coords[x].values
            else:
                raise ValueError(f"x coordinate '{x}' not found in data coords")
        elif isinstance(x, DataArray):
            x = x.values
        elif x is None:
            if isinstance(data, DataArray):
                x = data.coords[data.dims[-1]].values
            else:
                x = np.arange(data.shape[1])
        else:
            try:
                x = np.array(x)
            except Exception as e:
                raise TypeError("failed to convert x to ndarray") from e

        if isinstance(y, str):
            if not isinstance(data, DataArray):
                raise TypeError("if y is str, data must be DataArray")
            if y in data.coords:
                y = data.coords[y].values
            else:
                raise ValueError(f"y coordinate '{y}' not found in data coords")
        elif isinstance(y, DataArray):
            y = y.values
        elif y is None:
            if isinstance(data, DataArray):
                y = data.coords[data.dims[-2]].values
            else:
                y = np.arange(data.shape[0])
        else:
            try:
                y = np.array(y)
            except Exception as e:
                raise TypeError("failed to convert y to ndarray") from e

        # 检查坐标是否匹配
        if len(x) != data.shape[1] or len(y) != data.shape[0]:
            raise ValueError(f"the length of x and y must match the shape of data,"
                             f" but got x: {len(x)}, y: {len(y)}, "
                             f"data shape: {data.shape}")

        # 检查坐标必须是单调递增或递减
        if not (np.all(np.diff(x) > 0) or np.all(np.diff(x) < 0)):
            raise ValueError("x coordinate must be monotonically increasing "
                             "or decreasing")
        if not (np.all(np.diff(y) > 0) or np.all(np.diff(y) < 0)):
            raise ValueError("y coordinate must be monotonically increasing "
                             "or decreasing")

        if isinstance(data, DataArray):
            name = data.attrs.get("long_name", data.name or "DataArray")
            unit = data.attrs.get("units", "")
        else:
            name = "Value"
            unit = ""

        # 终端画图
        from matplotlib.cm import get_cmap

        # y宽度标签如果是数字，则 :8.3g，如果是时间，则 YYYY-MM-DD HH:MM:SS
        if y.dtype.kind == 'M':
            ytick_width = 24
        else:
            ytick_width = 13

        if x.dtype.kind == 'M':
            xtick_width = 24
        else:
            xtick_width = 13 + 1

        fig_width = CONSOLE.width - ytick_width

        # 缩放
        if data.shape[1] > fig_width:
            scale = fig_width / data.shape[1]
            fig_height = int(data.shape[0] * scale)
            x_index = np.linspace(0, data.shape[1]-1, fig_width, dtype=int,)
            y_index = np.linspace(0, data.shape[0]-1, fig_height, dtype=int,)
            render_data = data[y_index, :][:, x_index]
        else:
            scale = 1.0
            fig_width = data.shape[1]
            fig_height = data.shape[0]
            render_data = data
            x_index = np.arange(data.shape[1])
            y_index = np.arange(data.shape[0])

        # 实际渲染的行数，一行两个像素高
        render_rows = fig_height // 2 if fig_height % 2 == 0 else (fig_height // 2 + 1)

        # 如果宽度小于刻度数量*刻度宽度，则减少刻度数量
        if fig_width < xtick_width * tick_num + (tick_num - 1):
            x_tick_num = max(2, fig_width // (xtick_width + 1))
        else:
            x_tick_num = tick_num
        if render_rows < tick_num:
            y_tick_num = render_rows
        else:
            y_tick_num = tick_num

        # 选择 y ticks
        ytick_slots = ['' for _ in range(render_rows)]
        ytick_indices = np.linspace(0, len(y_index)-1, y_tick_num, dtype=int)
        for yi in ytick_indices:
            if y.dtype.kind == 'M':
                ytick_slots[yi//2] = "─" + format_datetime(y[y_index[yi]])
            else:
                ytick_slots[yi//2] = f"─ {y[y_index[yi]]:<8.3g}"

        # 处理渲染数据
        data_max = np.nanmax(render_data)
        data_min = np.nanmin(render_data)
        data_mid = np.nanmedian(render_data)

        # 自动识别是否需要以0为中心
        if zero_center is None:
            if data_min < 0 and data_max > 0 and \
                np.abs(data_max+data_min) / ((data_max-data_min) / 2) < 0.3:
                zero_center = True

        if zero_center:
            the_max = np.max([np.abs(data_max), np.abs(data_min)])
            render_max = the_max
            render_min = -the_max
        else:
            render_max = data_max
            render_min = data_min

        if cmap is None:
            if zero_center:
                cmap = 'RdBu_r'
            else:
                cmap = 'turbo'

        cmap = get_cmap(cmap)

        # to 0-1
        render_data = (render_data - render_min) / (render_max - render_min)
        render_text = ""

        # 画图
        def get_color(value):
            if np.isnan(value):
                return 'black'
            c = cmap(value)[:3]
            return f"rgb({int(c[0]*255)},{int(c[1]*255)},{int(c[2]*255)})"

        for r_row in range(render_rows):
            for col in range(fig_width):
                c = get_color(render_data[r_row*2, col])
                if r_row*2+1 >= fig_height:
                    render_text += f"[{c}]▀[/{c}]"
                else:
                    c1 = get_color(render_data[r_row*2+1, col])
                    render_text += f"[{c} on {c1}]▀[/{c} on {c1}]"
            render_text += ytick_slots[r_row]
            render_text += "\n"

        # x ticks
        xtick_indices = np.linspace(0, len(x_index)-1, x_tick_num, dtype=int)
        xtick_line = " " * fig_width
        xtick_text = " " * fig_width
        for i, xi in enumerate(xtick_indices):
            if x.dtype.kind == 'M':
                xtick_label = format_datetime(x[x_index[xi]])
            else:
                if i == 0:
                    xtick_label = f"{x[x_index[xi]]:<9.3g}"
                elif i == len(xtick_indices) - 1:
                    xtick_label = f"{x[x_index[xi]]:>9.3g}"
                else:
                    xtick_label = f"{x[x_index[xi]]:^9.3g}"

            if i == 0:
                xtick_text = xtick_label + xtick_text[len(xtick_label):]
                xtick_line = "|" + xtick_line[1:]
            elif i == len(xtick_indices) - 1:
                xtick_text = xtick_text[:-len(xtick_label)] + xtick_label
                xtick_line = xtick_line[:-1] + "|"
            else:
                pos = int(xi / (len(x_index)-1) * fig_width)
                t_len = len(xtick_label)
                if t_len % 2 == 0:
                    p_left = p_rigth = t_len // 2
                else:
                    p_left = t_len // 2
                    p_rigth = t_len // 2 + 1
                xtick_text = xtick_text[:pos-p_left] + xtick_label + \
                             xtick_text[pos+p_rigth:]
                xtick_line = xtick_line[:pos] + "|" + xtick_line[pos+1:]

        render_text += xtick_line + "\n" + xtick_text + "\n"

        # colorbar
        colorbar_values = np.linspace(0, 1, fig_width)
        colorbar_rendertxt = ""
        for cv in colorbar_values:
            c = cmap(cv)[:3]
            c = f"rgb({int(c[0]*255)},{int(c[1]*255)},{int(c[2]*255)})"
            colorbar_rendertxt += f"[{c}]█[/{c}]"

        # colorbar ticks
        if colorbar_tick_num * 9 + (colorbar_tick_num - 1) > fig_width:
            colorbar_tick_num = max(2, fig_width // 10)
        colorbar_tick_values = np.linspace(render_min, render_max, colorbar_tick_num)
        colorbar_tick_line = " " * fig_width
        colorbar_tick_text = " " * fig_width
        for i, cv in enumerate(colorbar_tick_values):
            if i == 0:
                tick_label = f"{cv:<9.3g}"
            elif i == len(colorbar_tick_values) - 1:
                tick_label = f"{cv:>9.3g}"
            else:
                tick_label = f"{cv:^9.3g}"

            if i == 0:
                colorbar_tick_text = tick_label + colorbar_tick_text[len(tick_label):]
                colorbar_tick_line = "|" + colorbar_tick_line[1:]
            elif i == len(colorbar_tick_values) - 1:
                colorbar_tick_text = colorbar_tick_text[:-len(tick_label)] + tick_label
                colorbar_tick_line = colorbar_tick_line[:-1] + "|"
            else:
                pos = int(i / (len(colorbar_tick_values)-1) * fig_width)
                t_len = len(tick_label)
                if t_len % 2 == 0:
                    p_left = p_rigth = t_len // 2
                else:
                    p_left = t_len // 2
                    p_rigth = t_len // 2 + 1
                colorbar_tick_text = colorbar_tick_text[:pos-p_left] + tick_label + \
                                colorbar_tick_text[pos+p_rigth:]
                colorbar_tick_line = colorbar_tick_line[:pos] + "|" + \
                                colorbar_tick_line[pos+1:]

        render_text += "\n" +colorbar_rendertxt + "\n" + colorbar_tick_line + \
            "\n" + colorbar_tick_text

        # colorbar_label
        if unit:
            if len(unit) > fig_width:
                unit = unit[:fig_width]
            if len(unit) % 2 == 0:
                p_left = p_rigth = len(unit) // 2
            else:
                p_left = len(unit) // 2
                p_rigth = len(unit) // 2 + 1
            colorbar_label = " " * fig_width
            colorbar_label = colorbar_label[:fig_width//2 - p_left] + \
                            unit + \
                            colorbar_label[fig_width//2 + p_rigth:]

            render_text += "\n" + colorbar_label

        # 底部信息
        info_text = f"[green]Max:[/green] [bold]{data_max:.4g}[/bold], "\
                    f"[green]Min:[/green] [bold]{data_min:.4g}[/bold], "\
                    f"[green]Mid:[/green] [bold]{data_mid:.4g}[/bold]"

        panel = Panel.fit(render_text, title=f"[cyan]{name}[/cyan] "
                        f"({data.shape[1]}*{data.shape[0]}, zoom: {scale:.2f})",
                        style="on black", subtitle=info_text)
        CONSOLE.print(panel)