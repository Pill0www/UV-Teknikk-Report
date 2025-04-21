import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_ctd(ctd_path):
    return pd.read_csv(ctd_path, skiprows=2, usecols=range(7))


if __name__ == '__main__':
    df1 = read_ctd('20150520_CTD_Stokkbergneset.csv')
    df2 = read_ctd('20150521_CTD_Nordleksa.csv')

    # Remove data points at surface
    df1 = df1[df1['Press'] > 0.4]
    df2 = df2[df2['Press'] > 0.4]

    df1['Density'] += 1000
    df2['Density'] += 1000

    # Plot density profile
    plt.figure()
    plt.plot(df1['Density'], df1['Press'], c='b', label='Stokkbergneset')
    plt.plot(df2['Density'], df2['Press'], c='r', label='Nordleksa')
    plt.xlim([1020.5, 1028])
    plt.ylim([0, 190])
    plt.gca().invert_yaxis()
    plt.legend()
    plt.xlabel(r'Density [kg/$m^3$]')
    plt.ylabel('Pressure [dbar]')

    # Plot temp/press
    plt.figure()
    plt.plot(df1['Temp'], df1['Press'], c='b', label='Stokkbergneset')
    plt.plot(df2['Temp'], df2['Press'], c='r', label='Nordleksa')
    plt.gca().invert_yaxis()
    plt.xlim([7, 10])
    plt.legend()
    plt.xlabel('Temperature [C]')
    plt.ylabel('Pressure [dbar]')

    # Plot sound speed
    plt.figure()
    plt.plot(df1['S. vel.'], df1['Press'], c='b', label='Stokkbergneset')
    plt.plot(df2['S. vel.'], df2['Press'], c='r', label='Nordleksa')
    plt.xlim([1476, 1486])
    plt.ylim([0, 265])
    plt.gca().invert_yaxis()
    plt.legend()
    plt.xlabel('Sound speed [m/s]')
    plt.ylabel('Pressure [dbar]')

    # Moving average (smooth)
    df1_smooth = df1.sort_values(by='Press').rolling(window=15).mean().dropna()
    df2_smooth = df2.sort_values(by='Press').rolling(window=15).mean().dropna()

    # Plot vertical stability profile (note: division by zero)
    """ Not used as it is very noisy
    g = 9.81

    grad1 = np.diff(df1_smooth['Density'].values) / np.diff(df1_smooth['Press'].values)
    grad2 = np.diff(df2_smooth['Density'].values) / np.diff(df2_smooth['Press'].values)
    N1 = np.sqrt((g / df1_smooth['Density'].values[:-1]) * grad1)
    N2 = np.sqrt((g / df2_smooth['Density'].values[:-1]) * grad2)

    plt.figure()
    plt.plot(N1, df1_smooth['Press'][:-1], c='b', label='Stokkbergneset')
    plt.plot(N2, df2_smooth['Press'][:-1], c='r', label='Nordleksa')
    plt.gca().invert_yaxis()
    plt.legend()
    plt.xlabel('Brunt-Väisälä frequency [rad/s]')
    plt.ylabel('Pressure [dbar]')
    """

    plt.show()




