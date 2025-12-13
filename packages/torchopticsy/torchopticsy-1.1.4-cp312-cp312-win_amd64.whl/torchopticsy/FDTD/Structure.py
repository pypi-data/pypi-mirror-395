import torch
import torch.nn.functional as F
from torchopticsy.Properties import Geometry
from torchopticsy.Utils import c
import opticsyCUDA.FDTD as FDTD_CUDA_Dispersion
import opticsyCUDA.FDTD4 as FDTD_MONO_CUDA


# 法向量的计算方法:(均匀网格)
# 第一步:不用子像素平滑,计算全局的ER数组/ER_beta数组.
# 因为直接在import上卷积必然受到import网格粒度的影响,
# 这是为了消除import粒度导致的差异.
# 另外,为了消除先后顺序的差异,应当引入pri_weight数组.
# 进行周期性扩展.
# 验证程序为,先加入和后加入的ER一致,基本ok


# 如果是subcell才进行后续步骤
# 第二步:对ER进行裁剪,去除周期扩展的部分.
# 生成二次衰减的卷积核.根据卷积核的大小,对于结构进行同质扩展.
# 卷积时周围留出格子,确保和差分算子卷积后,得到和ER裁剪后相同的结构.
# 合并N,归一化,如果周期,则扩展至完全体,得到正确的N向量.
# 验证程序为,对于基地和拓扑介质同时存在的x周期性y非周期性,且边界上存在材料的结构得到正确的N分布,ok
# 法向量就算我计算完成了,尽管存在这一些问题,但是本质上无关紧要,最多是针对非均匀网格要变动一下.


# 第三步:如果pri_id=pri_mat_id,则修改该处的有效介电常数.
# 修改的过程和之前差不多,差别就是N是已知的.
# 验证程序为,先加入和后加入的ER一致,ok.且光栅的仿真结果和lumerical  一致.
def create_distance_weighted_kernel(kernel_size):
    center = kernel_size // 2
    kernel = torch.zeros(kernel_size, kernel_size, kernel_size)

    for i in range(kernel_size):
        for j in range(kernel_size):
            for k in range(kernel_size):
                distance = (i - center) ** 2 + (j - center) ** 2 + (k - center) ** 2
                if distance != 0:
                    kernel[i, j, k] = 1 / distance
                else:
                    kernel[i, j, k] = 1

    # 归一化卷积核
    kernel /= kernel.sum()

    return kernel


def compute_normal_vector(input_tensor, kernel, periodic_num):
    # 确保输入张量是四维的 (p, x, y, z)
    if input_tensor.dim() != 4:
        raise ValueError("输入张量必须是四维的 (p, x, y, z)")

    # 将核调整为符合卷积操作的形状 (out_channels, in_channels, d, h, w)
    kernel = kernel.unsqueeze(0).unsqueeze(0)

    # 将输入张量调整为符合卷积操作的形状 (batch_size, channels, d, h, w)
    input_tensor = input_tensor.unsqueeze(1)

    # 确定填充大小
    padding = 1 + kernel.size(2) // 2  # 多出一格用于卷积

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

    # 计算梯度
    k = torch.tensor([-1, 0, 1], device=input_tensor.device).float()
    # grad_x = torch.nn.functional.conv3d(input_tensor.unsqueeze(1), k.view(1,1,-1,1,1), padding=(1, 0, 0)).squeeze(1).unsqueeze(-1)
    # grad_y = torch.nn.functional.conv3d(input_tensor.unsqueeze(1), k.view(1,1,1,-1,1), padding=(0, 1, 0)).squeeze(1).unsqueeze(-1)
    # grad_z = torch.nn.functional.conv3d(input_tensor.unsqueeze(1), k.view(1,1,1,1,-1), padding=(0, 0, 1)).squeeze(1).unsqueeze(-1)
    grad_x = (
        torch.nn.functional.conv3d(input_tensor.unsqueeze(1), k.view(1, 1, -1, 1, 1))
        .squeeze(1)
        .unsqueeze(-1)[:, :, 1:-1, 1:-1]
    )
    grad_y = (
        torch.nn.functional.conv3d(input_tensor.unsqueeze(1), k.view(1, 1, 1, -1, 1))
        .squeeze(1)
        .unsqueeze(-1)[:, 1:-1, :, 1:-1]
    )
    grad_z = (
        torch.nn.functional.conv3d(input_tensor.unsqueeze(1), k.view(1, 1, 1, 1, -1))
        .squeeze(1)
        .unsqueeze(-1)[:, 1:-1, 1:-1, :]
    )
    # 组合梯度
    gradient = torch.cat((grad_x, grad_y, grad_z), dim=-1)

    # 归一化梯度作为法向量
    norm = torch.norm(gradient, dim=-1, keepdim=True)
    norm[norm == 0] = 1  # 避免除以零
    normal_vector = gradient / norm

    return normal_vector, input_tensor


class Structure_Dispersion(Geometry):
    # 插值函数以后可以更加精细
    # 现在只需要输入范围即可,必定是均匀的,_import大小可变是比xs,ys,zs少一个维度的!!!!!!
    # 现在是fdtd求解器中有一个材料字典,根据名称返回序号,分别记录着名称(用于区分),各个系数,所以这里只需要记录名称就行了
    def __init__(self, area, material, _import, priority=2, sigma=0):
        Geometry.__init__(
            self, area[0][0], area[0][1], area[1][0], area[1][1], area[2][0], area[2][1]
        )
        self.material = material
        self.item()
        self.priority = priority
        self.area = area
        self.import_ = _import
        self.shape = _import[0].shape  # 第一个并行维度
        self.sigma = sigma
        self.grayscale = 2

    def Initialization(self, fdtd):
        # 和其它不同的地方在于,每次Update之前都要执行一次,否则会有Bug.
        # 每次执行之前都需要重置ER和mat
        # 如果fdtd.Nx为None,则执行体积平均
        self.import_ = self.import_.to("cuda")
        self.fdtd = fdtd
        self.pri_id = fdtd.material_dic[self.material]

        # 先写伪代码的一个分量:self.import_是(结构并行,x,y,z),获得
        # 直接通过Get_ER,修改pri_mat_id,sec_mat_id和ER
        x_int_id = FDTD_CUDA_Dispersion.get_id_range(self.area[0], fdtd.x2[::2])
        y_int_id = FDTD_CUDA_Dispersion.get_id_range(self.area[1], fdtd.y2[::2])
        z_int_id = FDTD_CUDA_Dispersion.get_id_range(self.area[2], fdtd.z2[1::2])
        x_range = slice(int(x_int_id[0]), int(x_int_id[1]) + 1)
        y_range = slice(int(y_int_id[0]), int(y_int_id[1]) + 1)
        z_range = slice(int(z_int_id[0]), int(z_int_id[1]) + 1)

        sec_mat_id = torch.sum(fdtd.pri_mat_idz[0, x_range, y_range, z_range]) // (
            torch.diff(x_int_id) * torch.diff(y_int_id) * torch.diff(z_int_id)
        ).to(fdtd.device)
        self.er_mean_sec = fdtd.er_mean[sec_mat_id].view(-1)
        self.er_mean_pri = fdtd.er_mean[self.pri_id].view(-1)
        self.er_sec = fdtd.er[sec_mat_id].view(-1)
        self.er_pri = fdtd.er[self.pri_id].view(-1)

        FDTD_CUDA_Dispersion.Set_weight_mat_id(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_,
            fdtd.x2[1::2],
            fdtd.y2[::2],
            fdtd.z2[::2],
            self.pri_id,
            fdtd.pri_weightx,
            fdtd.pri_mat_idx,
            fdtd.sec_mat_idx,
        )

        FDTD_CUDA_Dispersion.Set_weight_mat_id(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_,
            fdtd.x2[::2],
            fdtd.y2[1::2],
            fdtd.z2[::2],
            self.pri_id,
            fdtd.pri_weighty,
            fdtd.pri_mat_idy,
            fdtd.sec_mat_idy,
        )

        FDTD_CUDA_Dispersion.Set_weight_mat_id(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_,
            fdtd.x2[::2],
            fdtd.y2[::2],
            fdtd.z2[1::2],
            self.pri_id,
            fdtd.pri_weightz,
            fdtd.pri_mat_idz,
            fdtd.sec_mat_idz,
        )

        # 电导率
        weight, x_int_id, y_int_id, z_int_id = FDTD_CUDA_Dispersion.Mat_average(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_ * (1 - self.import_),
            fdtd.x2[1::2],
            fdtd.y2[::2],
            fdtd.z2[::2],
        )
        x_range = slice(int(x_int_id[0]), int(x_int_id[1]) + 1)
        y_range = slice(int(y_int_id[0]), int(y_int_id[1]) + 1)
        z_range = slice(int(z_int_id[0]), int(z_int_id[1]) + 1)
        fdtd.sigmadt_2x[:, x_range, y_range, z_range] = (
            self.sigma * weight * fdtd.dt / 2
        )

        weight, x_int_id, y_int_id, z_int_id = FDTD_CUDA_Dispersion.Mat_average(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_ * (1 - self.import_),
            fdtd.x2[::2],
            fdtd.y2[1::2],
            fdtd.z2[::2],
        )
        x_range = slice(int(x_int_id[0]), int(x_int_id[1]) + 1)
        y_range = slice(int(y_int_id[0]), int(y_int_id[1]) + 1)
        z_range = slice(int(z_int_id[0]), int(z_int_id[1]) + 1)
        fdtd.sigmadt_2y[:, x_range, y_range, z_range] = (
            self.sigma * weight * fdtd.dt / 2
        )

        weight, x_int_id, y_int_id, z_int_id = FDTD_CUDA_Dispersion.Mat_average(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_ * (1 - self.import_),
            fdtd.x2[::2],
            fdtd.y2[::2],
            fdtd.z2[1::2],
        )
        x_range = slice(int(x_int_id[0]), int(x_int_id[1]) + 1)
        y_range = slice(int(y_int_id[0]), int(y_int_id[1]) + 1)
        z_range = slice(int(z_int_id[0]), int(z_int_id[1]) + 1)
        fdtd.sigmadt_2z[:, x_range, y_range, z_range] = (
            self.sigma * weight * fdtd.dt / 2
        )

    def Set_subcell(self, fdtd):
        FDTD_CUDA_Dispersion.Set_weight_subcell(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_,
            fdtd.x2[1::2],
            fdtd.y2[::2],
            fdtd.z2[::2],
            fdtd.pri_weightx,
            self.pri_id,
            fdtd.pri_mat_idx,
            fdtd.sec_mat_idx,
            fdtd.Nx,
            torch.real(fdtd.er_mean),
            0,
        )

        FDTD_CUDA_Dispersion.Set_weight_subcell(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_,
            fdtd.x2[::2],
            fdtd.y2[1::2],
            fdtd.z2[::2],
            fdtd.pri_weighty,
            self.pri_id,
            fdtd.pri_mat_idy,
            fdtd.sec_mat_idy,
            fdtd.Ny,
            torch.real(fdtd.er_mean),
            1,
        )

        FDTD_CUDA_Dispersion.Set_weight_subcell(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_,
            fdtd.x2[::2],
            fdtd.y2[::2],
            fdtd.z2[1::2],
            fdtd.pri_weightz,
            self.pri_id,
            fdtd.pri_mat_idz,
            fdtd.sec_mat_idz,
            fdtd.Nz,
            torch.real(fdtd.er_mean),
            2,
        )
        return

    def Adjust(self, mat):
        # mat同样是(结构并行,x,y,z)
        # FDTD_MONO_CUDA.Mat_average唯一的区别就是增加了并行功能
        fdtd = self.fdtd
        self.import_ = mat.detach().to("cuda")
        if self.import_.dim() == 3:  # 说明是灰度图啦
            step = 1.0 / self.gray_scale  # 每个分割的高度范围
            # 计算每个分割的下界和上界
            lower_bounds = torch.linspace(
                0, 1 - step, steps=self.gray_scale, device=self.fdtd.device
            )  # 形状 (z,)
            upper_bounds = lower_bounds + step
            h = self.import_.unsqueeze(-1)
            # 调整下界和上界的形状以进行广播
            lower = lower_bounds.view(1, 1, 1, self.gray_scale)  # 形状 (1, 1, 1, z)
            upper = upper_bounds.view(1, 1, 1, self.gray_scale)  # 形状 (1, 1, 1, z)

            self.import_ = torch.where(
                h >= upper,
                torch.ones_like(h),  # 完全填充
                torch.where(
                    h <= lower,
                    torch.zeros_like(h),  # 不填充
                    (h - lower) / step,  # 线性插值填充比例
                ),
            )
        self.shape = self.import_[0].shape  # 第一个并行维度


class Structure_MONO(Geometry):
    # 插值函数以后可以更加精细
    # 现在只需要输入范围即可,必定是均匀的,_import大小可变是比xs,ys,zs少一个维度的!!!!!!
    # 现在是fdtd求解器中有一个材料字典,根据名称返回序号,分别记录着名称(用于区分),各个系数,所以这里只需要记录名称就行了
    def __init__(self, area, material, _import, priority=2, sigma=0):
        Geometry.__init__(
            self, area[0][0], area[0][1], area[1][0], area[1][1], area[2][0], area[2][1]
        )
        self.material = material
        self.item()
        self.priority = priority
        self.area = area
        self.import_ = _import
        self.shape = _import[0].shape  # 第一个并行维度
        self.sigma = sigma
        self.grayscale = 2

    def Initialization(self, fdtd):
        # 和其它不同的地方在于,每次Update之前都要执行一次,否则会有Bug.
        # 每次执行之前都需要重置ER和mat
        # 如果fdtd.Nx为None,则执行体积平均
        self.import_ = self.import_.to("cuda")
        self.fdtd = fdtd
        self.pri_id = fdtd.material_dic[self.material]

        # 先写伪代码的一个分量:self.import_是(结构并行,x,y,z),获得
        # 直接通过Get_ER,修改pri_mat_id,sec_mat_id和ER
        x_int_id = FDTD_MONO_CUDA.get_id_range(self.area[0], fdtd.x2[::2])
        y_int_id = FDTD_MONO_CUDA.get_id_range(self.area[1], fdtd.y2[::2])
        z_int_id = FDTD_MONO_CUDA.get_id_range(self.area[2], fdtd.z2[1::2])
        x_range = slice(int(x_int_id[0]), int(x_int_id[1]) + 1)
        y_range = slice(int(y_int_id[0]), int(y_int_id[1]) + 1)
        z_range = slice(int(z_int_id[0]), int(z_int_id[1]) + 1)

        sec_mat_id = torch.sum(fdtd.pri_mat_idz[0, x_range, y_range, z_range]) // (
            torch.diff(x_int_id) * torch.diff(y_int_id) * torch.diff(z_int_id)
        ).to(fdtd.device)
        self.er_mean_sec = fdtd.er_mean[sec_mat_id].view(-1)
        self.er_mean_pri = fdtd.er_mean[self.pri_id].view(-1)
        self.er_sec = fdtd.er[sec_mat_id].view(-1)
        self.er_pri = fdtd.er[self.pri_id].view(-1)

        FDTD_MONO_CUDA.Set_weight_mat_id(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_,
            fdtd.x2[1::2],
            fdtd.y2[::2],
            fdtd.z2[::2],
            self.pri_id,
            fdtd.pri_weightx,
            fdtd.pri_mat_idx,
            fdtd.sec_mat_idx,
        )

        FDTD_MONO_CUDA.Set_weight_mat_id(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_,
            fdtd.x2[::2],
            fdtd.y2[1::2],
            fdtd.z2[::2],
            self.pri_id,
            fdtd.pri_weighty,
            fdtd.pri_mat_idy,
            fdtd.sec_mat_idy,
        )

        FDTD_MONO_CUDA.Set_weight_mat_id(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_,
            fdtd.x2[::2],
            fdtd.y2[::2],
            fdtd.z2[1::2],
            self.pri_id,
            fdtd.pri_weightz,
            fdtd.pri_mat_idz,
            fdtd.sec_mat_idz,
        )

        # 电导率
        weight, x_int_id, y_int_id, z_int_id = FDTD_MONO_CUDA.Mat_average(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_ * (1 - self.import_),
            fdtd.x2[1::2],
            fdtd.y2[::2],
            fdtd.z2[::2],
        )
        x_range = slice(int(x_int_id[0]), int(x_int_id[1]) + 1)
        y_range = slice(int(y_int_id[0]), int(y_int_id[1]) + 1)
        z_range = slice(int(z_int_id[0]), int(z_int_id[1]) + 1)
        fdtd.sigmadt_2x[:, x_range, y_range, z_range] += (
            (self.sigma * weight) * fdtd.dt / 2
        )

        weight, x_int_id, y_int_id, z_int_id = FDTD_MONO_CUDA.Mat_average(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_ * (1 - self.import_),
            fdtd.x2[::2],
            fdtd.y2[1::2],
            fdtd.z2[::2],
        )
        x_range = slice(int(x_int_id[0]), int(x_int_id[1]) + 1)
        y_range = slice(int(y_int_id[0]), int(y_int_id[1]) + 1)
        z_range = slice(int(z_int_id[0]), int(z_int_id[1]) + 1)
        fdtd.sigmadt_2y[:, x_range, y_range, z_range] += (
            (self.sigma * weight) * fdtd.dt / 2
        )

        weight, x_int_id, y_int_id, z_int_id = FDTD_MONO_CUDA.Mat_average(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_ * (1 - self.import_),
            fdtd.x2[::2],
            fdtd.y2[::2],
            fdtd.z2[1::2],
        )
        x_range = slice(int(x_int_id[0]), int(x_int_id[1]) + 1)
        y_range = slice(int(y_int_id[0]), int(y_int_id[1]) + 1)
        z_range = slice(int(z_int_id[0]), int(z_int_id[1]) + 1)
        fdtd.sigmadt_2z[:, x_range, y_range, z_range] += (
            (self.sigma * weight) * fdtd.dt / 2
        )

    def Set_subcell(self, fdtd):
        FDTD_MONO_CUDA.Set_ER_subcell(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_,
            fdtd.x2[1::2],
            fdtd.y2[::2],
            fdtd.z2[::2],
            fdtd.ERx,
            self.pri_id,
            fdtd.pri_mat_idx,
            fdtd.sec_mat_idx,
            fdtd.Nx,
            torch.real(fdtd.er),
            0,
        )

        FDTD_MONO_CUDA.Set_ER_subcell(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_,
            fdtd.x2[::2],
            fdtd.y2[1::2],
            fdtd.z2[::2],
            fdtd.ERy,
            self.pri_id,
            fdtd.pri_mat_idy,
            fdtd.sec_mat_idy,
            fdtd.Ny,
            torch.real(fdtd.er),
            1,
        )

        FDTD_MONO_CUDA.Set_ER_subcell(
            self.area[0],
            self.area[1],
            self.area[2],
            self.import_,
            fdtd.x2[::2],
            fdtd.y2[::2],
            fdtd.z2[1::2],
            fdtd.ERz,
            self.pri_id,
            fdtd.pri_mat_idz,
            fdtd.sec_mat_idz,
            fdtd.Nz,
            torch.real(fdtd.er),
            2,
        )
        return

    def Adjust(self, mat):
        # mat同样是(结构并行,x,y,z)
        # FDTD_MONO_CUDA.Mat_average唯一的区别就是增加了并行功能
        fdtd = self.fdtd
        self.import_ = mat.detach().to("cuda")
        if self.import_.dim() == 3:  # 说明是灰度图啦
            step = 1.0 / self.gray_scale  # 每个分割的高度范围
            # 计算每个分割的下界和上界
            lower_bounds = torch.linspace(
                0, 1 - step, steps=self.gray_scale, device=self.fdtd.device
            )  # 形状 (z,)
            upper_bounds = lower_bounds + step
            h = self.import_.unsqueeze(-1)
            # 调整下界和上界的形状以进行广播
            lower = lower_bounds.view(1, 1, 1, self.gray_scale)  # 形状 (1, 1, 1, z)
            upper = upper_bounds.view(1, 1, 1, self.gray_scale)  # 形状 (1, 1, 1, z)

            self.import_ = torch.where(
                h >= upper,
                torch.ones_like(h),  # 完全填充
                torch.where(
                    h <= lower,
                    torch.zeros_like(h),  # 不填充
                    (h - lower) / step,  # 线性插值填充比例
                ),
            )
        self.shape = self.import_[0].shape  # 第一个并行维度
