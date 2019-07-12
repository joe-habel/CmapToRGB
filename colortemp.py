"""
This is the jet colormap. I literally just reinvented the jet colormap.
"""
import numpy as np
import matplotlib.pyplot as plt

from numba import jit

from makeCmap import array_to_arduino

K_RANGE = (1500, 12500)

#http://www.zombieprototypes.com/?p=210
#Parameters for region fits of T vs Color:
#Color = a + bx + cln(T + d)
FIT_PARAMS = {}
#Kelvin -> Red : K in [6600, inf)
FIT_PARAMS['R'] = {}
FIT_PARAMS['R']['a'] = 351.97690566805693
FIT_PARAMS['R']['b'] = 0.114206453784165
FIT_PARAMS['R']['c'] = -40.25366309332127
FIT_PARAMS['R']['d'] = -55
#Kelvin -> Green : K in (1000, 6600)
FIT_PARAMS['G'] = {}
FIT_PARAMS['G']['a1'] = -155.25485562709179
FIT_PARAMS['G']['b1'] = -0.44596950469579133
FIT_PARAMS['G']['c1'] = 104.49216199393888
FIT_PARAMS['G']['d1'] = -2
#Kelvin -> Green : K in [6600, inf)
FIT_PARAMS['G']['a2'] = 325.4494125711974
FIT_PARAMS['G']['b2'] = 0.07943456536662342
FIT_PARAMS['G']['c2'] = -28.0852963507957
FIT_PARAMS['G']['d2'] = -50
#Kelvin -> Blue : K in (2000, 6600)
FIT_PARAMS['B'] = {}
FIT_PARAMS['B']['a'] = -254.76935184120902
FIT_PARAMS['B']['b'] = 0.8274096064007395
FIT_PARAMS['B']['c'] = 115.67994401066147
FIT_PARAMS['B']['d'] = -10

KtoR = lambda T, a, b, c, d: 255 if T < 6600 else a + b*T + c*np.log(T/100. + d)

KtoG = lambda T, a1, b1, c1, d1, a2, b2, c2, d2: 0 if  T <= 1000 else a1 + b1*T + c1*np.log(T/100. + d1) if 1000 < T < 6600 else a2 + b2*T + c2*np.log(T/100. + d2)

KtoB = lambda T, a, b, c, d: 0 if T <= 2000 else 255 if T >= 6700 else a + b*T + c*np.log(T/100. + d)

def Kmap(data, k_range=K_RANGE):
    data_range = (np.min(data), np.max(data))
    a, b = data_range
    c, d = k_range

    K_trans = lambda x: (x - a)/(b - a)*(d - c) + c

    return K_trans(data)

@jit
def KtoRGB(data, img, parameters):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            T = data[i, j]
            img[i, j] = [KtoR(T, **parameters['R']), KtoG(T, **parameters['G']), KtoB(T, **parameters['B'])]



original = np.load('scan_array.npy')
data = Kmap(original)

save_img = data.astype(int)
plt.imsave('kmapped.png', save_img)

img = np.zeros((data.shape[0], data.shape[1], 3))
cmap = KtoRGB(data, img, FIT_PARAMS)

array_to_arduino(cmap)
