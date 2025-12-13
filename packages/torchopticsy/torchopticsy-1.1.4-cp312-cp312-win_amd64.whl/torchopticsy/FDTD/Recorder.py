import torch
from torch import floor, zeros
import torchopticsy.Properties as Properties
from torchopticsy.FDTD import Source
from torchopticsy.Utils import Matrix_visualizer
import opticsyCUDA.FDTD as FDTD
import matplotlib.pyplot as plt  # 姑且这么做
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


def get_id_range(pos_m, pos2, offset=0):
    grid = FDTD.get_id_range(pos_m, pos2)  # 必然是偶数
    if grid[1] == pos2.numel() - 3:
        grid[1] -= 2 * offset
    pos2_local = pos2[grid[0] : grid[1] + 1]
    # 处理pos_m的代码放在这里
    # 创建一个布尔掩码，指示pos_m中的每个元素是否位于x_grid指定的范围内
    mask = (pos_m >= pos2[grid[0]]) & (pos_m <= pos2[grid[1]])

    # 使用掩码来筛选pos_m中的元素
    pos_m_clamped = pos_m[mask]

    if not pos_m.numel() == pos_m_clamped.numel():
        print("Monitor pos_m was modified.")
        pos_m = pos_m_clamped

    grid = floor(grid / 2).int()
    grid[1] -= 1
    return grid, pos_m, pos2_local


nearest = True


class Monitor(Properties.Geometry):
    def __init__(self, area, delta, name="DFT", type="nearest", adjoint=False):
        # 有三种类型,nearest,interp和mean
        if type not in ["nearest", "interp", "mean"]:
            raise ValueError("type must be either 'nearest','interp' or 'mean'")
        super().__init__()  # Calls the constructor of the Geometry class
        self.type = type
        self.name = name
        self.delta = delta
        self.x_min = area[0][0]
        self.x_max = area[0][1]
        self.y_min = area[1][0]
        self.y_max = area[1][1]
        self.z_min = area[2][0]
        self.z_max = area[2][1]
        self.item()
        self.xm0, self.ym0, self.zm0 = self.get_posm(delta)
        self.name = name
        self.adjoint = adjoint
        self.adjoint_source = []

    def Initialization(self, fdtd):
        device = fdtd.device
        self.device = device
        self.debug = fdtd.debug
        self.lams = fdtd.lams.view(-1)
        self.xm0 = self.xm0.to(device)
        self.ym0 = self.ym0.to(device)
        self.zm0 = self.zm0.to(device)

        self.x_grid, self.xm, self.x2 = get_id_range(
            self.xm0, fdtd.x2, fdtd.periodic_num[0].cpu()
        )
        self.y_grid, self.ym, self.y2 = get_id_range(
            self.ym0, fdtd.y2, fdtd.periodic_num[1].cpu()
        )
        self.z_grid, self.zm, self.z2 = get_id_range(
            self.zm0, fdtd.z2, fdtd.periodic_num[2].cpu()
        )
        if self.type == "nearest":
            self.xm = self.x2[::2]
            self.ym = self.y2[::2]
            self.zm = self.z2[::2]

        # 获取起点的折射率
        er = torch.mean(
            fdtd.Material_list[
                fdtd.pri_mat_idx[0, self.x_grid[0], self.y_grid[0], self.z_grid[0]]
            ].er
        ).cpu()
        er = torch.real(er)
        mu = 1
        self.index = torch.sqrt(er * mu).item()
        #
        self.dV_co = 1 / (torch.min(fdtd.lams).cpu().item() / fdtd.N_res)
        self.dx2 = self.dV_co * fdtd.dx2[self.x_grid[0] * 2 : self.x_grid[1] * 2 + 3]
        self.dy2 = self.dV_co * fdtd.dy2[self.y_grid[0] * 2 : self.y_grid[1] * 2 + 3]
        self.dz2 = self.dV_co * fdtd.dz2[self.z_grid[0] * 2 : self.z_grid[1] * 2 + 3]

        self.dx = self.dV_co * torch.diff(
            torch.cat(
                [
                    1.5 * self.xm[0:1] - 0.5 * self.xm[1:2],
                    (self.xm[1:] + self.xm[:-1]) / 2,
                    1.5 * self.xm[-1:] - 0.5 * self.xm[-2:-1],
                ],
                dim=0,
            )
        )
        self.dy = self.dV_co * torch.diff(
            torch.cat(
                [
                    1.5 * self.ym[0:1] - 0.5 * self.ym[1:2],
                    (self.ym[1:] + self.ym[:-1]) / 2,
                    1.5 * self.ym[-1:] - 0.5 * self.ym[-2:-1],
                ],
                dim=0,
            )
        )
        self.dz = self.dV_co * torch.diff(
            torch.cat(
                [
                    1.5 * self.zm[0:1] - 0.5 * self.zm[1:2],
                    (self.zm[1:] + self.zm[:-1]) / 2,
                    1.5 * self.zm[-1:] - 0.5 * self.zm[-2:-1],
                ],
                dim=0,
            )
        )

        # 用Python的方式重写数组初始化
        self.Clear(fdtd)
        if self.adjoint:
            self.adjoint_source = Source.AdjointSource(fdtd, self)
        self.fdtd = fdtd

    def override_grid(
        self, structure=None, x=None, y=None, z=None
    ):  # 将监视器的坐标和structure对齐
        if self.debug:
            if self.type == "nearest":
                print("最近邻插值无法覆盖,请使用其它插值模式")
                return
            elif self.type == "interp":
                print("使用interp应当避免材料网格间距大于仿真放大间距")

        device = self.device

        # 如果传入了structure，计算网格坐标
        if structure is not None:
            delta = structure.x_span / structure.shape[0]
            self.xm = torch.linspace(
                structure.x_min + 0.5 * delta,
                structure.x_max - 0.5 * delta,
                structure.shape[0],
                device=device,
            )

            delta = structure.y_span / structure.shape[1]
            self.ym = torch.linspace(
                structure.y_min + 0.5 * delta,
                structure.y_max - 0.5 * delta,
                structure.shape[1],
                device=device,
            )

            delta = structure.z_span / structure.shape[2]
            self.zm = torch.linspace(
                structure.z_min + 0.5 * delta,
                structure.z_max - 0.5 * delta,
                structure.shape[2],
                device=device,
            )
        else:
            # 如果没有传入structure，则根据传入的x, y, z参数来创建网格
            if x is not None:
                self.xm = torch.tensor(x, dtype=torch.float32, device=device)
            if y is not None:
                self.ym = torch.tensor(y, dtype=torch.float32, device=device)
            if z is not None:
                self.zm = torch.tensor(z, dtype=torch.float32, device=device)

        self.dx = self.dV_co * torch.diff(
            torch.cat(
                [
                    1.5 * self.xm[0:1] - 0.5 * self.xm[1:2],
                    (self.xm[1:] + self.xm[:-1]) / 2,
                    1.5 * self.xm[-1:] - 0.5 * self.xm[-2:-1],
                ],
                dim=0,
            )
        )

        self.dy = self.dV_co * torch.diff(
            torch.cat(
                [
                    1.5 * self.ym[0:1] - 0.5 * self.ym[1:2],
                    (self.ym[1:] + self.ym[:-1]) / 2,
                    1.5 * self.ym[-1:] - 0.5 * self.ym[-2:-1],
                ],
                dim=0,
            )
        )

        self.dz = self.dV_co * torch.diff(
            torch.cat(
                [
                    1.5 * self.zm[0:1] - 0.5 * self.zm[1:2],
                    (self.zm[1:] + self.zm[:-1]) / 2,
                    1.5 * self.zm[-1:] - 0.5 * self.zm[-2:-1],
                ],
                dim=0,
            )
        )

    def dV(self, component=[]):
        if component == 0:
            return (
                self.dx2[1::2].view(1, 1, -1, 1, 1, 1)
                * self.dy2[::2].view(1, 1, 1, -1, 1, 1)
                * self.dz2[::2].view(1, 1, 1, 1, -1, 1)
            )
        elif component == 1:
            return (
                self.dx2[::2].view(1, 1, -1, 1, 1, 1)
                * self.dy2[1::2].view(1, 1, 1, -1, 1, 1)
                * self.dz2[::2].view(1, 1, 1, 1, -1, 1)
            )
        elif component == 2:
            return (
                self.dx2[::2].view(1, 1, -1, 1, 1, 1)
                * self.dy2[::2].view(1, 1, 1, -1, 1, 1)
                * self.dz2[1::2].view(1, 1, 1, 1, -1, 1)
            )
        else:
            if self.type == "nearest":
                return (
                    self.dx2[1::2].view(1, 1, -1, 1, 1, 1, 1)
                    * self.dy2[1::2].view(1, 1, 1, -1, 1, 1, 1)
                    * self.dz2[1::2].view(1, 1, 1, 1, -1, 1, 1)
                )
            else:
                return (
                    self.dx.view(1, 1, -1, 1, 1, 1, 1)
                    * self.dy.view(1, 1, 1, -1, 1, 1, 1)
                    * self.dz.view(1, 1, 1, 1, -1, 1, 1)
                )

    # 后续使用CUDA加速
    def Update(self, kernel, Ex, Ey, Ez):
        FDTD.Monitor_Update_E(
            self.Ex,
            self.Ey,
            self.Ez,
            Ex,
            Ey,
            Ez,
            kernel,
            self.x_grid,
            self.y_grid,
            self.z_grid,
        )

    #  后处理,归一化啥的
    # 先不插值.看一看互易性条件
    # 维度为(光源,结构,x,y,z,分量,频率),主要后面有好多东西遵从这个规律,再改就太麻烦了
    def Interp(self):
        # 一定要创建复数torch.complex64,之前吃过亏
        num_sources = self.fdtd.num_sources
        num_structures = self.fdtd.num_structures
        num_frequencies = self.lams.numel()
        self.E = zeros(
            (
                num_sources,
                num_structures,
                self.xm.numel(),
                self.ym.numel(),
                self.zm.numel(),
                3,
                num_frequencies,
            ),
            dtype=torch.complex64,
            device=self.device,
        )
        if self.type == "nearest":
            pad_int = torch.cat(
                [self.Ex[:, :, 0:1], self.Ex, self.Ex[:, :, -1:]], dim=2
            )
            self.E[..., 0, :] = (
                (torch.abs(pad_int[:, :, :-1]) + torch.abs(pad_int[:, :, 1:]))
                / 2
                * torch.exp(1j * torch.angle(pad_int[:, :, :-1] + pad_int[:, :, 1:]))
            )

            pad_int = torch.cat(
                [self.Ey[:, :, :, 0:1], self.Ey, self.Ey[:, :, :, -1:]], dim=3
            )
            self.E[..., 1, :] = (
                (torch.abs(pad_int[:, :, :, :-1]) + torch.abs(pad_int[:, :, :, 1:]))
                / 2
                * torch.exp(
                    1j * torch.angle(pad_int[:, :, :, :-1] + pad_int[:, :, :, 1:])
                )
            )

            pad_int = torch.cat(
                [self.Ez[:, :, :, :, 0:1], self.Ez, self.Ez[:, :, :, :, -1:]], dim=4
            )
            self.E[..., 2, :] = (
                (
                    torch.abs(pad_int[:, :, :, :, :-1])
                    + torch.abs(pad_int[:, :, :, :, 1:])
                )
                / 2
                * torch.exp(
                    1j * torch.angle(pad_int[:, :, :, :, :-1] + pad_int[:, :, :, :, 1:])
                )
            )
        elif self.type == "interp":
            self.E[..., 0, :] = FDTD.Trilinear_interpolation(
                self.x2[1::2],
                self.y2[::2],
                self.z2[::2],
                self.Ex,
                self.xm,
                self.ym,
                self.zm,
                nearest,
            )
            self.E[..., 1, :] = FDTD.Trilinear_interpolation(
                self.x2[::2],
                self.y2[1::2],
                self.z2[::2],
                self.Ey,
                self.xm,
                self.ym,
                self.zm,
                nearest,
            )
            self.E[..., 2, :] = FDTD.Trilinear_interpolation(
                self.x2[::2],
                self.y2[::2],
                self.z2[1::2],
                self.Ez,
                self.xm,
                self.ym,
                self.zm,
                nearest,
            )
        elif self.type == "mean":
            print("功能开发中")

    def Post_Process(self, nor=1):
        # nor放在七位数组的最后一个
        self.Ex = self.Ex / nor
        self.Ey = self.Ey / nor
        self.Ez = self.Ez / nor
        self.Interp()
        # self.H=self.H/nor/Common.eta0

    def Display(self):
        Matrix_visualizer(
            self.E,
            self.xm,
            self.ym,
            self.zm,
            self.lams,
            self.name,
        )

    def Clear(self, fdtd):
        # 用Python的方式重写数组初始化
        num_sources = fdtd.num_sources
        num_structures = fdtd.num_structures
        num_frequencies = self.lams.numel()
        self.Ex = torch.zeros(
            [
                num_sources,
                num_structures,
                self.x_grid[1] - self.x_grid[0] + 1,
                self.y_grid[1] - self.y_grid[0] + 2,
                self.z_grid[1] - self.z_grid[0] + 2,
                num_frequencies,
            ],
            dtype=torch.complex64,
            device=fdtd.device,
        )
        self.Ey = torch.zeros(
            [
                num_sources,
                num_structures,
                self.x_grid[1] - self.x_grid[0] + 2,
                self.y_grid[1] - self.y_grid[0] + 1,
                self.z_grid[1] - self.z_grid[0] + 2,
                num_frequencies,
            ],
            dtype=torch.complex64,
            device=fdtd.device,
        )
        self.Ez = torch.zeros(
            [
                num_sources,
                num_structures,
                self.x_grid[1] - self.x_grid[0] + 2,
                self.y_grid[1] - self.y_grid[0] + 2,
                self.z_grid[1] - self.z_grid[0] + 1,
                num_frequencies,
            ],
            dtype=torch.complex64,
            device=fdtd.device,
        )

    def Get_dP_interp(self, mat1, mat0, eps_delta, sigma):  # 纯验证作用,最后不会使用
        # 必须在正向仿真后进行
        # mat1是新的密度矩阵,支持梯度.mat0是旧的,纯数值.(结构,x,y,z)
        w = 2 * torch.pi * self.fdtd.f.reshape(1, 1, 1, 1, 1, 1, -1)
        eps_delta = eps_delta.view(1, 1, 1, 1, 1, 1, -1)
        dP = (
            self.E
            * (
                eps_delta
                + 1j
                * sigma
                / w
                * (-2 * mat0.unsqueeze(0).unsqueeze(-1).unsqueeze(-1) + 1)
            )
            * (mat1 - mat0).unsqueeze(0).unsqueeze(-1).unsqueeze(-1)
        )
        Px_E_interp = FDTD.Trilinear_reverse_interpolation(
            self.x2[1::2],
            self.y2[::2],
            self.z2[::2],
            dP[..., 0, :] * self.dV()[..., 0, :],
            self.xm,
            self.ym,
            self.zm,
        ) / self.dV(0)
        Py_E_interp = FDTD.Trilinear_reverse_interpolation(
            self.x2[::2],
            self.y2[1::2],
            self.z2[::2],
            dP[..., 1, :] * self.dV()[..., 0, :],
            self.xm,
            self.ym,
            self.zm,
        ) / self.dV(1)
        Pz_E_interp = FDTD.Trilinear_reverse_interpolation(
            self.x2[::2],
            self.y2[::2],
            self.z2[1::2],
            dP[..., 2, :] * self.dV()[..., 0, :],
            self.xm,
            self.ym,
            self.zm,
        ) / self.dV(2)
        return dP, Px_E_interp, Py_E_interp, Pz_E_interp
        # 这些东西真得先算好,因为后面不动了

    def AdjustAdjointSource(self, FOM, x):  # 只用获取关于E的偏导,因此x是无需任何计算的
        # 确保此前x.grad=False
        if not self.adjoint_source:
            print("Not set as a adjoint monitor")
        self.Ex.requires_grad = True
        self.Ey.requires_grad = True
        self.Ez.requires_grad = True
        x.requires_grad = False
        self.Interp()
        target, _ = FOM(self.E, x.detach())
        target.backward()
        self.Ex.requires_grad = False
        self.Ey.requires_grad = False
        self.Ez.requires_grad = False
        # Replace NaN values in gradients with 0
        Ex_grad_nonan = torch.nan_to_num(self.Ex.grad)
        Ey_grad_nonan = torch.nan_to_num(self.Ey.grad)
        Ez_grad_nonan = torch.nan_to_num(self.Ez.grad)

        # 清空梯度
        self.Ex.grad.zero_()
        self.Ey.grad.zero_()
        self.Ez.grad.zero_()

        # Adjust the adjoint source with the non-NaN gradients
        self.adjoint_source.Adjust(
            torch.conj(Ex_grad_nonan),
            torch.conj(Ey_grad_nonan),
            torch.conj(Ez_grad_nonan),
            True,
        )


class Movie(Properties.Geometry):
    """
    Movie - 时间域监视器
    """

    def __init__(self, area, delta, name="Movie"):
        super().__init__()  # Calls the constructor of the Geometry class
        self.name = name
        self.delta = delta
        self.x_min = area[0][0]
        self.x_max = area[0][1]
        self.y_min = area[1][0]
        self.y_max = area[1][1]
        self.z_min = area[2][0]
        self.z_max = area[2][1]
        self.item()
        self.xm0, self.ym0, self.zm0 = self.get_posm(delta)
        self.t_arr_sample = None
        self.delta_step = 10

    def Clear(self):
        self.E = 0 * self.E

    def Draw(self, fig):
        super().Draw(fig, face_color="yellow", alpha=0)

    def Initialization(self, fdtd):
        device = fdtd.device
        self.device = device
        self.lams = fdtd.lams.view(-1)
        self.xm0 = self.xm0.to(device)
        self.ym0 = self.ym0.to(device)
        self.zm0 = self.zm0.to(device)

        self.x_grid, self.xm, self.x2 = get_id_range(
            self.xm0, fdtd.x2, fdtd.periodic_num[0].cpu()
        )
        self.y_grid, self.ym, self.y2 = get_id_range(
            self.ym0, fdtd.y2, fdtd.periodic_num[1].cpu()
        )
        self.z_grid, self.zm, self.z2 = get_id_range(
            self.zm0, fdtd.z2, fdtd.periodic_num[2].cpu()
        )
        self.xm = self.x2[::2]
        self.ym = self.y2[::2]
        self.zm = self.z2[::2]

        self.t_arr_sample = fdtd.t_arr[:: self.delta_step]
        grid_shape = (
            self.x_grid[1] - self.x_grid[0] + 2,
            self.y_grid[1] - self.y_grid[0] + 2,
            self.z_grid[1] - self.z_grid[0] + 2,
            3,
            len(self.t_arr_sample),
        )
        self.E = torch.zeros(grid_shape).to(fdtd.device)
        self.H = torch.zeros(grid_shape).to(fdtd.device)

    def Update(self, step, Ex, Ey, Ez):
        if step % self.delta_step == 0:
            Ex = Ex[
                self.x_grid[0] : self.x_grid[1] + 1,
                self.y_grid[0] : self.y_grid[1] + 2,
                self.z_grid[0] : self.z_grid[1] + 2,
            ].clone()
            Ey = Ey[
                self.x_grid[0] : self.x_grid[1] + 2,
                self.y_grid[0] : self.y_grid[1] + 1,
                self.z_grid[0] : self.z_grid[1] + 2,
            ].clone()
            Ez = Ez[
                self.x_grid[0] : self.x_grid[1] + 2,
                self.y_grid[0] : self.y_grid[1] + 2,
                self.z_grid[0] : self.z_grid[1] + 1,
            ].clone()
            index = step // self.delta_step
            # Ex 填充和平均计算
            pad_int = torch.cat([Ex[0:1, :, :], Ex, Ex[-1:, :, :]], dim=0)
            self.E[:, :, :, 0, index] = 0.5 * (pad_int[:-1, :, :] + pad_int[1:, :, :])

            # Ey 填充和平均计算
            pad_int = torch.cat([Ey[:, 0:1, :], Ey, Ey[:, -1:, :]], dim=1)
            self.E[:, :, :, 1, index] = 0.5 * (pad_int[:, :-1, :] + pad_int[:, 1:, :])

            # Ez 填充和平均计算
            pad_int = torch.cat([Ez[:, :, 0:1], Ez, Ez[:, :, -1:]], dim=2)
            self.E[:, :, :, 2, index] = 0.5 * (pad_int[:, :, -1:] + pad_int[:, :, 1:])

    def Display(self, fdtd):
        Movie.Matrix_visualizer(
            self.E, self.xm, self.ym, self.zm, self.t_arr_sample, self.name
        )

    @staticmethod
    def Matrix_visualizer(M, x, y, z, t, name=""):
        output = Output()
        shape = [M.shape[0], M.shape[1], M.shape[2], M.shape[4]]
        slice_list = [x, y, z, t]
        # 当前选择的维度3.
        current_dimension = "z"
        # 初始化一个字典来存储每个维度的滑块位置
        slider_positions = {"x": 0, "y": 0, "z": 0, "t": 0}

        def plot_data(
            scalar, vector, x_choice, y_choice, z_choice, t_choice, slice_index
        ):
            with output:
                output.clear_output(wait=True)  # 清除之前的图形
                slider_temp = slider_positions.copy()
                slider_temp[current_dimension] = slice_index
                # 根据选择的向量分量更新数据
                if vector == "x":
                    data = M[:, :, :, 0, :]
                elif vector == "y":
                    data = M[:, :, :, 1, :]
                elif vector == "z":
                    data = M[:, :, :, 2, :]
                elif vector == "Magnitude":
                    data = torch.sqrt(torch.sum(torch.abs(M) ** 2, axis=3))

                # 根据选择处理数据
                if scalar == "Re":
                    data = torch.real(data)
                elif scalar == "Im":
                    data = torch.imag(data)
                elif scalar == "Abs":
                    data = torch.abs(data)
                elif scalar == "Angle":
                    data = torch.angle(data)

                choices = [x_choice, y_choice, z_choice, t_choice]
                # 根据选择的维度切片数据
                slices = [
                    slice(None),
                    slice(None),
                    slice(None),
                    slice(None),
                ]  # 默认为全选
                for dim, slice_value in enumerate(choices):
                    if slice_value == "Slice":
                        key = ["x", "y", "z", "t"][dim]
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

                idx = set(range(4)) - {idxX, idxY}

                # 使用 permute 重新排列张量的维度
                data = data.permute(idxX, idxY, *idx)
                X, Y = torch.meshgrid(slice_list[idxX], slice_list[idxY], indexing="ij")
                plt.subplot()
                plt.pcolormesh(
                    X.cpu(), Y.cpu(), torch.squeeze(data, axis=(2, 3)).cpu(), cmap="jet"
                )
                plt.colorbar()
                plt.show()

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
        t_dropdown = Dropdown(
            options=["Plot x", "Plot y", "Slice"],
            value="Slice",
            description="t",
            style=common_style,
            layout=layout0,
        )
        dropdowns = [x_dropdown, y_dropdown, z_dropdown, t_dropdown]
        V_drop = VBox(dropdowns)
        x_slice_button = Button(description="", layout=layout1)
        y_slice_button = Button(description="", layout=layout1)
        z_slice_button = Button(description="", layout=layout1)
        t_slice_button = Button(description="", layout=layout1)
        slice_button = [x_slice_button, y_slice_button, z_slice_button, t_slice_button]
        V_slice = VBox(slice_button)

        # 定义按钮点击事件处理函数
        # 创建一个函数，该函数返回一个事件处理函数
        def create_button_handler(tag):
            def on_button_clicked(b):
                nonlocal current_dimension  # 使用 nonlocal 声
                slider_positions[current_dimension] = slider.value
                current_dimension = tag
                # 先更新最大值,再更新当前值
                dim_index = {"x": 0, "y": 1, "z": 2, "t": 3}[current_dimension]
                slider.max = shape[dim_index] - 1
                slider.value = slider_positions[current_dimension]
                slider.description = tag

            return on_button_clicked

        x_slice_button.on_click(create_button_handler("x"))
        y_slice_button.on_click(create_button_handler("y"))
        z_slice_button.on_click(create_button_handler("z"))
        t_slice_button.on_click(create_button_handler("t"))

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
                    dd.value
                    for dd in other_dropdowns
                    if dd.value in ["Plot x", "Plot y"]
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
            x_choice=x_dropdown,
            y_choice=y_dropdown,
            z_choice=z_dropdown,
            t_choice=t_dropdown,
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
