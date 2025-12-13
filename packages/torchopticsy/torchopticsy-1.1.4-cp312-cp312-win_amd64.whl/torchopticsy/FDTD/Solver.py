import torch
from torch import tensor, ones
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import torchopticsy.Utils as Utils
import torchopticsy.Properties as Properties
from torchopticsy.FDTD import Recorder, Source, Structure
import torch.nn.functional as F
import opticsyCUDA.FDTD as FDTD_CUDA_Dispersion
import opticsyCUDA.FDTD4 as FDTD_CUDA_MONO

dnds = 0.04
# 非均匀插值函数有问题!!!!主要是周期性边界条件自动扩充了一格,实际上是不需要的因为统一扩充了,这是方便在非均匀网格和均匀网格之间变化
# 暂时不用非均匀网格的问题是伴随源的求解有点小问题.


# 对于正向模拟,将PML替换为Metal作为副本执行一遍,得到收敛能量,用于后续判定.,能量数组为(光源,波长)
# 对于伴随模拟,正向模拟中记录最长的模拟时间步长,作为下次伴随模拟的时间步长.
# 我还是希望解决斜入射的精度问题,因为这感觉还是有影响的
# 我猜测原本之所以需要5个时间步长来模拟这个东西,主要还是因为伪散射波的串扰.
def E_Property_Periodic(x, y, z, periodic_num):
    # 主要是权重的索引数组周期性赋值.
    # 现在xyz都是(结构并行,x,y,z)
    if periodic_num[0] > 0:
        x[:, -1, :, :] = x[:, 0, :, :]
        y[:, -1, :, :] = y[:, 1, :, :]
        y[:, -2, :, :] = y[:, 0, :, :]
        z[:, -1, :, :] = z[:, 1, :, :]
        z[:, -2, :, :] = z[:, 0, :, :]
    if periodic_num[1] > 0:
        y[:, :, -1, :] = y[:, :, 0, :]
        x[:, :, -1, :] = x[:, :, 1, :]
        x[:, :, -2, :] = x[:, :, 0, :]
        z[:, :, -1, :] = z[:, :, 1, :]
        z[:, :, -2, :] = z[:, :, 0, :]
    if periodic_num[2] > 0:
        z[:, :, :, -1] = z[:, :, :, 0]
        y[:, :, :, -1] = y[:, :, :, 1]
        y[:, :, :, -2] = y[:, :, :, 0]
        x[:, :, :, -1] = x[:, :, :, 1]
        x[:, :, :, -2] = x[:, :, :, 0]
    return x, y, z


def kadw2(w2, ka2=None):
    """
    返回κdp差分数组, 用于计算DH更新系数
    :param dim: 维度
    :param w2: 输入数组 w2
    :param ka2: 输入数组 ka2，如果未提供，则默认为与 w2 同形状的全1数组
    :return: 处理后的数组 kap
    默认周期性,因为非周期结构用不到两端的系数.
    """
    device = w2.device
    if ka2 is None:
        ka2 = torch.ones_like(w2).to(device)

    kap = torch.zeros_like(w2).to(device)
    kap[0::2] = (
        torch.diff(
            torch.cat(
                (w2[-2:-1] - w2[-1:] + w2[:1], w2[1::2], w2[-1] + w2[1:2] - w2[:1])
            )
        )
        * ka2[0::2]
    )
    kap[1::2] = torch.diff(w2[0::2]) * ka2[1::2]
    return kap


def PML2_kabc(dt, w2, PML_num1, ka_max=2, m=3):
    device = w2.device
    d = (w2[2] - w2[0]) * PML_num1
    len2 = w2.shape[0]

    R0 = -8  # 误差水平exp(R0)
    sig_max = -(m + 1) * R0 / (2 * d * Utils.eta0)
    a_max = 0.05
    m_a = 1

    ka2 = torch.ones(len2).to(device)
    sig2 = torch.zeros(len2).to(device)
    a2 = a_max * torch.ones(len2).to(device)

    # 计算小于起始序号的部分
    temp = 2 * PML_num1
    ids_left = torch.arange(temp).to(device)
    w_d = (temp - ids_left) / (2 * PML_num1)

    w_d *= 2
    ka2[ids_left.long()] = 1 + (ka_max - 1) * (w_d) ** m
    w_d[w_d > 1] = 1
    sig2[ids_left.long()] = sig_max * (w_d) ** m
    a2[ids_left.long()] = a_max * (1 - w_d) ** m_a

    # 计算大于终止序号的部分
    temp = len2 - 2 * PML_num1
    ids_right = torch.arange(temp, len2).to(device)
    w_d = (ids_right - temp + 1) / (2 * PML_num1)

    w_d *= 2
    ka2[ids_right.long()] = 1 + (ka_max - 1) * (w_d) ** m
    w_d[w_d > 1] = 1
    sig2[ids_right.long()] = sig_max * (w_d) ** m
    a2[ids_right.long()] = a_max * (1 - w_d) ** m_a

    b2 = torch.exp(-dt / Utils.eps0 * (sig2 / ka2 + a2)).to(device)
    c2 = sig2 / (sig2 * ka2 + ka2**2 * a2) * (b2 - 1)

    return ka2, b2, c2


class FDTD_Solver(Properties.Geometry):
    """
    FDTD Class - Inherits from Geometry
    所有的矢量按照(x, y, z, 3)的形式记录。
    最小网格对应最短介质波长的1/10。

    一般用高斯源，确定最大频率f_max，时间带宽0.5/f_max。
    t0>6倍时间带宽, 确保振幅是缓慢增加的。
    稳定性条件: dt < n_min / c / sqrt(1/dx^2 + 1/dy^2 + 1/dz^2)
    t_prop = (5nz/c + 12self.tau) / dt

    网格色散引起慢波和各向异性, 暂时不处理。
    """

    def __init__(
        self,
        area,
        bound_arr,
        lams,
        N_res=10,
        subcell=True,
        T_co=1,
        num_sources=1,
        num_structures=1,
        auto_shutoff_min=1e-4,
        debug_log=True,
        dt_stable_co=0.99,
        dispersion=False,
    ):
        super().__init__()
        self.debug = debug_log
        self.dispersion = dispersion
        self.device = "cuda"  # 其实只支持cuda
        area = tensor(area)
        self.x_min, self.y_min, self.z_min = area[:, 0]
        self.x_max, self.y_max, self.z_max = area[:, 1]
        self.item()

        # 验证 bound_arr 在指定选项内
        assert all(b in ["Metal", "PML", "Periodic"] for b in bound_arr)

        self.auto_shutoff_min = auto_shutoff_min
        self.bound_arr = bound_arr  # 赋值给对象
        self.PML_num = torch.tensor([0, 0, 0], dtype=torch.int32).to(self.device)
        self.periodic_num = torch.tensor([0, 0, 0], dtype=torch.int32).to(self.device)
        self.boundary_color = [""] * 3
        for i in range(3):
            if self.bound_arr[i] == "PML":
                self.PML_num[i] = 16
                self.boundary_color[i] = "red"
            elif self.bound_arr[i] == "Periodic":
                self.periodic_num[i] = 1
                self.boundary_color[i] = "green"
            elif self.bound_arr[i] == "Metal":
                self.boundary_color[i] = "blue"

        self.num_sources = num_sources
        self.num_structures = num_structures
        # 时间参数
        self.dt_stable_co = dt_stable_co
        self.dt = 1e-10
        self.t_arr = []  # n*1
        self.T_co = T_co
        self.steps = 1000
        self.tau = []

        # 频率参数
        lams = torch.tensor(lams, dtype=torch.float32).to(self.device)
        self.lams = lams.reshape((1, -1))  # 重塑lams
        self.f = Utils.c / self.lams
        # self.f_mean=torch.mean(self.f)
        self.n_max = []
        self.Kernel = []  # 频率变换核函数
        self.Kernel_arr = []  # 变换数组, (1,1,1,1,lam,T)

        # 空间参数
        self.subcell = subcell
        self.N_res = N_res  # 每个波长10个点
        self.x2 = self.y2 = self.z2 = []
        self.dx2 = self.dy2 = self.dz2 = []  # 用于计算总能量, 用于早停

        # 常规更新参数
        self.Cx = self.Cy = self.Cz = []

        # CPML参数
        self.bx = self.by = self.bz = []
        self.cx = self.cy = self.cz = torch.zeros([0, 2])

        # 光源, 监视器, 结构
        self.sources = []  # 光源, 暂时只有一个!
        self.monitors = []  # 监视器
        self.movies = []  # 监视器
        self.structures = []  # 结构, 暂时只允许方格

        # 测试参数
        self.energys = []
        self.Nx = None
        self.Ny = None
        self.Nz = None

    def Initialize(self):  # 待会去掉
        # 初始化，计算中间参数以及复用参数
        # 第一步就应该先添加材料,因为要确定网格.注意要初始化
        self.material_dic = {}
        self.Material_list = []
        id = 0
        # 添加空气
        self.Material_list.append(Properties.Material("Air", self.lams))
        id += 1
        for structure in self.structures:
            if structure.material not in self.material_dic:
                self.Material_list.append(
                    Properties.Material(structure.material, self.lams)
                )
                self.material_dic[structure.material] = id
                id += 1

        self.n_max = max(
            torch.max(torch.real(m.index)) for m in self.Material_list
        ).item()
        print("系统最大折射率", self.n_max)
        ds_2 = (
            torch.min(self.lams).item() / self.n_max / self.N_res / 2
        )  # 2x网格的最小长度

        # # 空间参数初始化

        # 非均匀网格的处理
        # indexs = torch.zeros(len(self.structures))
        # blocks = torch.zeros(2, len(self.structures))

        # for i in range(len(indexs)):
        #     indexs[i] = self.structures[i].index
        #     blocks[0, i] = self.structures[i].x_min
        #     blocks[1, i] = self.structures[i].x_max
        # self.x2 = FDTD_AUX_CUDA.GenerateNonUniformGrid(self.N_res, torch.min(self.lams).item(), torch.tensor([self.x_min, self.x_max]), blocks, indexs, 0.1,self.periodic_num[0]>0).to(self.device)
        nx = 1 + int(self.x_span / ds_2 / 2)
        self.x2 = torch.linspace(self.x_min, self.x_max, nx * 2 + 1).to(self.device)

        # for i in range(len(indexs)):
        #     blocks[0, i] = self.structures[i].y_min
        #     blocks[1, i] = self.structures[i].y_max
        # self.y2 = FDTD_AUX_CUDA.GenerateNonUniformGrid(self.N_res, torch.min(self.lams).item(),
        # torch.tensor([self.y_min, self.y_max]).cpu(), blocks.cpu(), indexs.cpu(), 0.1,self.periodic_num[1]>0).to(self.device)
        ny = 1 + int(self.y_span / ds_2 / 2)
        self.y2 = torch.linspace(self.y_min, self.y_max, ny * 2 + 1).to(self.device)

        # for i in range(len(indexs)):
        #     blocks[0, i] = self.structures[i].z_min
        #     blocks[1, i] = self.structures[i].z_max
        # self.z2 = FDTD_AUX_CUDA.GenerateNonUniformGrid(self.N_res, torch.min(self.lams).item(), torch.tensor([self.z_min, self.z_max]).cpu(), blocks.cpu(), indexs.cpu(), 0.1,self.periodic_num[2]>0).to(self.device)
        nz = 1 + int(self.z_span / ds_2 / 2)
        self.z2 = torch.linspace(self.z_min, self.z_max, nz * 2 + 1).to(self.device)

        # 时间参数
        # 时间参数
        self.dt = (
            (
                self.dt_stable_co
                / Utils.c
                / torch.sqrt(
                    1 / (self.x2[2] - self.x2[0]) ** 2
                    + 1 / (self.y2[2] - self.y2[0]) ** 2
                    + 1 / (self.z2[2] - self.z2[0]) ** 2
                )
            )
            .cpu()
            .item()
        )
        self.Kernel = torch.exp(2j * torch.pi * self.dt * self.f).to(
            self.device
        )  # 计算变换核函数
        self.tau = 1.75 / torch.max(self.f).item()
        T = (
            self.T_co * 5 * self.n_max * self.z_span / Utils.c
            + 2 * Source.t_offset * self.tau
        )
        self.steps = round(T / self.dt)
        self.base_steps = round(
            (2 * self.n_max * self.z_span / Utils.c + 2 * Source.t_offset * self.tau)
            / self.dt
        )

        print("总时间步数", self.steps, "基本步数", self.base_steps)
        self.t_arr = (
            torch.arange(1, self.steps + 1).to(self.device).view(-1, 1) * self.dt
        )

        # 频率参数
        T = torch.arange(self.steps).to(self.device).view(self.steps, 1)
        self.Kernel_arr = self.Kernel**T
        # 边界条件处理

        # 更新 PML 层的坐标

        pml_x_left = (
            torch.linspace(-2 * self.PML_num[0], -1, 2 * self.PML_num[0]).to(
                self.device
            )
            * (self.x2[1] - self.x2[0])
            + self.x2[0]
        )
        pml_x_right = (
            torch.linspace(
                1,
                2 * (self.PML_num[0] + self.periodic_num[0]),
                2 * (self.PML_num[0] + self.periodic_num[0]),
            ).to(self.device)
            * (self.x2[-1] - self.x2[-2])
            + self.x2[-1]
        )
        self.x2 = torch.cat([pml_x_left, self.x2, pml_x_right])
        nx += 2 * self.PML_num[0] + self.periodic_num[0]

        pml_y_left = (
            torch.linspace(-2 * self.PML_num[1], -1, 2 * self.PML_num[1]).to(
                self.device
            )
            * (self.y2[1] - self.y2[0])
            + self.y2[0]
        )
        pml_y_right = (
            torch.linspace(
                1,
                2 * (self.PML_num[1] + self.periodic_num[1]),
                2 * (self.PML_num[1] + self.periodic_num[1]),
            ).to(self.device)
            * (self.y2[-1] - self.y2[-2])
            + self.y2[-1]
        )
        self.y2 = torch.cat([pml_y_left, self.y2, pml_y_right])
        ny += 2 * self.PML_num[1] + self.periodic_num[1]

        pml_z_left = (
            torch.linspace(-2 * self.PML_num[2], -1, 2 * self.PML_num[2]).to(
                self.device
            )
            * (self.z2[1] - self.z2[0])
            + self.z2[0]
        )
        pml_z_right = (
            torch.linspace(
                1,
                2 * (self.PML_num[2] + self.periodic_num[2]),
                2 * (self.PML_num[2] + self.periodic_num[2]),
            ).to(self.device)
            * (self.z2[-1] - self.z2[-2])
            + self.z2[-1]
        )
        self.z2 = torch.cat([pml_z_left, self.z2, pml_z_right])
        nz += 2 * self.PML_num[2] + self.periodic_num[2]
        # 计算差分值

        self.nx = nx
        self.ny = ny
        self.nz = nz

        self.dx2 = kadw2(self.x2)
        self.dy2 = kadw2(self.y2)
        self.dz2 = kadw2(self.z2)

        # 更新参数
        # 假设 FDTD_Solver_3D.PML2_kabc 和 FDTD_Solver_3D.kadw2 已经定义
        kax2, self.bx2, self.cx2 = PML2_kabc(self.dt, self.x2, self.PML_num[0])
        kay2, self.by2, self.cy2 = PML2_kabc(self.dt, self.y2, self.PML_num[1])
        kaz2, self.bz2, self.cz2 = PML2_kabc(self.dt, self.z2, self.PML_num[2])
        self.cx2 *= Utils.c * self.dt / kadw2(self.x2)
        self.cy2 *= Utils.c * self.dt / kadw2(self.y2)
        self.cz2 *= Utils.c * self.dt / kadw2(self.z2)
        # 常规更新参数
        self.Cx = Utils.c * self.dt / kadw2(self.x2, kax2)
        self.Cy = Utils.c * self.dt / kadw2(self.y2, kay2)
        self.Cz = Utils.c * self.dt / kadw2(self.z2, kaz2)

        self.PML_idx = torch.zeros([2 * self.PML_num[0]], dtype=torch.int)
        self.PML_idy = torch.zeros([2 * self.PML_num[1]], dtype=torch.int)
        self.PML_idz = torch.zeros([2 * self.PML_num[2]], dtype=torch.int)
        for i in range(self.PML_num[0]):
            self.PML_idx[i] = i * 2
            self.PML_idx[i + self.PML_num[0]] = 2 * (i + nx - self.PML_num[0])
        for i in range(self.PML_num[1]):
            self.PML_idy[i] = i * 2
            self.PML_idy[i + self.PML_num[1]] = 2 * (i + ny - self.PML_num[1])
        for i in range(self.PML_num[2]):
            self.PML_idz[i] = i * 2
            self.PML_idz[i + self.PML_num[2]] = 2 * (i + nz - self.PML_num[2])

        # 计算材料和色散参数
        self.er_inf_list = []
        self.kp_list = []
        self.bp_list = []

        for mat in self.Material_list:
            mat.Initialization(self)
        self.er = torch.zeros(
            [len(self.Material_list), self.lams.numel()],
            dtype=torch.complex64,
            device=self.device,
        )
        self.f_co = torch.zeros_like(self.er, dtype=torch.float32)
        self.er_mean = torch.zeros(
            [len(self.Material_list)], dtype=torch.complex64, device=self.device
        )

        # 原先的无补偿版本
        # for i in range(len(self.Material_list)):
        #     self.er[i] = self.Material_list[i].er
        #     self.er_mean[i] = torch.mean(self.Material_list[i].er)
        # end
        # 暂定的数值色散版本
        lams = self.lams.view(-1)
        for i in range(len(self.Material_list)):
            self.er[i] = self.Material_list[i].er
            n = torch.abs(torch.sqrt(self.er[i]))
            f = torch.sinc(n * ds_2 * 2 / lams) / torch.sinc(Utils.c * self.dt / lams)
            self.f_co[i] = f
            self.er[i] *= f**2
            self.er_mean[i] = torch.mean(self.Material_list[i].er)
        if self.dispersion == False:
            self.er = self.er[:, 0:1]
            self.f_co = self.f_co[:, 0:1]
        # end

        # self.pri_weightx = torch.ones(nx, ny+1, nz+1, device=self.device)
        # self.pri_weighty = torch.ones(nx+1, ny, nz+1, device=self.device)
        # self.pri_weightz = torch.ones(nx+1, ny+1, nz, device=self.device)
        # self.Nx = torch.zeros(nx, ny+1, nz+1, 3, device=self.device)
        # self.Ny = torch.zeros(nx+1, ny, nz+1, 3, device=self.device)
        # self.Nz = torch.zeros(nx+1, ny+1, nz, 3, device=self.device)
        # #还没有开更好呢
        # self.ax = torch.zeros(nx, ny+1, nz+1, device=self.device)
        # self.ay = torch.zeros(nx+1, ny, nz+1, device=self.device)
        # self.az = torch.zeros(nx+1, ny+1, nz, device=self.device)

        # self.pri_mat_idx = torch.zeros_like(self.pri_weightx,dtype=torch.uint8)
        # self.pri_mat_idy = torch.zeros_like(self.pri_weighty,dtype=torch.uint8)
        # self.pri_mat_idz = torch.zeros_like(self.pri_weightz,dtype=torch.uint8)

        # self.sec_mat_idx = torch.zeros_like(self.pri_mat_idx)
        # self.sec_mat_idy = torch.zeros_like(self.pri_mat_idy)
        # self.sec_mat_idz = torch.zeros_like(self.pri_mat_idz)

        self.er_inf_list = tensor(self.er_inf_list, device=self.device)
        self.kp_list = tensor(self.kp_list, device=self.device)
        self.bp_list = tensor(self.bp_list, device=self.device)

        priorities = [structure.priority for structure in self.structures]
        sorted_indices = sorted(
            range(len(priorities)), key=lambda i: priorities[i], reverse=True
        )
        self.structures = [self.structures[i] for i in sorted_indices]

        if self.dispersion:
            self.Reset_structure_Dispersion(True)
        else:
            self.Reset_structure_MONO(True)
        # 材料
        # self.sigmadt_2x=torch.zeros_like(self.pri_weightx)
        # self.sigmadt_2y=torch.zeros_like(self.pri_weighty)
        # self.sigmadt_2z=torch.zeros_like(self.pri_weightz)

        # for structure in self.structures:
        #     structure.Initialization(self)
        # 初始化光源、监视器、结构
        for source in self.sources:
            source.Initialization(self)

        for monitor in self.monitors:
            monitor.Initialization(self)

        for movie in self.movies:
            movie.Initialization(self)

        # self.pri_mat_idx,self.pri_mat_idy,self.pri_mat_idz=FDTD_Solver_3D.E_Property_Periodic(self.pri_mat_idx,self.pri_mat_idy,self.pri_mat_idz,self.periodic_num)
        # self.sec_mat_idx,self.sec_mat_idy,self.sec_mat_idz=FDTD_Solver_3D.E_Property_Periodic(self.sec_mat_idx,self.sec_mat_idy,self.sec_mat_idz,self.periodic_num)

    def Reset_structure_Dispersion(self, start):
        # 第一次调用,是简单体积平均
        # 第二次调用,如果subcell为True,则运用子像素平滑.然后不管怎样,都清空不需要的辅助变量,给后续的仿真腾出显存.
        nx, ny, nz = self.nx, self.ny, self.nz
        if start:
            # 重置材料
            self.epsbeta_x = torch.ones(
                self.num_structures,
                nx,
                ny + 1,
                nz + 1,
                device=self.device,
            )
            self.epsbeta_y = torch.ones(
                self.num_structures,
                nx + 1,
                ny,
                nz + 1,
                device=self.device,
            )
            self.epsbeta_z = torch.ones(
                self.num_structures,
                nx + 1,
                ny + 1,
                nz,
                device=self.device,
            )

            self.pri_weightx = torch.ones(
                self.num_structures, nx, ny + 1, nz + 1, device=self.device
            )
            self.pri_weighty = torch.ones(
                self.num_structures, nx + 1, ny, nz + 1, device=self.device
            )
            self.pri_weightz = torch.ones(
                self.num_structures, nx + 1, ny + 1, nz, device=self.device
            )

            self.pri_mat_idx = torch.zeros(
                self.num_structures,
                nx,
                ny + 1,
                nz + 1,
                dtype=torch.uint8,
                device=self.device,
            )
            self.pri_mat_idy = torch.zeros(
                self.num_structures,
                nx + 1,
                ny,
                nz + 1,
                dtype=torch.uint8,
                device=self.device,
            )
            self.pri_mat_idz = torch.zeros(
                self.num_structures,
                nx + 1,
                ny + 1,
                nz,
                dtype=torch.uint8,
                device=self.device,
            )

            self.sec_mat_idx = torch.zeros_like(self.pri_mat_idx)
            self.sec_mat_idy = torch.zeros_like(self.pri_mat_idy)
            self.sec_mat_idz = torch.zeros_like(self.pri_mat_idz)

            self.sigmadt_2x = torch.zeros(
                self.num_structures, nx, ny + 1, nz + 1, device=self.device
            )
            self.sigmadt_2y = torch.zeros(
                self.num_structures, nx + 1, ny, nz + 1, device=self.device
            )
            self.sigmadt_2z = torch.zeros(
                self.num_structures, nx + 1, ny + 1, nz, device=self.device
            )

            for structure in self.structures:
                structure.Initialization(self)

            self.pri_weightx, self.pri_weighty, self.pri_weightz = E_Property_Periodic(
                self.pri_weightx,
                self.pri_weighty,
                self.pri_weightz,
                self.periodic_num,
            )
            self.pri_mat_idx, self.pri_mat_idy, self.pri_mat_idz = E_Property_Periodic(
                self.pri_mat_idx, self.pri_mat_idy, self.pri_mat_idz, self.periodic_num
            )
            self.sec_mat_idx, self.sec_mat_idy, self.sec_mat_idz = E_Property_Periodic(
                self.sec_mat_idx, self.sec_mat_idy, self.sec_mat_idz, self.periodic_num
            )

            FDTD_CUDA_Dispersion.Set_ER_average(
                self.epsbeta_x,
                self.pri_weightx,
                self.pri_mat_idx,
                self.sec_mat_idx,
                self.er_inf_list,
            )
            FDTD_CUDA_Dispersion.Set_ER_average(
                self.epsbeta_y,
                self.pri_weighty,
                self.pri_mat_idy,
                self.sec_mat_idy,
                self.er_inf_list,
            )
            FDTD_CUDA_Dispersion.Set_ER_average(
                self.epsbeta_z,
                self.pri_weightz,
                self.pri_mat_idz,
                self.sec_mat_idz,
                self.er_inf_list,
            )

            self.sigmadt_2x, self.sigmadt_2y, self.sigmadt_2z = E_Property_Periodic(
                self.sigmadt_2x, self.sigmadt_2y, self.sigmadt_2z, self.periodic_num
            )
        else:
            if self.subcell:
                # 取首位波长作为计算的依据
                pri_weightx = self.epsbeta_x.clone()
                pri_weighty = self.epsbeta_y.clone()
                pri_weightz = self.epsbeta_z.clone()

                if self.periodic_num[0] > 0:
                    pri_weightx = pri_weightx[:, :-1, :, :]
                    pri_weighty = pri_weighty[:, :-2, :, :]
                    pri_weightz = pri_weightz[:, :-2, :, :]
                if self.periodic_num[1] > 0:
                    pri_weightx = pri_weightx[:, :, :-2, :]
                    pri_weighty = pri_weighty[:, :, :-1, :]
                    pri_weightz = pri_weightz[:, :, :-2, :]
                if self.periodic_num[2] > 0:
                    pri_weightx = pri_weightx[:, :, :, :-2]
                    pri_weighty = pri_weighty[:, :, :, :-2]
                    pri_weightz = pri_weightz[:, :, :, :-1]

                self.N_kernel = Structure.create_distance_weighted_kernel(
                    3 + 2 * (self.N_res // 10)
                ).to(self.device)
                self.Nx, _ = Structure.compute_normal_vector(
                    pri_weightx, self.N_kernel, self.periodic_num
                )
                self.Ny, _ = Structure.compute_normal_vector(
                    pri_weighty, self.N_kernel, self.periodic_num
                )
                self.Nz, _ = Structure.compute_normal_vector(
                    pri_weightz, self.N_kernel, self.periodic_num
                )
                if self.periodic_num[0] > 0:
                    # 扩展第一个维度
                    self.Nx = torch.cat(
                        [self.Nx, self.Nx[:, :1, :, :, :]], dim=1
                    )  # Nx 末尾扩展1位
                    self.Ny = torch.cat(
                        [self.Ny, self.Ny[:, :2, :, :, :]], dim=1
                    )  # Ny 末尾扩展2位
                    self.Nz = torch.cat(
                        [self.Nz, self.Nz[:, :2, :, :, :]], dim=1
                    )  # Nz 末尾扩展2位

                if self.periodic_num[1] > 0:
                    # 扩展第二个维度
                    self.Nx = torch.cat(
                        [self.Nx, self.Nx[:, :, :2, :, :]], dim=2
                    )  # Nx 在第二维扩展2位
                    self.Ny = torch.cat(
                        [self.Ny, self.Ny[:, :, :1, :, :]], dim=2
                    )  # Ny 在第二维扩展1位
                    self.Nz = torch.cat(
                        [self.Nz, self.Nz[:, :, :2, :, :]], dim=2
                    )  # Nz 在第二维扩展2位

                if self.periodic_num[2] > 0:
                    # 扩展第三个维度
                    self.Nx = torch.cat(
                        [self.Nx, self.Nx[:, :, :, :2, :]], dim=3
                    )  # Nx 在第三维扩展2位
                    self.Ny = torch.cat(
                        [self.Ny, self.Ny[:, :, :, :2, :]], dim=3
                    )  # Ny 在第三维扩展2位
                    self.Nz = torch.cat(
                        [self.Nz, self.Nz[:, :, :, :1, :]], dim=3
                    )  # Nz 在第三维扩展1位
                for structure in self.structures:
                    structure.Set_subcell(self)

                self.pri_weightx, self.pri_weighty, self.pri_weightz = (
                    E_Property_Periodic(
                        self.pri_weightx,
                        self.pri_weighty,
                        self.pri_weightz,
                        self.periodic_num,
                    )
                )

                FDTD_CUDA_Dispersion.Set_ER_average(
                    self.epsbeta_x,
                    self.pri_weightx,
                    self.pri_mat_idx,
                    self.sec_mat_idx,
                    self.er_inf_list,
                )
                FDTD_CUDA_Dispersion.Set_ER_average(
                    self.epsbeta_y,
                    self.pri_weighty,
                    self.pri_mat_idy,
                    self.sec_mat_idy,
                    self.er_inf_list,
                )
                FDTD_CUDA_Dispersion.Set_ER_average(
                    self.epsbeta_z,
                    self.pri_weightz,
                    self.pri_mat_idz,
                    self.sec_mat_idz,
                    self.er_inf_list,
                )

                if not self.debug:
                    self.Nx = None
                    self.Ny = None
                    self.Nz = None

    def Reset_structure_MONO(self, start):
        # 第一次调用,是简单体积平均
        # 第二次调用,如果subcell为True,则运用子像素平滑.然后不管怎样,都清空不需要的辅助变量,给后续的仿真腾出显存.
        nx, ny, nz = self.nx, self.ny, self.nz
        if start:
            # 重置材料
            self.ERx = torch.ones(
                self.num_structures,
                nx,
                ny + 1,
                nz + 1,
                1,
                device=self.device,
            )
            self.ERy = torch.ones(
                self.num_structures,
                nx + 1,
                ny,
                nz + 1,
                1,
                device=self.device,
            )
            self.ERz = torch.ones(
                self.num_structures,
                nx + 1,
                ny + 1,
                nz,
                1,
                device=self.device,
            )

            self.pri_weightx = torch.ones(
                self.num_structures, nx, ny + 1, nz + 1, device=self.device
            )
            self.pri_weighty = torch.ones(
                self.num_structures, nx + 1, ny, nz + 1, device=self.device
            )
            self.pri_weightz = torch.ones(
                self.num_structures, nx + 1, ny + 1, nz, device=self.device
            )

            self.pri_mat_idx = torch.zeros(
                self.num_structures,
                nx,
                ny + 1,
                nz + 1,
                dtype=torch.uint8,
                device=self.device,
            )
            self.pri_mat_idy = torch.zeros(
                self.num_structures,
                nx + 1,
                ny,
                nz + 1,
                dtype=torch.uint8,
                device=self.device,
            )
            self.pri_mat_idz = torch.zeros(
                self.num_structures,
                nx + 1,
                ny + 1,
                nz,
                dtype=torch.uint8,
                device=self.device,
            )

            self.sec_mat_idx = torch.zeros_like(self.pri_mat_idx)
            self.sec_mat_idy = torch.zeros_like(self.pri_mat_idy)
            self.sec_mat_idz = torch.zeros_like(self.pri_mat_idz)

            self.sigmadt_2x = torch.zeros(
                self.num_structures, nx, ny + 1, nz + 1, device=self.device
            )
            self.sigmadt_2y = torch.zeros(
                self.num_structures, nx + 1, ny, nz + 1, device=self.device
            )
            self.sigmadt_2z = torch.zeros(
                self.num_structures, nx + 1, ny + 1, nz, device=self.device
            )
            for structure in self.structures:
                structure.Initialization(self)

            FDTD_CUDA_MONO.Set_ER_average(
                self.ERx,
                self.pri_weightx,
                self.pri_mat_idx,
                self.sec_mat_idx,
                torch.real(self.er),
            )
            FDTD_CUDA_MONO.Set_ER_average(
                self.ERy,
                self.pri_weighty,
                self.pri_mat_idy,
                self.sec_mat_idy,
                torch.real(self.er),
            )
            FDTD_CUDA_MONO.Set_ER_average(
                self.ERz,
                self.pri_weightz,
                self.pri_mat_idz,
                self.sec_mat_idz,
                torch.real(self.er),
            )
            k_list = (
                2
                * torch.pi
                * Utils.c
                / self.lams.view(-1)[0].cpu().item()
                * self.dt
                / 2
            ) * torch.imag(self.er[:, 0])
            FDTD_CUDA_MONO.Set_sigma_average(
                self.sigmadt_2x,
                self.pri_weightx,
                self.pri_mat_idx,
                self.sec_mat_idx,
                k_list,
            )
            FDTD_CUDA_MONO.Set_sigma_average(
                self.sigmadt_2y,
                self.pri_weighty,
                self.pri_mat_idy,
                self.sec_mat_idy,
                k_list,
            )
            FDTD_CUDA_MONO.Set_sigma_average(
                self.sigmadt_2z,
                self.pri_weightz,
                self.pri_mat_idz,
                self.sec_mat_idz,
                k_list,
            )

            # self.pri_mat_idx,self.pri_mat_idy,self.pri_mat_idz=E_Property_Periodic(self.pri_mat_idx,self.pri_mat_idy,self.pri_mat_idz,self.periodic_num)
            # self.sec_mat_idx,self.sec_mat_idy,self.sec_mat_idz=E_Property_Periodic(self.sec_mat_idx,self.sec_mat_idy,self.sec_mat_idz,self.periodic_num)
            self.ERx, self.ERy, self.ERz = E_Property_Periodic(
                self.ERx, self.ERy, self.ERz, self.periodic_num
            )
            self.sigmadt_2x, self.sigmadt_2y, self.sigmadt_2z = E_Property_Periodic(
                self.sigmadt_2x, self.sigmadt_2y, self.sigmadt_2z, self.periodic_num
            )
        else:
            if self.subcell:
                # 取首位波长作为计算的依据
                self.pri_weightx = self.ERx[..., 0].clone()
                self.pri_weighty = self.ERy[..., 0].clone()
                self.pri_weightz = self.ERz[..., 0].clone()
                if self.periodic_num[0] > 0:
                    self.pri_weightx = self.pri_weightx[:, :-1, :, :]
                    self.pri_weighty = self.pri_weighty[:, :-2, :, :]
                    self.pri_weightz = self.pri_weightz[:, :-2, :, :]
                if self.periodic_num[1] > 0:
                    self.pri_weightx = self.pri_weightx[:, :, :-2, :]
                    self.pri_weighty = self.pri_weighty[:, :, :-1, :]
                    self.pri_weightz = self.pri_weightz[:, :, :-2, :]
                if self.periodic_num[2] > 0:
                    self.pri_weightx = self.pri_weightx[:, :, :, :-2]
                    self.pri_weighty = self.pri_weighty[:, :, :, :-2]
                    self.pri_weightz = self.pri_weightz[:, :, :, :-1]
                self.N_kernel = Structure.create_distance_weighted_kernel(
                    3 + 2 * (self.N_res // 10)
                ).to(self.device)
                self.Nx, _ = Structure.compute_normal_vector(
                    self.pri_weightx, self.N_kernel, self.periodic_num
                )
                self.Ny, _ = Structure.compute_normal_vector(
                    self.pri_weighty, self.N_kernel, self.periodic_num
                )
                self.Nz, _ = Structure.compute_normal_vector(
                    self.pri_weightz, self.N_kernel, self.periodic_num
                )
                if self.periodic_num[0] > 0:
                    # 扩展第一个维度
                    self.Nx = torch.cat(
                        [self.Nx, self.Nx[:, :1, :, :, :]], dim=1
                    )  # Nx 末尾扩展1位
                    self.Ny = torch.cat(
                        [self.Ny, self.Ny[:, :2, :, :, :]], dim=1
                    )  # Ny 末尾扩展2位
                    self.Nz = torch.cat(
                        [self.Nz, self.Nz[:, :2, :, :, :]], dim=1
                    )  # Nz 末尾扩展2位

                if self.periodic_num[1] > 0:
                    # 扩展第二个维度
                    self.Nx = torch.cat(
                        [self.Nx, self.Nx[:, :, :2, :, :]], dim=2
                    )  # Nx 在第二维扩展2位
                    self.Ny = torch.cat(
                        [self.Ny, self.Ny[:, :, :1, :, :]], dim=2
                    )  # Ny 在第二维扩展1位
                    self.Nz = torch.cat(
                        [self.Nz, self.Nz[:, :, :2, :, :]], dim=2
                    )  # Nz 在第二维扩展2位

                if self.periodic_num[2] > 0:
                    # 扩展第三个维度
                    self.Nx = torch.cat(
                        [self.Nx, self.Nx[:, :, :, :2, :]], dim=3
                    )  # Nx 在第三维扩展2位
                    self.Ny = torch.cat(
                        [self.Ny, self.Ny[:, :, :, :2, :]], dim=3
                    )  # Ny 在第三维扩展2位
                    self.Nz = torch.cat(
                        [self.Nz, self.Nz[:, :, :, :1, :]], dim=3
                    )  # Nz 在第三维扩展1位
                for structure in self.structures:
                    structure.Set_subcell(self)
                self.ERx, self.ERy, self.ERz = E_Property_Periodic(
                    self.ERx, self.ERy, self.ERz, self.periodic_num
                )
                if not self.debug:
                    self.Nx = None
                    self.Ny = None
                    self.Nz = None
            if not self.debug:
                self.pri_weightx = None
                self.pri_weighty = None
                self.pri_weightz = None

                self.pri_mat_idx = None
                self.pri_mat_idy = None
                self.pri_mat_idz = None

                self.sec_mat_idx = None
                self.sec_mat_idy = None
                self.sec_mat_idz = None

    def Update(self, adjoint_simulation=False, isconj=None, delta_step=15):
        if self.dispersion:
            self.Update_Dispersion(adjoint_simulation, isconj, delta_step)
        else:
            self.Update_MONO(adjoint_simulation, isconj, delta_step)

    def Update_Dispersion(self, adjoint_simulation=False, isconj=None, delta_step=15):
        if isconj is None:
            isconj = adjoint_simulation

        device = self.device
        nx, ny, nz = self.nx, self.ny, self.nz
        num_sources = self.num_sources
        num_structures = self.num_structures
        f_num = self.lams.numel() * 2

        self.Reset_structure_Dispersion(True)
        self.Reset_structure_Dispersion(False)

        if len(self.sources) > 0:
            x_phase_offset, y_phase_offset = self.sources[0].Get_phase_offset()
        else:
            x_phase_offset = torch.ones(
                [self.num_sources, self.lams.numel()], dtype=type, device=device
            )
            y_phase_offset = torch.ones(
                [self.num_sources, self.lams.numel()], dtype=type, device=device
            )
        x_phase_offset = torch.cat(
            [torch.real(x_phase_offset), torch.imag(x_phase_offset)], dim=-1
        )
        y_phase_offset = torch.cat(
            [torch.real(y_phase_offset), torch.imag(y_phase_offset)], dim=-1
        )
        # 清除监视器和影片的数据
        for monitor in self.monitors:
            monitor.Clear(self)
        for movie in self.movies:
            movie.Clear()

        Ex = torch.zeros(
            num_sources,
            num_structures,
            nx,
            ny + 1,
            nz + 1,
            f_num,
            device=device,
        )
        Ey = torch.zeros(
            num_sources,
            num_structures,
            nx + 1,
            ny,
            nz + 1,
            f_num,
            device=device,
        )
        Ez = torch.zeros(
            num_sources,
            num_structures,
            nx + 1,
            ny + 1,
            nz,
            f_num,
            device=device,
        )

        Ex_1 = torch.zeros_like(Ex, device=device)
        Ey_1 = torch.zeros_like(Ey, device=device)
        Ez_1 = torch.zeros_like(Ez, device=device)

        pri_Jpdtx = torch.zeros_like(Ex, dtype=torch.complex64, device=device)
        pri_Jpdty = torch.zeros_like(Ey, dtype=torch.complex64, device=device)
        pri_Jpdtz = torch.zeros_like(Ez, dtype=torch.complex64, device=device)

        sec_Jpdtx = torch.zeros_like(Ex, dtype=torch.complex64, device=device)
        sec_Jpdty = torch.zeros_like(Ey, dtype=torch.complex64, device=device)
        sec_Jpdtz = torch.zeros_like(Ez, dtype=torch.complex64, device=device)

        Hx = torch.zeros(
            num_sources,
            num_structures,
            nx + 1,
            ny,
            nz,
            f_num,
            device=device,
        )
        Hy = torch.zeros(
            num_sources,
            num_structures,
            nx,
            ny + 1,
            nz,
            f_num,
            device=device,
        )
        Hz = torch.zeros(
            num_sources,
            num_structures,
            nx,
            ny,
            nz + 1,
            f_num,
            device=device,
        )

        # CPML
        PsixH = torch.zeros(
            num_sources,
            num_structures,
            2 * self.PML_num[0],
            ny,
            nz,
            2,
            f_num,
            device=device,
        )
        PsiyH = torch.zeros(
            num_sources,
            num_structures,
            nx,
            2 * self.PML_num[1],
            nz,
            2,
            f_num,
            device=device,
        )
        PsizH = torch.zeros(
            num_sources,
            num_structures,
            nx,
            ny,
            2 * self.PML_num[2],
            2,
            f_num,
            device=device,
        )

        PsixD = torch.zeros(
            num_sources,
            num_structures,
            2 * self.PML_num[0],
            ny,
            nz,
            2,
            f_num,
            device=device,
        )
        PsiyD = torch.zeros(
            num_sources,
            num_structures,
            nx,
            2 * self.PML_num[1],
            nz,
            2,
            f_num,
            device=device,
        )
        PsizD = torch.zeros(
            num_sources,
            num_structures,
            nx,
            ny,
            2 * self.PML_num[2],
            2,
            f_num,
            device=device,
        )

        dx2_0 = self.dx2[None, None, 0::2, None, None, None]
        dy2_0 = self.dy2[None, None, None, 0::2, None, None]
        dz2_0 = self.dz2[None, None, None, None, 0::2, None]
        dx2_1 = self.dx2[None, None, 1::2, None, None, None]
        dy2_1 = self.dy2[None, None, None, 1::2, None, None]
        dz2_1 = self.dz2[None, None, None, None, 1::2, None]

        base_step_offset = round(self.base_steps / delta_step)
        max_energy = torch.zeros(num_sources, num_structures, f_num)
        # energy_id=0
        energy_list = torch.zeros(num_sources, num_structures, f_num, base_step_offset)
        energy_list_min = torch.ones_like(energy_list)  # 真正用于比较的,
        # energy_list_total=torch.zeros(num_sources,num_structures,self.lams.numel(),1+self.steps//delta_step)

        for t in range(self.steps - 1):
            FDTD_CUDA_Dispersion.Update_H(
                Hx,
                Hy,
                Hz,
                Ex,
                Ey,
                Ez,
                self.Cx[1::2],
                self.Cy[1::2],
                self.Cz[1::2],
                PsixH,
                PsiyH,
                PsizH,
                self.bx2[self.PML_idx + 1],
                self.by2[self.PML_idy + 1],
                self.bz2[self.PML_idz + 1],
                self.cx2[self.PML_idx + 1],
                self.cy2[self.PML_idy + 1],
                self.cz2[self.PML_idz + 1],
                self.PML_num,
                self.periodic_num,
            )

            if not adjoint_simulation:
                for s in self.sources:
                    if t < s.t_max:
                        FDTD_CUDA_Dispersion.Inject_H(
                            Hx,
                            Hy,
                            self.Cz[1::2],
                            s.Ext[..., t],
                            s.Eyt[..., t],
                            s.phi_Ex,
                            s.phi_Ey,
                            self.PML_num,
                            s.bound,
                        )
            # 更新源

            FDTD_CUDA_Dispersion.Update_E(
                Ex,
                Ey,
                Ez,
                Hx,
                Hy,
                Hz,
                self.epsbeta_x,
                self.epsbeta_y,
                self.epsbeta_z,
                self.sigmadt_2x,
                self.sigmadt_2y,
                self.sigmadt_2z,
                self.Cx[0::2],
                self.Cy[0::2],
                self.Cz[0::2],
                PsixD,
                PsiyD,
                PsizD,
                self.bx2[self.PML_idx],
                self.by2[self.PML_idy],
                self.bz2[self.PML_idz],
                self.cx2[self.PML_idx],
                self.cy2[self.PML_idy],
                self.cz2[self.PML_idz],
                self.PML_num,
                self.periodic_num,
            )

            # Dz[5+self.PML_num[0],5+self.PML_num[1],5+self.PML_num[2],None]-=Source.gt(self.t_arr[t+1],self.tau,self.f_mean)-Source.gt(self.t_arr[t],self.tau,self.f_mean)
            if not adjoint_simulation:
                for s in self.sources:
                    if t < s.t_max:
                        FDTD_CUDA_Dispersion.Inject_E(
                            Ex,
                            Ey,
                            self.Cz[0::2],
                            s.Hxt[..., t],
                            s.Hyt[..., t],
                            s.phi_Hx,
                            s.phi_Hy,
                            self.PML_num,
                            s.bound,
                        )
            else:
                for i in range(len(self.monitors)):
                    s = self.monitors[i].adjoint_source
                    if s:
                        FDTD_CUDA_Dispersion.Inject_J(
                            Ex, Ey, Ez, s.Jt(t, 0), s.Jt(t, 1), s.Jt(t, 2), s.n_offset
                        )

            FDTD_CUDA_Dispersion.Update_E_Dispersion(
                Ex,
                Ey,
                Ez,
                Ex_1,
                Ey_1,
                Ez_1,
                self.pri_weightx,
                self.pri_weighty,
                self.pri_weightz,
                self.pri_mat_idx,
                self.pri_mat_idy,
                self.pri_mat_idz,
                self.sec_mat_idx,
                self.sec_mat_idy,
                self.sec_mat_idz,
                self.epsbeta_x,
                self.epsbeta_y,
                self.epsbeta_z,
                self.sigmadt_2x,
                self.sigmadt_2y,
                self.sigmadt_2z,
                self.kp_list,
                self.bp_list,
                pri_Jpdtx,
                pri_Jpdty,
                pri_Jpdtz,
                sec_Jpdtx,
                sec_Jpdty,
                sec_Jpdtz,
                self.periodic_num,
            )
            FDTD_CUDA_Dispersion.Update_E_Periodic(
                Ex, Ey, Ez, x_phase_offset, y_phase_offset, self.periodic_num, isconj
            )

            # 早停
            offset_grid = 1
            # [:,:,offset_grid+self.PML_num[0]:-offset_grid-self.PML_num[0],offset_grid+self.PML_num[1]:-offset_grid-self.PML_num[1],offset_grid+self.PML_num[2]:-offset_grid-self.PML_num[2],:]
            if t % delta_step == 0:
                energy = (Hx * Hx * dx2_0 * dy2_1 * dz2_1)[
                    :,
                    :,
                    offset_grid + self.PML_num[0] : -offset_grid - self.PML_num[0],
                    offset_grid + self.PML_num[1] : -offset_grid - self.PML_num[1],
                    offset_grid + self.PML_num[2] : -offset_grid - self.PML_num[2],
                    :,
                ].sum(dim=(2, 3, 4))
                energy += (Hy * Hy * dx2_1 * dy2_0 * dz2_1)[
                    :,
                    :,
                    offset_grid + self.PML_num[0] : -offset_grid - self.PML_num[0],
                    offset_grid + self.PML_num[1] : -offset_grid - self.PML_num[1],
                    offset_grid + self.PML_num[2] : -offset_grid - self.PML_num[2],
                    :,
                ].sum(dim=(2, 3, 4))
                energy += (Hz * Hz * dx2_1 * dy2_1 * dz2_0)[
                    :,
                    :,
                    offset_grid + self.PML_num[0] : -offset_grid - self.PML_num[0],
                    offset_grid + self.PML_num[1] : -offset_grid - self.PML_num[1],
                    offset_grid + self.PML_num[2] : -offset_grid - self.PML_num[2],
                    :,
                ].sum(dim=(2, 3, 4))

                # energy_list_total[:,:,:,energy_id]=energy.cpu()
                energy_list[:, :, :, :-1] = energy_list[:, :, :, 1:].clone()
                energy_list[:, :, :, -1] = energy.cpu().clone()
                # energy_id+=1
                max_energy = torch.max(max_energy, energy.cpu())
                if t > self.base_steps:
                    delta_energy = torch.std(energy_list, dim=-1) / max_energy
                    if torch.max(delta_energy) > 0.2:
                        energy_list_min = energy_list.clone()
                    else:
                        energy_list_min = torch.min(
                            energy_list_min, energy_list.clone()
                        )
                    delta_energy = torch.std(energy_list_min, dim=-1) / max_energy
                    # print("能量数组",energy_list)
                    # print("归一化标准差",delta_energy)
                    # print("归一化平均值",torch.mean(energy_list, dim=-1)/max_energy)
                    if torch.max(delta_energy) < self.auto_shutoff_min:
                        if self.debug:
                            print("早停,当前时间步", t)
                        break

            # 可以对复数场做fft!也可以对实数场做fft,因为这俩相差pi/2
            for i in range(len(self.monitors)):
                if f_num == 1:
                    self.monitors[i].Update(
                        self.Kernel_arr[t, :],
                        Ex,
                        Ey,
                        Ez,
                    )
                else:
                    self.monitors[i].Update(
                        self.Kernel_arr[t, :],
                        Ex[..., : f_num // 2],
                        Ey[..., : f_num // 2],
                        Ez[..., : f_num // 2],
                    )

            for i in range(len(self.movies)):
                # 只探测首位的
                self.movies[i].Update(
                    t,
                    Ex[0, 0, :, :, :, 0],
                    Ey[0, 0, :, :, :, 0],
                    Ez[0, 0, :, :, :, 0],
                )
        # 暂时非伴随源靠归一化
        if not adjoint_simulation:
            nor = torch.pi * self.tau / self.dt
        else:
            nor = 1
            for i in range(len(self.monitors)):
                s = self.monitors[i].adjoint_source
                if s:
                    s.Clear()  # 清空伴随源,防止影响到下次伴随模拟
        for i in range(len(self.monitors)):
            self.monitors[i].Post_Process(nor)

    def Update_MONO(self, adjoint_simulation=False, isconj=None, delta_step=15):
        if isconj is None:
            isconj = adjoint_simulation
        device = self.device
        nx, ny, nz = self.nx, self.ny, self.nz
        num_sources = self.num_sources
        num_structures = self.num_structures
        f_num = 1
        self.Reset_structure_MONO(True)
        self.Reset_structure_MONO(False)

        type = torch.complex64
        if len(self.sources) > 0:
            x_phase_offset, y_phase_offset = self.sources[0].Get_phase_offset()
        else:
            x_phase_offset = torch.ones(
                [self.num_sources, self.lams.numel()], dtype=type, device=device
            )
            y_phase_offset = torch.ones(
                [self.num_sources, self.lams.numel()], dtype=type, device=device
            )
        # 清除监视器和影片的数据

        for monitor in self.monitors:
            monitor.Clear(self)

        for movie in self.movies:
            movie.Clear()

        Ex = torch.zeros(
            num_sources,
            num_structures,
            nx,
            ny + 1,
            nz + 1,
            f_num,
            dtype=type,
            device=device,
        )
        Ey = torch.zeros(
            num_sources,
            num_structures,
            nx + 1,
            ny,
            nz + 1,
            f_num,
            dtype=type,
            device=device,
        )
        Ez = torch.zeros(
            num_sources,
            num_structures,
            nx + 1,
            ny + 1,
            nz,
            f_num,
            dtype=type,
            device=device,
        )

        Hx = torch.zeros(
            num_sources,
            num_structures,
            nx + 1,
            ny,
            nz,
            f_num,
            dtype=type,
            device=device,
        )
        Hy = torch.zeros(
            num_sources,
            num_structures,
            nx,
            ny + 1,
            nz,
            f_num,
            dtype=type,
            device=device,
        )
        Hz = torch.zeros(
            num_sources,
            num_structures,
            nx,
            ny,
            nz + 1,
            f_num,
            dtype=type,
            device=device,
        )

        # CPML
        PsixH = torch.zeros(
            num_sources,
            num_structures,
            2 * self.PML_num[0],
            ny,
            nz,
            2,
            f_num,
            dtype=type,
            device=device,
        )
        PsiyH = torch.zeros(
            num_sources,
            num_structures,
            nx,
            2 * self.PML_num[1],
            nz,
            2,
            f_num,
            dtype=type,
            device=device,
        )
        PsizH = torch.zeros(
            num_sources,
            num_structures,
            nx,
            ny,
            2 * self.PML_num[2],
            2,
            f_num,
            dtype=type,
            device=device,
        )

        PsixD = torch.zeros(
            num_sources,
            num_structures,
            2 * self.PML_num[0],
            ny,
            nz,
            2,
            f_num,
            dtype=type,
            device=device,
        )
        PsiyD = torch.zeros(
            num_sources,
            num_structures,
            nx,
            2 * self.PML_num[1],
            nz,
            2,
            f_num,
            dtype=type,
            device=device,
        )
        PsizD = torch.zeros(
            num_sources,
            num_structures,
            nx,
            ny,
            2 * self.PML_num[2],
            2,
            f_num,
            dtype=type,
            device=device,
        )

        dx2_0 = self.dx2[None, None, 0::2, None, None, None]
        dy2_0 = self.dy2[None, None, None, 0::2, None, None]
        dz2_0 = self.dz2[None, None, None, None, 0::2, None]
        dx2_1 = self.dx2[None, None, 1::2, None, None, None]
        dy2_1 = self.dy2[None, None, None, 1::2, None, None]
        dz2_1 = self.dz2[None, None, None, None, 1::2, None]

        base_step_offset = round(self.base_steps / delta_step)
        max_energy = torch.zeros(num_sources, num_structures, self.lams.numel())
        # energy_id=0
        energy_list = torch.zeros(
            num_sources, num_structures, self.lams.numel(), base_step_offset
        )
        energy_list_min = torch.ones_like(energy_list)  # 真正用于比较的,
        # energy_list_total=torch.zeros(num_sources,num_structures,self.lams.numel(),1+self.steps//delta_step)

        for t in range(self.steps - 1):
            FDTD_CUDA_MONO.Update_H(
                Hx,
                Hy,
                Hz,
                Ex,
                Ey,
                Ez,
                self.Cx[1::2],
                self.Cy[1::2],
                self.Cz[1::2],
                PsixH,
                PsiyH,
                PsizH,
                self.bx2[self.PML_idx + 1],
                self.by2[self.PML_idy + 1],
                self.bz2[self.PML_idz + 1],
                self.cx2[self.PML_idx + 1],
                self.cy2[self.PML_idy + 1],
                self.cz2[self.PML_idz + 1],
                self.PML_num,
                self.periodic_num,
            )

            if not adjoint_simulation:
                for s in self.sources:
                    if t < s.t_max + s.t_source_delay:
                        # FDTD_CUDA_MONO.Inject_H(
                        #     Hx,
                        #     Hy,
                        #     self.Cz[1::2],
                        #     s.Ext[..., t],
                        #     s.Eyt[..., t],
                        #     s.phi_Ex,
                        #     s.phi_Ey,
                        #     self.PML_num,
                        #     s.bound,
                        # )
                        FDTD_CUDA_MONO.Inject_H(
                            Hx,
                            Hy,
                            self.Cz[1::2],
                            s.Ext,
                            s.Eyt,
                            s.phi_Ex,
                            s.phi_Ey,
                            s.delay_map_Ex,
                            s.delay_map_Ey,
                            self.PML_num,
                            s.bound,
                            t,
                        )
            FDTD_CUDA_MONO.Update_E(
                Ex,
                Ey,
                Ez,
                Hx,
                Hy,
                Hz,
                self.ERx,
                self.ERy,
                self.ERz,
                self.sigmadt_2x,
                self.sigmadt_2y,
                self.sigmadt_2z,
                self.Cx[0::2],
                self.Cy[0::2],
                self.Cz[0::2],
                PsixD,
                PsiyD,
                PsizD,
                self.bx2[self.PML_idx],
                self.by2[self.PML_idy],
                self.bz2[self.PML_idz],
                self.cx2[self.PML_idx],
                self.cy2[self.PML_idy],
                self.cz2[self.PML_idz],
                self.PML_num,
                self.periodic_num,
            )
            # Ez[0,0,5+self.PML_num[0],5+self.PML_num[1],5+self.PML_num[2],:]-=FDTD_Source4.gt(self.t_arr[t+1],self.tau,self.f[0]).view(-1)-FDTD4_Source.gt(self.t_arr[t],self.tau,self.f[0]).view(-1)

            if not adjoint_simulation:
                for s in self.sources:
                    if t < s.t_max + s.t_source_delay:
                        FDTD_CUDA_MONO.Inject_E(
                            Ex,
                            Ey,
                            self.Cz[0::2],
                            s.Hxt,
                            s.Hyt,
                            s.phi_Hx,
                            s.phi_Hy,
                            s.delay_map_Hx,
                            s.delay_map_Hy,
                            self.PML_num,
                            s.bound,
                            t,
                        )
            else:
                for i in range(len(self.monitors)):
                    s = self.monitors[i].adjoint_source
                    if s:
                        FDTD_CUDA_MONO.Inject_J(
                            Ex, Ey, Ez, s.Jt(t, 0), s.Jt(t, 1), s.Jt(t, 2), s.n_offset
                        )

            FDTD_CUDA_MONO.Update_E_Dispersion(
                Ex,
                Ey,
                Ez,
                self.ERx,
                self.ERy,
                self.ERz,
                self.sigmadt_2x,
                self.sigmadt_2y,
                self.sigmadt_2z,
                self.periodic_num,
            )  # 包括周期性矫正

            FDTD_CUDA_MONO.Update_E_Periodic(
                Ex, Ey, Ez, x_phase_offset, y_phase_offset, self.periodic_num, isconj
            )

            # 早停
            offset_grid = 1
            # [:,:,offset_grid+self.PML_num[0]:-offset_grid-self.PML_num[0],offset_grid+self.PML_num[1]:-offset_grid-self.PML_num[1],offset_grid+self.PML_num[2]:-offset_grid-self.PML_num[2],:]
            if t % delta_step == 0:
                energy = (
                    Ex.real * Ex.real * self.ERx.unsqueeze(0) * dx2_1 * dy2_0 * dz2_0
                )[
                    :,
                    :,
                    offset_grid + self.PML_num[0] : -offset_grid - self.PML_num[0],
                    offset_grid + self.PML_num[1] : -offset_grid - self.PML_num[1],
                    offset_grid + self.PML_num[2] : -offset_grid - self.PML_num[2],
                    :,
                ].sum(
                    dim=(2, 3, 4)
                )
                energy += (
                    Ey.real * Ey.real * self.ERy.unsqueeze(0) * dx2_0 * dy2_1 * dz2_0
                )[
                    :,
                    :,
                    offset_grid + self.PML_num[0] : -offset_grid - self.PML_num[0],
                    offset_grid + self.PML_num[1] : -offset_grid - self.PML_num[1],
                    offset_grid + self.PML_num[2] : -offset_grid - self.PML_num[2],
                    :,
                ].sum(
                    dim=(2, 3, 4)
                )
                energy += (
                    Ez.real * Ez.real * self.ERz.unsqueeze(0) * dx2_0 * dy2_0 * dz2_1
                )[
                    :,
                    :,
                    offset_grid + self.PML_num[0] : -offset_grid - self.PML_num[0],
                    offset_grid + self.PML_num[1] : -offset_grid - self.PML_num[1],
                    offset_grid + self.PML_num[2] : -offset_grid - self.PML_num[2],
                    :,
                ].sum(
                    dim=(2, 3, 4)
                )
                energy += (Hx.real * Hx.real * dx2_0 * dy2_1 * dz2_1)[
                    :,
                    :,
                    offset_grid + self.PML_num[0] : -offset_grid - self.PML_num[0],
                    offset_grid + self.PML_num[1] : -offset_grid - self.PML_num[1],
                    offset_grid + self.PML_num[2] : -offset_grid - self.PML_num[2],
                    :,
                ].sum(dim=(2, 3, 4))
                energy += (Hy.real * Hy.real * dx2_1 * dy2_0 * dz2_1)[
                    :,
                    :,
                    offset_grid + self.PML_num[0] : -offset_grid - self.PML_num[0],
                    offset_grid + self.PML_num[1] : -offset_grid - self.PML_num[1],
                    offset_grid + self.PML_num[2] : -offset_grid - self.PML_num[2],
                    :,
                ].sum(dim=(2, 3, 4))
                energy += (Hz.real * Hz.real * dx2_1 * dy2_1 * dz2_0)[
                    :,
                    :,
                    offset_grid + self.PML_num[0] : -offset_grid - self.PML_num[0],
                    offset_grid + self.PML_num[1] : -offset_grid - self.PML_num[1],
                    offset_grid + self.PML_num[2] : -offset_grid - self.PML_num[2],
                    :,
                ].sum(dim=(2, 3, 4))
                # energy_list_total[:,:,:,energy_id]=energy.cpu()
                energy_list[:, :, :, :-1] = energy_list[:, :, :, 1:].clone()
                energy_list[:, :, :, -1] = energy.cpu().clone()
                # energy_id+=1
                max_energy = torch.max(max_energy, energy.cpu())
                if t > self.base_steps:
                    delta_energy = torch.std(energy_list, dim=-1) / max_energy
                    if torch.max(delta_energy) > 0.05:
                        energy_list_min = energy_list.clone()
                    else:
                        energy_list_min = torch.min(
                            energy_list_min, energy_list.clone()
                        )
                    delta_energy = torch.std(energy_list_min, dim=-1) / max_energy
                    # print("能量数组",energy_list)
                    # print("归一化标准差",delta_energy)
                    # print("归一化平均值",torch.mean(energy_list, dim=-1)/max_energy)
                    if torch.max(delta_energy) < self.auto_shutoff_min:
                        if self.debug:
                            print("早停,当前时间步", t)
                        break
            # 可以对复数场做fft!也可以对实数场做fft,因为这俩相差pi/2
            for i in range(len(self.monitors)):
                self.monitors[i].Update(
                    self.Kernel_arr[t, :],
                    torch.real(Ex),
                    torch.real(Ey),
                    torch.real(Ez),
                )

            for i in range(len(self.movies)):
                # 只探测首位的
                self.movies[i].Update(
                    t,
                    torch.real(Ex[0, 0, :, :, :, 0]),
                    torch.real(Ey[0, 0, :, :, :, 0]),
                    torch.real(Ez[0, 0, :, :, :, 0]),
                )

        # 暂时非伴随源靠归一化
        if not adjoint_simulation:
            # 如果是多色FDTD,每个波长的归一化因子显然不一样,但是现在吗,每个频率用单独的光源,中心激发频率都是自己
            # 那就都是self.tau咯
            # 除以2pi的2和只用实部的2抵消了
            nor = (
                torch.pi
                * self.tau
                / self.dt
                * self.sources[0].Amp.view(1, 1, 1, 1, 1, -1)
            )
            # nor = torch.sum(
            #     FDTD4_Source.gt(self.t_arr, self.tau, self.f) * self.Kernel_arr, dim=0
            # )
        else:
            nor = 1
            for i in range(len(self.monitors)):
                s = self.monitors[i].adjoint_source
                if s:
                    s.Clear()  # 清空伴随源,防止影响到下次伴随模拟
        for i in range(len(self.monitors)):
            self.monitors[i].Post_Process(nor)
        # self.energy_list_total=energy_list_total

    def AddPlane(
        self,
        z=0,
        theta=0,
        phi=0,
        polar=0,
        phase=0,
        custom_phasor=None,
        custom_delay=None,
        x=None,
        y=None,
    ):
        out = Source.PlaneSource(
            z, theta, phi, polar, phase, custom_phasor, custom_delay, x, y
        )
        self.sources.append(out)
        return out

    def AddImport(
        self,
        area=[[0, 0], [0, 0], [0, 0]],
        name="Air",
        import_obj=None,
        priority=2,
        sigma=0,
    ):
        # 假设 Structure 类已定义
        if import_obj == None:
            import_obj = ones(self.num_structures, 1, 1, 1)
        if self.dispersion:
            out = Structure.Structure_Dispersion(
                tensor(area), name, import_obj, priority, sigma
            )
        else:
            out = Structure.Structure_MONO(
                tensor(area), name, import_obj, priority, sigma
            )
        self.structures.append(out)
        return out

    def AddHeightmap(  # 添加高度图,目前只支持z方向的
        self,
        area=[[0, 0], [0, 0], [0, 0]],
        name="Air",
        import_obj=None,
        gray_scale=2,  # 灰阶数,比如只能0或1,灰阶数就是2
        priority=2,
    ):
        # 假设 Structure 类已定义
        if import_obj == None:
            import_obj = ones(self.num_structures, 1, 1)
        import_obj = import_obj.to(self.device)
        """
        将三维张量 import_obj 转换为四维张量 import3d。        
        参数:
        - import_obj (torch.Tensor): 输入的三维张量，形状为 (batch, x, y)，所有元素在 [0, 1] 之间。
        - gray_scale (int): 分割数目，决定 z 轴的维度。
        返回:
        - import3d (torch.Tensor): 输出的四维张量，形状为 (batch, x, y, z)，每个元素在 [0, 1] 之间。
        """
        # 确保 gray_scale 是正整数
        assert isinstance(gray_scale, int) and gray_scale > 0, "gray_scale 必须是正整数"

        step = 1.0 / gray_scale  # 每个分割的高度范围
        # 计算每个分割的下界和上界
        lower_bounds = torch.linspace(
            0, 1 - step, steps=gray_scale, device=self.device
        )  # 形状 (z,)
        upper_bounds = lower_bounds + step
        h = import_obj.unsqueeze(-1)
        # 调整下界和上界的形状以进行广播
        lower = lower_bounds.view(1, 1, 1, gray_scale)  # 形状 (1, 1, 1, z)
        upper = upper_bounds.view(1, 1, 1, gray_scale)  # 形状 (1, 1, 1, z)

        import_obj = torch.where(
            h >= upper,
            torch.ones_like(h),  # 完全填充
            torch.where(
                h <= lower,
                torch.zeros_like(h),  # 不填充
                (h - lower) / step,  # 线性插值填充比例
            ),
        )

        if self.dispersion:
            out = Structure.Structure_Dispersion(
                tensor(area), name, import_obj, priority, 0.0
            )
        else:
            out = Structure.Structure_MONO(
                tensor(area), name, import_obj, priority, 0.0
            )
        out.gray_scale = gray_scale
        self.structures.append(out)
        return out

    def AddMonitor(
        self,
        area=[[0, 0], [0, 0], [0, 0]],
        index=1,
        name="DFT",
        type="nearest",
        adjoint=False,
    ):
        # 假设 Monitor 类已定义
        delta = torch.min(self.lams).item() / self.N_res / index
        out = Recorder.Monitor(tensor(area), delta, name, type, adjoint)
        self.monitors.append(out)
        return out

    def AddMovie(self, area=[[0, 0], [0, 0], [0, 0]], index=1, name="Movie"):
        # 假设 Movie 类已定义
        delta = torch.min(self.lams).item() / self.N_res / index
        movie = Recorder.Movie(tensor(area), delta, name)
        self.movies.append(movie)
        return movie

    def Display(self):
        # 遍历监视器并调用它们的 Display 方法
        for monitor in self.monitors:
            monitor.Display()
        # 遍历影片并调用它们的 Display 方法
        for movie in self.movies:
            movie.Display(self)

    def Check(self):
        plt.figure()
        plt.suptitle("gT")
        for i, source in enumerate(self.sources):
            # 绘制每个光源的 gT
            plt.subplot(1, len(self.sources), i + 1)
            plt.plot(self.t_arr.cpu(), source.gT.cpu())

            # # 绘制每个光源的 n_delay_zb
            # plt.subplot(2, len(self.sources), i+1+len(self.sources))
            # # 假设 self.x2 和 self.y2 是一维数组
            # X, Y = np.meshgrid(self.x2[::2].cpu(), self.y2[::2].cpu())
            # plt.pcolormesh(X, Y, source.n_delay_zb[:,:,0,0,0].cpu() * self.dt, shading='flat', cmap='jet')
            # plt.colorbar()
        plt.show()

        # 创建一个空的 Plotly 图表
        fig = go.Figure()

        # 设置3D视图
        fig.update_layout(
            scene=dict(
                xaxis=dict(backgroundcolor="black", showbackground=True),
                yaxis=dict(backgroundcolor="black", showbackground=True),
                zaxis=dict(backgroundcolor="black", showbackground=True),
                aspectmode="auto",
            ),
            title_text="光源",
        )

        # 假设 self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max, self.x2, self.y2, self.z2, self.y, self.z, self.x_span, self.y_span, self.z_span, self.boundary_color 已经定义

        # 使用 Draw_box 函数绘制长方体
        # 使用 Draw_box 函数绘制长方体
        Utils.Draw_box(
            fig,
            [0.5 * (self.x_min + self.x2[0].item()), self.y, self.z],
            [self.x_min - self.x2[0].item(), self.y_span, self.z_span],
            self.boundary_color[0],
            0,
        )
        Utils.Draw_box(
            fig,
            [0.5 * (self.x_max + self.x2[-1].item()), self.y, self.z],
            [self.x2[-1].item() - self.x_max, self.y_span, self.z_span],
            self.boundary_color[0],
            0,
        )
        Utils.Draw_box(
            fig,
            [self.x, 0.5 * (self.y_min + self.y2[0].item()), self.z],
            [self.x_span, self.y_min - self.y2[0].item(), self.z_span],
            self.boundary_color[1],
            0,
        )
        Utils.Draw_box(
            fig,
            [self.x, 0.5 * (self.y_max + self.y2[-1].item()), self.z],
            [self.x_span, self.y2[-1].item() - self.y_max, self.z_span],
            self.boundary_color[1],
            0,
        )
        Utils.Draw_box(
            fig,
            [self.x, self.y, 0.5 * (self.z_min + self.z2[0].item())],
            [self.x_span, self.y_span, self.z_min - self.z2[0].item()],
            self.boundary_color[2],
            0,
        )
        Utils.Draw_box(
            fig,
            [self.x, self.y, 0.5 * (self.z_max + self.z2[-1].item())],
            [self.x_span, self.y_span, self.z2[-1].item() - self.z_max],
            self.boundary_color[2],
            0,
        )

        # 遍历 sources 列表并调用每个元素的 Draw 方法
        for source in self.sources:
            source.Draw(fig)

        # 遍历 monitors 列表并调用每个元素的 Draw 方法
        for monitor in self.monitors:
            monitor.Draw(fig)

        # 遍历 movies 列表并调用每个元素的 Draw 方法
        for movie in self.movies:
            movie.Draw(fig)

        fig.show()
        #     for i=1:numel(self.structures)
        #         color=Utils.color_interpolation_jet((self.structures(i).index-1)/(self.n_max-1+Utils.e))
        #         self.structures(i).Draw(color,1-self.structures(i).priority/10,color)
        #     end
        #     %Recorder.Monitor.Matrix_visualizer(self.ER,self.x_arr,self.y_arr,self.z_arr,self.lams(1),'ER')
        # end
