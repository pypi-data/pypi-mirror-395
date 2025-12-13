# %%
import torch
import torchopticsy.Utils as Utils
from torchopticsy.Properties import Geometry
import matplotlib.pyplot as plt

t_offset = 8  # 滞后8tau,防止从最高点开始,去除高频分量,对于斜入射波非常重要,防止倏失波,因为倏失波是无法被激发的.
H_t_offset = 0.5  # H落后0.5个时间单位,取决于FDTD的更新顺序


# 看从-无穷到+无穷的积分啦,否则不太对哦
# fft也不行,因为对于出于频率分辨率的要求,所以对于仿真时间要求很长.


# 高斯光源每个波长是一样的就很好,大致验证过波前,看起来问题并不是很大.
# 矢量分量的微小变化?别人也没有讨论这个问题,可能也差不大多.
# 能量归一化?这个还是要算一算的,否则会误以为性能下降很多哈.
def generate_gaussian_beam_from_fiber(NA, MFD, z, x, y, wavelength, n=1.0):
    # Beam waist
    w0 = MFD / 2

    # Beam quality factor M^2 from your formula
    M2 = torch.pi * n * w0 / wavelength * torch.arcsin(torch.tensor(NA / n))

    # Rayleigh range z_R (using your formula)
    z_R = torch.tensor((w0**2 / M2) * (torch.pi * n / wavelength))

    # Spot size w(z)
    wz = w0 * torch.sqrt(1 + (z / z_R) ** 2)

    # Radius of curvature R(z)
    Rz = z + (z_R**2 / z)

    # Spatial grid
    X, Y = torch.meshgrid(x, y, indexing="ij")
    r2 = X**2 + Y**2

    # Amplitude
    amplitude = torch.exp(-r2 / wz**2)

    # Quadratic phase term using your Gaussian beam phase formula
    k = 2 * torch.pi * n / wavelength
    phase = k * (r2 / (2 * Rz))
    phase_term = torch.exp(1j * phase)

    # Delay
    delay = n * torch.sqrt(z**2 + r2) / Utils.c
    delay = delay - torch.min(delay)

    return amplitude * phase_term, delay


# def generate_gaussian_beam_from_fiber(NA, D_core, z, x, y, wavelength):
#     w0 = D_core / 2
#     M2 = torch.pi * w0 / wavelength * torch.arcsin(torch.tensor(NA))
#     z_R = (w0**2 / M2) * (torch.pi / wavelength)
#     wz = w0 * torch.sqrt(torch.tensor(1 + (z / z_R) ** 2, device=x.device))

#     X, Y = torch.meshgrid(x, y, indexing="ij")
#     r2 = X**2 + Y**2

#     amplitude = torch.exp(-r2 / wz**2)

#     phase = (2 * torch.pi / wavelength) * torch.sqrt(z**2 + r2)
#     phase_term = torch.exp(1j * phase)

#     delay = torch.sqrt(z**2 + r2) / Utils.c
#     delay = delay - torch.min(delay)
#     return amplitude * phase_term, delay


# 如果在f截止后用tanh(imag)过度,那么光源前后的误差看起来是更大的.但是由于振幅没有波动,猜测仅仅有后方的行波干扰场.虽然后方误差大,,前方似乎仅仅需要进行振幅校准而没有固定场干扰.
class AdjointSource:  # 暂时不改
    # 只需要存储Wm(1,1,1,w,wm),bm xyz(x,y,z,1,wm),Wt(1,1,1,t,wm)
    # 现在前面都增加(1,1)
    # xm,ym,zm来自显示器校正后的坐标,也可以自行添加.只支持均匀坐标
    def __init__(self, fdtd, monitor):
        # 这个init就是初始化函数
        self.device = fdtd.device
        self.debug = fdtd.debug

        self.x_grid, self.xm, self.x2 = monitor.x_grid, monitor.xm, monitor.x2
        self.y_grid, self.ym, self.y2 = monitor.y_grid, monitor.ym, monitor.y2
        self.z_grid, self.zm, self.z2 = monitor.z_grid, monitor.zm, monitor.z2

        self.dx2 = fdtd.dx2[self.x_grid[0] * 2 : self.x_grid[1] * 2 + 3] / (
            torch.min(fdtd.lams).cpu().item() / fdtd.N_res
        )
        self.dy2 = fdtd.dy2[self.y_grid[0] * 2 : self.y_grid[1] * 2 + 3] / (
            torch.min(fdtd.lams).cpu().item() / fdtd.N_res
        )
        self.dz2 = fdtd.dz2[self.z_grid[0] * 2 : self.z_grid[1] * 2 + 3] / (
            torch.min(fdtd.lams).cpu().item() / fdtd.N_res
        )

        self.n_offset = torch.tensor([self.x_grid[0], self.y_grid[0], self.z_grid[0]])

        w = 2 * torch.pi * Utils.c / fdtd.lams.view(-1)
        dt = fdtd.dt
        w_sort, _ = torch.sort(w)

        if w.numel() == 1:
            dw = 0.2 * w.item()
        else:
            dw = torch.min(
                torch.abs(torch.diff(w_sort))
            )  # 不能太大了,我还没有短脉冲补偿呢.
            dw = torch.min(dw, 0.2 * w_sort[0]).item()
        wm_num = w.numel() * 2
        wm = (
            torch.linspace(w_sort[0] - 0.9 * dw, w_sort[-1] + 0.9 * dw, wm_num)
            .view(1, 1, 1, 1, 1, 1, wm_num, 1)
            .to(w.device)
        )

        w = w.view(1, 1, 1, 1, 1, -1, 1, 1)

        a = torch.tensor(
            [0.355768, 0.4873960, 0.144232, 0.012604], device=w.device
        ).view(1, 1, 1, 1, 1, 1, 1, -1)
        a_index = torch.tensor([0, 1, 2, 3], device=w.device).view(
            1, 1, 1, 1, 1, 1, 1, -1
        )

        self.N = int(2 * torch.pi / dw / dt)

        self.Wm = (1 - torch.exp(1j * (self.N + 1) * (w - wm + a_index * dw) * dt)) / (
            1 - torch.exp(1j * (w - wm + a_index * dw) * dt)
        ) + (1 - torch.exp(1j * (self.N + 1) * (w - wm - a_index * dw) * dt)) / (
            1 - torch.exp(1j * (w - wm - a_index * dw) * dt)
        )
        self.Wm = self.Wm * 0.5 * a * ((-1) ** a_index)
        self.Wm = torch.sum(self.Wm, dim=7)  # 只需对a求和

        self.Wm_pinv = torch.linalg.pinv(
            self.Wm.view(-1, self.Wm.size(5), self.Wm.size(6))
        )  # (1,1,1, 1, 1, wm, w)
        self.Wm_pinv = self.Wm_pinv.view(
            1, 1, 1, 1, 1, self.Wm.size(6), self.Wm.size(5)
        )  # (1,1,1, 1, 1, w, wm)
        self.Wm_pinv = self.Wm_pinv.transpose(5, 6)  # (1,1,1, 1, 1, wm, w)

        n = (
            torch.linspace(0, self.N, self.N + 1)
            .to(w.device)
            .view(1, 1, 1, 1, 1, -1, 1, 1)
        )

        self.PWn = (
            torch.exp(-1j * wm * n * dt)
            * a
            * ((-1) ** a_index)
            * torch.cos(a_index * dw * dt * n)
        )
        self.PWn = torch.sum(2 * (self.PWn), dim=7)
        self.JWn = (
            a
            * ((-1) ** a_index)
            * torch.exp(-1j * wm * n * dt)
            * (
                -1j * wm * dt * torch.cos(a_index * dw * dt * n)
                - a_index * dw * dt * torch.sin(a_index * dw * dt * n)
            )
        )
        self.JWn = torch.sum(2 * (self.JWn), dim=7)

        self.bmx = torch.zeros(
            [
                fdtd.num_sources,
                fdtd.num_structures,
                self.x_grid[1] - self.x_grid[0] + 1,
                self.y_grid[1] - self.y_grid[0] + 2,
                self.z_grid[1] - self.z_grid[0] + 2,
                1,
                wm.shape[5],
            ],
            device=w.device,
        )  # bm是扩展后的系数
        self.bmy = torch.zeros(
            [
                fdtd.num_sources,
                fdtd.num_structures,
                self.x_grid[1] - self.x_grid[0] + 2,
                self.y_grid[1] - self.y_grid[0] + 1,
                self.z_grid[1] - self.z_grid[0] + 2,
                1,
                wm.shape[5],
            ],
            device=w.device,
        )  # bm是扩展后的系数
        self.bmz = torch.zeros(
            [
                fdtd.num_sources,
                fdtd.num_structures,
                self.x_grid[1] - self.x_grid[0] + 2,
                self.y_grid[1] - self.y_grid[0] + 2,
                self.z_grid[1] - self.z_grid[0] + 1,
                1,
                wm.shape[5],
            ],
            device=w.device,
        )  # bm是扩展后的系数

        self.Px = torch.zeros_like(
            monitor.Ex, dtype=torch.complex64, device=w.device
        )  # bm是扩展后的系数
        self.Py = torch.zeros_like(
            monitor.Ey, dtype=torch.complex64, device=w.device
        )  # bm是扩展后的系数
        self.Pz = torch.zeros_like(
            monitor.Ez, dtype=torch.complex64, device=w.device
        )  # bm是扩展后的系数

        self.shape_interp = torch.Size(
            [
                fdtd.num_sources,
                fdtd.num_structures,
                self.xm.numel(),
                self.ym.numel(),
                self.zm.numel(),
                3,
                w.numel(),
            ]
        )
        self.shape_nearest = torch.Size(
            [
                fdtd.num_sources,
                fdtd.num_structures,
                self.x_grid[1] - self.x_grid[0] + 1,
                self.y_grid[1] - self.y_grid[0] + 1,
                self.z_grid[1] - self.z_grid[0] + 1,
                3,
                w.numel(),
            ]
        )

    def Adjust(self, Px, Py, Pz, dV_correct):
        # 经过实践,J必须直接赋值到Yee网格上,如果反向插值会有较大的误差!!
        if dV_correct:
            self.Px = (
                Px
                / self.dx2[1::2].view(1, 1, -1, 1, 1, 1)
                / self.dy2[::2].view(1, 1, 1, -1, 1, 1)
                / self.dz2[::2].view(1, 1, 1, 1, -1, 1)
            )
            self.Py = (
                Py
                / self.dx2[::2].view(1, 1, -1, 1, 1, 1)
                / self.dy2[1::2].view(1, 1, 1, -1, 1, 1)
                / self.dz2[::2].view(1, 1, 1, 1, -1, 1)
            )
            self.Pz = (
                Pz
                / self.dx2[::2].view(1, 1, -1, 1, 1, 1)
                / self.dy2[::2].view(1, 1, 1, -1, 1, 1)
                / self.dz2[1::2].view(1, 1, 1, 1, -1, 1)
            )
        else:
            self.Px = Px.clone()
            self.Py = Py.clone()
            self.Pz = Pz.clone()

        self.bmx = torch.sum(self.Px.unsqueeze(6) * self.Wm_pinv, dim=5, keepdim=True)
        self.bmy = torch.sum(self.Py.unsqueeze(6) * self.Wm_pinv, dim=5, keepdim=True)
        self.bmz = torch.sum(self.Pz.unsqueeze(6) * self.Wm_pinv, dim=5, keepdim=True)

        err = torch.tensor(
            [
                torch.max(torch.abs(self.Px - self.Pw(0))),
                torch.max(torch.abs(self.Py - self.Pw(1))),
                torch.max(torch.abs(self.Pz - self.Pw(2))),
            ]
        )
        if self.debug:
            print("最大拟合误差", torch.max(err))

    def Clear(self):
        self.bmx *= 0
        self.bmy *= 0
        self.bmz *= 0

    def Pw(self, component):
        if component == 0:
            bm = self.bmx
        elif component == 1:
            bm = self.bmy
        elif component == 2:
            bm = self.bmz
        return torch.sum(bm * self.Wm, dim=6)

    def Pt(self, t, component):
        if component == 0:
            bm = self.bmx
        elif component == 1:
            bm = self.bmy
        elif component == 2:
            bm = self.bmz
        if t <= self.N:
            return torch.sum(bm * self.PWn[:, :, :, :, :, t : t + 1, :], dim=6).squeeze(
                -1
            )
        else:
            return torch.zeros(bm.shape[0:5], dtype=torch.complex64, device=self.device)

    def Jt(self, t, component):
        if component == 0:
            bm = self.bmx
        elif component == 1:
            bm = self.bmy
        elif component == 2:
            bm = self.bmz
        if t <= self.N:
            return torch.sum(bm * self.JWn[:, :, :, :, :, t : t + 1, :], dim=6).squeeze(
                -1
            )
        else:
            return torch.zeros(bm.shape[0:5], dtype=torch.complex64, device=self.device)


class PlaneSource(Geometry):
    # 目前只是平面波
    # 强制从z轴注入
    # 只用更新一个面
    # 暂时没有考虑数值色散
    def __init__(
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
        # 现在theta, phi, polar, phase都是一维列表
        super().__init__()
        self.z = z
        self.theta = torch.tensor(theta)
        self.phi = torch.tensor(phi)
        self.polar = -torch.tensor(polar)
        self.phase = torch.tensor(phase)

        # 物理量
        self.w_simu = None  # 一维,仿真角频率
        self.w_int = None  # 一维,积分角频率
        self.nw = None  # 一维,仿真折射率,并且作为积分角频率中的统一折射率
        self.k = None  # 仿真波长,介质中的波矢量

        # (光源,z*3,仿真波长,积分波长)
        self.Exw = None
        self.Eyw = None
        self.Hxw = None
        self.Hyw = None

        # (光源,x,y,仿真波长)
        self.phase_Ex = None
        self.phase_Ey = None
        self.phase_Hx = None
        self.phase_Hy = None

        # (光源,z*3,仿真波长,时间)
        self.Ext = None
        self.Eyt = None
        self.Hxt = None
        self.Hyt = None

        # 几何量
        self.bound = 0

        # 物理量
        self.index = None  # 更新介质处的折射率
        self.A_inc = None  # (光源并行,分量)
        self.custom_phasor = custom_phasor
        self.custom_delay = custom_delay
        self.custom_x = x
        self.custom_y = y

    def Initialization(self, fdtd):
        # 平面波源设置
        self.t_arr = fdtd.t_arr.view(-1)
        self.dt = fdtd.dt
        self.tau = fdtd.tau
        self.device = fdtd.device
        self.x = fdtd.x
        self.x_span = fdtd.x_span
        self.y = fdtd.y
        self.y_span = fdtd.y_span

        self.bound = Utils.Index_1d(fdtd.z2[::2], self.z)  # 通过n_delay_offset补偿
        # 计算局部位置
        x2 = fdtd.x2 - self.x
        y2 = fdtd.y2 - self.y
        z2 = fdtd.z2[2 * self.bound + 1 : 2 * self.bound + 3] - self.z

        xc_id = fdtd.pri_mat_idx.size(1) // 2
        yc_id = fdtd.pri_mat_idx.size(2) // 2

        er = fdtd.Material_list[fdtd.pri_mat_idx[0, xc_id, yc_id, self.bound]].er[0:1]
        er = torch.real(er)
        # 数值色散补偿
        f_co = fdtd.f_co[fdtd.pri_mat_idx[0, xc_id, yc_id, self.bound].cpu().item()]
        er *= f_co**2
        # end
        mu = 1
        f = fdtd.f.view(-1)
        f = f[0:1]
        self.w_simu = 2 * torch.pi * f
        self.nw = torch.sqrt(er * mu).view(-1)
        self.index = torch.mean(self.nw)
        # 入射方向计算
        self.A_inc = torch.zeros([fdtd.num_sources, 3], device=self.device)
        self.A_inc[:, 0] = torch.sin(torch.deg2rad(self.theta)) * torch.cos(
            torch.deg2rad(self.phi)
        )
        self.A_inc[:, 1] = torch.sin(torch.deg2rad(self.theta)) * torch.sin(
            torch.deg2rad(self.phi)
        )
        self.A_inc[:, 2] = torch.cos(torch.deg2rad(self.theta))

        lams = fdtd.lams.view(-1)
        lams = lams[0:1]  # 角度以第一个波长为准
        self.k = 2 * torch.pi / lams * self.nw
        # 恒定波矢量计算(光源,仿真波长)
        kx = self.A_inc[:, 0:1] * self.k.view(1, -1)
        ky = self.A_inc[:, 1:2] * self.k.view(1, -1)
        w_int_max = (
            torch.max(fdtd.f) * 2 * torch.pi + torch.sqrt(torch.tensor(32)) / self.tau
        )
        w_int_min = (
            torch.min(fdtd.f) * 2 * torch.pi - torch.sqrt(torch.tensor(32)) / self.tau
        )
        w_int_min = torch.clamp(w_int_min, min=0.2 * torch.min(fdtd.f) * 2 * torch.pi)
        self.w_int = torch.linspace(w_int_min, w_int_max, 400).to(self.device)
        # 计算kz的时候,如果是倏失波,则强制为0,不计入积分范围内
        kz = (
            (self.nw.view(1, -1, 1) * self.w_int.view(1, 1, -1) / Utils.c) ** 2
            - kx.unsqueeze(-1) ** 2
            - ky.unsqueeze(-1) ** 2
        )
        kz = torch.sqrt(kz.to(torch.complex64))
        self.Az_int = (
            (torch.real(kz))
            * Utils.c
            / self.w_int.view(1, 1, -1)
            / self.nw.view(1, -1, 1)
        ) - torch.tanh(
            (torch.imag(kz))
            * Utils.c
            / self.w_int.view(1, 1, -1)
            / self.nw.view(1, -1, 1)
        )  # 个人经验,加上这个可以缓解振幅震荡,但是新方案中暂且删除

        self.theta = self.theta.to(self.device)
        self.polar = self.polar.view(-1, 1, 1).to(self.device)
        self.phi = self.phi.view(-1, 1, 1).to(self.device)
        self.phase = self.phase.view(-1, 1, 1).to(self.device)
        phase_offset = torch.exp(1j * torch.deg2rad(self.phase)).to(torch.complex64)
        self.kz = kz.clone()  # 待会删了
        kz = kz.to(self.device)
        self.Az_int = self.Az_int.to(self.device)

        self.Exw = phase_offset * torch.cos(torch.deg2rad(self.polar - 90)) * torch.sin(
            torch.deg2rad(self.phi)
        ) - torch.sin(torch.deg2rad(self.polar - 90)) * self.Az_int * torch.cos(
            torch.deg2rad(self.phi)
        )
        self.Eyw = -phase_offset * torch.cos(
            torch.deg2rad(self.polar - 90)
        ) * torch.cos(torch.deg2rad(self.phi)) - torch.sin(
            torch.deg2rad(self.polar - 90)
        ) * self.Az_int * torch.sin(
            torch.deg2rad(self.phi)
        )
        self.Hxw = torch.sin(torch.deg2rad(self.polar - 90)) * torch.sin(
            torch.deg2rad(self.phi)
        ) + phase_offset * torch.cos(
            torch.deg2rad(self.polar - 90)
        ) * self.Az_int * torch.cos(
            torch.deg2rad(self.phi)
        )
        self.Hyw = -torch.sin(torch.deg2rad(self.polar - 90)) * torch.cos(
            torch.deg2rad(self.phi)
        ) + phase_offset * torch.cos(
            torch.deg2rad(self.polar - 90)
        ) * self.Az_int * torch.sin(
            torch.deg2rad(self.phi)
        )
        w_real = fdtd.f * 2 * torch.pi
        self.Amp = torch.exp(-(((-self.w_simu[0] + w_real) * self.tau) ** 2) / 4)

        self.z2 = z2.clone()
        temp = (
            torch.exp(
                1j
                * (-self.w_simu.view(1, -1, 1) + self.w_int.view(1, 1, -1))
                * t_offset
                * self.tau
            )
            * self.tau
            * torch.exp(
                -(
                    (
                        (-self.w_simu.view(1, -1, 1) + self.w_int.view(1, 1, -1))
                        * self.tau
                    )
                    ** 2
                )
                / 4
            )
        )

        Ew_weight = temp * torch.exp(1j * kz * z2[1])  # 同时包含了E和H
        Hw_weight = temp * torch.exp(
            1j * kz * z2[0] - 1j * self.w_int.view(1, 1, -1) * H_t_offset * fdtd.dt
        )  # 同时包含了E和H
        self.Exw = Ew_weight * self.Exw
        self.Eyw = Ew_weight * self.Eyw
        self.Hxw = Hw_weight * self.Hxw * torch.sqrt(er / mu).view(1, -1, 1)
        self.Hyw = Hw_weight * self.Hyw * torch.sqrt(er / mu).view(1, -1, 1)

        self.t_max = int(2 * t_offset * self.tau / self.dt)
        fft = torch.exp(
            -1j
            * self.w_int.view(1, 1, -1, 1)
            * self.t_arr[: self.t_max].view(1, 1, 1, -1)
        ) * (self.w_int[1] - self.w_int[0])

        self.Ext = torch.sum(fft * self.Exw.unsqueeze(-1), dim=-2)
        self.Eyt = torch.sum(fft * self.Eyw.unsqueeze(-1), dim=-2)
        self.Hxt = torch.sum(fft * self.Hxw.unsqueeze(-1), dim=-2)
        self.Hyt = torch.sum(fft * self.Hyw.unsqueeze(-1), dim=-2)
        fft = (
            torch.exp(
                1j
                * self.w_int.view(1, 1, 1, -1)
                * self.t_arr[: self.t_max].view(1, 1, -1, 1)
            )
            * self.dt
            / 2
            / torch.pi
        )
        self.Exwt = torch.sum(fft * torch.real(self.Ext.unsqueeze(-1)) * 2, dim=-2)
        self.Eywt = torch.sum(fft * torch.real(self.Eyt.unsqueeze(-1)) * 2, dim=-2)
        self.Hxwt = torch.sum(fft * torch.real(self.Hxt.unsqueeze(-1)) * 2, dim=-2)
        self.Hywt = torch.sum(fft * torch.real(self.Hyt.unsqueeze(-1)) * 2, dim=-2)

        self.phi_Ex = self.k.view(1, 1, 1, -1) * (
            self.A_inc[:, 0:1, None, None] * x2[1::2].view(1, -1, 1, 1)
            + self.A_inc[:, 1:2, None, None] * y2[::2].view(1, 1, -1, 1)
        )
        self.phi_Ey = self.k.view(1, 1, 1, -1) * (
            self.A_inc[:, 0:1, None, None] * x2[::2].view(1, -1, 1, 1)
            + self.A_inc[:, 1:2, None, None] * y2[1::2].view(1, 1, -1, 1)
        )
        self.phi_Hx = self.k.view(1, 1, 1, -1) * (
            self.A_inc[:, 0:1, None, None] * x2[::2].view(1, -1, 1, 1)
            + self.A_inc[:, 1:2, None, None] * y2[1::2].view(1, 1, -1, 1)
        )
        self.phi_Hy = self.k.view(1, 1, 1, -1) * (
            self.A_inc[:, 0:1, None, None] * x2[1::2].view(1, -1, 1, 1)
            + self.A_inc[:, 1:2, None, None] * y2[::2].view(1, 1, -1, 1)
        )

        self.phi_Ex = torch.exp(1j * self.phi_Ex)
        self.phi_Ey = torch.exp(1j * self.phi_Ey)
        self.phi_Hx = torch.exp(1j * self.phi_Hx)
        self.phi_Hy = torch.exp(1j * self.phi_Hy)

        self.delay_map_Hx = torch.zeros_like(
            self.phi_Hx[0, :, :, 0], dtype=torch.float32
        )
        self.delay_map_Hy = torch.zeros_like(
            self.phi_Hy[0, :, :, 0], dtype=torch.float32
        )
        self.delay_map_Ex = torch.zeros_like(
            self.phi_Ex[0, :, :, 0], dtype=torch.float32
        )
        self.delay_map_Ey = torch.zeros_like(
            self.phi_Ey[0, :, :, 0], dtype=torch.float32
        )
        if fdtd.dispersion == False:  # 含义变了
            self.Ext = self.Ext.squeeze(1)
            self.Eyt = self.Eyt.squeeze(1)
            self.Hxt = self.Hxt.squeeze(1)
            self.Hyt = self.Hyt.squeeze(1)
        self.t_source_delay = 0
        if (
            self.custom_phasor != None
        ):  # 现在必须要求custom_source是和波长无关的(x,y)二维张量
            x2 = fdtd.x2
            y2 = fdtd.y2
            self.custom_x = self.custom_x.to(fdtd.device)
            self.custom_y = self.custom_y.to(fdtd.device)
            self.custom_phasor = self.custom_phasor.to(fdtd.device)
            self.custom_delay = self.custom_delay.to(fdtd.device)

            custom_phasor = Utils.interp2d(
                self.custom_x,
                self.custom_y,
                self.custom_phasor,
                x2[1::2],
                y2[::2],
                method="cubic",
            )
            self.phi_Ex = self.phi_Ex * custom_phasor.unsqueeze(0).unsqueeze(-1)
            self.delay_map_Ex = (
                Utils.interp2d(
                    self.custom_x,
                    self.custom_y,
                    self.custom_delay,
                    x2[1::2],
                    y2[::2],
                    method="cubic",
                )
                / fdtd.dt
            )
            self.t_source_delay = max(
                self.t_source_delay, torch.max(self.delay_map_Ex).cpu().item()
            )

            custom_phasor = Utils.interp2d(
                self.custom_x,
                self.custom_y,
                self.custom_phasor,
                x2[::2],
                y2[1::2],
                method="cubic",
            )
            self.phi_Ey = self.phi_Ey * custom_phasor.unsqueeze(0).unsqueeze(-1)
            self.delay_map_Ey = (
                Utils.interp2d(
                    self.custom_x,
                    self.custom_y,
                    self.custom_delay,
                    x2[::2],
                    y2[1::2],
                    method="cubic",
                )
                / fdtd.dt
            )

            custom_phasor = Utils.interp2d(
                self.custom_x,
                self.custom_y,
                self.custom_phasor,
                x2[::2],
                y2[1::2],
                method="cubic",
            )
            self.phi_Hx = self.phi_Hx * custom_phasor.unsqueeze(0).unsqueeze(-1)
            self.delay_map_Hx = (
                Utils.interp2d(
                    self.custom_x,
                    self.custom_y,
                    self.custom_delay,
                    x2[::2],
                    y2[1::2],
                    method="cubic",
                )
                / fdtd.dt
            )

            custom_phasor = Utils.interp2d(
                self.custom_x,
                self.custom_y,
                self.custom_phasor,
                x2[1::2],
                y2[::2],
                method="cubic",
            )
            self.phi_Hy = self.phi_Hy * custom_phasor.unsqueeze(0).unsqueeze(-1)
            self.delay_map_Hy = (
                Utils.interp2d(
                    self.custom_x,
                    self.custom_y,
                    self.custom_delay,
                    x2[1::2],
                    y2[::2],
                    method="cubic",
                )
                / fdtd.dt
            )

    def Verify(self):
        ## 先验证方向对不对
        # 取某一个光源,某一个波长,z=0看Ex/Ey,Hx/Hy关于w_int的变化是不是和理论上一致
        Ex = self.Exw[0, -1, 0, :]
        Hy = self.Hyw[0, 0, 0, :]
        x = torch.cos(torch.deg2rad(self.polar - 90)) * torch.sin(
            torch.deg2rad(self.phi)
        ) - torch.sin(torch.deg2rad(self.polar - 90)) * self.Az_int * torch.cos(
            torch.deg2rad(self.phi)
        )
        x = x[0, 0, 0, :]

        y = -torch.sin(torch.deg2rad(self.polar - 90)) * torch.cos(
            torch.deg2rad(self.phi)
        ) + torch.cos(torch.deg2rad(self.polar - 90)) * self.Az_int * torch.sin(
            torch.deg2rad(self.phi)
        )
        y = y[0, 0, 0, :]
        y = y * torch.exp(
            -1j
            * (
                self.kz[0, 0] * (self.z2[-1] - self.z2[0])
                + self.w_int.view(-1) * H_t_offset * self.dt
            )
        )

        plt.plot(torch.real(Hy / Ex).cpu(), "r--")
        plt.plot(torch.imag(Hy / Ex).cpu(), "g")
        plt.plot(torch.real(y / x).cpu(), "b-o")
        plt.plot(torch.imag(y / x).cpu(), "y-o")

        ## 再验证关于w_int的kz变化对不对
        # simu_id = 0
        # plt.plot(torch.real(self.kz[0, simu_id, :]).cpu(), "r")
        # plt.plot(torch.imag(self.kz[0, simu_id, :]).cpu(), "g")
        # plt.show()

    def Get_phase_offset(self):
        k = self.k.view(1, -1)
        x_phase_offset = torch.exp(1j * k * self.A_inc[:, 0:1] * self.x_span)
        y_phase_offset = torch.exp(1j * k * self.A_inc[:, 1:2] * self.y_span)
        return x_phase_offset, y_phase_offset

    def Draw(self, fig):
        super().Draw(fig, face_color="white", alpha=0)
        #     s=0.5*mean([obj.x_span,obj.y_span,obj.z_span]);
        #     quiver3(obj.x,obj.y,obj.z,s*obj.A_inc(1),s*obj.A_inc(2),s*obj.A_inc(3), 'Color', 'magenta','LineWidth',3);
        #     quiver3(obj.x,obj.y,obj.z,s*obj.Ep(1),s*obj.Ep(2),s*obj.Ep(3), 'Color', 'cyan','LineWidth',3);
