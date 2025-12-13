"""
sketchbook - 高性能图像合成与文本渲染库

这是一个基于 Rust 的 Python 图像处理库, 提供高效的图层合成、
自适应文本渲染和丰富的图像变换功能.

主要特性:
    - 图层系统: 支持多图层合成、透明度、旋转、偏移等变换
    - 自适应文本: 自动调整字号以适应指定区域
    - 富文本解析: 支持自定义标记语法 (如 [高亮]、**粗体** 等)
    - 高性能: 核心使用 Rust 实现, 支持并行渲染

Note:
    - 所有颜色使用 RGBA 格式: (r, g, b, a), 每个分量范围 0-255
    - 图像数据支持文件路径(str)或 PNG 字节数据(bytes)
    - Layer 方法返回新实例, 支持链式调用
    - Drawer.base/overlay/layer 返回自身, 支持链式调用
"""

from __future__ import annotations

# =============================================================================
# 类型别名
# =============================================================================

type Color = tuple[int, int, int, int]

type ImageSource = str | bytes
"""图像来源, 支持以下格式:

- str: 图像文件路径(支持 PNG、JPEG、WebP 等常见格式) 
- bytes: 图像的字节数据, 会自动识别格式

Examples:
    >>> layer.image("background.png", 0, 0)  # 文件路径
    >>> layer.image(png_bytes, 0, 0)         # 字节数据
"""

class Align:
    """水平对齐方式.

    用于控制文本或图像在区域内的水平位置.

    Attributes:
        Left: 左对齐
        Center: 居中对齐
        Right: 右对齐

    Examples:
        >>> layer.image_fit(img, region, align=Align.Right)
    """

    Left: Align
    Center: Align
    Right: Align

class VAlign:
    """垂直对齐方式.

    用于控制文本或图像在区域内的垂直位置.

    Attributes:
        Top: 顶部对齐
        Middle: 垂直居中
        Bottom: 底部对齐

    Examples:
        >>> layer.image_fit(img, region, valign=VAlign.Bottom)
    """

    Top: VAlign
    Middle: VAlign
    Bottom: VAlign

class ScaleMode:
    """图像缩放模式.

    控制图像在目标区域中的缩放行为.

    Attributes:
        Fit: 保持比例, 确保图像完全可见 (可能有留白)
        Fill: 保持比例, 确保区域完全填满 (可能裁剪)
        Stretch: 拉伸填充, 不保持比例
        Original: 不缩放, 保持原始尺寸

    Examples:
        >>> layer.image_fit(avatar, region, scale=ScaleMode.Fill)
        >>> layer.image_fit(logo, region, scale=ScaleMode.Fit)
    """

    Fit: ScaleMode
    Fill: ScaleMode
    Stretch: ScaleMode
    Original: ScaleMode

class Region:
    """矩形区域, 定义绘制操作的位置和大小.

    用于指定文本渲染、图像放置、填充等操作的目标区域.

    Attributes:
        x (int): 左上角 X 坐标
        y (int): 左上角 Y 坐标
        width (int): 区域宽度
        height (int): 区域高度

    Examples:
        >>> # 创建指定位置和大小的区域
        >>> region = Region(100, 50, 400, 200)
        >>>
        >>> # 创建全画布区域
        >>> full = Region.full(800, 600)
        >>>
        >>> # 创建内边距区域
        >>> padded = full.inset(20)  # 四边各缩进 20 像素
    """

    x: int
    y: int
    width: int
    height: int

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """创建矩形区域.

        Args:
            x: 左上角 X 坐标 (像素)
            y: 左上角 Y 坐标 (像素)
            width: 区域宽度 (像素)
            height: 区域高度 (像素)
        """
        ...

    @staticmethod
    def full(width: int, height: int) -> Region:
        """创建从原点开始的全尺寸区域.

        等价于 `Region(0, 0, width, height)`.

        Args:
            width: 区域宽度
            height: 区域高度

        Returns:
            从 (0, 0) 开始的矩形区域
        """
        ...

    def inset(self, padding: int) -> Region:
        """创建向内缩进的子区域.

        四边同时向内缩进指定像素数.

        Args:
            padding: 内边距大小 (像素)

        Returns:
            缩进后的新区域
        """
        ...

    def __repr__(self) -> str: ...

class StyleMod:
    """文本样式修饰器.

    用于定义富文本解析规则中匹配文本的样式变化.
    可以修改颜色、粗体、斜体等属性.

    Examples:
        >>> # 创建红色高亮样式
        >>> highlight = StyleMod(color=(255, 0, 0, 255))
        >>>
        >>> # 使用预设
        >>> bold = StyleMod.bold()
        >>> italic = StyleMod.italic()
        >>>
        >>> # 组合样式
        >>> bold_red = StyleMod.bold().merge(StyleMod.color(255, 0, 0))
    """

    def __init__(
        self,
        color: Color = (0, 0, 0, 255),
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
    ) -> None:
        """创建样式修饰器.

        Args:
            color: 文字颜色 (R, G, B, A)
            bold: 是否粗体
            italic: 是否斜体
            underline: 是否下划线
            strikethrough: 是否删除线
        """
        ...

    @staticmethod
    def bold() -> StyleMod:
        """创建粗体样式."""
        ...

    @staticmethod
    def italic() -> StyleMod:
        """创建斜体样式."""
        ...

    @staticmethod
    def color(r: int, g: int, b: int, a: int = 255) -> StyleMod:
        """创建指定颜色的样式.

        Args:
            r: 红色分量 (0-255)
            g: 绿色分量 (0-255)
            b: 蓝色分量 (0-255)
            a: 透明度 (0-255), 默认 255 (不透明)
        """
        ...

    def merge(self, other: StyleMod) -> StyleMod:
        """合并两个样式修饰器.

        other 中的非默认值会覆盖 self 中的值.

        Args:
            other: 要合并的另一个样式

        Returns:
            合并后的新样式
        """
        ...

class ParseRule:
    """富文本解析规则.

    定义如何识别和渲染特殊标记的文本.

    Examples:
        >>> # 自定义规则: [高亮文本] 显示为红色
        >>> rule = ParseRule(
        ...     name="highlight",
        ...     start="[",
        ...     end="]",
        ...     style=StyleMod.color(255, 0, 0),
        ...     keep_delim=False,  # 不显示方括号
        ...)
        >>>
        >>> # 使用预设规则
        >>> bracket = ParseRule.bracket((255, 0, 0, 255))  # [红色]
        >>> bold = ParseRule.bold()                        # **粗体**
    """

    def __init__(
        self,
        name: str,
        start: str,
        end: str,
        style: StyleMod,
        keep_delim: bool = False,
    ) -> None:
        """创建解析规则.

        Args:
            name: 规则名称 (用于调试)
            start: 起始分隔符
            end: 结束分隔符
            style: 匹配文本的样式
            keep_delim: 是否在输出中保留分隔符
        """
        ...

    @staticmethod
    def bracket(color: Color) -> ParseRule:
        """创建方括号规则: [文本]

        Args:
            color: 匹配文本的颜色
        """
        ...

    @staticmethod
    def cn_bracket(color: Color) -> ParseRule:
        """创建中文方括号规则: 【文本】

        Args:
            color: 匹配文本的颜色
        """
        ...

    @staticmethod
    def brace(color: Color) -> ParseRule:
        """创建花括号规则: {文本}

        Args:
            color: 匹配文本的颜色
        """
        ...

    @staticmethod
    def paren(color: Color) -> ParseRule:
        """创建圆括号规则: (文本)

        Args:
            color: 匹配文本的颜色
        """
        ...

    @staticmethod
    def cn_paren(color: Color) -> ParseRule:
        """创建中文圆括号规则: （文本）

        Args:
            color: 匹配文本的颜色
        """
        ...

    @staticmethod
    def bold() -> ParseRule:
        """创建 Markdown 粗体规则: **文本**"""
        ...

    @staticmethod
    def italic() -> ParseRule:
        """创建 Markdown 斜体规则: *文本*"""
        ...

    def __repr__(self) -> str: ...

# =============================================================================
# 文本样式
# =============================================================================

class TextStyle:
    """文本渲染样式配置.

    控制文本的字号、颜色、对齐方式和富文本解析规则.
    支持自动字号调整以适应指定区域.

    Attributes:
        默认值:
            - color: (0, 0, 0, 255) 黑色
            - max_font_size: None (自动)
            - min_font_size: 1.0
            - line_spacing: 0.15 (行高的 15%)
            - align: Align.Center
            - valign: VAlign.Middle
            - antialias: True

    Examples:
        >>> # 默认样式 (自动字号, 居中对齐)
        >>> style = TextStyle()
        >>>
        >>> # 自定义样式
        >>> style = TextStyle(
        ...     color=(255, 255, 255, 255),  # 白色
        ...     max_font_size=48.0,          # 最大 48px
        ...     align=Align.Left,
        ...     valign=VAlign.Top,
        ...)
        >>>
        >>> # 带富文本解析
        >>> style = TextStyle(
        ...     parse_rules=[
        ...         ParseRule.bracket((255, 0, 0, 255)),  # [红色]
        ...         ParseRule.bold(),                     # **粗体**
        ...     ]
        ...)
        >>>
        >>> # 纯文本模式 (不解析任何标记)
        >>> plain_style = TextStyle.plain()

    Note:
        - 字号自动调整: 从 max_font_size 开始尝试, 逐渐减小直到文本适应区域
        - 如果 max_font_size 为 None, 将根据区域高度自动计算
        - 最小字号由 min_font_size 控制, 防止文字过小
    """

    def __init__(
        self,
        color: Color = (0, 0, 0, 255),
        max_font_size: float | None = None,
        min_font_size: float = 1.0,
        line_spacing: float = 0.15,
        align: Align = Align.Center,
        valign: VAlign = VAlign.Middle,
        antialias: bool = True,
        parse_rules: list[ParseRule] | None = None,
    ) -> None:
        """创建文本样式.

        Args:
            color: 默认文字颜色 (R, G, B, A)
            max_font_size: 最大字号, None 表示自动计算
            min_font_size: 最小字号, 文本不会小于此值
            line_spacing: 行间距, 相对于行高的比例
            align: 水平对齐方式
            valign: 垂直对齐方式
            antialias: 是否启用抗锯齿
            parse_rules: 富文本解析规则列表, None 使用默认规则
        """
        ...

    @staticmethod
    def plain() -> TextStyle:
        """创建纯文本样式.

        不启用任何富文本解析规则, 文本原样显示.

        Returns:
            纯文本样式实例
        """
        ...

    def __repr__(self) -> str: ...

class FontSet:
    """字体集合, 管理多个字体用于文本渲染.

    支持加载 TrueType (.ttf)、OpenType (.otf) 格式.
    渲染时按添加顺序查找字形, 支持多字体回退.

    Examples:
        >>> # 空字体集
        >>> fonts = FontSet()
        >>> fonts.add("main.ttf")
        >>> fonts.add("fallback.ttf")
        >>>
        >>> # 直接初始化多个字体
        >>> fonts = FontSet("main.ttf", "emoji.ttf", "cjk.ttf")

    Note:
        - 字体按添加顺序作为回退链
        - 建议第一个字体包含主要字符, 后续字体作为补充
    """

    def __init__(self, *paths: str) -> None:
        """创建字体集合.

        Args:
            *paths: 字体文件路径 (可变参数)

        Raises:
            ValueError: 字体文件加载失败

        Examples:
            >>> fonts = FontSet()  # 空集合
            >>> fonts = FontSet("font.ttf")  # 单个字体
            >>> fonts = FontSet("a.ttf", "b.ttf", "c.ttf")  # 多个字体
        """
        ...

    def add(self, path: str) -> None:
        """添加字体文件.

        Args:
            path: 字体文件路径

        Raises:
            ValueError: 字体文件加载失败
        """
        ...

    def len(self) -> int:
        """返回已加载的字体数量."""
        ...

    def __repr__(self) -> str: ...

class Layer:
    """图层, 用于组织绘制操作.

    每个图层可以包含多个绘制操作 (文本、图像、填充等),
    并可以应用变换 (透明度、偏移、旋转等).

    所有绘制方法返回新的 Layer 实例, 支持链式调用.

    Attributes:
        name (str): 图层名称, 用于调试和日志

    Examples:
        >>> # 创建带文本的图层
        >>> layer = Layer("title").text("Hello", region, style)
        >>>
        >>> # 链式调用多个操作
        >>> layer = (
        ...     Layer("card")
        ...     .fill(region, (255, 255, 255, 255))
        ...     .image("avatar.png", 10, 10)
        ...     .text("Username", name_region, style)
        ...     .opacity(0.9)
        ...)

    Note:
        - Layer 是不可变的, 每个方法返回新实例
        - 同名图层添加到 Drawer 时会覆盖之前的
        - 变换 (opacity, offset, rotate) 应用于整个图层
    """

    name: str

    def __init__(self, name: str) -> None:
        """创建新图层.

        Args:
            name: 图层名称, 建议使用有意义的名称便于调试
        """
        ...

    def text(
        self,
        text: str,
        region: Region,
        style: TextStyle | None = None,
    ) -> Layer:
        """在指定区域绘制文本.

        文本会自动调整字号以适应区域, 支持富文本标记.

        Args:
            text: 要绘制的文本内容
            region: 文本绘制区域
            style: 文本样式, None 使用默认样式

        Returns:
            Layer

        Examples:
            >>> layer = Layer("text").text("Hello World", region)
            >>> layer = Layer("styled").text("**Bold** text", region, style)
        """
        ...

    def image(self, image: ImageSource, x: int, y: int) -> Layer:
        """在指定位置绘制图像.

        图像左上角放置在 (x, y) 位置, 保持原始尺寸.

        Args:
            image: 图像来源 (路径或字节数据)
            x: 左上角 X 坐标
            y: 左上角 Y 坐标

        Returns:
            Layer

        Raises:
            ValueError: 图像加载失败
        """
        ...

    def image_fit(
        self,
        image: ImageSource,
        region: Region,
        align: Align = ...,  # Align.Center
        valign: VAlign = ...,  # VAlign.Middle
        scale: ScaleMode = ...,  # ScaleMode.Fit
    ) -> Layer:
        """在区域内自适应绘制图像.

        根据缩放模式调整图像大小以适应目标区域.

        Args:
            image: 图像来源
            region: 目标区域
            align: 水平对齐方式
            valign: 垂直对齐方式
            scale: 缩放模式

        Returns:
            Layer

        Examples:
            >>> # 头像: 填满区域并居中
            >>> layer.image_fit(avatar, region, scale=ScaleMode.Fill)
            >>>
            >>> # Logo: 完整显示在左上角
            >>> layer.image_fit(logo, region, Align.Left, VAlign.Top, ScaleMode.Fit)
        """
        ...

    def fill(self, region: Region, color: Color) -> Layer:
        """填充矩形区域.

        Args:
            region: 填充区域
            color: 填充颜色 (R, G, B, A)

        Returns:
            Layer

        Examples:
            >>> # 半透明黑色遮罩
            >>> layer.fill(region, (0, 0, 0, 128))
        """
        ...

    def opacity(self, opacity: float) -> Layer:
        """设置图层整体透明度.

        Args:
            opacity: 不透明度 (0.0 完全透明 ~ 1.0 完全不透明)

        Returns:
            Layer

        Examples:
            >>> layer = Layer("ghost").text("Fade", region).opacity(0.5)
        """
        ...

    def offset(self, x: int, y: int) -> Layer:
        """设置图层整体偏移.

        Args:
            x: X 方向偏移 (正值向右)
            y: Y 方向偏移 (正值向下)

        Returns:
            Layer
        """
        ...

    def rotate(self, angle_deg: float) -> Layer:
        """绕中心点旋转图层.

        Args:
            angle_deg: 旋转角度 (度数, 正值顺时针)

        Returns:
            Layer
        """
        ...

    def rotate_around(self, angle_deg: float, cx: float, cy: float) -> Layer:
        """绕指定点旋转图层.

        Args:
            angle_deg: 旋转角度 (度数, 正值顺时针)
            cx: 旋转中心 X 坐标
            cy: 旋转中心 Y 坐标

        Returns:
            Layer
        """
        ...

    def is_empty(self) -> bool:
        """检查图层是否为空 (没有任何绘制操作)."""
        ...

    def op_count(self) -> int:
        """返回图层中的绘制操作数量."""
        ...

    def __repr__(self) -> str: ...

class Drawer:
    """图像合成绘制器, 管理图层并渲染最终图像.

    Drawer 是核心合成引擎, 负责:
    1. 管理画布尺寸和字体
    2. 维护图层栈 (base → layers → overlay)
    3. 按顺序渲染所有图层

    Attributes:
        size (tuple[int, int]): 画布尺寸 (width, height)

    Examples:
        >>> # 基本用法
        >>> drawer = Drawer(800, 600, fonts)
        >>> drawer.layer(Layer("bg").fill(drawer.full_region(), (255, 255, 255, 255)))
        >>> drawer.layer(Layer("text").text("Hello", drawer.full_region()))
        >>> png_data = drawer.render()
        >>>
        >>> # 使用底层和覆盖层
        >>> drawer = Drawer(800, 600, fonts)
        >>> drawer.base("background.png")
        >>> drawer.layer(Layer("content").text("Content", region))
        >>> drawer.overlay("watermark.png")
        >>> png_data = drawer.render()
        >>>
        >>> # 链式调用
        >>> png_data = (
        ...     Drawer(800, 600, fonts)
        ...     .base("bg.png")
        ...     .layer(Layer("title").text("Title", title_region))
        ...     .layer(Layer("body").text("Body", body_region))
        ...     .render()
        ...)

    Note:
        - 渲染顺序: base (最底) → layers (按添加顺序) → overlay (最顶)
        - 同名图层会被覆盖 (后添加的替换先添加的)
        - base/overlay/layer 返回 self, 支持链式调用
        - render() 返回 PNG 格式的字节数据
    """

    size: tuple[int, int]

    def __init__(self, width: int, height: int, fonts: FontSet) -> None:
        """创建绘制器.

        Args:
            width: 画布宽度 (像素)
            height: 画布高度 (像素)
            fonts: 字体集合

        Examples:
            >>> fonts = FontSet("font.ttf")
            >>> drawer = Drawer(1920, 1080, fonts)
        """
        ...

    @staticmethod
    def from_image(image: ImageSource, fonts: FontSet) -> Drawer:
        """从图像创建绘制器.

        画布尺寸与图像尺寸相同, 图像作为初始内容.

        Args:
            image: 图像来源
            fonts: 字体集合

        Returns:
            以图像为基础的绘制器

        Raises:
            ValueError: 图像加载失败

        Examples:
            >>> drawer = Drawer.from_image("template.png", fonts)
        """
        ...

    def base(self, image: ImageSource) -> Drawer:
        """设置底层图像.

        底层在所有图层之下渲染, 通常用于背景.

        Args:
            image: 图像来源

        Returns:
            Drawer

        Note:
            底层图像会被缩放以适应画布尺寸.
        """
        ...

    def overlay(self, image: ImageSource) -> Drawer:
        """设置覆盖层图像.

        覆盖层在所有图层之上渲染, 通常用于水印.

        Args:
            image: 图像来源

        Returns:
            Drawer

        Note:
            覆盖层图像会被缩放以适应画布尺寸.
        """
        ...

    def layer(self, layer: Layer) -> Drawer:
        """添加图层.

        图层按添加顺序渲染, 同名图层会被覆盖.

        Args:
            layer: 要添加的图层

        Returns:
            Drawer

        Examples:
            >>> drawer.layer(Layer("bg").fill(region, WHITE))
            >>> drawer.layer(Layer("text").text("Hello", region))
        """
        ...

    def full_region(self) -> Region:
        """获取覆盖整个画布的区域.

        等价于 `Region(0, 0, width, height)`.

        Returns:
            Region: 全画布区域
        """
        ...

    def render(self) -> bytes:
        """渲染所有图层并返回 PNG 图像数据.

        渲染顺序: base → layers (按添加顺序) → overlay

        Returns:
            bytes: PNG 格式的图像字节数据

        Examples:
            >>> png_data = drawer.render()
            >>> with open("output.png", "wb") as f:
            ...     f.write(png_data)
        """
        ...

    def __repr__(self) -> str: ...
