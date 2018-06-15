#!/usr/bin/env python

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

Bet = pd.read_csv('Responses.csv', engine = 'python', index_col = 'Name')
Bet.rename(index = str.strip, columns = str.strip, inplace = True)
Bet.drop_duplicates(subset = 'Email', keep = 'last', inplace = True)
Bet = Bet[['Russia','Saudi Arabia','Egypt','Uruguay','Portugal','Spain' ,'Morocco','IR Iran' ,'France' ,'Australia' ,'Peru' ,'Denmark' ,'Argentina' ,'Iceland' ,'Croatia' ,'Nigeria' ,'Brazil' ,'Switzerland' ,'Costa Rica' ,'Serbia','Germany' ,'Mexico' ,'Sweden' ,'Korea Republic' ,'Belgium' ,'Panama' ,'Tunisia' ,'England' ,'Poland' ,'Colombia' ,'Senegal' ,'Japan']]
if (Bet.sum(1) != 16).any():
    print('The following entries do not have 16 shares and will be removed:')
    print(Bet[Bet.sum(1) != 16].sum(1))
    Bet.drop(Bet.loc[Bet.sum(1) != 16].index, inplace = True)

Bet = Bet.sort_index(1)
Expect = pd.read_csv('Results.csv', index_col = 0).sort_index()
Expect.rename(index = str.strip, columns = str.strip, inplace = True)
Result = Expect.copy() == 1
Result.drop('points', inplace = True)

for i in Result.index:
    Expect.loc[i] *= Expect.loc['points'].values
    Result.loc[i] *= Expect.loc['points'].values
Expect.drop('points', inplace = True)
Result['Tpoints'] = Result.sum(1)
Expect['Tpoints'] = Expect.sum(1)
Result['Shares'] = Bet.sum()
Result.loc[Result.Shares == 0, 'Shares'] = 1
Result['pps'] = Result.Tpoints/Result.Shares
Expect['pps'] = Expect.Tpoints/Result.Shares

for i in Bet.index:
    Bet.loc[i, 'Predicted_Score'] = (Bet.loc[i] * Expect.pps).sum()
    Bet.loc[i, 'Actual_Score'] = (Bet.loc[i] * Result.pps).sum()

Bet.sort_values('Predicted_Score', ascending = False).to_csv('Competition_Results.csv')
