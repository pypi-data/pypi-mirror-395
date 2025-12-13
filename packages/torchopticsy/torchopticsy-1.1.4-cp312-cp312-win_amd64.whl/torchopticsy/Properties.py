# %%
import torch
from torch import tensor
import json
import os
import matplotlib.pyplot as plt
import opticsyCUDA.Utils as Utils

c = 299792458


class Geometry:
    def __init__(self, x_min=0, x_max=0, y_min=0, y_max=0, z_min=0, z_max=0):
        self._x_min = x_min
        self._x_max = x_max
        self._x_span = x_max - x_min
        self._x = 0.5 * (x_max + x_min)

        self._y_min = y_min
        self._y_max = y_max
        self._y_span = y_max - y_min
        self._y = 0.5 * (y_max + y_min)

        self._z_min = z_min
        self._z_max = z_max
        self._z_span = z_max - z_min
        self._z = 0.5 * (z_max + z_min)

    def item(self):
        self.x_min = self.x_min.item()
        self.x_max = self.x_max.item()
        self.y_min = self.y_min.item()
        self.y_max = self.y_max.item()
        self.z_min = self.z_min.item()
        self.z_max = self.z_max.item()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._x_min = value - 0.5 * self._x_span
        self._x_max = value + 0.5 * self._x_span

    @property
    def x_span(self):
        return self._x_span

    @x_span.setter
    def x_span(self, value):
        self._x_span = value
        self._x_min = self._x - 0.5 * value
        self._x_max = self._x + 0.5 * value

    @property
    def x_min(self):
        return self._x_min

    @x_min.setter
    def x_min(self, value):
        self._x_min = value
        self._x_span = self._x_max - self._x_min
        self._x = 0.5 * (self._x_min + self._x_max)

    @property
    def x_max(self):
        return self._x_max

    @x_max.setter
    def x_max(self, value):
        self._x_max = value
        self._x_span = self._x_max - self._x_min
        self._x = 0.5 * (self._x_min + self._x_max)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._y_min = value - 0.5 * self._y_span
        self._y_max = value + 0.5 * self._y_span

    @property
    def y_span(self):
        return self._y_span

    @y_span.setter
    def y_span(self, value):
        self._y_span = value
        self._y_min = self._y - 0.5 * value
        self._y_max = self._y + 0.5 * value

    @property
    def y_min(self):
        return self._y_min

    @y_min.setter
    def y_min(self, value):
        self._y_min = value
        self._y_span = self._y_max - self._y_min
        self._y = 0.5 * (self._y_min + self._y_max)

    @property
    def y_max(self):
        return self._y_max

    @y_max.setter
    def y_max(self, value):
        self._y_max = value
        self._y_span = self._y_max - self._y_min
        self._y = 0.5 * (self._y_min + self._y_max)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value
        self._z_min = value - 0.5 * self._z_span
        self._z_max = value + 0.5 * self._z_span

    @property
    def z_span(self):
        return self._z_span

    @z_span.setter
    def z_span(self, value):
        self._z_span = value
        self._z_min = self._z - 0.5 * value
        self._z_max = self._z + 0.5 * value

    @property
    def z_min(self):
        return self._z_min

    @z_min.setter
    def z_min(self, value):
        self._z_min = value
        self._z_span = self._z_max - self._z_min
        self._z = 0.5 * (self._z_min + self._z_max)

    @property
    def z_max(self):
        return self._z_max

    @z_max.setter
    def z_max(self, value):
        self._z_max = value
        self._z_span = self._z_max - self._z_min
        self._z = 0.5 * (self._z_min + self._z_max)

    def get_posm(self, delta):
        n = int(torch.ceil(torch.tensor(self.x_span / delta)))
        if n > 1:
            d = self.x_span / n
            xm = torch.linspace(self.x_min + 0.5 * d, self.x_max - 0.5 * d, n)
        else:
            xm = tensor([self.x])
        n = int(torch.ceil(torch.tensor(self.y_span / delta)))
        if n > 1:
            d = self.y_span / n
            ym = torch.linspace(self.y_min + 0.5 * d, self.y_max - 0.5 * d, n)
        else:
            ym = tensor([self.y])
        n = int(torch.ceil(torch.tensor(self.z_span / delta)))
        if n > 1:
            d = self.z_span / n
            zm = torch.linspace(self.z_min + 0.5 * d, self.z_max - 0.5 * d, n)
        else:
            zm = tensor([self.z])
        return xm, ym, zm


class Material:
    @staticmethod
    def get_user_data_path():
        # 获取用户的数据目录
        user_data_dir = os.path.expanduser("~/.myapp/")  # 你可以更改此路径
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)  # 如果目录不存在，创建
        return os.path.join(user_data_dir, "materials.json")

    @staticmethod
    def Add_Fit_Plot(name, wavelengths, refractive_indices, poles=1, iteration=1):
        # Load JSON data from the user's materials.json file
        materials_file_path = Material.get_user_data_path()

        if os.path.exists(materials_file_path):
            with open(materials_file_path, "r") as file:
                data = json.load(file)
        else:
            print("materials.json not found, creating a new one.")
            data = {"materials": []}

        mat_index = next(
            (
                index
                for index, material in enumerate(data["materials"])
                if material["name"] == name
            ),
            None,
        )

        lams = torch.tensor(wavelengths)
        w = 2 * torch.pi * c / lams  # c is the speed of light
        er = torch.tensor(refractive_indices, dtype=torch.complex64) ** 2

        cp, er_inf, ap = Utils.Rational_fitting(w, er, poles, iteration)
        er_fit = er_inf + torch.sum(
            cp / (-1j * w.view(-1, 1) - ap)
            + torch.conj(cp) / (-1j * w.view(-1, 1) - torch.conj(ap)),
            dim=1,
        )
        # Plot real and imaginary refractive indices
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(
            lams,
            torch.real(torch.tensor(refractive_indices)),
            "o",
            label="Real Refractive Index",
        )
        plt.plot(lams, torch.real(torch.sqrt(er_fit)), "-", label="Real Fitted")
        plt.legend()
        plt.show()

        plt.figure()
        plt.subplot(2, 1, 2)
        plt.plot(
            lams,
            torch.imag(torch.tensor(refractive_indices)),
            "o",
            label="Imag Refractive Index",
        )
        plt.plot(lams, torch.imag(torch.sqrt(er_fit)), "-", label="Imag Fitted")
        plt.legend()
        plt.show()

        # Update or add the material data
        if mat_index is not None:
            data["materials"][mat_index]["er_inf"] = er_inf.item()
            data["materials"][mat_index]["cp_real"] = torch.real(cp).tolist()
            data["materials"][mat_index]["cp_imag"] = torch.imag(cp).tolist()
            data["materials"][mat_index]["ap_real"] = torch.real(ap).tolist()
            data["materials"][mat_index]["ap_imag"] = torch.imag(ap).tolist()
        else:
            new_material = {
                "name": name,
                "er_inf": er_inf.item(),
                "cp_real": torch.real(cp).tolist(),
                "cp_imag": torch.imag(cp).tolist(),
                "ap_real": torch.real(ap).tolist(),
                "ap_imag": torch.imag(ap).tolist(),
            }
            data["materials"].append(new_material)

        # Save updated data to the user's materials.json file
        with open(materials_file_path, "w") as file:
            json.dump(data, file, indent=4)

    def __init__(self, name, lams):
        # Load material data from the user's materials.json file
        materials_file_path = Material.get_user_data_path()

        if os.path.exists(materials_file_path):
            with open(materials_file_path, "r") as file:
                data = json.load(file)
        else:
            print("Error: materials.json not found. Please add materials first.")
            self.er_inf = 1.0
            self.cp = 0.0 + 0.0j
            self.ap = 0.0 + 0.0j
            return

        mat_index = next(
            (
                index
                for index, material in enumerate(data["materials"])
                if material["name"] == name
            ),
            None,
        )

        if mat_index is None:
            print("Material not found. Using default values.")
            self.er_inf = 1.0
            self.cp = 0.0 + 0.0j
            self.ap = 0.0 + 0.0j
        else:
            self.er_inf = data["materials"][mat_index]["er_inf"]
            self.cp = torch.tensor(
                data["materials"][mat_index]["cp_real"]
            ) + 1j * torch.tensor(data["materials"][mat_index]["cp_imag"])
            self.ap = torch.tensor(
                data["materials"][mat_index]["ap_real"]
            ) + 1j * torch.tensor(data["materials"][mat_index]["ap_imag"])

        self.er_inf = torch.tensor(self.er_inf, device=lams.device)
        self.cp = torch.tensor(self.cp, device=lams.device)
        self.ap = torch.tensor(self.ap, device=lams.device)

        w = 2 * torch.pi * c / lams.view(-1, 1)
        self.er = self.er_inf + torch.sum(
            self.cp / (-1j * w - self.ap)
            + torch.conj(self.cp) / (-1j * w - torch.conj(self.ap)),
            dim=1,
        )
        self.er = self.er.to(torch.complex64)
        self.index = torch.sqrt(self.er)

    def Initialization(self, fdtd):
        # Calculate kp and bp
        kp = (1 + self.ap * fdtd.dt / 2) / (1 - self.ap * fdtd.dt / 2)
        bp = self.cp * fdtd.dt / (1 - self.ap * fdtd.dt / 2)

        # Append the parameters to the lists in the FDTD object
        # 这种写法只支持一种偶极子
        fdtd.er_inf_list.append(self.er_inf)
        fdtd.kp_list.append(kp.item())
        fdtd.bp_list.append(bp.item())


if __name__ == "__main__":
    # Example for adding material
    lams = torch.tensor([480.6, 600, 800]) * 1e-9
    index = torch.tensor([1.53 + 0j, 1.53 + 0j, 1.53 + 0j], dtype=torch.complex64)
    mat = "1_53Test"
    Material.Add_Fit_Plot(mat, lams.tolist(), index.tolist(), 1, 2)
