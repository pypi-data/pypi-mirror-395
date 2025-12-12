import ctypes
import json
import tkinter as tk
from tkinter import colorchooser, filedialog
from tkinter.scrolledtext import ScrolledText
from typing import Any, Callable, Literal, TypeVar, Union

_TkVar = TypeVar('_TkVar', bound=Union[tk.StringVar, tk.IntVar, tk.DoubleVar, tk.BooleanVar])


class BForm(tk.Tk):

    _rowIndex = -1
    _initHandlerList: list[Callable[..., None]] = []
    _varList: list[tk.Variable] = []  # 用于强制引用 var 否则没有引用回导致界面异常（可能是被回收了变量）
    _isCancel = False  # 是否取消操作（点击右上角按钮）

    def __init__(
        self,
        *,
        title: str = '',
        resiable: bool = False,
        miniWindow: bool = True,
    ):
        super().__init__()
        self.title(title)
        self.resizable(resiable, resiable)
        if miniWindow:
            self.addInitHandler(self._setMiniWindow)
        self.bind("<Map>", self._onInit)
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def _setMiniWindow(self):
        GWL_STYLE = -16
        WS_MINIMIZEBOX = 0x00020000
        WS_MAXIMIZEBOX = 0x00010000
        SWP_NOSIZE = 0x0001
        SWP_NOMOVE = 0x0002
        SWP_NOZORDER = 0x0004
        SWP_FRAMECHANGED = 0x0020
        self.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())

        # 获取原窗口样式
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)

        # 移除最大化、最小化按钮（保留关闭按钮）
        style &= ~WS_MAXIMIZEBOX
        style &= ~WS_MINIMIZEBOX

        # 设置新的窗口样式
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)

        # 强制刷新窗口，让样式生效
        ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0,
                                          SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

    def _onInit(self, evt: tk.Event):
        if evt.widget == self:
            for callback in self._initHandlerList:
                callback()
            self._initHandlerList.clear()

    def _initVar(self, var: _TkVar) -> _TkVar:
        self._varList.append(var)
        return var

    def _initFocus(self, widget: tk.Widget):
        self.addInitHandler(
            lambda: widget.focus_set()
        )

    def addInitHandler(self, handler: Callable[..., None]):
        self._initHandlerList.append(handler)

    def run(self) -> Any:
        self.center()
        self.mainloop()
        if self._isCancel:
            return None
        else:
            return self.getResult()

    def getResult(self) -> Any:
        return None

    def cancel(self):
        self._isCancel = True
        self.destroy()

    def center(self):
        self.withdraw()  # 先隐藏窗口，避免闪动
        self.update_idletasks()  # 确保获取正确的窗口尺寸
        width = self.winfo_width()  # 获取窗口宽度
        height = self.winfo_height()  # 获取窗口高度
        screen_width = self.winfo_screenwidth()  # 屏幕宽度
        screen_height = self.winfo_screenheight()  # 屏幕高度
        x = (screen_width - width) // 2  # 水平居中
        y = (screen_height - height) // 2  # 垂直居中
        self.geometry(f"+{x}+{y}")  # 设置窗口位置
        self.deiconify()  # 恢复显示窗口

    def addRow(self, desc: str, widget: tk.Widget, labelSticky: str = 'E', *, pady: int = 5):
        self._rowIndex += 1
        tk.Label(text=desc).grid(row=self._rowIndex, column=0, padx=10, pady=5, sticky=labelSticky)
        widget.grid(row=self._rowIndex, column=1, padx=10, pady=pady, sticky='W')

    def addRowFrame(self):
        self._rowIndex += 1
        frame = tk.Frame(self)
        frame.grid(row=self._rowIndex, column=0, columnspan=2, padx=10, pady=5)
        return frame

    def addRowFrameWithDesc(self, desc: str):
        self._rowIndex += 1
        tk.Label(text=desc).grid(row=self._rowIndex, column=0, padx=10, pady=5, sticky='e')
        frame = tk.Frame(self)
        frame.grid(row=self._rowIndex, column=1, padx=10, pady=5, sticky='w')
        return frame

    def addLabel(
        self,
        desc: str,
        text: str
    ):
        self.addRow(desc, tk.Label(text=text))

    def addBtn(
        self,
        label: str,
        command: Callable[..., None],
        *,
        width: int = 20,
        focus: bool = False
    ):
        frame = self.addRowFrame()
        btn = tk.Button(frame, text=label, width=width, command=command)
        btn.pack(side="left", expand=True, padx=15)
        if focus:
            self._initFocus(btn)

    def addEntry(
        self,
        desc: str,
        var: tk.StringVar,
        *,
        width: int = 60,
        focus: bool = False,
        justify: Literal['left', 'right', 'center'] = tk.LEFT,
        password: bool = False,
        command: Callable[..., Any] | None = None,
    ):
        self._initVar(var)
        entry = tk.Entry(self, width=width, justify=justify, textvariable=var)
        entry.icursor(tk.END)
        self.addRow(desc, entry)
        if password:
            entry.config(show='*')
        if focus:
            self._initFocus(entry)
        if command:
            entry.bind('<Return>', lambda event: command())
        return entry

    def addColorChooser(
        self,
        desc: str,
        var: tk.StringVar,
    ):
        self._initVar(var)
        frame = self.addRowFrameWithDesc(desc)

        # 色块展示（可点击）
        swatch_size = 20
        swatch = tk.Canvas(frame, width=swatch_size, height=swatch_size, bd=1, relief='solid', highlightthickness=0)
        swatch.pack(side='left')

        def _update_swatch(color: str | None):
            if not color:
                color = '#FFFFFF'
            try:
                swatch.itemconfig(_rect_id, fill=color, outline=color)
            except Exception:
                # 如果还没创建 rect 或颜色无效则忽略
                pass

        # 初始颜色
        initial_color = var.get() or '#FFFFFF'
        _rect_id = swatch.create_rectangle(0, 0, swatch_size, swatch_size, fill=initial_color, outline=initial_color)

        # 打开颜色选择器并更新变量与色块
        def choose_color(event: tk.Event | None = None):
            result = colorchooser.askcolor(title="选择颜色", initialcolor=var.get() or initial_color)
            if result and result[1]:
                color_hex = result[1]
                var.set(color_hex)
                _update_swatch(color_hex)

        # 点击色块打开选择器
        swatch.bind("<Button-1>", choose_color, add="+")

        # 允许点击时获得焦点（类似其它控件的行为）
        setWidgetClickFocus(swatch)

        return swatch

    def addScrolledText(
        self,
        desc: str,
        var: tk.StringVar,
        *,
        width: int = 60,
        height: int = 3,
        focus: bool = False,
    ):
        self._initVar(var)
        scrolledText = ScrolledText(self, width=width, height=height)
        scrolledText.insert(tk.END, var.get())
        self.addRow(desc, scrolledText)
        scrolledText.bind("<KeyRelease>", lambda event: on_text_change(event))
        scrolledText.bind("<Tab>", lambda event: on_tab(event))

        def on_text_change(event: tk.Event):
            new_value = scrolledText.get("1.0", tk.END)
            if new_value != var.get():
                var.set(new_value)

        def on_tab(event: tk.Event):
            widget = event.widget.tk_focusNext()
            assert widget
            widget.focus_set()
            return "break"

        if focus:
            self._initFocus(scrolledText)
        return scrolledText

    def addRadioBtnList(
        self,
        desc: str,
        optionList: list[str],
        var: tk.StringVar,
        *,
        focusIndex: int | None = None,
        onChanged: Callable[[str], None] | None = None,
    ):
        self._initVar(var)
        frame = tk.Frame()
        self.addRow(desc, frame)
        radioBtnList: list[tk.Radiobutton] = []
        for version in optionList:
            radioBtn = tk.Radiobutton(frame, text=version, variable=var, value=version)
            radioBtn.pack(side="left", padx=(0, 15))
            setWidgetClickFocus(radioBtn)
            radioBtnList.append(radioBtn)
        if focusIndex is not None:
            self._initFocus(radioBtnList[focusIndex])
        if onChanged:
            var.trace_add('write', lambda *args: onChanged(var.get()))  # type: ignore
            self.addInitHandler(lambda: onChanged(var.get()))  # 外面有侦听，初始化的状态如果缺少这个会有问题

        return radioBtnList

    def addCheckBox(
        self,
        desc: str,
        text: str,
        var: tk.BooleanVar,
        *,
        focus: bool = False,
    ):
        self._initVar(var)
        checkBox = tk.Checkbutton(text=text, variable=var)
        self.addRow(desc, checkBox)
        setWidgetClickFocus(checkBox)
        if focus:
            self._initFocus(checkBox)
        return checkBox

    def addCheckBoxList(
        self,
        desc: str,
        dataList: list[tuple[str, tk.BooleanVar]],
    ):
        frame = tk.Frame(self)
        self.addRow(desc, frame)
        checkBoxList: list[tk.Checkbutton] = []
        for label, var in dataList:
            self._initVar(var)
            checkbox = tk.Checkbutton(frame, text=label, variable=var)
            checkbox.pack(side="left", expand=True, padx=(0, 15))
            checkBoxList.append(checkbox)
            setWidgetClickFocus(checkbox)
        return checkBoxList

    def addChoisePath(
        self,
        desc: str,
        var: tk.StringVar,
        *,
        width: int = 47,
        focus: bool = False,
        isDir: bool = False,
        isMulti: bool = False,
    ):
        self._initVar(var)
        frame = self.addRowFrameWithDesc(desc)
        entry = tk.Entry(frame, width=width, textvariable=var)
        entry.icursor(tk.END)
        entry.pack(side="left")
        btn = tk.Button(frame, text=f'选择{'目录' if isDir else '文件'} ...', width=10, command=lambda: onBtn())
        btn.pack(side="left", padx=(10, 0))
        if focus:
            self._initFocus(btn)

        def onBtn():
            if isDir:
                var.set(filedialog.askdirectory())
            elif isMulti:
                result = filedialog.askopenfilenames()
                if result:
                    var.set(json.dumps(result))
            else:
                var.set(filedialog.askopenfilename())

    def addScale(
        self,
        desc: str,
        var: tk.IntVar | tk.DoubleVar,
        *,
        length: int = 138,
        from_: int | float = 0,
        to: int | float = 100,
        resolution: float = 1.0,
    ):
        self._initVar(var)
        scale = tk.Scale(
            variable=var,
            from_=from_,
            to=to,
            orient=tk.HORIZONTAL,
            length=length,
            resolution=resolution,
        )
        self.addRow(desc, scale, labelSticky='SE', pady=0)


def setWidgetEnabled(widget: tk.Widget, value: bool):
    widget['state'] = tk.NORMAL if value else tk.DISABLED


def setWidgetClickFocus(widget: tk.Widget):
    # 使用 add='+' 追加绑定，避免覆盖已有的 "<Button-1>" 处理器（例如色块的 choose_color）
    widget.bind("<Button-1>", lambda event: event.widget.focus_set(), add="+")
