import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import datetime

def read_file(filename):
    data = {}
    title = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        indeks = 0
        for line in reader:
            title_number = 0
            if indeks == 0:
                for i in range(len(line)):
                    data[line[i]] = []
                    title.append(line[i])
                indeks += 1
        
            else:
                for i in range(len(line)):
                    data[title[i]].append(line[i])

    return data

data1 = read_file("ROV_NAV/Data/pos1.csv")
data2 = read_file("ROV_NAV/Data/pos2.csv")
data3 = read_file("ROV_NAV/Data/pos3.csv")
data4 = read_file("ROV_NAV/Data/pos4.csv")
data5 = read_file("ROV_NAV/Data/pos5.csv")
data6 = read_file("ROV_NAV/Data/pos6.csv")


def samle_lister(dict1, dict2, dict3,dict4, dict5, dict6):
    resultat = {}
    for key in dict1:
        resultat[key] = dict1[key] + dict2[key] + dict3[key]+dict4[key] + dict5[key] + dict6[key]
    return resultat

data = samle_lister(data1,data2,data3,data4,data5,data6)


def parse_time(tid_str):
    t = datetime.datetime.strptime(tid_str, "%H:%M:%S.%f")
    return t.hour * 3600 + t.minute * 60 + t.second + t.microsecond/1e6

def plot_pos_time(data):
    # Ekstraher data
    x = np.array([float(val) for val in data["ROV East"]])
    y = np.array([float(val) for val in data["ROV North"]])
    z = np.array([float(val) for val in data["ROV Height"]])
    time = np.array([parse_time(tid) for tid in data["Time"]])  # FIKSET HER

    # Lag linjesegmenter
    points = np.array([x, y, z]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Normaliser tid for farger
    t_numeric = (time - time.min()) / (time.max() - time.min())  # 0-1 skala
    t_mean = (t_numeric[:-1] + t_numeric[1:]) / 2

    # Sett opp fargekart
    cmap = plt.get_cmap('viridis')
    norm = mcolors.Normalize(vmin=0, vmax=1)
    colors = cmap(norm(t_mean))

    # Lag Line3DCollection
    lc = Line3DCollection(segments, colors=colors, linewidth=2)

    # Sett opp plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.add_collection3d(lc)

    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())
    ax.set_zlim(z.min(), z.max())

    ax.set_xlabel('East [m]')
    ax.set_ylabel('North [m]')
    ax.set_zlabel('Height [m]')
    ax.set_title('ROV 3D Posisjon med tidsfarge')

    mappable = cmx.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array(time)
    cbar = fig.colorbar(mappable, ax=ax, shrink=0.5, aspect=10)
    cbar.set_label('Normalisert tid')

    plt.show()

plot_pos_time(data)

def animate_rov(data):
 
    x = np.array([float(val) for val in data["ROV East"]])
    y = np.array([float(val) for val in data["ROV North"]])
    z = np.array([float(val) for val in data["ROV Height"]])
    heading_deg = np.array([float(val) for val in data["ROV Gyro"]])
    time = np.array([parse_time(tid) for tid in data["Time"]])

    t_numeric = (time - time.min()) / (time.max() - time.min())

    points = np.array([x, y, z]).T.reshape(-1, 1, 3)
    segments_all = np.concatenate([points[:-1], points[1:]], axis=1)

    cmap = plt.get_cmap('viridis')
    norm = mcolors.Normalize(vmin=0, vmax=1)
    colors_all = cmap(norm((t_numeric[:-1] + t_numeric[1:]) / 2))

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())
    ax.set_zlim(z.min(), z.max())

    ax.set_xlabel('East [m]')
    ax.set_ylabel('North [m]')
    ax.set_zlabel('Height [m]')
    ax.set_title('ROV 3D Posisjon Animasjon med Heading og Farge')

    lc = Line3DCollection([], linewidth=2)
    ax.add_collection3d(lc)

    # PILEN starter som None
    arrow = None

    mappable = cmx.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array(t_numeric)
    cbar = fig.colorbar(mappable, ax=ax, shrink=0.5, aspect=10)
    cbar.set_label('Normalisert tid')

    step = 10

    def init():
        lc.set_segments([])
        return lc,

    def update(frame):
        nonlocal arrow
        idx = frame * step
        if idx >= len(x)-1:
            idx = len(x)-2

        # Oppdater linjen
        current_segments = segments_all[:idx]
        current_colors = colors_all[:idx]
        lc.set_segments(current_segments)
        lc.set_color(current_colors)

        # Fjern gammel pil hvis den eksisterer
        if arrow is not None:
            arrow.remove()

        # Lag ny pil
        x0, y0, z0 = x[idx], y[idx], z[idx]
        head = np.deg2rad(90 - heading_deg[idx])  # 0 grader = Nord
        u = np.cos(head)
        v = np.sin(head)
        w = 0
        arrow = ax.quiver(x0, y0, z0, u, v, w, color='red', length=5)

        return lc, arrow

    ani = animation.FuncAnimation(
        fig, update, frames=int(len(x)/step), init_func=init,
        interval=20, blit=False
    )

    plt.show()

    return ani

animate_rov(data)
