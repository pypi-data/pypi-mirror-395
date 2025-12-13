# %%
import torch
import torch.nn.functional as F
import scipy
from tqdm import trange


class BluesteinDFT:
    # Due to the error in periodic expansion, it can be treated by making up for zeros in the future
    # Now only the central region is relatively accurate, and the surrounding area is affected by pseudo-diffraction by periodic conditions
    def __init__(self, f1, f2, fs, mout, m_input, device="cpu"):
        self.device = torch.device(device)
        self.f1 = f1
        self.f2 = f2
        self.fs = fs
        self.mout = mout
        self.m_input = m_input

        # Frequency adjustment
        f11 = f1 + (mout * fs + f2 - f1) / (2 * mout)
        f22 = f2 + (mout * fs + f2 - f1) / (2 * mout)
        self.f11 = f11
        self.f22 = f22

        # Chirp parameters
        a = torch.exp(1j * 2 * torch.pi * torch.tensor(f11 / fs))
        w = torch.exp(-1j * 2 * torch.pi * torch.tensor(f22 - f11) / (mout * fs))
        self.a = a.to(self.device)
        self.w = w.to(self.device)

        h = torch.arange(
            -m_input + 1,
            max(mout - 1, m_input - 1) + 1,
            device=self.device,
            dtype=torch.float64,
        )
        h = self.w ** ((h**2) / 2)

        self.h = h
        self.mp = m_input + mout - 1
        padded_len = 2 ** int(torch.ceil(torch.log2(torch.tensor(self.mp))))
        self.padded_len = padded_len

        h_inv = torch.zeros(padded_len, dtype=torch.complex64, device=self.device)
        h_inv[: self.mp] = 1 / h[: self.mp]
        self.ft = torch.fft.fft(h_inv)

        b_exp = torch.arange(0, m_input, device=self.device)
        self.b_phase = (self.a**-b_exp) * h[m_input - 1 : 2 * m_input - 1]

        l = torch.linspace(0, mout - 1, mout, device=self.device)
        l = l / mout * (f22 - f11) + f11
        Mshift = -m_input / 2
        self.Mshift = torch.exp(-1j * 2 * torch.pi * l * (Mshift + 0.5) / fs)

    def transform(self, x, dim=-1):
        x = x.to(self.device)
        m = self.m_input

        dim = dim if dim >= 0 else x.ndim + dim

        if x.shape[dim] != m:
            print(m)
            print(x.shape)
            raise ValueError(
                f"Expected dimension {dim} to be of size {m}, but got {x.shape[dim]}"
            )

        x = x.transpose(dim, -1)

        b_phase = self.b_phase.view((1,) * (x.ndim - 1) + (-1,))
        x_weighted = x * b_phase

        original_shape = x_weighted.shape
        x_weighted = x_weighted.reshape(-1, m)

        b_padded = torch.zeros(
            (x_weighted.shape[0], self.padded_len),
            dtype=torch.complex64,
            device=self.device,
        )
        b_padded[:, :m] = x_weighted

        b_fft = torch.fft.fft(b_padded, dim=1)
        conv = b_fft * self.ft[None, :]
        result = torch.fft.ifft(conv, dim=1)

        result = (
            result[:, self.m_input - 1 : self.mp] * self.h[self.m_input - 1 : self.mp]
        )
        result = result * self.Mshift[None, :]

        new_shape = list(original_shape[:-1]) + [self.mout]
        result = result.reshape(*new_shape)

        result = result.transpose(-1, dim)

        return result


class DebyeWolf:
    def __init__(
        self,
        Min,
        xrange,
        yrange,
        zrange,
        Mout,
        lams,  # list of wavelengths
        NA,
        focal_length,
        n1=1,
        device="cpu",
    ):
        self.device = device
        self.Min = Min
        self.xrange = xrange
        self.yrange = yrange
        self.z_arr = torch.linspace(zrange[0], zrange[1], Mout[2], device=device)
        self.Moutx, self.Mouty = Mout[0], Mout[1]
        lams = torch.tensor(lams, device=device)
        self.lams, self.k0, self.n1, self.NA, self.focal_length = (
            lams,
            2 * torch.pi / lams,
            n1,
            NA,
            focal_length,
        )

        self.N = (Min - 1) / 2

        m = torch.linspace(-Min / 2, Min / 2, Min, device=self.device)
        n = torch.linspace(-Min / 2, Min / 2, Min, device=self.device)
        self.m_grid, self.n_grid = torch.meshgrid(m, n, indexing="ij")

        self.th = torch.asin(
            torch.clamp(
                NA * torch.sqrt(self.m_grid**2 + self.n_grid**2) / (self.N * n1), max=1
            )
        )
        self.mask = self.th > torch.arcsin(torch.tensor(NA / n1))
        self.phi = torch.atan2(self.n_grid, self.m_grid)
        self.phi[self.phi < 0] += 2 * torch.pi

        self._sqrt_costh = 1 / torch.sqrt(torch.cos(self.th).unsqueeze(-1))
        self._sqrt_costh[torch.isnan(self._sqrt_costh)] = 0
        self._sqrt_costh[self.mask] = 0

        fs = lams * (Min - 1) / (2 * NA)
        self.fs = fs
        self.bluesteins_y = []
        self.bluesteins_x = []
        self.C = (
            -1j
            * torch.exp(1j * self.k0 * n1 * focal_length)
            * focal_length
            * (lams)
            / (self.n1)
            / fs
            / fs
        )
        fs = fs.cpu().tolist()
        for f in fs:
            self.bluesteins_y.append(
                BluesteinDFT(
                    f / 2 + self.yrange[0],
                    f / 2 + self.yrange[1],
                    f,
                    self.Mouty,
                    Min,
                    device=device,
                )
            )
            self.bluesteins_x.append(
                BluesteinDFT(
                    f / 2 + self.xrange[0],
                    f / 2 + self.xrange[1],
                    f,
                    self.Moutx,
                    Min,
                    device=device,
                )
            )
        self.E_ideals = torch.ones_like(self.lams)
        self.R = torch.stack(
            [
                -torch.sin(self.th) * torch.cos(self.phi),
                -torch.sin(self.th) * torch.sin(self.phi),
                torch.cos(self.th),
            ],
            dim=-1,
        )
        self.R = self.R.unsqueeze(-2)

    def __call__(self, E, correct=False):
        # The input E has shape (batch, x, y, 2, lam),
        # where the z-component is not included.
        # The output E has shape (batch, x, y, z, 3, lam).
        # For different wavelengths (lam), a simple for-loop is used for now.

        Ex_in, Ey_in = E[..., 0:1, :], E[..., 1:2, :]
        th = self.th.unsqueeze(-1).unsqueeze(-1)
        phi = self.phi.unsqueeze(-1).unsqueeze(-1)
        z_arr = self.z_arr.unsqueeze(0).unsqueeze(0).unsqueeze(-1)
        k0, n1 = self.k0.view(1, 1, 1, -1), self.n1

        costh = torch.cos(th)
        _sqrt_costh = self._sqrt_costh.unsqueeze(-1)
        phase = torch.exp(1j * k0 * n1 * z_arr * costh)
        deltadim = 0
        C = (self.C / self.E_ideals).view(1, 1, 1, -1)
        E_out = torch.zeros(
            [self.Moutx, self.Mouty, self.z_arr.numel(), 3, self.lams.numel()],
            dtype=torch.complex64,
            device=self.device,
        )
        if E.dim() == 5:
            th = th.unsqueeze(0)
            phi = phi.unsqueeze(0)
            z_arr = z_arr.unsqueeze(0)
            k0 = k0.unsqueeze(0)
            costh = costh.unsqueeze(0)
            _sqrt_costh = _sqrt_costh.unsqueeze(0)
            phase = phase.unsqueeze(0)
            C = C.unsqueeze(0)
            deltadim = 1
            E_out = torch.zeros(
                [
                    E.size(0),
                    self.Moutx,
                    self.Mouty,
                    self.z_arr.numel(),
                    3,
                    self.lams.numel(),
                ],
                dtype=torch.complex64,
                device=self.device,
            )
        Ex = (
            (
                Ex_in * (1 + (costh - 1) * torch.cos(phi) ** 2)
                + Ey_in * (costh - 1) * torch.cos(phi) * torch.sin(phi)
            )
            * phase
            * _sqrt_costh
        )

        Ey = (
            (
                Ex_in * (costh - 1) * torch.cos(phi) * torch.sin(phi)
                + Ey_in * (1 + (costh - 1) * torch.sin(phi) ** 2)
            )
            * phase
            * _sqrt_costh
        )

        Ez = (
            (Ex_in * torch.cos(phi) + Ey_in * torch.sin(phi))
            * torch.sin(th)
            * phase
            * _sqrt_costh
        )
        if correct:
            temp = torch.stack([Ex, Ey, Ez], dim=-1)
            temp = temp - 0.5 * self.R * torch.sum(self.R * temp, dim=-1, keepdim=True)
            Ex, Ey, Ez = temp[:, :, :, 0], temp[:, :, :, 1], temp[:, :, :, 2]
        for i in range(self.lams.numel()):
            E_out[..., 0, i] = self.bluesteins_x[i].transform(
                self.bluesteins_y[i].transform(Ex[..., i], dim=1 + deltadim),
                dim=0 + deltadim,
            )
            E_out[..., 1, i] = self.bluesteins_x[i].transform(
                self.bluesteins_y[i].transform(Ey[..., i], dim=1 + deltadim),
                dim=0 + deltadim,
            )
            E_out[..., 2, i] = self.bluesteins_x[i].transform(
                self.bluesteins_y[i].transform(Ez[..., i], dim=1 + deltadim),
                dim=0 + deltadim,
            )

        return C * E_out

    def Get_Z_offset_Phase(self, z):
        k0, n1 = self.k0, self.n1
        costh = torch.cos(self.th)
        phase = k0.view(1, 1, -1) * n1 * z * (-costh).unsqueeze(-1)
        return phase


def fft_circular_conv2d(E, G):
    E_fft = torch.fft.fft2(E.permute(2, 0, 1))
    G_fft = torch.fft.fft2(G.permute(2, 0, 1))
    C_fft = E_fft * G_fft
    C_ifft = torch.fft.ifft2(C_fft).permute(1, 2, 0)
    return C_ifft


def fourier_upsample2d(E: torch.Tensor, up_sample=1) -> torch.Tensor:
    x, y = E.shape[0], E.shape[1]
    Xn, Yn = x * up_sample, y * up_sample

    # 2D FFT（仅前两维），正交归一避免缩放差异
    F = torch.fft.fft2(E, dim=(0, 1), norm="ortho")
    Fc = torch.fft.fftshift(F, dim=(0, 1))

    # 频域补零到更大网格
    Fp = torch.zeros((Xn, Yn) + E.shape[2:], dtype=E.dtype, device=E.device)

    x0 = (Xn - x + 1) // 2
    y0 = (Yn - y + 1) // 2
    Fp[x0 : x0 + x, y0 : y0 + y, ...] = Fc

    Fp = torch.fft.ifftshift(Fp, dim=(0, 1))
    up_E_full = torch.fft.ifft2(Fp, dim=(0, 1), norm="ortho")

    X_keep = (x - 1) * up_sample + 1
    Y_keep = (y - 1) * up_sample + 1
    up_E = up_E_full[:X_keep, :Y_keep, ...] * up_sample
    return up_E


def upsample_coords_xy(x: torch.Tensor, y: torch.Tensor, up_sample: int):
    """
    Fourier 零填充插值对应的坐标放大：
      - 范围保持不变
      - 步长缩小 1/up_sample
    """
    if up_sample < 1:
        raise ValueError("up_sample 必须 >= 1")
    if up_sample == 1:
        return x, y

    if x.numel() < 2 or y.numel() < 2:
        raise ValueError("x 和 y 至少需要 2 个点用于定义范围。")

    # 原始步长
    dx = x[1] - x[0]
    dy = y[1] - y[0]

    # 新步长 = 原步长 / up_sample
    new_dx = dx / up_sample
    new_dy = dy / up_sample

    # 保持相同起止点，采样更密
    x_up = torch.linspace(
        x[0], x[-1], (x.numel() - 1) * up_sample + 1, device=x.device, dtype=x.dtype
    )
    y_up = torch.linspace(
        y[0], y[-1], (y.numel() - 1) * up_sample + 1, device=y.device, dtype=y.dtype
    )
    return x_up, y_up


class Luneburg:
    # The calculation method for Ez is different and omitted here.
    # The sampling theorem must be satisfied: T < lambda / 2
    def __init__(
        self,
        uv_len,  # Integration region
        x_range,
        y_range,
        z_range,
        sampling_interval,  # Sampling interval, a 1D array; strictly followed in xy-directions,
        # while z-direction is adaptively adjusted
        lams,
        focal_length,  # Evaluation is based on this focal length
        n1=1,
        up_sample=1,  # Integer > 1,
        sinc_interp=True,
        device="cuda",
    ):
        self.device = device
        self.up_sample = up_sample
        lams = torch.tensor(lams, device=device)
        self.lams = lams
        self.k = 2 * torch.pi * n1 / self.lams
        self.n1 = n1
        self.focal_length = focal_length

        # 先确定u,再确定x,最后确定ux
        u_arr = torch.linspace(
            -uv_len / 2 + sampling_interval[0] / 2,
            uv_len / 2 - sampling_interval[0] / 2,
            int(round(uv_len / sampling_interval[0])),
        )
        xs = (
            torch.ceil((x_range[0] - u_arr[0]) / sampling_interval[0])
            * sampling_interval[0]
            + u_arr[0]
        )
        xe = (
            torch.floor((x_range[1] - u_arr[0]) / sampling_interval[0])
            * sampling_interval[0]
            + u_arr[0]
        )
        x_arr = torch.linspace(
            xs, xe, 1 + int(torch.round((xe - xs) / sampling_interval[0]))
        )
        xs = x_arr[0] - u_arr[-1]
        xe = x_arr[-1] - u_arr[0]
        ux_arr = torch.linspace(
            xs - sampling_interval[0],
            xe,
            2 + int(torch.round((xe - xs) / sampling_interval[0])),
        )
        # 先确定v,再确定y,最后确定vy
        v_arr = torch.linspace(
            -uv_len / 2 + sampling_interval[1] / 2,
            uv_len / 2 - sampling_interval[1] / 2,
            int(round(uv_len / sampling_interval[1])),
        )
        ys = (
            torch.ceil((y_range[0] - v_arr[0]) / sampling_interval[1])
            * sampling_interval[1]
            + v_arr[0]
        )
        ye = (
            torch.floor((y_range[1] - v_arr[0]) / sampling_interval[1])
            * sampling_interval[1]
            + v_arr[0]
        )
        y_arr = torch.linspace(
            ys, ye, 1 + int(torch.round((ye - ys) / sampling_interval[1]))
        )
        ys = y_arr[0] - v_arr[-1]
        ye = y_arr[-1] - v_arr[0]
        vy_arr = torch.linspace(
            ys - sampling_interval[1],
            ye,
            2 + int(torch.round((ye - ys) / sampling_interval[1])),
        )
        #
        u_arr = u_arr.to(device)
        ux_arr = ux_arr.to(device)
        v_arr = v_arr.to(device)
        vy_arr = vy_arr.to(device)

        # 确定z
        z_arr = torch.linspace(
            z_range[0] + focal_length,
            z_range[1] + focal_length,
            int((z_range[1] - z_range[0]) / sampling_interval[2] / 2) * 2 + 1,
            device=device,
        )

        co_public = (
            -1j
            * sampling_interval[0]
            * sampling_interval[1]
            * n1
            / self.lams.view(1, 1, 1, -1)
        )  # / 4 / torch.pi
        R_q = torch.sqrt(
            (ux_arr.view(-1, 1, 1, 1)) ** 2
            + (vy_arr.view(1, -1, 1, 1)) ** 2
            + z_arr.view(1, 1, -1, 1) ** 2
        )
        G_2D = self.k * R_q * 1j
        G_2D = torch.exp(G_2D) / R_q**2 * co_public * (1 - 1 / G_2D)
        if sinc_interp:
            G_2D *= torch.sinc(
                n1
                * ux_arr.view(-1, 1, 1, 1)
                * sampling_interval[0]
                / (R_q * lams.view(1, 1, 1, -1))
            ) * torch.sinc(
                n1
                * vy_arr.view(1, -1, 1, 1)
                * sampling_interval[1]
                / (R_q * lams.view(1, 1, 1, -1))
            )

        self.G_2D = G_2D

        self.u_arr = u_arr
        self.v_arr = v_arr
        self.x_num = x_arr.numel()
        self.y_num = y_arr.numel()
        self.x_arr, self.y_arr = upsample_coords_xy(x_arr, y_arr, up_sample)
        self.z_arr = z_arr

        self.u_pad_num = ux_arr.numel() - u_arr.numel()
        self.v_pad_num = vy_arr.numel() - v_arr.numel()
        self.dS = sampling_interval[0] * sampling_interval[1]

    def __call__(self, E):
        # E should have shape (u, v, lam)
        if E.dim() == 3:
            E_padded = E
            pad = (
                0,
                0,  # No padding applied to the 2nd dimension (D2)
                self.v_pad_num,
                0,  # Extend on both sides of the 1st dimension (D1)
                self.u_pad_num,
                0,  # Extend on both sides of the 0th dimension (D0)
            )

            E_padded = F.pad(E_padded, pad, mode="constant", value=0)
            E_out = torch.zeros(
                [
                    self.x_num,
                    self.y_num,
                    self.z_arr.numel(),
                    self.lams.numel(),
                ],
                device=self.device,
                dtype=torch.complex64,
            )
            for z in range(self.z_arr.numel()):
                E_out[:, :, z, :] = fft_circular_conv2d(
                    E_padded, self.G_2D[:, :, z] * self.z_arr[z]
                )[
                    : self.x_num,
                    : self.y_num,
                ]
            E_out = fourier_upsample2d(E_out, self.up_sample)
            return E_out

    def Get_G_2D(self, x_f, y_f, z_f):  # Typically used for optimization and validation
        z = self.focal_length + z_f  # Detection coordinate
        co_public = -1j * self.dS * self.n1 / self.lams  # / 4 / torch.pi
        R_q = torch.sqrt(
            z**2
            + (x_f - self.u_arr.view(-1, 1, 1)) ** 2
            + (y_f - self.v_arr.view(1, -1, 1)) ** 2
        )
        ik0R = self.k.view(1, 1, -1) * R_q * 1j
        G_2D = torch.exp(ik0R) / R_q**2 * (1 - 1 / ik0R) * co_public

        return z * G_2D


class Luneburg_Direct:
    # SCALAR_DIFFRACTION_2D 2维标量衍射
    # Ez的计算方式不同，参照书籍。
    # 必须满足采样定理T<lambda/2
    # 只能用于小规模验证
    def __init__(
        self,
        z0,
        x_range,
        y_range,
        L,
        lams,
        n_out=1,
        device="cuda",
    ):
        self.device = device
        self.z0 = z0
        self.L = L
        lams = torch.tensor(lams, device=device).view(1, 1, -1)
        self.lams = lams
        self.k0 = 2 * torch.pi * n_out / self.lams
        self.x_arr = torch.linspace(
            x_range[0],
            x_range[1],
            round((x_range[1] - x_range[0]) / L + 1),
            device=device,
        ).view(-1, 1, 1)
        self.y_arr = torch.linspace(
            y_range[0],
            y_range[1],
            round((y_range[1] - y_range[0]) / L + 1),
            device=device,
        ).view(1, -1, 1)
        self.U_2D_shape = [self.x_arr.numel(), self.y_arr.numel(), self.lams.numel()]

    def Get_G_2D(self, x_f, y_f, z_f, h_offset=None):  # 暂时不允许r_f,z_f,tc的并行化
        # 验证用这个函数。获取绝对的格林函数
        # 返回的形式是(x,y,波长)
        device = self.device
        if h_offset == None:
            h_offset = torch.zeros(
                [self.x_arr.numel(), self.y_arr.numel(), 1], device=device
            )

        z = self.z0 + z_f  # 探测坐标

        co_public = -1j * self.L * self.L / self.lams  # / 4 / torch.pi
        R_q = torch.sqrt(
            (z - h_offset) ** 2 + (x_f - self.x_arr) ** 2 + (y_f - self.y_arr) ** 2
        )
        ik0R = self.k0 * R_q * 1j
        G_2D = torch.exp(ik0R) / R_q**2 * (1 - 1 / ik0R) * co_public

        G_2Dxxyy = (z - h_offset) * G_2D
        G_2Dzx = (self.x_arr - x_f) * G_2D
        G_2Dzy = (self.y_arr - y_f) * G_2D

        return (
            G_2Dxxyy,
            G_2Dzx,
            G_2Dzy,
        )  # 前两个卷积分量都一样,z轴分量不一样,要分别和xy分量作用

    def override_grid(self, x_arr, y_arr):
        # 覆盖原本的网格,主要用于TO过程,懒得再写一个带有ad的插值函数了
        self.x_arr = x_arr.view(-1, 1, 1).to(self.device)
        self.y_arr = y_arr.view(1, -1, 1).to(self.device)
        self.L = torch.sqrt((x_arr[1] - x_arr[0]) * (y_arr[1] - y_arr[0])).cpu().item()

    def Get_E_far(self, E_near, x_f_arr, y_f_arr, z_f_arr, h_offset=None):
        # 理论上讲直接矢量化计算也行,但是出于内存的考虑还是一个一个算吧
        # E_near可以是(x,y,3分量,波长)或者纯标量
        if E_near.dim() == 4:
            E_far = torch.zeros(
                [
                    x_f_arr.numel(),
                    y_f_arr.numel(),
                    z_f_arr.numel(),
                    3,
                    self.lams.numel(),
                ],
                dtype=torch.complex64,
                device=self.device,
            )
            for i in range(x_f_arr.numel()):
                for j in range(y_f_arr.numel()):
                    for k in range(z_f_arr.numel()):
                        Gxxyy, Gzx, Gzy = self.Get_G_2D(
                            x_f_arr[i], y_f_arr[j], z_f_arr[k], h_offset
                        )
                        E_far[i, j, k, 0] = torch.sum(
                            Gxxyy * E_near[:, :, 0], dim=(0, 1)
                        )
                        E_far[i, j, k, 1] = torch.sum(
                            Gxxyy * E_near[:, :, 1], dim=(0, 1)
                        )
                        E_far[i, j, k, 2] = torch.sum(
                            Gzx * E_near[:, :, 0] + Gzy * E_near[:, :, 1], dim=(0, 1)
                        )
        elif E_near.dim() == 3:
            E_far = torch.zeros(
                [x_f_arr.numel(), y_f_arr.numel(), z_f_arr.numel(), self.lams.numel()],
                dtype=torch.complex64,
                device=self.device,
            )
            for i in range(x_f_arr.numel()):
                for j in range(y_f_arr.numel()):
                    for k in range(z_f_arr.numel()):
                        Gxxyy, _, _ = self.Get_G_2D(
                            x_f_arr[i], y_f_arr[j], z_f_arr[k], h_offset
                        )
                        E_far[i, j, k] = torch.sum(Gxxyy * E_near, dim=(0, 1))
        return E_far


b2 = 3.054238425420026  # 二阶贝塞尔函数的最大值点对应的x值


# 看样子平面衍射公式有点小问题啊,到时候改一下
class Diffraction_R:
    # SCALAR_DIFFRACTION_R 径向对称标量衍射公式
    # Ez的计算方式不同，参照书籍。
    # 如果是常量要满足采样定理T<lambda/(2*NA)
    # 现在要兼容涡旋光的计算模式
    # 目前U_parallel_num主要是处理优化问题而引入的
    def __init__(
        self,
        focal_length,
        R_size,
        L,
        lams,
        offset,
        U_parallel_num=1,
        n_basis=[],
        n_out=1,
        device="cuda",
    ):
        self.device = device
        self.focal_length = focal_length
        self.R_size = (int(R_size / L) + 0.5 + offset) * L
        self.L = L
        lams = torch.tensor(lams, device=device)
        self.lams = lams
        self.k0 = 2 * torch.pi * n_out / self.lams
        if n_basis == []:
            n_basis = torch.ones_like(self.lams)
        self.n_basis = n_basis
        self.r_arr = torch.arange(
            (offset + 0.5) * L, R_size + 0.5 * L, L, device=device
        )
        self.NA = (
            n_out
            * self.R_size
            / torch.sqrt(
                torch.tensor(self.R_size**2 + self.focal_length**2, device=device)
            )
        )
        if self.L > min(self.lams) / (2 * self.NA):
            print("间隔不符合采样定理")
        # self.FocusRadius = 1.5 * max(self.lams) / self.NA
        # self.Ur_arr = torch.zeros(
        #     [U_parallel_num, self.r_arr.numel(), self.lams.numel()], device=device
        # )
        self.U_parallel_num = U_parallel_num
        # 计算归一化光强
        E_ideal = (
            torch.sqrt(self.n_basis)
            * torch.pi
            * self.focal_length
            / self.lams
            * torch.log(
                torch.tensor(1 + (self.R_size / self.focal_length) ** 2, device=device)
            )
            / 4
            / torch.pi
        )
        self.I_ideal = abs(E_ideal) ** 2

    def override_grid(self, r_arr):
        # 覆盖原本的网格,主要用于TO过程,懒得再写一个带有ad的插值函数了
        self.L = ((r_arr[-1] - r_arr[0]) / (r_arr.numel() - 1)).cpu().item()
        self.r_arr = r_arr

    # 计算格林函数,反正只要算一次,慢一点也无所谓
    # 如果是涡旋光,获取的是极角相同的点的电场,其它极角有相位1.荷数用tc表示
    # 其余的都可以矢量化,tc还是用循环吧
    # tc,r_f的维度必须和波长相同,即必须指定每个波长对应的拓扑荷和优化位置
    def Get_GR_relative(
        self, tc, r_f, z_f=0, phi=0, h_offset=None
    ):  # 暂时不允许r_f,z_f,tc的并行化哈,要用的话暂时在外面给我循环调用去
        # 优化用这个函数。获取相对电场（实际电场与理想透镜中心电场之比）
        # h_offset的维度必须和r_arr一致
        # (r,lam)
        device = self.device
        r_f = torch.tensor([r_f], device=device).view(-1)
        tc = torch.tensor([tc]).view(-1)
        if r_f.numel() != self.lams.numel():
            print("r_f的维度必须和波长对应")
        if tc.numel() != self.lams.numel():
            print("tc的维度必须和波长对应")

        Gr_arr = torch.zeros(
            [self.r_arr.numel(), self.lams.numel()],
            device=device,
            dtype=torch.complex64,
        )
        if h_offset == None:
            h_offset = torch.zeros_like(self.r_arr)

        for i in range(tc.numel()):
            R_q = torch.sqrt(
                (z_f + self.focal_length - h_offset) ** 2 + self.r_arr**2 + r_f[i] ** 2
            )
            co = -2j / torch.log(1 + (self.r_arr[-1] / self.focal_length) ** 2)
            co = co / torch.sqrt(self.n_basis[i]) * (1 - h_offset / self.focal_length)
            self.r_R_arr = self.r_arr / R_q
            rdr_R = self.r_R_arr * self.L
            ik0R = self.k0[i] * R_q * 1j
            J = (self.k0[i] * r_f[i] * self.r_R_arr).cpu()
            J = scipy.special.jv(tc[i], J.numpy())
            J = (
                torch.tensor(J, device=device) * (-1j) ** tc[i]
            )  # 注意方向哈,有可能算出来相位有差别,LCP和RCP各不一样捏
            # 而且算的是相同的方向没有考虑phi咯
            temp = (
                co * rdr_R * torch.exp(ik0R) / R_q * (1 - 1 / ik0R) * J
            )  # 贝塞尔函数，用于计算不在焦点的电场,相比焦点，仅仅多乘了一个这个。
            Gr_arr[:, i] = (
                temp * torch.exp(1j * tc[i] * phi) * torch.sinc(rdr_R / self.lams[i])
            )  # 最后一项主要是应用了常量假设
        return Gr_arr

    def Get_efficiency(self, U, radius, sample_num):
        r_f = torch.linspace(0, radius, sample_num, device=self.device)
        dr = r_f[1] - r_f[0]
        I_f = torch.zeros(r_f.numel(), self.lams.numel(), device=self.device)
        for i in trange(r_f.numel()):
            G = self.Get_GR_relative(
                torch.zeros_like(self.lams).tolist(),
                (r_f[i] * torch.ones_like(self.lams)).tolist(),
            )
            E_far = torch.sum(U * G, dim=0)
            I_f[i, :] = torch.abs(E_far) ** 2
        out = (
            torch.sum(I_f * r_f.view(-1, 1) * dr, 0)
            * self.I_ideal
            * 2
            / (self.R_size**2)
        )
        return out


class Grating:
    # 专门分析衍射
    # 一定在fdtd初始化之后执行e
    # 基地和出射介质都是不管色散的
    # 输出维度(光源,结构,x,y,z,分量,波长,衍射级次)
    def __init__(self, source, monitor, plane_dim=2):
        self.A_inc = source.A_inc.clone()
        self.x = monitor.xm.clone().view(1, 1, -1, 1, 1, 1, 1, 1)
        self.y = monitor.ym.clone().view(1, 1, 1, -1, 1, 1, 1, 1)
        self.lams = monitor.lams.clone().view(1, 1, 1, 1, 1, 1, -1, 1)
        self.n_in = source.index
        self.n_out = monitor.index
        self.Tx = monitor.x_span
        self.Ty = monitor.y_span

    def Set_G(self, n, m):
        # 预先设置格林函数
        # 默认z轴光轴,暂时只支持正入射
        # 注意弧度/角度
        # 输出维度(光源,结构,x,y,z,分量,波长,衍射级次)
        n = torch.tensor(n, device=self.A_inc.device).view(1, 1, 1, 1, 1, 1, 1, -1)
        m = torch.tensor(m, device=self.A_inc.device).view(1, 1, 1, 1, 1, 1, 1, -1)
        Ax = self.A_inc[:, 0].view(-1, 1, 1, 1, 1, 1, 1, 1)
        Ay = self.A_inc[:, 1].view(-1, 1, 1, 1, 1, 1, 1, 1)
        Az = self.A_inc[:, 2].view(-1, 1, 1, 1, 1, 1, 1, 1)

        kz_inc = Az * self.n_in * 2 * torch.pi / self.lams
        kx_out = 2 * torch.pi * n / self.Tx + Ax * self.n_in * 2 * torch.pi / self.lams
        ky_out = 2 * torch.pi * m / self.Ty + Ay * self.n_in * 2 * torch.pi / self.lams
        k_out = self.n_out * 2 * torch.pi / self.lams
        kz_out = torch.sqrt(k_out**2 - kx_out**2 - ky_out**2)
        co = torch.sqrt(torch.real(kz_out / kz_inc))  # 更好只是为了让振幅平方就是效率
        self.G = (
            co * torch.exp(-1j * kx_out * self.x) * torch.exp(-1j * ky_out * self.y)
        )

    def Get_efficiency(self, E, projection=False):
        # 输入E的维度和标准的一致
        # 返回光源,波长,衍射级次
        I = (
            torch.mean(E.unsqueeze(-1) * self.G, dim=(2, 3, 4)) ** 2
        )  # 输出维度(光源,结构,分量,波长,衍射级次)
        if projection:
            return torch.sum(torch.real(I), 2)  # 输出维度(光源,结构,波长,衍射级次)
        else:
            return torch.sum(torch.abs(I), 2)  # 输出维度(光源,结构,波长,衍射级次)

    def Get_tr(self, E):
        return torch.mean(
            E.unsqueeze(-1) * self.G, dim=(2, 3, 4)
        )  # 输出维度(光源,结构,分量,波长,衍射级次)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    lams = [0.62]
    device = "cuda"
    xysize = 40.25  # 奇偶都试一试
    period = 0.25
    RR = xysize / 2
    ff = torch.sqrt(torch.tensor(RR / 0.85) ** 2 - RR**2)

    dfft = Luneburg(
        xysize,
        [-2, 4],
        [-3, 2],
        [0, 0],  # 这个距离和焦距可能有区别,再优化的时候以这个为准
        [period, period, 0.2],
        lams,
        focal_length=ff,
        up_sample=5,  # 先验证不升采样的，应该完全一样才对
        sinc_interp=False,
        device=device,
    )
    G_2D = dfft.Get_G_2D(0, 0, 0)
    phase = torch.zeros_like(G_2D, dtype=torch.float32)
    u_arr = dfft.u_arr.view(-1, 1)
    v_arr = dfft.v_arr.view(1, -1)
    phase[:, :, 0] = (
        -2
        * torch.pi
        / lams[0]
        * torch.sqrt((u_arr + 0.5) ** 2 + (v_arr - 0.5) ** 2 + ff**2)
    ) + torch.atan2(
        v_arr + 2, u_arr - 1
    )  # 带点漂移的相位

    Ein = torch.exp(1j * (phase))
    d2 = Luneburg_Direct(
        0,
        [-xysize / 2, xysize / 2],
        [-xysize / 2, xysize / 2],
        period,
        [0.62],
        1,
        device=device,
    )
    d2.override_grid(dfft.u_arr, dfft.v_arr)
    Eout1 = dfft(Ein)
    Eout2 = d2.Get_E_far(
        Ein, dfft.x_arr.view(-1), dfft.y_arr.view(-1), dfft.z_arr.view(-1)
    )
    XF, YF = torch.meshgrid(dfft.x_arr.cpu(), dfft.y_arr.cpu(), indexing="ij")
    print(torch.max(torch.abs(Eout1 - Eout2)))
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.pcolormesh(XF, YF, Eout1[:, :, 0, 0].abs().cpu())
    plt.colorbar()
    plt.subplot(1, 3, 2)
    plt.pcolormesh(XF, YF, Eout2[:, :, 0, 0].abs().cpu())
    plt.colorbar()
    plt.subplot(1, 3, 3)
    plt.pcolormesh(XF, YF, torch.abs(Eout1 - Eout2)[:, :, 0, 0].cpu())
    plt.colorbar()
