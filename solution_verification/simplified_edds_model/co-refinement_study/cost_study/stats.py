import pandas as pd
import numpy as np

dataMesh=pd.read_csv('meshCost.dat', sep='\\s+')
dataMeshTime=pd.read_csv('meshTimeCost.dat', sep='\\s+')
dataTime=pd.read_csv('timeCost.dat', sep='\\s+')
def computeTime(data,label):
    totalsec = np.array(data['CT']) *np.array(data['Processors']) # seconds
    data['Total (sec)'] = totalsec
    print(f'data_{label} \n {data}')
    return data
dataM = computeTime(dataMesh,'Mesh')
dataMT = computeTime(dataMeshTime,'MeshTime')
dataT = computeTime(dataTime, 'Time')

dataM.to_csv('statsMesh.dat',sep=' ')
dataMT.to_csv('statsMeshTime.dat',sep=' ')
dataT.to_csv('statsTime.dat',sep=' ')
