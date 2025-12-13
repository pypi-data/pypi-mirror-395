import torch
import plotly.graph_objects as go
from scipy.interpolate import griddata
from IPython.display import display
from ipywidgets import (
    Dropdown,
    VBox,
    HBox,
    Output,
    IntSlider,
    Button,
    interactive,
    Layout,
)

c = 299792458
eps0 = 8.854187817e-12
u0 = 1.256637061e-6
eta0 = 376.7303134096266


def Matrix_visualizer(M, x, y, z, lam, name=""):
    # 现在M的shape变了
    output = Output()
    shape = [M.shape[0], M.shape[1], M.shape[2], M.shape[3], M.shape[4], M.shape[6]]
    source = torch.arange(shape[0]).float().to(M.device)
    structure = torch.arange(shape[1]).float().to(M.device)
    slice_list = [source, structure, x, y, z, lam]
    # 当前选择的维度3.
    current_dimension = "z"
    # 初始化一个字典来存储每个维度的滑块位置
    slider_positions = {"source": 0, "structure": 0, "x": 0, "y": 0, "z": 0, "λ": 0}

    def plot_data(
        scalar,
        vector,
        source_choice,
        structure_choice,
        x_choice,
        y_choice,
        z_choice,
        lam_choice,
        slice_index,
    ):
        with output:
            output.clear_output(wait=True)  # 清除之前的图形
            slider_temp = slider_positions.copy()
            slider_temp[current_dimension] = slice_index
            # 根据选择的向量分量更新数据
            if vector == "x":
                data = M[:, :, :, :, :, 0, :]
            elif vector == "y":
                data = M[:, :, :, :, :, 1, :]
            elif vector == "z":
                data = M[:, :, :, :, :, 2, :]
            elif vector == "Magnitude":
                data = torch.sqrt(torch.sum(torch.abs(M) ** 2, axis=-2))

            # 根据选择处理数据
            if scalar == "Re":
                data = torch.real(data)
            elif scalar == "Im":
                data = torch.imag(data)
            elif scalar == "Abs":
                data = torch.abs(data)
            elif scalar == "Angle":
                data = torch.angle(data)

            choices = [
                source_choice,
                structure_choice,
                x_choice,
                y_choice,
                z_choice,
                lam_choice,
            ]
            # 根据选择的维度切片数据
            slices = [
                slice(None),
                slice(None),
                slice(None),
                slice(None),
                slice(None),
                slice(None),
            ]  # 默认为全选
            for dim, slice_value in enumerate(choices):
                if slice_value == "Slice":
                    key = ["source", "structure", "x", "y", "z", "λ"][dim]
                    slices[dim] = slice(slider_temp[key], slider_temp[key] + 1)
                    slice_button[dim].description = (
                        "{:.5e}".format(slice_list[dim][slider_temp[key]].item())
                        .rstrip("0")
                        .rstrip(".")
                    )
                else:
                    slice_button[dim].description = "  "

            data = data[tuple(slices)]
            # 获取下拉菜单选项

            # 找到 'Plot x' 和 'Plot y' 的索引
            idxX = choices.index("Plot x")
            idxY = choices.index("Plot y")

            # 确保找到了 'Plot x' 和 'Plot y'
            if idxX is None or idxY is None:
                raise ValueError("Plot x and Plot y must be selected")

            idx = set(range(6)) - {idxX, idxY}

            # 使用 permute 重新排列张量的维度
            data = data.permute(idxX, idxY, *idx)
            Z = torch.squeeze(data, axis=(2, 3, 4, 5)).cpu().numpy()

            fig = go.Figure(
                data=go.Heatmap(
                    z=Z.T,
                    x=slice_list[idxX].cpu(),
                    y=slice_list[idxY].cpu(),
                    colorscale="Jet",
                    colorbar=dict(title="Value"),
                )
            )
            fig.update_layout(
                xaxis_title=["source", "structure", "x", "y", "z", "λ"][idxX],
                yaxis_title=["source", "structure", "x", "y", "z", "λ"][idxY],
                height=500,
            )
            output.clear_output(wait=True)
            display(fig)

    layout0 = Layout(width="auto")
    layout1 = Layout(width="80px")
    layout2 = Layout(width="60%")

    common_style = {"description_width": "initial"}  # 这会影响描述标签的宽度

    # 创建下拉菜单和按钮
    scalar_dropdown = Dropdown(
        options=["Re", "Im", "Abs", "Angle"], description="Scalar:"
    )
    vector_dropdown = Dropdown(
        options=["x", "y", "z", "Magnitude"], description="Vector:"
    )
    slider = IntSlider(
        min=0,
        max=shape[2] - 1,
        step=1,
        description="z",
        layout=layout2,
        style=common_style,
    )

    source_dropdown = Dropdown(
        options=["Plot x", "Plot y", "Slice"],
        value="Slice",
        description="source",
        style=common_style,
        layout=layout0,
    )
    structure_dropdown = Dropdown(
        options=["Plot x", "Plot y", "Slice"],
        value="Slice",
        description="structure",
        style=common_style,
        layout=layout0,
    )
    x_dropdown = Dropdown(
        options=["Plot x", "Plot y", "Slice"],
        value="Plot x",
        description="x",
        style=common_style,
        layout=layout0,
    )
    y_dropdown = Dropdown(
        options=["Plot x", "Plot y", "Slice"],
        value="Plot y",
        description="y",
        style=common_style,
        layout=layout0,
    )
    z_dropdown = Dropdown(
        options=["Plot x", "Plot y", "Slice"],
        value="Slice",
        description="z",
        style=common_style,
        layout=layout0,
    )
    lam_dropdown = Dropdown(
        options=["Plot x", "Plot y", "Slice"],
        value="Slice",
        description="λ",
        style=common_style,
        layout=layout0,
    )
    dropdowns = [
        source_dropdown,
        structure_dropdown,
        x_dropdown,
        y_dropdown,
        z_dropdown,
        lam_dropdown,
    ]
    V_drop = VBox(dropdowns)
    source_slice_button = Button(description="", layout=layout1)
    structure_slice_button = Button(description="", layout=layout1)
    x_slice_button = Button(description="", layout=layout1)
    y_slice_button = Button(description="", layout=layout1)
    z_slice_button = Button(description="", layout=layout1)
    lam_slice_button = Button(description="", layout=layout1)
    slice_button = [
        source_slice_button,
        structure_slice_button,
        x_slice_button,
        y_slice_button,
        z_slice_button,
        lam_slice_button,
    ]
    V_slice = VBox(slice_button)

    # 定义按钮点击事件处理函数
    # 创建一个函数，该函数返回一个事件处理函数
    def create_button_handler(tag):
        def on_button_clicked(b):
            nonlocal current_dimension  # 使用 nonlocal 声
            slider_positions[current_dimension] = slider.value
            current_dimension = tag
            # 先更新最大值,再更新当前值
            dim_index = {
                "source": 0,
                "structure": 1,
                "x": 2,
                "y": 3,
                "z": 4,
                "λ": 5,
            }[current_dimension]
            slider.max = shape[dim_index] - 1
            slider.value = slider_positions[current_dimension]
            slider.description = tag

        return on_button_clicked

    source_slice_button.on_click(create_button_handler("source"))
    structure_slice_button.on_click(create_button_handler("structure"))
    x_slice_button.on_click(create_button_handler("x"))
    y_slice_button.on_click(create_button_handler("y"))
    z_slice_button.on_click(create_button_handler("z"))
    lam_slice_button.on_click(create_button_handler("λ"))

    def handle_dropdown_change(change):
        changed_dropdown = change.owner
        new_value = change.new
        other_dropdowns = [dd for dd in dropdowns if dd is not changed_dropdown]

        if new_value == "Plot x" or new_value == "Plot y":
            for dd in other_dropdowns:
                if dd.value == new_value:
                    dd.value = "Slice"
                    break
        elif new_value == "Slice":
            current_plots = [
                dd.value for dd in other_dropdowns if dd.value in ["Plot x", "Plot y"]
            ]
            if len(current_plots) < 2:
                start_idx = dropdowns.index(changed_dropdown)
                for i in range(4):
                    idx = (start_idx + i + 1) % 4
                    if dropdowns[idx].value == "Slice":
                        dropdowns[idx].value = (
                            "Plot x" if "Plot x" not in current_plots else "Plot y"
                        )
                        break

    # 为每个下拉菜单添加观察者
    for dd in dropdowns:
        dd.observe(handle_dropdown_change, names="value")
    # 使用interactive确保我们可以更新图表
    interactive_plot = interactive(
        plot_data,
        scalar=scalar_dropdown,
        vector=vector_dropdown,
        source_choice=source_dropdown,
        structure_choice=structure_dropdown,
        x_choice=x_dropdown,
        y_choice=y_dropdown,
        z_choice=z_dropdown,
        lam_choice=lam_dropdown,
        slice_index=slider,
    )

    controls = VBox(
        [
            output,
            HBox([scalar_dropdown, vector_dropdown]),
            HBox([V_drop, V_slice, slider]),
        ]
    )

    # 显示布局
    display(controls)


def Draw_box(fig, center, span, face_color, alpha, edge_width=5):
    # Calculate the coordinates of the box vertices
    x0, y0, z0 = center
    dx, dy, dz = span
    x = [
        x0 - dx / 2,
        x0 + dx / 2,
        x0 + dx / 2,
        x0 - dx / 2,
        x0 - dx / 2,
        x0 + dx / 2,
        x0 + dx / 2,
        x0 - dx / 2,
    ]
    y = [
        y0 - dy / 2,
        y0 - dy / 2,
        y0 + dy / 2,
        y0 + dy / 2,
        y0 - dy / 2,
        y0 - dy / 2,
        y0 + dy / 2,
        y0 + dy / 2,
    ]
    z = [
        z0 - dz / 2,
        z0 - dz / 2,
        z0 - dz / 2,
        z0 - dz / 2,
        z0 + dz / 2,
        z0 + dz / 2,
        z0 + dz / 2,
        z0 + dz / 2,
    ]

    # i, j, k indices for the vertices of the triangles
    i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
    j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
    k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]

    # Define the edges of the box
    edges_x = [
        x[0],
        x[1],
        x[2],
        x[3],
        x[0],
        None,
        x[4],
        x[5],
        x[6],
        x[7],
        x[4],
        None,
        x[0],
        x[4],
        None,
        x[1],
        x[5],
        None,
        x[2],
        x[6],
        None,
        x[3],
        x[7],
        None,
    ]
    edges_y = [
        y[0],
        y[1],
        y[2],
        y[3],
        y[0],
        None,
        y[4],
        y[5],
        y[6],
        y[7],
        y[4],
        None,
        y[0],
        y[4],
        None,
        y[1],
        y[5],
        None,
        y[2],
        y[6],
        None,
        y[3],
        y[7],
        None,
    ]
    edges_z = [
        z[0],
        z[1],
        z[2],
        z[3],
        z[0],
        None,
        z[4],
        z[5],
        z[6],
        z[7],
        z[4],
        None,
        z[0],
        z[4],
        None,
        z[1],
        z[5],
        None,
        z[2],
        z[6],
        None,
        z[3],
        z[7],
        None,
    ]

    if alpha == 0:  # Only draw edges if alpha is 0
        fig.add_trace(
            go.Scatter3d(
                x=edges_x,
                y=edges_y,
                z=edges_z,
                mode="lines",
                line=dict(color=face_color, width=edge_width),
                showlegend=False,
            )
        )
    else:  # Draw faces
        fig.add_trace(
            go.Mesh3d(
                x=x,
                y=y,
                z=z,
                i=i,
                j=j,
                k=k,
                color=face_color,
                opacity=alpha,
                flatshading=True,
                showlegend=False,
            )
        )


def Index_1d(values, target_values, return_int=True):
    def find_nearest_index(values, target):
        # 计算最接近的索引
        if isinstance(values, torch.Tensor):
            index = torch.argmin(torch.abs(values - target)).item()
        else:
            index = torch.argmin(torch.abs(torch.tensor(values - target)))
        return int(index) if return_int else index

    # 如果 target_values 是单个数字（不是列表或数组）
    if isinstance(target_values, (int, float)):
        return find_nearest_index(values, target_values)
    else:
        # 如果 target_values 是列表或数组
        nearest_indices = []
        for target in target_values:
            nearest_indices.append(find_nearest_index(values, target))
        return nearest_indices


def interp2d(
    x: torch.Tensor,
    y: torch.Tensor,
    z: torch.Tensor,
    x_new: torch.Tensor,
    y_new: torch.Tensor,
    method: str = "cubic",
) -> torch.Tensor:
    """
    对二维矩阵进行插值（支持实数或复数），基于 scipy.griddata。

    参数：
    - x: 原始 x 坐标（一维 torch tensor）
    - y: 原始 y 坐标（一维 torch tensor）
    - z: 原始二维数据，形状为 (len(x), len(y))，可以是复数 tensor
    - x_new: 新 x 坐标（一维 torch tensor）
    - y_new: 新 y 坐标（一维 torch tensor）
    - method: 插值方法，可选 'linear', 'nearest', 'cubic'

    返回：
    - 插值后的二维 tensor，形状为 (len(x_new), len(y_new))，保留复数结构
    """
    X, Y = torch.meshgrid(x, y, indexing="ij")  # 原始网格
    X_new, Y_new = torch.meshgrid(x_new, y_new, indexing="ij")  # 新网格

    # 转为 numpy
    points = torch.stack([X.flatten(), Y.flatten()], dim=1).cpu().numpy()
    values = z.flatten()
    real_vals = values.real.cpu().numpy()
    imag_vals = values.imag.cpu().numpy() if torch.is_complex(z) else None

    xi = torch.stack([X_new.flatten(), Y_new.flatten()], dim=1).cpu().numpy()

    # 插值
    interp_real = griddata(points, real_vals, xi, method=method, fill_value=0.0)
    if imag_vals is not None:
        interp_imag = griddata(points, imag_vals, xi, method=method, fill_value=0.0)
        interp = interp_real + 1j * interp_imag
    else:
        interp = interp_real

    # 转为 torch tensor，reshape
    interp_tensor = (
        torch.from_numpy(interp.reshape(X_new.shape)).to(z.dtype).to(z.device)
    )
    return interp_tensor
