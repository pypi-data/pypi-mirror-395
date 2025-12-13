from vec_utils_py import *
from random import random
import matplotlib.pyplot as plt

def plot_list(vecs, ax, name):
    x = [i.x for i in vecs]
    y = [i.y for i in vecs]
    ax.plot(x, y, label=name, marker="o")

py_list = []
for _ in range(5):
    py_list.append(Vec3d(random(), 0, random()))

rs_list = VecList(py_list)
rotation = Quat.from_axis_angle(Vec3d.k(), AngleRadians.quarter_pi())
rs_list.rotate(rotation)
sub_list = rs_list - Vec3d.j()
collapse_list = rs_list.collapse(0)
all_list = VecList.empty()
all_list.extend(collapse_list)
all_list.extend(sub_list)

fig = plt.figure()
ax = fig.add_subplot()
plot_list(py_list, ax, "py")
plot_list(rs_list, ax, "rs")
plot_list(sub_list, ax, "sub")
plot_list(collapse_list, ax, "collapse")
plot_list(all_list, ax, "all")
# centroid = all_list.get_centroid(2)
# ax.plot(centroid[0], centroid[1], marker="o")
ax.grid()
ax.set_aspect("equal")
ax.legend()
plt.savefig("testfig.png")

