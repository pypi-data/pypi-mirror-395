# PCLTheme

一个用 Python 构建 PCL（个人启动页/主页）XAML 模板的轻量库，目标是让用户无需编写 XAML，就能通过 Python 语法快速构建并输出 PCL 自定义主页（Custom.xaml）。

主要思想：把常用的控件封装为 Python 函数/上下文管理器，按顺序渲染为 XAML 字符串，最后通过 `build()` 输出或保存为文件。

主要特点

- 用 Python API 构建 XAML，降低学习 XAML 的门槛
- 支持容器（Grid、StackPanel、Card 等）与常用控件（TextBlock、Button、Image、ListItem 等）
- 支持嵌套容器与栈式渲染，按添加顺序拼接输出
- 可直接保存为 PCL 本地自定义主页路径（例如保存为 Custom.xaml）

## :rocket: 快速开始

### :memo: 前提要求

- Python 3.6 或更高版本

### :computer: 安装方式

从 PyPI 安装

``` bash
pip install PCLTheme
```

### :coffee: 示例代码

下面示例展示了一个最小的使用流程：创建容器与控件，然后调用 `build()` 获取生成的 XAML。

```python
from PCLTheme import grid, my_card, text_block, my_button, my_image, build

# 在 Grid 中安排两个单元格，并在其中放置文本、按钮和图片
with grid(column=2, row=1):
    text_block("欢迎使用 PCLTheme", row=0, column=0)
    with my_card("示例卡片", row=0, column=1):
        my_image("https://example.com/logo.png", width=120, height=120)
        my_button("访问网站", event_type="打开网页", event_data1="https://example.com")

# 生成 XAML 字符串
out_xaml = build()
print(out_xaml)

# 或保存为文件（示例：保存到 C:\PCL\Custom.xaml）
# build(file_path=r"C:\PCL", file_name="Custom.xaml")
```

注意事项与 API 要点

- 导入：库的顶层模块在 `PCLTheme.__init__` 中导出了常用的控件/方法，示例中直接使用 `from PCLTheme import ...` 即可。
- 容器类（如 `grid`, `stack_panel`, `my_card`）实现为上下文管理器（支持 with 语法），用于管理内部子控件的缩进与嵌套关系。
- 基本控件（如 `text_block`, `my_button`, `my_image`）为函数，接收丰富的参数（margin/padding/row/column/width/height/alignment 等）。
- `build(file_path=None, file_name=None)`：按添加顺序渲染并返回拼接后的 XAML 字符串；当同时提供 `file_path` 和 `file_name` 时会把结果写入磁盘。
- 事件类型（`my_button` 的 `event_type`）支持一系列字符串（比如“打开网页”、“执行命令”等），具体可见代码注释或项目文档。

## 常用控件速览

- `grid(column=1, row=1, column_width=None, row_height=None, margin=None, self_row=-1, self_column=-1)`
  - 创建 Grid 容器；`column`/`row` 指列数/行数，`column_width`/`row_height` 支持如 `"1*"` 或像素值。
- `stack_panel(orientation='Vertical', margin=None, row=-1, column=-1)`
  - 垂直或水平排列的面板。
- `my_card(title, can_swap=True, default_swaped=False, margin=None, row=-1, column=-1)`
  - 卡片容器，支持可折叠（可用于分组显示子控件）。
- `text_block(text, font_size=None, foreground='T2', background=None, margin=None, row=-1, column=-1)`
  - 文本控件，支持主题色（T1~T8）或颜色代码。
- `my_button(text, color_type=None, event_type=None, event_data1=None, row=-1, column=-1, width=None, height=None)`
  - 按钮控件，支持事件绑定与颜色类型（例如 Red/Highlight）。
- `my_image(source, fallback_source=None, loading_source=None, enable_cache=True, margin=None, row=-1, column=-1, width=None, height=None)`
  - 图片控件，建议显式指定宽高。

## 自定义默认样式与全局设置

项目在 `PCLTheme.global_var` 中维护了若干全局默认值（如默认 margin/padding/文本大小等），并导出了 getter/setter，示例：

```python
from PCLTheme import set_default_text_size, set_default_panel_margin

set_default_text_size(14)
set_default_panel_margin([20, 30, 20, 12])
```

## 错误检查与常见异常

- 大多数控件会对 `margin`/`padding` 长度（只接受长度 1~4）做检查。
- 当控件需要在 Grid 中指定 `row`/`column` 时，如果当前并不在有 row/column 的容器内部，会抛出 ValueError。
- 请按照控件函数签名提供正确类型与取值范围，会在运行时抛出有意义的异常提示。

## 开发与贡献

欢迎贡献：修复 bug、完善示例或增加控件。贡献流程：

1. Fork 仓库
2. 新建分支实现修改
3. 提交 PR，并在描述中说明修改内容与测试方式

## 依赖与测试

本项目依赖（至少）以下第三方包：

- chameleon
- pydantic（用于颜色解析）

这些依赖在 `requirements.txt` 或 `pyproject.toml` 中有所列出。请使用虚拟环境进行安装与测试。

