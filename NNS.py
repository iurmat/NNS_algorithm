# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 16:37:49 2025

@author: Matteo Iurato
"""


import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
from argparse import ArgumentParser
from matplotlib.ticker import FormatStrFormatter

plt.close('all')


def NNS(ref, rep, accThr, bThr):

    #Defines the NNS algorithms

    """
    Parameters
    ----------
    ref : list of two lists (a and b coordinates)
        template trajectory.
    rep : list of two lists (a and b coordinates)
        trajectory of a single repetition.
    accThr : float
        accuracy threshold (based on the measurement instrument).
    bThr : float
        tolerance threshold (based on the curve amplitude).

    Returns
    -------
    score : float
        agreement score between the two trajectories.
    """

    score=0

    for i in range(len(ref[0])):
        #Calculate Euclidean distances
        dist=(np.sqrt(np.array(np.power(np.array(rep[0])-ref[0][i], 2))+np.array(np.power(np.array(rep[1])-ref[1][i], 2))))

        #Sort Euclidean distances
        sortedDist=np.sort(dist)

        #Find indexes of least Euclidean distance elements
        ind1=[ind for ind in range(len(dist)) if dist[ind]==sortedDist[0]][0]
        ind2=[ind for ind in range(len(dist)) if dist[ind]==sortedDist[1]][0]
        p=1
        while(rep[0][ind1]==rep[0][ind2]):
            #Avoid vertical lines: if two points with same abscissa, move forward to next point
            p+=1
            ind2=[ind for ind in range(len(dist)) if dist[ind]==sortedDist[p]][0]

        #Find maximum and minimum index
        minInd=min(ind1, ind2)
        maxInd=max(ind1, ind2)

        #Perform interpolation
        intPoint = ((((ref[0][i]-rep[0][maxInd])*rep[1][minInd])/(rep[0][minInd]-rep[0][maxInd])) -
                    (((ref[0][i]-rep[0][minInd])*rep[1][maxInd])/(rep[0][minInd]-rep[0][maxInd])))

        #Increment score
        if(abs(intPoint - ref[1][i]) < accThr):
            score += 1
        else:
            if(abs(intPoint - ref[1][i]) < bThr):
                score += 1

    #Express score as percentage
    score = (score/len(ref[0]))*100

    return score


def plot(i, ref, rep, labels):

    #Plots template and repetitions trajectories

    """
    Parameters
    ----------
    i : int
        figure number.
    ref : list of two lists (a and b coordinates)
        template trajectory.
    rep : list of lists of two lists (a and b coordinates)
        repetitions trajectories.

    Returns
    -------
    None.

    """

    repColors='#d0cece'

    plt.figure(i)
    ax=plt.subplot()

    #Plot repetitions
    for i in range(len(rep[0])-1):
        plt.plot(rep[0][i], rep[1][i], linewidth=1.5, color=repColors)
    plt.plot(rep[0][len(rep[0])-1], rep[1][len(rep[0])-1], linewidth=1.5, color=repColors)

    #Plot template
    plt.plot(ref[0], ref[1], linewidth=3)

    #Labels and ticks
    plt.xlabel(labels.split(' ')[0], fontsize=24)
    plt.ylabel(labels.split(' ')[1], fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    N = 2
    yticks_pos, yticks_labels = plt.yticks()
    myticks = [j for i,j in enumerate(yticks_pos) if not i%N]
    newlabels = [label for i,label in enumerate(yticks_labels) if not i%N]
    plt.yticks(myticks[1:], newlabels[1:])

    plt.tight_layout()


def main():

    # Set data directory
    movement = input('Please insert the name of the dataset subdirectory (e.g. "ABD_30") of your interest: ')
    nrep = len(os.listdir(movement)) - 1
    # nrep = 9

    referencePath = movement+"\\trial01.csv"

    #Read file for reference template
    file = open(referencePath)

    qRef=[]

    for row in file:
        qRef.append(row.split(','))

    file.close()

    for i in range(len(qRef)):
        for j in range(len(qRef[i])):
            qRef[i][j] = float(qRef[i][j])

    # Read files for repetition trajectories
    start=2
    end=nrep+2

    qRep = []

    for k in range (start, end):
        if k<10:
            repPath = movement+"\\trial0"+str(k)+".csv"
        else:
            repPath = movement+"\\trial"+str(k)+".csv"

        file = open(repPath)

        qRep.append([])

        for row in file:
            qRep[k-2].append(row.split(','))

        file.close()

        for i in range(0,len(qRep[k-2])):
            for j in range(0,len(qRep[k-2][i])):
                qRep[k-2][i][j] = float(qRep[k-2][i][j])

    #Define quaternion components signals
    refW = []
    refX = []
    refY = []
    refZ = []
    for i in range(len(qRef)):
        refW.append(qRef[i][0])
        refX.append(qRef[i][1])
        refY.append(qRef[i][2])
        refZ.append(qRef[i][3])

    repW = []
    repX = []
    repY = []
    repZ = []
    for j in range(0, nrep):
        W=[]
        X=[]
        Y=[]
        Z=[]
        for i in range(len(qRep[j])):
            W.append(qRep[j][i][0])
            X.append(qRep[j][i][1])
            Y.append(qRep[j][i][2])
            Z.append(qRep[j][i][3])
        repW.append(W)
        repX.append(X)
        repY.append(Y)
        repZ.append(Z)

    # Define thresholds
    coeff = 0.2

    thrY = abs(max(refY)-min(refY))*coeff
    thrZ = abs(max(refZ)-min(refZ))*coeff
    thrW = abs(max(refW)-min(refW))*coeff

    accThr = 0.025

    # Apply NNS
    scoresXY=[]
    scoresYZ=[]
    scoresXZ=[]
    scoresXW=[]
    scoresYW=[]
    scoresZW=[]

    for i in range(0,nrep):
        scoresXY.append(NNS([refX,refY],[repX[i],repY[i]], accThr, thrY))
        scoresYZ.append(NNS([refY,refZ],[repY[i],repZ[i]], accThr, thrZ))
        scoresXZ.append(NNS([refX,refZ],[repX[i],repZ[i]], accThr, thrZ))
        scoresXW.append(NNS([refX,refW],[repX[i],repW[i]], accThr, thrW))
        scoresYW.append(NNS([refY,refW],[repY[i],repW[i]], accThr, thrW))
        scoresZW.append(NNS([refZ,refW],[repZ[i],repW[i]], accThr, thrW))

    scores = (np.array(scoresXY) + np.array(scoresYZ) + np.array(scoresXZ) + np.array(scoresXW) + np.array(scoresYW) + np.array(scoresZW))/6

    # Output restult
    print('The agreement scores for the ' + str(nrep) + ' considered repetitions with respect to the template are:')
    print(scores)

    #Plots
    plot(0,[refX,refY], [repX, repY], 'X Y')
    plot(1,[refY,refZ], [repY, repZ], 'Y Z')
    plot(2,[refX,refZ], [repX, repZ], 'X Z')
    plot(3,[refX,refW], [repX, repW], 'X W')
    plot(4,[refY,refW], [repY, repW], 'Y W')
    plot(5,[refZ,refW], [repZ, repW], 'Z W')

    plt.show()


if __name__ == "__main__":
    main()