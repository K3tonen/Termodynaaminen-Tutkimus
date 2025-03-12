# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 19:30:23 2025

@author: kalle
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit

#Ladataan csv-tiedosto
df = pd.read_csv("TermoPitLämKer.csv", delimiter=';')
df = df.apply(lambda x: x.str.replace(',', '.').astype(float) if x.dtype == 'object' else x)

aika = df["Time (s) alpha"]
jännite = df["Voltage (V) alpha"]


#Lasketaan jännitteen nollataso ja uusi tasapainoasema
kalib_alue = jännite[aika <= 140]
nollataso = np.mean(kalib_alue)
nolla_err = np.std(kalib_alue, ddof=1)

tasap_alue = jännite[(aika >= 420) & (aika <= 485)]
tasapaino = np.mean(tasap_alue)
tasap_err = np.std(tasap_alue, ddof=1)

deltaV = nollataso - tasapaino
deltaV_err = np.sqrt(nolla_err**2 + tasap_err**2)

print("Jännite-ero:")
print(f"ΔV = {deltaV:.5f} ± {deltaV_err:.5f} V")

#Plotataan data, nollataso ja tasapainoasema
plt.scatter(aika, jännite, s=10, label="Jännite (V)")
plt.axhline(nollataso, color='r', linestyle=':', linewidth=2, label=f'Nollataso = {nollataso:.5f} V')
plt.axhline(tasapaino, color='r', linestyle='--', linewidth=2, label=f'Tasapaino = {tasapaino:.5f} V')

plt.xlim(100, 475)
plt.ylim(-3.5, 2)

#Otsikot ja muotoilu
plt.xlabel("Aika (s)")
plt.ylabel("Jännite (V)")

'''
plt.text(0.5, 0.9, f'Nollataso = {nollataso:.5f} V', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
plt.text(0.5, 0.85, f'Tasapaino = {tasapaino:.5f} V', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
'''

plt.title("Jännite ajan funktiona (alpha)")
plt.legend()
plt.grid(True)

plt.show()
