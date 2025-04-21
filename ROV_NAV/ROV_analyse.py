import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.cm as cmx

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

def samle_lister(dict1, dict2, dict3):
    resultat = {}
    for key in dict1:
        resultat[key] = dict1[key] + dict2[key] + dict3[key]
    return resultat

data = samle_lister(data1,data2,data3)
print(data.keys())

def plot_pos_time(data):
    # Ekstraher data
    x = data["ROV East"].values
    y = data["ROV North"].values
    z = data["ROV Height"].values
    time = data["Time"].values  # antar tid er i stigende rekkefølge
    
    # Lag linjesegmenter for 3D plotting
    points = np.array([x, y, z]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    # Gjør om tid til numerisk skala for farge
    t_numeric = np.linspace(0, 1, len(time))  # normaliser 0-1

    # Sett opp fargekart
    cmap = plt.get_cmap('viridis')  # du kan bruke 'plasma', 'inferno', osv. hvis du vil
    norm = mcolors.Normalize(vmin=0, vmax=1)
    lc = Line3DCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(t_numeric)
    lc.set_linewidth(2)

    # Sett opp plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.add_collection3d(lc)

    # Sett grenser på akser
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())
    ax.set_zlim(z.min(), z.max())

    # Aksetitler
    ax.set_xlabel('East [m]')
    ax.set_ylabel('North [m]')
    ax.set_zlabel('Height [m]')
    ax.set_title('ROV 3D Posisjon med tidsfarge')

    # Fargebar
    cbar = fig.colorbar(lc, ax=ax, shrink=0.5, aspect=10)
    cbar.set_label('Normalisert tid')

    plt.show()
