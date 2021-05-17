# %%

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import re
import pandas as pd
import io
import os

def splitMatrixFromAFMData(matrixPlanned,matrixOriginal):

    # determine the number of columns and rows, now I am using the information
    # of the information from the planned image
    numRows,numColumns = matrixPlanned.shape
    
    matrixHeigthTmp = matrixOriginal.iloc[:,8] # taking only the information of heigth
    matrixYoungTmp = matrixOriginal.iloc[:,46] # taking only the information of Young Modulus
    #print("matrixHeigthTmp:")
    #print(matrixHeigthTmp)

    columnsInterval = list(range(0,(len(matrixHeigthTmp)-1),numColumns)) # range (initial value, final value, step)
    
    # declare matrix
    matrixHeigth = np.ones((numRows,numColumns),dtype=np.float)*-1 # declaration of the matrix with heigth 
    matrixYoung = np.ones((numRows,numColumns),dtype=np.float)*-1 # declaration of the matrix with young
    #print("matrixHeigth:")
    #print(matrixHeigth)
    #print(matrixYoung)

    for i in range(numRows-1):
        matrixHeigth[i,0:(numColumns)] = matrixHeigthTmp[columnsInterval[i]:columnsInterval[i+1]]
        matrixYoung[i,0:(numColumns)] = matrixYoungTmp[columnsInterval[i]:columnsInterval[i+1]]
        
    # include the last row
    matrixHeigth[numRows-1,0:numColumns] = matrixHeigthTmp[columnsInterval[-1]:matrixHeigthTmp.shape[0]]
    matrixYoung[numRows-1,0:numColumns] = matrixYoungTmp[columnsInterval[-1]:matrixHeigthTmp.shape[0]]
    #print("matrixHeigth:")
    #print(matrixHeigth)
    #print(matrixYoung)

    """# alternative using reshape
    matrixHeigth2 = matrixHeigthTmp.reshape((numRows,numColumns))
    matrixYoung2 = matrixYoungTmp.reshape((numRows,numColumns))"""

    # normalize the heigths between 0 and 1
    minHeigth = np.amin(matrixHeigth)
    maxHeigth = np.amax(matrixHeigth)
    #print(matrixYoung)

    """# alternative using reshape
    matrixHeigth2 = matrixHeigthTmp.reshape((numRows,numColumns))
    matrixYoung2 = matrixYoungTmp.reshape((numRows,numColumns))"""

    # normalize the heigths between 0 and 1
    minHeigth = np.amin(matrixHeigth)
    maxHeigth = np.amax(matrixHeigth)
    matrixHeigthNorm = (matrixHeigth-minHeigth)/(maxHeigth-minHeigth)

    return matrixYoung

# %%
def countsAFMYoungHeigthNotNormPlanned(matrixOriginal,matrixPlanned,minHeigth,maxHeigth,numDivisions):
    numRows,numColumns = matrixPlanned.shape
    #print(numRows,numColumns)
    # call function
    matrixYoung = splitMatrixFromAFMData(matrixPlanned,matrixOriginal)
    #print(matrixPlanned)
        
    # determine the intervals for histograms
    #print(matrixPlanned.values)
    vectorPlanned = matrixPlanned.values.reshape((1,matrixPlanned.shape[0]*matrixPlanned.shape[1]))
    #vectorPlanned = vectorPlanned[0]

    #usefull dataframe

    usefullVector, usefullVColumns = selectColumns()
    matrixUsefull = usefullDataframe(matrixOriginal, matrixPlanned, usefullVector, usefullVColumns)
    #print(matrixUsefull)

    string=matrixOriginal.iloc[1,0].split(sep='_')
    name=string[0]+'_'+string[1]+'_'+string[2]+'_'+string[3]+'_'+string[4]+'_'+string[5]
    parameter = 'Height_'+name

    # scatter plot
    Hlim = 10**-7
    mask1 = (matrixUsefull["Planned Height"]) > Hlim
    filter1 = matrixUsefull[mask1]
    YMlim = 150*10**3
    mask2 = (filter1["YM_Fmax0300pN"]) < YMlim
    filter2 = filter1[mask2]
    xlimite = 2.6*10**-6
    step = xlimite/10
    colours = ['','k','r','orange','yellow','c','m','g','b','gray','pink']
    #colours = {'black': 'k','red':,'orange','yellow',]
    for f in range(1, 11, 1):
        maskf = (filter2["Planned Height"]) > (f*step-step)
        dataf = filter2[maskf]
        maskf = (dataf["Planned Height"]) < (f*step) 
        dataf = dataf[maskf]
        
        x = dataf.iloc[:,15]
        y = dataf.iloc[:,-1]
        plt.scatter(y,x, c=colours[f], marker='.')
        #plt.show()


    plt.xlim([0,xlimite])
    plt.ylim([0,50*10**3])
    
    plt.savefig("file/YMvsHeight_"+name+".png")
    plt.clf()


    # sns.histplot(vet)
    heigthStep = (maxHeigth-minHeigth)/numDivisions

    initialRange = minHeigth
    binsHeigth = []

    for i in range(numDivisions):

        binsHeigth.append(initialRange)
        initialRange = initialRange+heigthStep

    distributionHeigthPlanned = np.histogram(vectorPlanned,bins=binsHeigth)

    #ImagePlot(matrixYoung, matrixYoung, [5*10**4], "YoungModulus")
    ImagePlot(matrixPlanned.values, matrixYoung, [5*10**4], parameter)

def usefullDataframe(matrixOriginal, matrixPlanned, usefullVector, usefullVColumns):

    matrixUsefull = matrixOriginal.iloc[:, usefullVector] # selecionando 
    matrixUsefull.columns = usefullVColumns

    columnPlanned = pd.DataFrame(matrixPlanned.values.reshape((1,matrixPlanned.shape[0]*matrixPlanned.shape[1])).transpose())
    columnPlanned.columns = ["Planned Height"]
    
    matrixUsefull = pd.concat([matrixUsefull, columnPlanned], axis=1)
    #print(matrixUsefull)
    
    return matrixUsefull

def ImagePlot(matrixGen, matrixfilter,limGen,parameter):
    # plot image
    # matrixGen: matrix input need to be array type
    # limGen: number
    # parameter: string that is the name of the parameter of the plot image

    """matrixIntern = np.zeros(matrixYoung.shape,dtype=bool)
    
    for i in range(matrixYoung.shape[0]):
        for j in range(matrixYoung.shape[1]):
            if (matrixYoung[i,j]<(5*(10**4))):
                matrixIntern[i,j]=True
    xypos=np.argwhere(matrixIntern)"""
    xyposIntern = np.argwhere(matrixfilter<limGen)
    xyposExtern = np.argwhere(matrixfilter>limGen)

    matrixGenTmp = np.copy(matrixGen) 
     # normalize the heigths between 0 and 1
    minGen = np.amin(matrixGenTmp)
    maxGen = np.amax(matrixGenTmp)
    matrixGenNorm = ((matrixGenTmp-minGen)/(maxGen-minGen))*255
    matrixGenNorm = np.round(matrixGenNorm)
    matrixPaint = np.zeros(matrixGenTmp.shape,dtype=np.uint8) # definiçao da matrix que vai definir dentro e fora da celula
    
    for p in xyposExtern:
        matrixPaint[p[0]] = 255
        
    matPlotTmp = np.array([matrixGenNorm,matrixGenNorm,matrixGenNorm],dtype=np.uint8) # criando uma matrix com os canais RGB para o plot da imagem
   
    matPlot = np.zeros((matrixGenNorm.shape[0],matrixGenNorm.shape[1],3),dtype=np.uint8)

    for i in range(matrixGenTmp.shape[0]):
        for j in range(matrixGenTmp.shape[1]): 
            matPlot[i,j,0] = matPlotTmp[0,i,j]
            matPlot[i,j,1] = matPlotTmp[1,i,j]
            matPlot[i,j,2] = matPlotTmp[2,i,j]


    #matPlotfilterTmp = np.array([matrixGenNorm,(matrixPaint+matrixGenNorm)/2,matrixGenNorm],dtype=np.uint8) # criando uma matrix com os canais RGB para o plot da imagem
    matPlotfilterTmp = np.array([matrixGenNorm,matrixPaint,matrixGenNorm],dtype=np.uint8) # criando uma matrix com os canais RGB para o plot da imagem
    matPlotfilter = np.zeros((matrixGenNorm.shape[0],matrixGenNorm.shape[1],3),dtype=np.uint8)

    for i in range(matrixGenTmp.shape[0]):
        for j in range(matrixGenTmp.shape[1]): 
            matPlotfilter[i,j,0] = matPlotfilterTmp[0,i,j]
            matPlotfilter[i,j,1] = matPlotfilterTmp[1,i,j]
            matPlotfilter[i,j,2] = matPlotfilterTmp[2,i,j]

    cv2.imwrite("file/matrix_"+parameter+".png",matPlot) # plot matrix height
    cv2.imwrite("file/matrixfilter_"+parameter+".png",matPlotfilter) # plot matrix height young filter
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    print('achoo!')

def selectColumns():
    #function to resume code, only return usefullVector, usefullVColumns
    usefullVector = [0,2,3,
                    6,
                    8,
                    10,11,17,
                    20,
                    22,29,
                    30,37,
                    38,45,
                    46,53,
                    54,61,
                    62,69,
                    70,77,
                    78,85,
                    86,93,
                    94,101,
                    102,109,
                    110,
                    111,112,113,114,
                    117,118,119,120,
                    123,124,125,126,
                    129,130,131,132]
    usefullVColumns = ["filename","X Position","Y Position",
                        "Height 10%",
                        "Height 5%",
                        "Ajuste_X_CP_YM","Ajuste_X_CP_CP","Ajuste_X_CP_RRMS",
                        "Indentation F80%",
                        "Ajuste_Y_CP_YM","Ajuste_Y_CP_RRMS",
                        "YM_Fmax0100pN","RMS_Fmax0100pN",
                        "YM_Fmax0200pN","RMS_Fmax0200pN",
                        "YM_Fmax0300pN","RMS_Fmax0300pN",
                        "YM_Fmax0400pN","RMS_Fmax0400pN",
                        "YM_Fmax0500pN","RMS_Fmax0500pN",
                        "YM_Fmax0600pN","RMS_Fmax0600pN",
                        "YM_Fmax0800pN","RMS_Fmax0800pN",
                        "YM_Fmax1000pN","RMS_Fmax1000pN",
                        "YM_Fmax1200pN","RMS_Fmax1200pN",
                        "YM_Fmax1500pN","RMS_Fmax1500pN",
                        "Filter Group",
                        "MinForce_F0000pN","minPosition_F0000pN","MaxForce_F0500pN","MaxPosition_F0500pN",
                        "MinForce_F0000pN","minPosition_F0000pN","MaxForce_F1000pN","MaxPosition_F1000pN",
                        "MinForce_F0000pN","minPosition_F0000pN","MaxForce_F1500pN","MaxPosition_F1500pN",
                        "MinForce_F0000pN","minPosition_F0000pN","MaxForce_F3000pN","MaxPosition_F3000pN"]
    
    return usefullVector, usefullVColumns

main_folder = '/media/cleyton/Arquivos/Tratamento Python/Proj_Trat_Height/AFM_QIMode'

for roots, dirs, files in os.walk(main_folder):
    for file in files:
        if not re.search(r'\.tsv', file):
            if not re.search(r'\.txt', file):
                continue
        print(file)
        
        if re.search(r'\.tsv', file):
            root = os.path.join(roots, file)
            matrixOriginal = pd.read_csv(root, sep='\t') #, index_col='Position Index')
            print('TSV file')
            print(matrixOriginal.shape)
        elif re.search(r'\.txt', file):
            root = os.path.join(roots, file)
            dataframestr=""
            df=open(root)
            while (True):
                line = df.readline()
                if line[0] != "#":
                    dataframestr=dataframestr+line+df.read()
                    df.close()
                    break
            df=io.StringIO(dataframestr)
            matrixPlanned = pd.read_csv(df, sep=" ", header=None) 
            print('TXT file')
            print(matrixPlanned.shape)
        
            matrixYoung = splitMatrixFromAFMData(matrixPlanned,matrixOriginal)
            countsAFMYoungHeigthNotNormPlanned(matrixOriginal,matrixPlanned,0.1,0.9,10)
        else:
            continue
        #root = u"\\\\?\\" + os.path.join(roots, file)
        """root = os.path.join(roots, file)
        df = pd.read_csv(root, sep='\t', index_col='Position Index')
        print("a função abriu"+file)
        print(roots)"""


        """matrixPlanned=np.array([[1,2,3],
                                [4,5,6],
                                [7,8,9],
                                [10,11,12]],dtype=float)

        matrixOriginal=np.array([12,11,10,9,8,7,6,5,4,3,2,1],dtype=float).transpose()
        
        matrixPlanned=np.random.random((80,60))

        matrixOriginal=np.random.random((4800,50))*1000000
        
        matrixYoung = splitMatrixFromAFMData(matrixPlanned,matrixOriginal)
        
        countsAFMYoungHeigthNotNormPlanned(matrixOriginal,matrixPlanned,0.1,0.9,10)
        """

# %%
