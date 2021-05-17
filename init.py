# %%

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2

def splitMatrixFromAFMData(matrixPlanned,matrixOriginal):

    # determine the number of columns and rows, now I am using the information
    # of the information from the planned image
    numRows,numColuns = matrixPlanned.shape

    matrixHeigthTmp=matrixOriginal[:,8] # taking only the information of heigth
    matrixYoungTmp=matrixOriginal[:,46] # taking only the information of Young Modulus

    columnsInterval=list(range(0,(len(matrixHeigthTmp)-1),numColuns)) # range (initial value, final value, step)

    # declare matrix
    matrixHeigth = np.ones((numRows,numColuns),dtype=np.float)*-1 # declaration of the matrix with heigth 
    matrixYoung = np.ones((numRows,numColuns),dtype=np.float)*-1 # declaration of the matrix with young

    for i in range(numRows-1):
        matrixHeigth[i,0:(numColuns)]=matrixHeigthTmp[columnsInterval[i]:columnsInterval[i+1]]
        matrixYoung[i,0:(numColuns)]=matrixYoungTmp[columnsInterval[i]:columnsInterval[i+1]]

    # include the last row
    matrixHeigth[numRows-1,0:numColuns]=matrixHeigthTmp[columnsInterval[-1]:matrixHeigthTmp.shape[0]]
    matrixYoung[numRows-1,0:numColuns]=matrixYoungTmp[columnsInterval[-1]:matrixHeigthTmp.shape[0]]

    # alternative using reshape
    matrixHeigth2=matrixHeigthTmp.reshape((numRows,numColuns))
    matrixYoung2=matrixYoungTmp.reshape((numRows,numColuns))

    # normalize the heigths between 0 and 1
    minHeigth=np.amin(matrixHeigth)
    maxHeigth=np.amax(matrixHeigth)
    matrixHeigthNorm=(matrixHeigth-minHeigth)/(maxHeigth-minHeigth)

    return matrixYoung


def countsAFMYoungHeigthNotNormPlanned(matrixOriginal,matrixPlanned,minHeigth,maxHeigth,numDivisions):

    # call function
    matrixYoung=splitMatrixFromAFMData(matrixPlanned,matrixOriginal)

    # determine the intervals for histograms
    vectorPlanned=matrixPlanned.reshape((1,matrixPlanned.shape[0]*matrixPlanned.shape[1]))
    vectorPlanned=vectorPlanned[0]
   # sns.histplot(vet)
    heigthStep=(maxHeigth-minHeigth)/numDivisions

    initialRange=minHeigth
    binsHeigth=[]

    for i in range(numDivisions):

        binsHeigth.append(initialRange)
        initialRange=initialRange+heigthStep

    distributionHeigthPlanned=np.histogram(vectorPlanned,bins=binsHeigth)

    # plot image
    matrixIntern=np.zeros(matrixYoung.shape,dtype=bool)
    """for i in range(matrixYoung.shape[0]):
        for j in range(matrixYoung.shape[1]):
            if (matrixYoung[i,j]<(5*(10**4))):
                matrixIntern[i,j]=True
    xypos=np.argwhere(matrixIntern)"""
    xyposIntern=np.argwhere(matrixYoung<(5*(10**4)))
    xyposExtern=np.argwhere(matrixYoung>(5*(10**4)))

    matrixYoungTmp=np.copy(matrixYoung) 
     # normalize the heigths between 0 and 1
    minYoung=np.amin(matrixYoungTmp)
    maxYoung=np.amax(matrixYoungTmp)
    matrixYoungNorm=((matrixYoungTmp-minYoung)/(maxYoung-minYoung))*255
    matrixYoungNorm=np.round(matrixYoungNorm)
    matrixPaint=np.zeros(matrixYoungTmp.shape,dtype=np.uint8) # definiçao da matrix que vai definir dentro e fora da celula
    
    for p in xyposExtern:
        matrixPaint[p]=255
        
    matPlotTmp=np.array([(matrixPaint+matrixYoungNorm)/2,matrixYoungNorm,matrixYoungNorm],dtype=np.uint8) # criando uma matrix com os canais RGB para o plot da imagem
   
    matPlot=np.zeros((matrixYoungNorm.shape[0],matrixYoungNorm.shape[1],3),dtype=np.uint8)





    for i in range(matrixYoungTmp.shape[0]):
        for j in range(matrixYoungTmp.shape[1]): 
            matPlot[i,j,0]=matPlotTmp[0,i,j]
            matPlot[i,j,1]=matPlotTmp[1,i,j]
            matPlot[i,j,2]=matPlotTmp[2,i,j]

    cv2.imwrite('matrixYoung.png',matPlot) # plot matrix young
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    print('vinicius idiota')






matrixPlanned=np.array([[1,2,3],
                         [4,5,6],
                         [7,8,9],
                         [10,11,12]],dtype=float)

matrixOriginal=np.array([12,11,10,9,8,7,6,5,4,3,2,1],dtype=float).transpose()
# %%
matrixPlanned=np.random.random((80,60))

matrixOriginal=np.random.random((4800,50))*1000000

splitMatrixFromAFMData(matrixPlanned,matrixOriginal)
# %%
countsAFMYoungHeigthNotNormPlanned(matrixOriginal,matrixPlanned,0.1,0.9,10)
# %%
