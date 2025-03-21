# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 19:30:23 2025

@author: kalle
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Ladataan csv-tiedosto
df = pd.read_csv("Termo98N.csv", delimiter=';')
df = df.apply(lambda x: x.str.replace(',', '.').astype(float) if x.dtype == 'object' else x)

aika = df["Time (s) 98N"]
jännite = df["Voltage (V) 98N"]

#Lasketaan jännitteen nollataso
kalib_alue = jännite[aika <= 100]
nollataso = np.mean(kalib_alue)
nolla_err = np.std(kalib_alue, ddof=1)
print("Nollatao:")
print(f"{nollataso:.5f} ± {nolla_err:.5f}")

#Luodaan käyrä adiabaattisen venytyksen jälkeiselle datalle
t1 = 111
t2 = 230

aika2 = aika[(aika >= t1) & (aika <= t2)]
jännite2 = jännite[(aika >= t1) & (aika <= t2)]

def exp_ftio(x, a, b, c):
    return a * np.exp(-b * x) + c

params, covariance = curve_fit(exp_ftio, aika2, jännite2, p0=[max(jännite2), 0.01, min(jännite2)], maxfev=5000)
a, b, c = params

aika3 = np.linspace(t1 - 10, t2, 1000)
käyrä = exp_ftio(aika3, *params)

kes_poik = np.std(jännite2, ddof=1)

#Parametrien virheet
param_errors = np.sqrt(np.diag(covariance))
a_err, b_err, c_err = param_errors
print(f"Käyrän parametrit virheineen:")
print(f"a = {a:.3e} ± {a_err:.3e}")
print(f"b = {b:.3e} ± {b_err:.3e}")
print(f"c = {c:.3e} ± {c_err:.3e}")

#Ekstrapolointi venytyksen alkamiskohtaan
t = 108.5
y = exp_ftio(t, a, b, c)
y_err = np.sqrt((a_err * np.exp(-b * t))**2 + (b_err * t * a * np.exp(-b * t))**2 + c_err**2)
print("Ekstrapoloitu maksimijännite:")
print(f"{y:.5f} ± {y_err:.5f}")

#Lasketaan jännite-ero ja sen virhe
deltaV = y - nollataso
deltaV_err = np.sqrt(y_err**2 + nolla_err**2)
print("Jännite-ero:")
print(f"ΔV = {deltaV:.5f} ± {deltaV_err:.5f} V")

#Sovitetun käyrän yhtälö
yhtälö = f"y = {a:.3f} * exp(-{b:.3f} * x) + {c:.3f}"

#Plotataan data, käyrä ja venytyksen alkamishetki
plt.scatter(aika, jännite, s=10, zorder=0, label="Jännite (V)")
plt.plot(aika3, käyrä, 'r-', zorder=1, linewidth=3, label=f"Sovitettu eksponenttifunktio")
plt.axvline(t, color='r', zorder=1, linestyle='--', linewidth=2, label=f'Aika = {t} s')
plt.axhline(nollataso, color='r', zorder=1, linestyle=':', linewidth=2, label=f'Nollataso = {nollataso:.5f} V')
plt.scatter(t, y, s=30, color='g', zorder=2, label=f'Ekstrapoloitu jännite = {y:.5f} V')

plt.xlim(40, 225)
plt.ylim(1.7, 2.5)

#Otsikot ja muotoilu
plt.xlabel("Aika (s)")
plt.ylabel("Jännite (V)")
plt.text(0.02, 0.99 - 0.15, yhtälö, transform=plt.gca().transAxes, fontsize=13, verticalalignment='top')
#plt.text(0.02, 0.94 - 0.12, f'Ekstrapoloitu maksimijännite = {y:.3f} V', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
#plt.text(0.02, 0.94 - 0.14, f'Keskipoikkeama = {kes_poik:.5f} V', transform=plt.gca().transAxes, fontsize=13, verticalalignment='top')
plt.title("Jännite ajan funktiona (98 N)")
plt.legend()
plt.grid(True)

plt.show()
