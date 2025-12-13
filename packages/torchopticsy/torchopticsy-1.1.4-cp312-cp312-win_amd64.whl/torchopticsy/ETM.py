import torch
from torchopticsy.Properties import Material

# % 常用变量和直接函数
dtype = torch.complex64
if dtype == torch.complex128:
    dtype_real = torch.double
    eps = 1e-15
else:
    dtype_real = torch.float32
    eps = 1e-7
pi = torch.pi
sin = torch.sin
cos = torch.cos
tensor = torch.tensor  # tensor创建时,是把一个一个列向量并起来!
numel = torch.numel
arange = torch.arange
ndgrid = torch.meshgrid
ones = torch.ones
zeros = torch.zeros
sum = torch.sum
nonzero = torch.nonzero
sort = torch.sort
cat = torch.cat
diag = torch.diag
eye = torch.eye
cross = torch.cross
norm = torch.norm
stack = torch.stack
pinv = torch.pinverse
real = torch.real
fftshift = torch.fft.fftshift
lsolve = torch.linalg.solve
flip = torch.flip


def fft2(A):
    # 计算2D FFT并进行fftshift
    B = torch.fft.fftshift(torch.fft.fft2(A), dim=(-2, -1)) / (A.size(-2) * A.size(-1))

    # 计算中心索引
    n_center = (A.size(-2) // 2, A.size(-1) // 2)  # python索引从零开始,不用加1

    return B, n_center


def sqrt_real(x):
    # 定义这个函数是为了保证对实数开更号时,保证获得正数或者虚部为正的纯虚数,否则在ETM中是错误的
    condition = x.real < 0
    y = torch.where(condition, torch.sqrt(-x) * 1j, torch.sqrt(x))
    return y


# ETM（增强透射矩阵法）具有更强的稳定性，但会消耗更多的内存。对于单层来说这不是问题
# 视频中说的不大对，实际上它的时间和RCWA差不多=
# 在进行矩阵除法时要小心，左除和右除是不同的

# W作为特征向量矩阵，其列向量表示特定的电磁场模式通过层传播后只会有相位和振幅变化，
# 而各分量比例保持不变，在TMM中是单位矩阵
# 可以直接使用torch.matrix_exp来表示对矩阵进行特征分解后对特征值矩阵进行该操作，
# 而在Matlab中，exp是对矩阵中每一个元素进行操作。特征值描述了相位/振幅在z轴传播时的变化


# 网格的选择会影响采样密度，从而影响效率。为了提高效率，需要增加采样数，保持周期不变
# 可以通过使用长方形网格和周期性来模拟六角网格结构
# 为了应用自动微分,必须使用torch,截止matlab r2023b还不支持特征分解的自动微分,需要额外的工作量
# GPU比CPU快150倍卧槽
# 只支持周期结构


# 我早就想支持材料id优化了，这次正好乘着紫外波带片的契机做一下。
# 引入（优化层数，材料数目）
def sigmoid(y, beta, eta=0.5):
    beta = torch.tensor(beta).to(y.device)
    z = (torch.tanh(beta * eta) + torch.tanh(beta * (y - eta))) / (
        torch.tanh(beta * eta) + torch.tanh(beta * (1 - eta))
    )
    return z


class ETM:
    def __init__(
        self,
        period,
        lams,
        material_list,  # 材料列表
        is_opt_material,
        background_material_id,  # 背景材料序号
        stack_material_id,  # 填充的背景材料id,默认全是
        surf_material_id,  # (每层材料的初始id)
        height,
        is_opt_surf,
        surf,  # 默认全0
        theta_deg,
        phi_deg,
        polar_deg,
        phase_deg,
        F_u=9,
        F_v=9,
        m_order=0,
        n_order=0,
        device="cpu",
    ):
        # 正入射时，pte是y分量，ptm是x分量
        self.device = device
        lams = tensor(lams, device=device).view(-1)
        height = tensor(height, device=device)
        is_opt_surf = tensor(is_opt_surf, dtype=torch.bool, device=device)
        surf = tensor(surf, dtype=torch.float32, device=device)
        theta_deg = tensor(theta_deg, device=device)
        phi_deg = tensor(phi_deg, device=device)
        polar_deg = tensor(polar_deg, device=device)
        phase_deg = tensor(phase_deg, device=device)

        self.lams = lams
        self.k0 = 2 * torch.pi / lams
        self.Tx = period[0]
        self.Ty = period[1]
        self.F_u = F_u
        self.F_v = F_v
        self.stack_material_id = tensor(
            stack_material_id, device=device, dtype=torch.long
        )
        self.is_opt_Material = tensor(is_opt_material, dtype=torch.bool, device=device)
        self.opt_id_list = torch.nonzero(self.is_opt_Material, as_tuple=False).view(-1)
        self.num_opt_mat = self.opt_id_list.numel()

        self.surf = tensor(surf, device=device, dtype=dtype_real)
        self.is_opt_surf = is_opt_surf
        self.height = tensor(height, device=device)

        self.Material_list = []

        for m in material_list:
            self.Material_list.append(
                Material(m, self.lams)  # 改回来!![0] * torch.ones_like(self.lams)
            )

        self.surf_logits = self.convert_surf(tensor(surf_material_id, device=device))
        self.n_re = self.Material_list[background_material_id[0]].index
        self.n_tr = self.Material_list[background_material_id[1]].index
        self.er_stack = torch.ones(
            [self.stack_material_id.numel(), self.lams.numel()],
            dtype=dtype,
            device=device,
        )
        for z in range(self.er_stack.size(0)):
            self.er_stack[z] = (
                self.Material_list[int(self.stack_material_id[z])].index ** 2
            )

        self.mat_shape = [surf.size(1), surf.size(2)]  # surf是(z,x,y)
        M = 2 * F_u + 1
        N = 2 * F_v + 1
        self.m_size = M * N
        self.m_arr, self.n_arr = torch.meshgrid(
            torch.arange(-F_u, F_u + 1, device=device),
            torch.arange(-F_v, F_v + 1, device=device),
            indexing="ij",
        )
        # 笑死我了,没有这行代码后面的判据据出大问题了
        self.m_arr = self.m_arr.reshape(-1)
        self.n_arr = self.n_arr.reshape(-1)
        # 入射光分析
        polar = torch.deg2rad(polar_deg).view(-1).to(device)
        theta = torch.deg2rad(theta_deg).view(-1).to(device)
        phi = torch.deg2rad(phi_deg).view(-1).to(device)
        phase = torch.deg2rad(phase_deg).view(-1).to(device)

        # 计算入射相对波矢量矩阵,(光源,波长,谐波数)
        n_re = self.n_re.view(1, -1, 1)
        A0x = (sin(theta) * cos(phi)).view(-1, 1, 1)
        A0y = (sin(theta) * sin(phi)).view(-1, 1, 1)
        A0z = (cos(theta)).view(-1, 1, 1)
        lam0 = lams.view(1, -1, 1)

        self.Ax = (n_re * A0x - lam0 * self.m_arr.reshape(1, 1, -1) / self.Tx).to(dtype)
        self.Ay = (n_re * A0y - lam0 * self.n_arr.reshape(1, 1, -1) / self.Ty).to(dtype)

        diag1 = torch.eye(self.m_size, device=device).unsqueeze(0).unsqueeze(0)
        self.Ax = self.Ax.unsqueeze(-1) * diag1
        self.Ay = self.Ay.unsqueeze(-1) * diag1

        # 计算偏振分量
        ptm = cos(polar).view(-1, 1)
        pte = (sin(polar) * torch.exp(1j * phase)).view(-1, 1)
        en = tensor([0, 0, -1.0], device=device).view(1, -1)

        n_re = self.n_re.view(1, -1, 1, 1)
        n_tr = self.n_tr.view(1, -1, 1, 1)
        self.Az_re = sqrt_real(n_re**2 * diag1 - self.Ax**2 - self.Ay**2)
        self.Az_tr = sqrt_real(n_tr**2 * diag1 - self.Ax**2 - self.Ay**2)

        A0 = torch.cat(
            [A0x.view(-1, 1), A0y.view(-1, 1), A0z.view(-1, 1)], dim=-1
        )  # (光源,3)
        ate = torch.cross(A0, en, dim=-1)
        # 计算每行的模长
        norms = torch.norm(ate, dim=-1)
        zero_norm_indices = norms == 0
        replacement = torch.tensor([0, 1.0, 0], device=device, dtype=ate.dtype)
        ate[zero_norm_indices] = replacement
        norms = torch.norm(ate, dim=-1).view(-1, 1)
        ate = ate / norms

        atm = cross(ate, A0, dim=-1)
        norms = torch.norm(atm, dim=-1).view(-1, 1)
        atm = atm / norms

        # 根据TE，TM偏振比例求xy分量
        P = pte * ate + ptm * atm
        P = P / torch.norm(P, dim=-1).view(-1, 1)

        # 计算s_in列向量,(光源,波长,列,行)
        delta_pq = zeros([self.m_size, 1], device=device, dtype=dtype_real)
        condition = (self.m_arr == 0) & (self.n_arr == 0)
        index = nonzero(condition, as_tuple=False)
        delta_pq[index[0, 0]] = 1
        delta_pq = delta_pq.view(1, 1, -1, 1)

        s1 = P[:, 0].view(-1, 1, 1, 1) * delta_pq * torch.ones_like(n_re)
        s2 = P[:, 1].view(-1, 1, 1, 1) * delta_pq * torch.ones_like(n_re)
        s3 = (
            1j
            * n_re
            * (A0[:, 2] * P[:, 1] - A0[:, 1] * P[:, 2]).view(-1, 1, 1, 1)
            * delta_pq
        )
        s4 = (
            1j
            * n_re
            * (A0[:, 0] * P[:, 2] - A0[:, 2] * P[:, 0]).view(-1, 1, 1, 1)
            * delta_pq
        )
        self.s_in = torch.cat((s1, s2, s3, s4), dim=-2)

        self.Az_tr_inv = pinv(self.Az_tr, eps)
        self.Az_re_inv = pinv(self.Az_re, eps)

        # 计算复用参数
        self.allowed_n = torch.stack(
            [self.Material_list[int(i)].index for i in self.opt_id_list], dim=0
        )  # shape: (K, num_lams)

        _, center_id = fft2(torch.zeros(self.mat_shape, dtype=dtype))
        self.M_arr = (
            self.m_arr.reshape(-1, 1) - self.m_arr.reshape(1, -1) + center_id[0]
        )
        self.N_arr = (
            self.n_arr.reshape(-1, 1) - self.n_arr.reshape(1, -1) + center_id[1]
        )

        ur_mat = torch.ones(
            [1, surf.size(1), surf.size(2)], device=device, dtype=dtype
        )  # (波长,x,y)
        self.ur_conv, ur_conv_z_inv, _ = self.Conv_mat(ur_mat)  # self.PML
        self.ur_conv_inv = ur_conv_z_inv

        self.Q11 = self.Ax @ ur_conv_z_inv @ self.Ay
        self.Q12 = -self.Ax @ ur_conv_z_inv @ self.Ax
        self.Q21 = self.Ay @ ur_conv_z_inv @ self.Ay
        self.Q22 = -self.Ay @ ur_conv_z_inv @ self.Ax

        Axy = self.Ax @ self.Ay
        A_xx = -self.Ax @ self.Ax
        Ayy = self.Ay @ self.Ay
        # (光源,波长,x,y)
        part1 = -1j * Axy @ self.Az_re_inv
        part2 = -1j * (Ayy @ self.Az_re_inv + self.Az_re)
        part3 = 1j * (-A_xx @ self.Az_re_inv + self.Az_re)
        part4 = 1j * Axy @ self.Az_re_inv

        # 拼接两个部分，形成矩阵 self.A
        self.A = cat((cat((part1, part2), dim=-1), cat((part3, part4), dim=-1)), dim=-2)

        # 创建矩阵 self.A 的扩展版本
        e = torch.eye(self.A.size(-1)).unsqueeze(0).unsqueeze(0).to(device)
        e = e * torch.ones_like(self.A)
        self.A = cat((e, self.A), dim=-2)

        part1 = 1j * Axy @ self.Az_tr_inv
        part2 = 1j * (Ayy @ self.Az_tr_inv + self.Az_tr)
        part3 = -1j * (-A_xx @ self.Az_tr_inv + self.Az_tr)
        part4 = -1j * Axy @ self.Az_tr_inv
        # 拼接四个部分，形成矩阵 self.B
        self.B = cat((cat((part1, part2), dim=-1), cat((part3, part4), dim=-1)), dim=-2)
        # 创建矩阵 self.B 的扩展版本
        self.B = cat((e, self.B), dim=-2)

        # (光源,波长,谐波数)
        self.r_co = zeros(
            [polar.numel(), lam0.numel(), self.m_size],
            device=device,
            dtype=dtype,
        )
        self.t_co = torch.zeros_like(self.r_co)

        # 计算能量透过率和振幅透过率的参数
        for i in range(self.m_size):
            self.r_co[..., i] = sqrt_real(
                torch.clamp(
                    real(self.Az_re[..., i, i] / (n_re.view(1, -1) * A0[:, 2:3])),
                    min=0.0,
                )
            )
            self.t_co[..., i] = sqrt_real(
                torch.clamp(
                    real(self.Az_tr[..., i, i] / (n_re.view(1, -1) * A0[:, 2:3])),
                    min=0.0,
                )
            )

        m_order = -tensor([m_order]).reshape(-1)
        n_order = -tensor([n_order]).reshape(-1)
        order_id = torch.zeros_like(m_order)
        # 循环为 order_id 中的每个元素找到对应的索引
        for i in range(order_id.numel()):
            condition = (self.m_arr == m_order[i]) & (self.n_arr == n_order[i])
            index = nonzero(condition, as_tuple=False)
            if index.numel() > 0:
                order_id[i] = index[0, 0]  # 选择第一个满足条件的索引
        self.order_id = order_id

    def convert_surf(self, x):
        """
        自动检测输入格式:
        1D: surf_material_id (相对于 Material_list) → 返回 surf_logits (L,K)
        2D: surf_logits (L,K) → 返回 surf_material_id (相对于 Material_list)

        其中 K = number of True in is_opt_Material
        """
        x = torch.tensor(x, device=self.device)

        opt_ids = self.opt_id_list  # 真实 Material_list 索引列表 (K,)
        K = self.num_opt_mat

        # ------------ case 1: 输入 1D，材料 ID → logits ------------ #
        if x.dim() == 1:
            L = x.numel()
            logits = torch.zeros((L, K), device=self.device)

            # 将 Material_list 编号的材料映射到优化材料维度
            # 对于每层：找到 x[i] 在 opt_ids 中的位置
            for i in range(L):
                idx = (opt_ids == int(x[i])).nonzero(as_tuple=False)
                if idx.numel() > 0:
                    logits[i, idx[0, 0]] = 1.0  # one-hot
                else:
                    raise ValueError(f"材料 {int(x[i])} 不是可优化材料")

            return logits

        # ------------ case 2: 输入 2D logits → 材料 ID ------------ #
        elif x.dim() == 2:
            # softmax 最大 index → 对应 opt_ids 中的材料
            max_idx = torch.argmax(x, dim=-1)  # (L,)
            material_id = opt_ids[max_idx]  # 映射回 Material_list 编号
            return material_id

        else:
            raise ValueError("convert_surf 输入必须为 1D 材料 ID 或 2D logits")

    def compute_er_surf(self, beta):
        # (L, K)
        w = torch.softmax(self.surf_logits, dim=-1)
        # 二值逼近
        w_sig = sigmoid(w, beta)
        w_norm = w_sig / (w_sig.sum(dim=-1, keepdim=True) + 1e-9)

        # 使用预计算 allowed_n (K, num_lams)
        allowed_n = self.allowed_n

        # 加权插值
        self.n_surf = (w_norm.unsqueeze(-1) * allowed_n.unsqueeze(0)).sum(dim=1)

        # epsilon
        self.er_surf = self.n_surf**2

    def Conv_mat(self, er_mat):
        # 输入的是(波长,x,y)
        er_fft, _ = fft2(er_mat)
        E = torch.zeros(
            [er_fft.shape[0], self.M_arr.size(0), self.M_arr.size(1)],
            device=self.device,
            dtype=er_fft.dtype,
        )
        for i in range(E.size(0)):
            E[i] = er_fft[i][self.M_arr, self.N_arr]
        try:
            E_1 = pinv(E, eps)
        except Exception as e:
            return False, False, False
        return E.unsqueeze(0), E_1.unsqueeze(0), True

    def FX(self, k0l, er_conv_x, er_conv_y, er_conv_z_inv):
        # 计算 FX
        Q = cat(
            (
                cat((self.Q11, er_conv_y + self.Q12), dim=-1),
                cat((self.Q21 - er_conv_x, self.Q22), dim=-1),
            ),
            dim=-2,
        )
        er_conv_Ax = lsolve(er_conv_x, self.Ax)
        er_conv_Ay = lsolve(er_conv_x, self.Ay)

        P = cat(
            (
                cat(
                    (self.Ax @ er_conv_Ay, self.ur_conv - self.Ax @ er_conv_Ax),
                    dim=-1,
                ),
                cat(
                    (self.Ay @ er_conv_Ay - self.ur_conv, -self.Ay @ er_conv_Ax),
                    dim=-1,
                ),
            ),
            dim=-2,
        )

        D, W = torch.linalg.eig(P @ Q)  # 和matlab相反

        D = torch.sqrt(D)

        condition = D.real > 0
        D = torch.where(condition, -1 * D, D)
        D = torch.eye(D.size(-1), device=self.device).unsqueeze(0).unsqueeze(
            0
        ) * D.unsqueeze(-1)
        V = Q @ W @ pinv(D, eps)
        X = torch.matrix_exp(D * k0l.view(1, -1, 1, 1))  # 注意是torch.matrix_exp

        F = cat((cat((W, W), dim=-1), cat((-V, V), dim=-1)), dim=-2)
        return F, X

    def Update(self, beta=1000):
        surf_index = 0
        # 先从后界面往前界面走
        self.compute_er_surf(beta)
        for z in range(self.stack_material_id.numel()):
            if self.is_opt_surf[-z - 1]:  # 如果是最后一面
                er_mat = (self.er_surf[-surf_index - 1] - self.er_stack[-z - 1]).view(
                    -1, 1, 1
                ) * self.surf[-surf_index - 1].unsqueeze(0) + self.er_stack[
                    -z - 1
                ].view(
                    -1, 1, 1
                )  # 必须
                er_conv_xy, er_conv_z_inv, nor = self.Conv_mat(er_mat)  # 必须
                if not nor:
                    return False
                surf_index = surf_index + 1
            else:
                er_conv_xy = self.ur_conv * self.er_stack[-z - 1].view(1, -1, 1, 1)
                er_conv_z_inv = self.ur_conv_inv / self.er_stack[-z - 1].view(
                    1, -1, 1, 1
                )
            [F, X] = self.FX(
                self.k0 * self.height[-z - 1],
                er_conv_xy,
                er_conv_xy,
                er_conv_z_inv,
            )
            if z == 0:  # 最后一个界面创建数组
                XN = torch.zeros(
                    [self.stack_material_id.numel()] + list(X.size()),
                    device=self.device,
                    dtype=dtype,
                )
                XN[-z - 1] = X.clone()

                temp = torch.linalg.solve(F, self.B)
                num = temp.size(-2) // 2
                aN = torch.zeros(
                    [self.stack_material_id.numel()] + list(temp[..., :num, :].size()),
                    device=self.device,
                    dtype=dtype,
                )
                bN = temp[..., num:, :].clone()
                aN[-1 - z] = temp[..., :num, :].clone()

                I = eye(X.size(-2), device=self.device).unsqueeze(0).unsqueeze(
                    0
                ) * torch.ones(
                    [bN.size(0), bN.size(1), 1, 1], device=self.device, dtype=dtype
                )
                Z = torch.zeros_like(X)

                temp2 = torch.linalg.solve(temp[..., :num, :], X)
            else:
                temp = (
                    torch.linalg.solve(F, FN)
                    @ cat((cat((I, Z), dim=-1), cat((Z, XN[-z]), dim=-1)), dim=-2)
                    @ cat((I, bN @ temp2), dim=-2)
                )
                aN[-z - 1] = temp[..., :num, :].clone()
                bN = temp[..., num:, :].clone()
                temp2 = torch.linalg.solve(temp[..., :num, :], X)
                XN[-z - 1] = X.clone()

            FN = F.clone()

        # 再从前界面往后界面走
        for z in range(self.stack_material_id.numel()):
            a1_X1 = torch.linalg.solve(aN[z], XN[z])
            if z == 0:
                B_p = F @ cat((I, XN[z] @ bN @ a1_X1), dim=-2)
                temp = torch.linalg.solve(cat((-self.A, B_p), dim=-1), self.s_in)

                r = temp[..., :num, :]
                t1 = temp[..., num:, :]
                t = a1_X1 @ t1
            else:
                t = a1_X1 @ t

        num = r.size(-2) // 2
        rx = r[..., :num, :]
        ry = r[..., num:, :]
        rz = -self.Az_re_inv @ (self.Ax @ rx + self.Ay @ ry)
        self.r = cat((rx, ry, rz), dim=-1)
        self.R = torch.real(self.r_co * norm(self.r, dim=-1)) ** 2

        tx = t[..., :num, :]
        ty = t[..., num:, :]
        tz = self.Az_tr_inv @ (self.Ax @ tx + self.Ay @ ty)  # 原本有负号的,现在没有了

        self.t = cat((tx, ty, tz), dim=-1)
        self.T = torch.real(self.t_co * norm(self.t, dim=-1)) ** 2

    def Get_TR(self):
        order_id = self.order_id
        T_out = self.T[..., order_id]
        R_out = self.R[..., order_id]
        return T_out, R_out

    def Get_tr(self, norm=True):
        order_id = self.order_id
        if norm:
            t_out = self.t[..., order_id, :] * self.t_co[..., order_id, None]
            r_out = self.r[..., order_id, :] * self.r_co[..., order_id, None]
        else:
            t_out = self.t[..., order_id, :]
            r_out = self.r[..., order_id, :]
        return t_out, r_out

    def get_discrete_surf_material_id(self):
        return self.convert_surf(self.surf_logits)
