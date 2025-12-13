# %%放置一些优化相关的常用函数
# 包括随机扰动的鲁棒性直方图分析
# 现在需要考虑一个维度为1的情况了

import torch
from torch import tensor, zeros, norm
from torchopticsy.FDTD.Structure import create_distance_weighted_kernel
import numpy as np
import torchopticsy.mma as mma
from torchvision.transforms.functional import gaussian_blur
import torch.nn.functional as F


# 步骤 1: 创建线性帽形滤波器核（按距离，支持1D/2D，圆形核）
def create_filter_kernel(r, dim=2):
    """
    生成 1D 或 2D 的线性帽形滤波器核（基于欧氏距离），
    使用权重  w = max(0, 1 - d/(r+1))，
    确保在 d = r 时仍为正数 1/(r+1)。

    参数:
        r   : torch.tensor 标量，滤波半径
        dim : 1 或 2，生成 1D 或 2D 核

    返回:
        dim=1: kernel.shape = [size]
        dim=2: kernel.shape = [size, size]
    """
    R = float(r)
    size = 2 * int(R) + 1

    if dim == 1:
        # 一维: 只考虑距离 i - R
        coords = torch.arange(size, dtype=torch.float32)
        dist = torch.abs(coords - R)  # [size]
        weights = torch.clamp(1.0 - dist / (R + 1.0), min=0.0)
        kernel = weights / weights.sum()
        return kernel

    elif dim == 2:
        # 二维: 欧氏距离 √((i-R)^2 + (j-R)^2)
        xs = torch.arange(size, dtype=torch.float32)
        ys = torch.arange(size, dtype=torch.float32)
        grid_x, grid_y = torch.meshgrid(xs, ys, indexing="ij")  # [size, size]

        dist = torch.sqrt((grid_x - R) ** 2 + (grid_y - R) ** 2)
        weights = torch.clamp(1.0 - dist / (R + 1.0), min=0.0)  # 圆形帽
        kernel = weights / weights.sum()
        return kernel

    else:
        raise ValueError("dim must be 1 or 2")


# 步骤 2: 线性滤波,
def linear_hat_filter(
    design_field, filter_kernel, parallel_dim=None, padding_mode=None
):
    """
    通用滤波函数：
    - 自动识别1D或2D（根据kernel维度）
    - 自动从 kernel 大小推断 r
    - 支持 zero / periodic padding
    - parallel_dim=None 时自动恢复形状
    - output 和 input 的形状一致
    """

    # -----------------------
    # 1. 判定卷积维度 + 推断 r
    # -----------------------
    if filter_kernel.dim() == 1:
        conv_dim = 1
        K = filter_kernel.shape[0]
        r = (K - 1) // 2
    else:
        conv_dim = 2
        K = filter_kernel.shape[0]
        r = (K - 1) // 2

    # 默认全部 zero padding
    if padding_mode is None:
        padding_mode = ["zero"] * conv_dim

    x = design_field
    original_shape = x.shape
    original_dim = x.dim()

    # -----------------------
    # 2. 把 parallel_dim 移到 batch=0
    # -----------------------
    moved_parallel = False
    if parallel_dim is not None:
        if parallel_dim != 0:
            x = x.transpose(0, parallel_dim)
            moved_parallel = True

    # -----------------------
    # 3. reshape 成 conv 输入格式
    # -----------------------
    if conv_dim == 1:
        # 1D 输入
        if x.dim() == 1:  # [L]
            x = x.unsqueeze(0).unsqueeze(0)  # [1,1,L]
            added_batch = True
        elif x.dim() == 2:  # [P,L]
            x = x.unsqueeze(1)  # [P,1,L]
            added_batch = False
        else:
            raise ValueError("Invalid input shape for 1D kernel.")
    else:
        # 2D 输入
        if x.dim() == 2:  # [H,W]
            x = x.unsqueeze(0).unsqueeze(0)  # [1,1,H,W]
            added_batch = True
        elif x.dim() == 3:  # [P,H,W]
            x = x.unsqueeze(1)  # [P,1,H,W]
            added_batch = False
        else:
            raise ValueError("Invalid input shape for 2D kernel.")

    # -----------------------
    # 4. padding
    # -----------------------
    if conv_dim == 1:
        mode = padding_mode
        if mode == "periodic":
            x = torch.cat([x[..., -r:], x, x[..., :r]], dim=-1)
        else:
            x = F.pad(x, (r, r))

        kernel = filter_kernel[None, None, :]
        y = F.conv1d(x, kernel).squeeze(1)  # [P,L] or [1,L]

    else:
        mode_x, mode_y = padding_mode

        # X padding
        if mode_x == "periodic":
            x = torch.cat([x[:, :, -r:, :], x, x[:, :, :r, :]], dim=2)
        else:
            x = F.pad(x, (0, 0, r, r))

        # Y padding
        if mode_y == "periodic":
            x = torch.cat([x[:, :, :, -r:], x, x[:, :, :, :r]], dim=3)
        else:
            x = F.pad(x, (r, r, 0, 0))

        kernel = filter_kernel[None, None, :, :]
        y = F.conv2d(x, kernel).squeeze(1)  # [P,H,W] or [1,H,W]

    # -----------------------
    # 5. 恢复 parallel_dim
    # -----------------------
    if moved_parallel:
        dims = list(range(y.dim()))
        dims[0], dims[parallel_dim] = dims[parallel_dim], dims[0]
        y = y.permute(*dims)

    # -----------------------
    # 6. 如果一开始没有 batch → 去掉多余维度
    # -----------------------
    if parallel_dim is None:
        # 1D: 输出从 [1,L] → [L]
        # 2D: 输出从 [1,H,W] → [H,W]
        if added_batch:
            y = y.squeeze(0)

    return torch.clamp(y, 0.01, 0.99)


# 步骤 3: 投影函数,beta要增大哈
def projection_function(filtered_field, beta, eta=0.5):
    """
    将过滤后的设计场投影到物理场上，使用阈值 eta。
    """
    eta = torch.tensor(eta, device=filtered_field.device)
    return (torch.tanh(beta * eta) + torch.tanh(beta * (filtered_field - eta))) / (
        torch.tanh(beta * eta) + torch.tanh(beta * (1.0 - eta))
    )


# 步骤 4: 合并指示函数 I,就是投影值接近0/1且周围和自身一样的地方
# 而要惩罚指示函数存在值但是滤波后的函数值不够靠近0-1的地方
def geometric_constraints(filtered_field, r, parallel_dim=None, alpha=2):
    """
    适配 1D/2D 输入和任意并行维度的几何约束计算函数。

    参数:
        filtered_field : 输入场
                         1D: [L], [P,L], [L,P]
                         2D: [H,W], [P,H,W], [H,P,W], [H,W,P]
        r : 半径 (Tensor 或 int)
        parallel_dim : 并行维度 axis (None 表示没有 batch/P 维度)

    返回:
        constraint_sum, I1, I2
    """

    # -------------------------
    # 1. 识别维度 1D 或 2D
    # -------------------------
    x = filtered_field

    # 去掉并行维度后看看剩余的空间维度
    dims = list(range(x.dim()))
    if parallel_dim is not None:
        dims.remove(parallel_dim)

    space_dims = len(dims)

    if space_dims == 1:
        conv_dim = 1
    elif space_dims == 2:
        conv_dim = 2
    else:
        raise ValueError("Input must be 1D or 2D with optional parallel dimension.")

    # -------------------------
    # 2. 将 parallel_dim 移到最前（batch）
    # -------------------------
    moved_parallel = False
    if parallel_dim is not None and parallel_dim != 0:
        x = x.transpose(0, parallel_dim)
        moved_parallel = True

    # 此时:
    # 1D: [L] 或 [P,L]
    # 2D: [H,W] 或 [P,H,W]

    # -------------------------
    # 3. reshape 成 conv 输入格式
    # -------------------------
    if conv_dim == 1:
        # 1D 输入统一成 [B,1,L]
        if x.dim() == 1:  # [L]
            x = x.unsqueeze(0).unsqueeze(0)
            added_batch = True
        else:  # [P,L]
            x = x.unsqueeze(1)
            added_batch = False

    else:
        # 2D 输入统一成 [B,1,H,W]
        if x.dim() == 2:  # [H,W]
            x = x.unsqueeze(0).unsqueeze(0)
            added_batch = True
        else:  # [P,H,W]
            x = x.unsqueeze(1)
            added_batch = False

    # -------------------------
    # 4. 计算梯度（使用 replicate padding）
    # -------------------------
    if conv_dim == 1:
        # 差分核 [-1, 0, 1]
        kernel = torch.tensor(
            [-1, 0, 1], dtype=torch.float32, device=filtered_field.device
        ).view(1, 1, 3)

        # replicate padding
        x_pad = F.pad(x, (1, 1), mode="replicate")

        grad = F.conv1d(x_pad, kernel).squeeze(1)  # [B,L]
        grad_mag = torch.abs(grad)

    else:
        # Sobel 核
        sobel_x = torch.tensor(
            [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
            dtype=torch.float32,
            device=filtered_field.device,
        ).view(1, 1, 3, 3)

        sobel_y = torch.tensor(
            [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],
            dtype=torch.float32,
            device=filtered_field.device,
        ).view(1, 1, 3, 3)

        x_pad = F.pad(x, (1, 1, 1, 1), mode="replicate")

        gx = F.conv2d(x_pad, sobel_x).squeeze(1)
        gy = F.conv2d(x_pad, sobel_y).squeeze(1)

        grad_mag = torch.sqrt(gx**2 + gy**2)

    # -------------------------
    # 5. 计算 I 函数与约束项
    # -------------------------
    c = alpha * float(r) ** 2

    I = torch.exp(-c * grad_mag**2)
    core = torch.minimum(10 * (torch.abs(x - 0.5) - 0.4), torch.tensor(0.0))

    constraint = I * (core**2)
    constraint = torch.clamp(constraint - 1e-3, min=0)

    # -------------------------
    # 6. 恢复 parallel_dim
    # -------------------------
    if moved_parallel:
        dims = list(range(constraint.dim()))
        dims[0], dims[parallel_dim] = dims[parallel_dim], dims[0]
        constraint = constraint.permute(*dims)
    # -------------------------
    # 7. 去掉 batch 维度
    # -------------------------
    if parallel_dim is None and added_batch:
        constraint = constraint.squeeze(0)

    return constraint.sum()


def Sensitivity_filtering(input_tensor, kernel, periodic_num):
    # 之前没有试过直接对灵敏度滤波,今天试一试
    # 确保输入张量是四维的 (p, x, y, z)
    if input_tensor.dim() != 4:
        raise ValueError("输入张量必须是四维的 (p, x, y, z)")

    # 将核调整为符合卷积操作的形状 (out_channels, in_channels, d, h, w)
    kernel = kernel.unsqueeze(0).unsqueeze(0)

    # 将输入张量调整为符合卷积操作的形状 (batch_size, channels, d, h, w)
    input_tensor = input_tensor.unsqueeze(1)

    # 确定填充大小
    padding = kernel.size(2) // 2  # 多出一格用于卷积

    # 根据 periodic_num 设置填充模式

    # 逐个维度应用填充
    if periodic_num[0] > 0:
        input_tensor = F.pad(
            input_tensor, (0, 0, 0, 0, padding, padding), mode="circular"
        )
    else:
        input_tensor = F.pad(
            input_tensor, (0, 0, 0, 0, padding, padding), mode="reflect"
        )
    if periodic_num[1] > 0:
        input_tensor = F.pad(
            input_tensor, (0, 0, padding, padding, 0, 0), mode="circular"
        )
    else:
        input_tensor = F.pad(
            input_tensor, (0, 0, padding, padding, 0, 0), mode="reflect"
        )

    if periodic_num[2] > 0:
        input_tensor = F.pad(
            input_tensor, (padding, padding, 0, 0, 0, 0), mode="circular"
        )
    else:
        input_tensor = F.pad(
            input_tensor, (padding, padding, 0, 0, 0, 0), mode="reflect"
        )

    # 应用卷积操作
    input_tensor = F.conv3d(input_tensor, kernel)

    # 调整输出张量的形状回到 (p, x, y, z)
    input_tensor = input_tensor.squeeze(1)
    return input_tensor


# 现在期望Convert_variables直接就能得到完整的结构,包括了滤波二值化等操作
def Convert_variables(variables, show):
    return (
        variables  # 尽管我们可以预先对于场先做变换(累加等)减少计算图中的变量以提高速度
    )
    # 但是从通用性的角度来说,还是直接构造从优化变量到四维矢量的映射最好,并且始终保持材料网格的密度和仿真网格相当.


def FOM(E, x):
    return 0, 0


def Constraint(x):
    return 0 * torch.mean(x) - 1  #


# 应用位移场到图像
def generate_displacement_fields(size, alpha, sigma, num_fields=4, device="cuda"):
    # 使用矢量化方式生成4个随机位移场
    displacement_x = torch.rand(num_fields, 1, size[0], size[1], device=device) * 2 - 1
    displacement_y = torch.rand(num_fields, 1, size[0], size[1], device=device) * 2 - 1

    # 使用高斯模糊平滑位移场
    displacement_x = gaussian_blur(
        displacement_x, kernel_size=(sigma * 6 + 1, sigma * 6 + 1), sigma=sigma
    )
    displacement_y = gaussian_blur(
        displacement_y, kernel_size=(sigma * 6 + 1, sigma * 6 + 1), sigma=sigma
    )

    # 合并位移场
    displacement_fields = torch.cat((displacement_x, displacement_y), dim=1)

    # 计算平均位移距离
    avg_distance = torch.mean(
        torch.sqrt(
            displacement_fields[:, 0, :, :] ** 2 + displacement_fields[:, 1, :, :] ** 2
        )
    )

    displacement_fields = displacement_fields / (avg_distance + 1e-8)  # 防止除以0

    # 应用缩放因子α
    displacement_fields = displacement_fields * alpha

    return displacement_fields


def apply_displacement(image, displacement_fields):
    # image(x,y)
    # displacement_fields(并行,x,y)
    num_fields = displacement_fields.size(0)
    xsize = image.size(0)
    ysize = image.size(1)

    # 创建网格并扩展到每个位移场
    grid = (
        torch.stack(
            torch.meshgrid(torch.arange(xsize), torch.arange(ysize), indexing="ij"),
            dim=-1,
        )
        .float()
        .to(image.device)
    )
    print(grid.shape)
    grid = grid.unsqueeze(0).expand(
        num_fields, -1, -1, -1
    )  # 扩展为 (num_fields, H, W, 2)

    # 应用位移场到网格
    grid = grid + displacement_fields.permute(0, 2, 3, 1)

    # 归一化坐标
    grid[..., 0] = 2.0 * grid[..., 0] / (xsize - 1) - 1.0
    grid[..., 1] = 2.0 * grid[..., 1] / (ysize - 1) - 1.0

    # 扩展图像维度以匹配批量大小，并应用 grid_sample 进行变换
    image_batch = image.unsqueeze(0).unsqueeze(0).expand(num_fields, -1, -1, -1)
    print(image_batch.shape)
    print(grid.shape)
    transformed_images = F.grid_sample(
        image_batch.permute(0, 1, 3, 2),
        grid.permute(0, 2, 1, 3),
        mode="bilinear",
        align_corners=True,
        padding_mode="border",
    ).permute(0, 1, 3, 2)

    return transformed_images.squeeze(1)  # 返回 (num_fields, H, W)


class Optimizer:
    # FOM是关于E(x)和x的函数
    def __init__(self, fdtd, structure, opt_Monitor):
        self.debug = fdtd.debug
        self.fdtd = fdtd
        self.structure = structure
        self.Eexc = fdtd.AddMonitor(structure.area, name="Eexc", type="interp")
        self.opt_Monitor = opt_Monitor
        self.LOSSes = []
        self.kernel = (
            create_distance_weighted_kernel(5).to(fdtd.device).to(torch.cfloat)
        )

    def f0df0fdf(self, x):
        torch.cuda.empty_cache()
        Convert_variables = self.Convert_variables
        structure = self.structure
        fdtd = self.fdtd
        FOM = self.FOM
        Constraint = self.Constraint
        eps_delta = self.eps_delta
        w = self.w

        projected_mat0 = Convert_variables(x, True)
        structure.Adjust(projected_mat0)  # 调整结构
        fdtd.Update()
        EF = self.Eexc.E.clone()
        self.opt_Monitor.AdjustAdjointSource(FOM, x)

        # 下面才需要x的梯度
        x.requires_grad = True
        FOM0, _ = FOM(self.opt_Monitor.E.detach(), x)

        fdtd.Update(True)
        dot = torch.sum(
            EF * self.Eexc.E * self.Eexc.dV(), dim=(0, 5)
        )  # 对多个光源和分量求和,得到(结构,x,y,z,lam)

        dot = torch.sum(
            dot
            * (
                eps_delta
                + 1j
                * self.structure.sigma
                / w
                * (-2 * projected_mat0[:, :, :, :, None] + 1)
            ),
            dim=-1,
        )  # (并行,x,y,z)

        dot = Sensitivity_filtering(dot, self.kernel, fdtd.periodic_num)  # 灵敏度滤波

        projected_mat = Convert_variables(x, False)
        dFOM_AVM_interp = torch.sum((projected_mat - projected_mat0) * dot)
        dFOM_AVM = torch.real(dFOM_AVM_interp)

        LOSS = dFOM_AVM + FOM0  # 前面是含E的偏导
        try:
            LOSS.backward()  # retain_graph=True
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"x.requires_grad: {x.requires_grad}")

        f0dx = x.grad.clone()
        x.grad.zero_()

        constraint1 = Constraint(x)
        try:
            constraint1.backward()  # retain_graph=True
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"x.requires_grad: {x.requires_grad}")
        f1dx = x.grad.clone()
        x.grad.zero_()

        x.requires_grad = False
        self.LOSSes.append(LOSS.detach())
        return (
            LOSS.detach(),
            f0dx.detach(),
            constraint1.detach().view(-1),
            f1dx.detach().view(1, -1),
        )

    def Run(
        self,
        init_variables,
        variables_min,
        variables_max,
        Convert_variables=Convert_variables,
        FOM=FOM,
        Constraint=Constraint,
        move=0.25,
        num_epochs=25,
    ):
        device = self.fdtd.device
        self.Convert_variables = Convert_variables
        self.FOM = FOM
        self.Constraint = Constraint

        init_variables = init_variables.to(device)

        projected_mat = Convert_variables(init_variables, False)
        projected_mat_origin = projected_mat.detach().clone().cpu()
        self.structure.Adjust(projected_mat.detach())  # 调整结构
        self.Eexc.override_grid(self.structure)  # 对齐监视器网格

        self.fdtd.Update()
        self.opt_Monitor.AdjustAdjointSource(FOM, init_variables.detach())
        self.eps_delta = (self.structure.er_pri - self.structure.er_sec).view(
            1, 1, 1, 1, -1
        )  # 能够简化为2维的时代一去不复返啦
        self.w = 2 * torch.pi * self.fdtd.f.reshape(1, 1, 1, 1, -1)

        f, x = mma.Single_Optimizer(
            self.f0df0fdf,
            init_variables.clone(),
            variables_min,
            variables_max,
            maxoutit=num_epochs,
            move=move,
        )
        return x
