import pandas as pd
import os
import matplotlib.pyplot as plt
import sep_col_filter
#import numpy

#freq,bins=numpy.histogram(z.YM)
#numpy.average(lista, axis=0)

def histogram(YMlim1, YMlim2, filterend, file_path, file_name):
    #
    mfs=["YM_MaxF_0100pN", "YM_MaxF_0200pN", "YM_MaxF_0300pN", "YM_MaxF_0400pN", "YM_MaxF_0500pN", "YM_MaxF_0600pN", "YM_MaxF_0800pN", "YM_MaxF_1000pN", "YM_MaxF_1200pN", "YM_MaxF_1500pN"]
    #
    fig, axes = plt.subplots(2, 5, figsize=(12.5,5), dpi=300, sharex=True, sharey=True)
    #
    for az, mf in zip(axes.flatten(),mfs):
        z=filterend[filterend.maxforce==mf]
        az.hist(z.YM, alpha=0.5, bins=int(YMlim1/500), density=True, stacked=True, label=str(mf), range=(0,YMlim1))
        az.set_title(mf)
        plt.suptitle(file_name+' Young Modulus', y=1.05, size=16)
        plt.tight_layout()
        #plt.savefig(file_path+"_maxforces.png")
    plt.savefig(file_path+"_maxforces.png")
    #
    plt.subplots.clf()
    #
    for mf in mfs:
        z=filterend[filterend.maxforce==mf]
        z.YM.hist(bins=int(YMlim1/500), range=(0,YMlim1), label=mf)
        plt.legend(loc=0)
        plt.title(file_name)
        plt.xlabel("Young Modulus (Pa)")
        plt.ylabel("Frequency")
        #plt.savefig(file_path+"_150kPa_filter.png")
    plt.savefig(file_path+"_150kPa_filter.png")
    #
    plt.clf()
    #
    for mf in mfs:
        z=filterend[filterend.maxforce==mf]
        z.YM.hist(bins=int(YMlim2/200), range=(0,YMlim2), label=mf)
        plt.legend(loc=0)
        plt.title(file_name)
        plt.xlabel("Young Modulus (Pa)")
        plt.ylabel("Frequency")
        #plt.savefig(file_path+"50kPa_filter.png")
    plt.savefig(file_path+"50kPa_filter.png")
    #
    plt.clf()
    

def row_filter(datafilter, file_name, YMlim1, YMlim2, RMSlim, Hlim):
    #
    fullsize=len(datafilter)
    #
    #Filtro 1
    # definir o valor mínimo de altura, aplicar filtro em linha: Xi-Xmin>300nm  
    hmin=datafilter["Height_ref_5%"].min()
    mask=(datafilter["Height_ref_5%"]-hmin) > Hlim
    filter_h=datafilter[mask]
    filter1=filter_h.drop("Height_ref_5%", axis=1)
    cols=filter1.columns
    pairs=[[cols[i], cols[i+1]] for i in range(0, len(cols), 2)]
    dfs=[filter1[pair] for pair in pairs]
    temp=[]
    for df in dfs:
        x=df.copy()
        x["maxforce"]=x.columns[0]
        x.columns=["YM", "RMS", "maxforce"]
        temp.append(x)
    filter1=pd.concat(temp)
    #registrar quantidade de espectros restantes
    #
    #Remontar imagem em função das posições dos pixels
    #
    #Filtro 2
    #Xi-Xmin>300nm & ResidualRMS<150pN
    filter2=filter_h.drop("Height_ref_5%", axis=1)
    cols=filter2.columns
    pairs=[[cols[i], cols[i+1]] for i in range(0, len(cols), 2)]
    dfs=[filter2[pair] for pair in pairs]
    dfs=[df[df.iloc[:,1] < RMSlim] for df in dfs]
    temp=[]
    for df in dfs:
        x=df.copy()
        x["maxforce"]=x.columns[0]
        x.columns=["YM", "RMS", "maxforce"]
        temp.append(x)
    filter2=pd.concat(temp)
    #
    #Filtro 3
    #Young Modulus<150kPa
    #Filtro precisa ser aplicado para cada coluna indivudualmente
    filter3=datafilter.drop("Height_ref_5%", axis=1)
    cols=filter3.columns
    pairs=[[cols[i], cols[i+1]] for i in range(0, len(cols), 2)]
    dfs=[filter3[pair] for pair in pairs]
    dfs=[df[df.iloc[:,0] < YMlim1] for df in dfs]
    temp=[]
    for df in dfs:
        x=df.copy()
        x["maxforce"]=x.columns[0]
        x.columns=["YM", "RMS", "maxforce"]
        temp.append(x)
    filter3=pd.concat(temp)
    #
    #Filtro 4
    filter4=filter_h.drop("Height_ref_5%", axis=1)
    cols=filter4.columns
    pairs=[[cols[i], cols[i+1]] for i in range(0, len(cols), 2)]
    dfs=[filter4[pair] for pair in pairs]
    dfs=[df[df.iloc[:,1] < RMSlim] for df in dfs]
    dfs=[df[df.iloc[:,0] < YMlim1] for df in dfs]
    temp=[]
    for df in dfs:
        x=df.copy()
        x["maxforce"]=x.columns[0]
        x.columns=["YM", "RMS", "maxforce"]
        temp.append(x)
    filter4=pd.concat(temp)
    #
    #Filtro final
    filterend = filter4
    #
    #Registrar
    #Remontar

    #Gerar tabela:
        #Colunas: [Nome do arquivo, Quantidade de espectros YM 10 colunas Filtro 1, Filtro 2 e Filtro 3]
        #Colunas: [Index, YM 10 colunas]

    """results = pd.Series({'File Name': file_name, 'Tamanho original' : fullsize})
    results = results.append((filter1.groupby("maxforce").size()/fullsize*100).add_suffix('_1'))
    results = results.append((filter2.groupby("maxforce").size()/fullsize*100).add_suffix('_2')) 
    results = results.append((filter3.groupby("maxforce").size()/fullsize*100).add_suffix('_3'))
    results = results.append((filter4.groupby("maxforce").size()/fullsize*100).add_suffix('_4'))"""
    results = pd.Series({'File Name': file_name, 'Tamanho original' : fullsize})
    results = results.append((filter1.groupby("maxforce").size()).add_suffix('_1'))
    results = results.append((filter2.groupby("maxforce").size()).add_suffix('_2')) 
    results = results.append((filter3.groupby("maxforce").size()).add_suffix('_3'))
    results = results.append((filter4.groupby("maxforce").size()).add_suffix('_4'))
    #print(results)
    results = pd.concat([results], axis=1).transpose()
    #print(results)
    return filterend, results

def filter_hist(df, file_name):
    #Parâmetros de filtragem
    YMlim1 = 150E3 #Young Modulus limite 1
    YMlim2 = 50E3 #Young Modulus limite 2
    RMSlim = 80E-12 #RMS limite
    Hlim = 300E-9 #Altura limite
    
    #Filtragem dos dados
    filterend, results = row_filter(df, file_name, YMlim1, YMlim2, RMSlim, Hlim)

    #Definição de diretório para salvar os histogramas
    path = sep_col_filter.correctpath(file_name)
    file_path = os.path.join(path + 'Histogram/')
    if not os.path.exists(file_path):
        print('criando Histogram_DIR')
        os.makedirs(file_path)
    file_path = os.path.join(file_path + file_name)
    
    # função para criação de histogramas
    #histogram(YMlim1, YMlim2, filterend, file_path, file_name)

    return filterend, results

if __name__=="__main__":
    
    #Chamada do arquivo
    file_name="KO_Control_909604_2019_11_27_Cell_4_auto_calib_datafilter.tsv"
    df=pd.read_csv(file_name, sep="\t", index_col='Position Index')
    
    filter_hist(df, file_name)
    #print(f2.head())

    #print(f1.groupby("maxforce"))