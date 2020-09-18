#!/usr/bin/python3
import numpy as np
import gstools as gs
import math
from pykrige.uk import UniversalKriging
from pykrige.ok import OrdinaryKriging 
from matplotlib import ticker
from matplotlib import pyplot as plt
from datetime import datetime
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

def myPlot(varLabel=0, varData=[34,5,10,22,200]):

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
            [5.1, 4.1, varData[3]], #Nodo 4
            [0.1, 5.1, varData[4]], #Nodo 5
        ])       
    # convert conditioning data
    x, y, val = data[:, 0], data[:, 1], data[:, 2]
    # grid definition for output field
    gridx = np.arange(0.0, 6.0, 0.01)
    gridy = np.arange(0.0, 5.6, 0.01)
    # a gaussian covariance model
    cov_model = gs.Gaussian( dim=2, len_scale=2.8340093019680803, anis=1.0, angles=-0, var=0.7320789975351657, nugget=0.0)  
 
    pk_kwargs = cov_model.pykrige_kwargs
    OK1 = OrdinaryKriging(x, y, val, **pk_kwargs)
    z1, ss1 = OK1.execute("grid", gridx, gridy)
    
    fig = plt.figure(figsize=(6.4*1.7, 4.8*1.7))
    #Vmax Vmin
    #vMax, vMin = get_v(int(z1.max()), int(z1.min()))
    #print(vMax, vMin) 
    
    ss = plt.imshow(z1, origin="lower",  cmap=plt.cm.get_cmap('jet', 30), vmin=z1.min(),vmax=z1.max())
    v1 = np.linspace(z1.min(), z1.max(), 16, endpoint=True) 
    cbar = plt.colorbar(ss, label=labelName + units, ticks=v1)

    cbar.ax.tick_params(labelsize=10)
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    title = labelName + units + " - Campo: 6mx5.6m " + dt_string
    fig.suptitle(title, fontsize=18)
    #plt.show() 
    plt.close() 

    #Guardar Imagen
    dt_string = dt_string.replace(":", "-").replace("/", "-")
    nameFile = "charts/" + folder +  labelName + " " + dt_string +  '.png'
    fig.savefig(nameFile, dpi=200, format='png' )

    return nameFile



if __name__ == "__main__":
    myPlot(0,[55,45,60,40,55])


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