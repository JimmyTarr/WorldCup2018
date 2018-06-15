#!/usr/bin/env python

import numpy as np
import argparse

## Command line options
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--niter', type = int, required = True, help = "Number of iterations")
parser.add_argument('-A', default = 'A', help = "Team A name")
parser.add_argument('-B', default = 'B', help = "Team B name")
parser.add_argument('-C', default = 'C', help = "Team C name")
parser.add_argument('-D', default = 'D', help = "Team D name")
parser.add_argument('-AB')
parser.add_argument('-AC')
parser.add_argument('-AD')
parser.add_argument('-BC')
parser.add_argument('-BD')
parser.add_argument('-CD')
args = parser.parse_args()

Pdraw = 0.27
Pwin = Pdraw + 0.5 * (1 - Pdraw)

def GS_sim(Inital):
    Res = Inital.copy()
    points = {args.A : 0, args.B : 0, args.C : 0, args.D : 0}

    for i in range(len(Res)):
        if not Res[i, 2]:
            rval = np.random.rand()
            if rval <= Pdraw:
                Res[i, 2] = Res[i, 0] + Res[i, 1]
            elif rval <= Pwin:
                Res[i, 2] = Res[i, 0]
            else:
                Res[i, 2] = Res[i, 1]
        for T in points.keys():
            if Res[i, 2] == T:
                points[T] += 3
            elif T in Res[i, 2]:
                points[T] += 1
    return (points)

def Qual(pts):
    ret = {}
    for T in pts.keys():
        if (pts[T] > np.array(list(pts.values()))).sum() >= 2:
            ret[T] = 1
        elif (pts[T] < np.array(list(pts.values()))).sum() >= 2:
            ret[T] = 0
    if len(ret) < 4:
        for T in pts.keys():
            Prob = (2 - sum(ret.values()))/(4 - len(ret))
            if T not in ret.keys():
                if np.random.rand() < Prob:
                    ret[T] = 1
                else:
                    ret[T] = 0
                if len(ret) == 4:
                    break
    return ret

if __name__ == '__main__':
    Inital = np.array(((args.A, args.B, args.AB), (args.A, args.C, args.AC), (args.A, args.D, args.AD), (args.B, args.C, args.BC), (args.B, args.D, args.BD), (args.C, args.D, args.CD)))

    cum = {args.A : 0, args.B : 0, args.C : 0, args.D : 0}
    for i in range(args.niter):
        pts = GS_sim(Inital)
        Qi = Qual(pts)
        for T in cum.keys():
            cum[T] += Qi[T]

    for T in cum.keys():
        print('Probability of',T,'qualifying is', round((cum[T])/args.niter,2))
