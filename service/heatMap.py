#!/usr/bin/python3
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import gstools as gs
import math
from pykrige.uk import UniversalKriging
from pykrige.ok import OrdinaryKriging
from matplotlib import ticker
from matplotlib import pyplot as plt
plt.style.use('ggplot')


def round_up(n, decimals= -1):
    multiplier = 10 ** decimals
    return int (math.ceil(n * multiplier) / multiplier)

def round_down(n, decimals= -1):
    multiplier = 10 ** decimals
    return int (math.floor(n * multiplier) / multiplier)

def get_v(vmax, vmin):
    outMax = round_up(vmax)
    outMin = round_down(vmin)
    return outMax, outMin

def myPlot(varLabel=0, varData=[34,5,10,22,200], currentDateTime="19/09/20 20:53:10"):

    folder = ''
    labelName = ''
    units = ''
    if varLabel == 0:
        folder = 'at/'
        labelName = 'Temperatura Aire'
        units = ' (°C)'
    elif varLabel == 1:
        folder = 'ah/'
        labelName = 'Humedad Aire'
        units = ' (%)'
    elif varLabel == 2:
        folder = 'et/'
        labelName = 'Temperatura Tierra'
        units = ' (°C)'
    elif varLabel == 3:
        folder = 'eh/'
        labelName = 'Humedad Tierra'
        units = ' (%)'
    elif varLabel == 4:
        folder = 'l/'
        labelName = 'Luz'
        units = ' (Lux - lm/m2)'


    # conditioning data (x, y, values)
    data = np.array([
            [5.8, 2.0, varData[0]], #Nodo 1
            [0.1, 1.4, varData[1]], #Nodo 2
            [3.0, 2.3, varData[2]], #Nodo 3
            [5.1, 5.1, varData[3]], #Nodo 4
            [0.1, 5.1, varData[4]], #Nodo 5
        ])
    # convert conditioning data
    x, y, val = data[:, 0], data[:, 1], data[:, 2]
    # grid definition for output field
    gridx = np.arange(0.0, 6.0, 0.01)
    gridy = np.arange(0.0, 5.6, 0.01)
    # a gaussian covariance model
    cov_model = gs.Gaussian( dim=2, len_scale=2.160045727989625, anis=1.0, angles=-0, var=0.6679932602095421, nugget=0.0)

    pk_kwargs = cov_model.pykrige_kwargs
    OK1 = OrdinaryKriging(x, y, val, **pk_kwargs)
    z1, ss1 = OK1.execute("grid", gridx, gridy)

    fig = plt.figure(figsize=(6.4*1.3, 4.8*1.3))
    #Vmax Vmin
    #vMax, vMin = get_v(int(z1.max()), int(z1.min()))
    #print(vMax, vMin)

    ss = plt.imshow(z1, origin="lower",  cmap=plt.cm.get_cmap('jet', 30), vmin=z1.min(),vmax=z1.max())
    v1 = np.linspace(z1.min(), z1.max(), 16, endpoint=True)
    cbar = plt.colorbar(ss, label=labelName + units, ticks=v1)

    cbar.ax.tick_params(labelsize=10)

    title = labelName + units + " - Fecha: " + currentDateTime
    fig.suptitle(title, fontsize=18)

    #plt.show()
    plt.close()

    #Guardar Imagen
    currentDateTime = currentDateTime.replace(":", "-").replace("/", "-").replace(" ", "_")
    rootPath = "/home/pi/iot/store/charts/"
    fileName = labelName.replace(" ", "-") + "-" + currentDateTime +  '.png'
    pathFile = rootPath + folder + fileName
    fig.savefig(pathFile, dpi=75, format='png')

    return pathFile, fileName



if __name__ == "__main__":
    from datetime import datetime
    dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pathFile, nameDoc = myPlot(0, [55,45,60,40,55], dateTime)
    print(pathFile)
    print("Nombre del documento {}".format(nameDoc))


# #Si es positivo aproxima arriba cada 10
# #143 => 150
# #Si es negativo aproxima hacia arriba cada 10
# #-143 => -140
# print(-a)
# print(round_up(-a, -1))

# #Si es positivo aproxima hacia abajo cada 10
# #25 => 20
# #Si es Negativo aproxima hacia abajo cada 10
# #-24 => -30
# print(-b)
# print(round_down(-b, -1))






