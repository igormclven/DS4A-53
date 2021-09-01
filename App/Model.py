#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import statsmodels.formula.api as sm
import pickle



df = pd.read_csv('datos_recaudo.csv')


df['recaudo_1000000000'] = df['recaudo_1000000000'].str.replace("$","")
df['recaudo_1000000000'] = df['recaudo_1000000000'].str.replace(",","")
df['cambio_trm'] = df['cambio_trm'].str.replace(",","")
df['IPVU_nom_medellin'] = df['IPVU_nom_medellin'].str.replace(",","")



df['recaudo_1000000000'] = df['recaudo_1000000000'].astype('float64')
df['cambio_trm'] = df['cambio_trm'].astype('float64')
df['IPVU_nom_medellin'] = df['IPVU_nom_medellin'].astype('float64')



formula = 'recaudo_1000000000 ~ cambio_trm + IPVU_nom_medellin+tasa_ocupacion_7a'

model = sm.ols(formula, df)



fitted = model.fit()



filename = 'finalized_model.sav'
pickle.dump(fitted, open(filename, 'wb'))
