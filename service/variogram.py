#!/usr/bin/python3
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import gstools as gs
from matplotlib import pyplot as plt
plt.style.use('ggplot')



def main():
    data = np.array([
        [0.1, 5.1],   #Nodo 5
        [0.1, 1.4],   #Nodo 2
        [3.0, 2.3],   #Nodo 3
        [5.1, 5.1],   #Nodo 4
        [5.8, 2.0],   #Nodo 1
        ])

    # convert conditioning data
    x, y = data[:, 0], data[:, 1]

    model = gs.Gaussian(dim=2, var=2, len_scale=3.6)
    srf = gs.SRF(model, mean=2, seed=42000)#seed=19970221)
    field = srf((x, y))
    # estimate the variogram of the field with 40 bins
    bins = np.arange(12)
    bin_center, gamma = gs.vario_estimate_unstructured((x, y), field, bins, sampling_size=10, sampling_seed=10)
    # fit the variogram with a stable model. (no nugget fitted)
    fit_model = gs.Stable(dim=2)
    fit_model.fit_variogram(bin_center, gamma, nugget=False)
    # output
    ax = fit_model.plot(x_max=max(bin_center))
    ax.plot(bin_center, gamma)
    #plt.show()
    plt.close()
    print(fit_model)

if __name__ == "__main__":
    main()

