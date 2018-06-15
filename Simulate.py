#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

n = 67
PW0 = 0.99
PD0 = 0.8
Wsig = 80
Dsig = 0.55*n/PD0

def Pdraw(x, A = PD0, s = Dsig):
    return A * np.exp(-x/s)

def Pwin(x, A = PW0, s = Wsig, n = n):
    return A * np.exp(-((x - n)/s)**2)

def GSsim(data):
    df = data.copy()
    df['qpts'] = 0
    ## Simulate Group stage points
    for i in df.iloc[:3].index:
        for j in df.loc[i:].iloc[1:].index:
            if np.random.rand() <= Pdraw(abs(df.Fifa[i] - df.Fifa[j])):
                df.loc[[i,j], ['points','qpts']] += 5,1
            else:
                df.loc[SimMatch(i, j, data.Fifa[i], data.Fifa[j])[0], ['points','qpts']] += 10,3

    ## Pick qualifying teams
    for i in df.index:
        if (df.qpts[i] > df.qpts).sum() >= 2:
            df.loc[i, 'qual'] = True
            df.loc[i, 'points'] += 10
        elif (df.qpts[i] < df.qpts).sum() >= 2:
            df.loc[i, 'qual'] = False
    if df.qual.isna().any():
        for i in df.index:
            if np.isnan(df.qual[i]):
                Pqual = (2 - df.qual.sum())/(df.qual.isna().sum())
                if np.random.rand() <= Pqual:
                    df.loc[i, 'qual'] = True
                    df.loc[i, 'points'] += 10
                else:
                    df.loc[i, 'qual'] = False

    return df[['qual', 'points']]

def SimMatch(teamA, teamB, rankA, rankB):
    if np.random.rand() <= Pwin(abs(rankA - rankB)):
        return np.array([teamA,teamB])[np.argsort([rankA, rankB])]
    else:
        return np.array([teamA,teamB])[np.argsort([rankA, rankB][::-1])]

def FullSim():
    data = pd.read_csv('Data.csv', index_col = 0)
    data['qual'] = np.nan
    data['QuatM'] = np.nan
    data['SemiM'] = np.nan
    data['Finals'] = np.nan
    data['points'] = 0
    data['pps'] = 0

    ##Group Stage
    for S in data.Group.unique():
        data.loc[data.Group == S, ['qual', 'points']] = GSsim(data.loc[data.Group == S])

    ##Playoffs
    for G1,G2,QM in zip(['A','C','E','G'],['B','D','F','H'],[1,1,3,3]):
        for m in [0,1]:
            i = data.loc[data.qual & (data.Group == G1)].index[m]
            j = data.loc[data.qual & (data.Group == G2)].index[[1,0][m]]
            winner = SimMatch(i, j, data.Fifa[i], data.Fifa[j])[0]
            data.loc[winner, 'points'] += 20
            data.loc[winner, 'QuatM'] = QM + m

    ##Quater Finals
    for m in [1,2,3,4]:
        i,j = data.loc[data.QuatM == m].index
        winner = SimMatch(i, j, data.Fifa[i], data.Fifa[j])[0]
        data.loc[winner, 'points'] += 40
        data.loc[winner, 'SemiM'] = m%2

    ##Semi Finals
    for m in [0,1]:
        i,j = data.loc[data.SemiM == m].index
        winner, loser = SimMatch(i, j, data.Fifa[i], data.Fifa[j])
        data.loc[winner, 'points'] += 80
        data.loc[winner, 'Finals'] = 1
        data.loc[loser, 'Finals'] = 0

    ##Third Place
    i,j = data.loc[data.Finals == 0].index
    data.loc[winner, 'points'] += 40

    ##First place
    i,j = data.loc[data.Finals == 1].index
    data.loc[winner, 'points'] += 120

    shares = np.histogram(np.ceil(np.random.normal(8,25,500)), bins = np.linspace(0, n, n+1))[0][data.Fifa.values - 1]
    shares[shares == 0] = 1
    data.pps += data.points/shares

    return data[['Fifa', 'Group', 'points', 'pps']]

if __name__ == "__main__":

    # x = np.arange(1,n+1)
    # W = Pwin(x)
    # D = Pdraw(x)
    # print('w',W.sum())
    # print('d',D.sum())
    # plt.plot(x,W)
    # plt.plot(x,D)
    # plt.show()
    # exit()

    iter = int(sys.argv[1])
    res = FullSim()

    for i in range(iter):
        if i%10 == 0: print(i)
        temp = FullSim()
        res.points += temp.points
        res.pps += temp.pps
    res.points /= iter + 1
    res.pps /= iter + 1
    print(res.sort_values(['pps']))
    res.to_csv('out.csv')
