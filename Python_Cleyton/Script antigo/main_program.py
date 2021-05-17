import pandas as pd
import os
import re
import numpy as np
import matplotlib.pyplot as plt

#print('Script abriu')
# Abrir os arquivos
#main_folder = 'C:\\Users\\cleyt\\Desktop\\JPK Dados\\INCor\\Originais'
#main_folder = '/mnt/d/JPK Dados/INCor/Originais'
#main_folder = '/mnt/d/JPK Dados/INCor/Originais/2020_08_20'   #Gel
main_folder = '/mnt/d/Tratamento Python/Proj_Trat/Dados_Brutos'
#print(main_folder)

#Separar em um novo arquivo: Colunas Contact point; Young Modulus ([xi:xf]Fmax); ResidualRMS ([xi:xf]Fmax). Aprox. 21 colunas e outro arquivo com o restante dos dados.
import sep_col_filter 

#Abrir os dados recem separados e aplicar filtros de linha
import row_filter
#Filtros
#Filtro linhas 1: Altura > 300nm
#Filtro linhas 2: Altura > 300nm; ResidualRMS <150pN
#Filtro linhas 3: Young Modulus < 150kPa
#Calcular porcentagem de espectros aproveitados e comparar para avaliar quantidade de dados perdidos.

#Remontar as imagens e avaliar perda


#Criar histograma para todos as colunas: Young Modulus e ResidualRMS
#Exportar histogramas em 1 documento e 1 arquivo tsv


#Realizar média dos histogramas de amostras iguais
import hist_average 

#plot das médias dos histogramas


# Load the example Titanic dataset
#df = sns.load_dataset("titanic")

# Make a custom palette with gendered colors
#pal = dict(male="#6495ED", female="#F08080")

# Show the survival probability as a function of age and sex
#g = sns.lmplot(x="age", y="survived", col="sex", hue="sex", data=df,
#               palette=pal, y_jitter=.02, logistic=True, truncate=False)
#g.set(xlim=(0, 80), ylim=(-.05, 1.05))

#Exportar 


#Realizar extração de parâmetros dos histogramas: Média e Mediana; Ajuste de função; Análises não paramétricas.
#Montar uma tabela com valores de parâmetros para cada imagem e coluna


#Aplicar testes: Kruskal-Wallis e Komolgorov-Smirnov
filter_av = pd.DataFrame()
media_hist = pd.DataFrame()
hist_mc_KO_Control = pd.DataFrame()
hist_mc_KO_ROCKi = pd.DataFrame()
hist_mc_KO_Ang = pd.DataFrame()
hist_mc_WT_Control = pd.DataFrame()
hist_mc_WT_ROCKi = pd.DataFrame()
hist_mc_WT_Ang = pd.DataFrame()
hist_ac_KO_Control = pd.DataFrame()
hist_ac_KO_ROCKi = pd.DataFrame()
hist_ac_KO_Ang = pd.DataFrame()
hist_ac_WT_Control = pd.DataFrame()
hist_ac_WT_ROCKi = pd.DataFrame()
hist_ac_WT_Ang = pd.DataFrame()
#hist_Gel = pd.DataFrame()
#hist_Outros = pd.DataFrame()

for roots, dirs, files in os.walk(main_folder):
    
    for file in files:
        if not re.search(r'\.tsv', file):
            continue
        #root = u"\\\\?\\" + os.path.join(roots, file)
        root = os.path.join(roots, file)
        df = pd.read_csv(root, sep='\t', index_col='Position Index')
        #print("a função abriu")
        if not len(df.T)==150:
            print(len(df.T))
            print("Este arquivo não é compatível com o programa:" + root)
            continue
        #print(root)
        datafilter, new_name = sep_col_filter.sep_col_filter(root)

        #Filtragem dos dados e criação dos histogramas
        datafend, results = row_filter.filter_hist(datafilter, new_name)
        #print(results.columns)
        filter_av = filter_av.append(results)
        filter_av.to_csv('Avaliação dos filtros.tsv', sep='\t')

        #Separação YM de uma força máxima em dataframe único
        mf="YM_MaxF_1500pN"
        hist_mf, hist_norm, hist_mc_KO_Control, hist_mc_KO_ROCKi, hist_mc_KO_Ang, hist_mc_WT_Control, hist_mc_WT_ROCKi, hist_mc_WT_Ang, hist_ac_KO_Control, hist_ac_KO_ROCKi, hist_ac_KO_Ang, hist_ac_WT_Control, hist_ac_WT_ROCKi, hist_ac_WT_Ang= hist_average.mf_hist(datafend, new_name, mf, media_hist, hist_mc_KO_Control, hist_mc_KO_ROCKi, hist_mc_KO_Ang, hist_mc_WT_Control, hist_mc_WT_ROCKi, hist_mc_WT_Ang, hist_ac_KO_Control, hist_ac_KO_ROCKi, hist_ac_KO_Ang, hist_ac_WT_Control, hist_ac_WT_ROCKi, hist_ac_WT_Ang)
        #print(media_hist)
        #hist_average(datafend, new_name, mf)
        plt.plot(hist_mf["Young Modulus (Pa)"], hist_norm[new_name], label="Normalized")
        plt.savefig("hist_norm_"+mf+".png")

plt.clf()

hists = [hist_mc_KO_Control, hist_mc_KO_ROCKi, hist_mc_KO_Ang, hist_mc_WT_Control, hist_mc_WT_ROCKi, hist_mc_WT_Ang, hist_ac_KO_Control, hist_ac_KO_ROCKi, hist_ac_KO_Ang, hist_ac_WT_Control, hist_ac_WT_ROCKi, hist_ac_WT_Ang]
name_hists = ["hist_Manual_Calib_KO_Control", "hist_Manual_Calib_KO_ROCKi", "hist_Manual_Calib_KO_Ang", "hist_Manual_Calib_WT_Control", "hist_Manual_Calib_WT_ROCKi", "hist_Manual_Calib_WT_Ang", "hist_Auto_Calib_KO_Control", "hist_Auto_Calib_KO_ROCKi", "hist_Auto_Calib_KO_Ang", "hist_Auto_Calib_WT_Control", "hist_Auto_Calib_WT_ROCKi", "hist_Auto_Calib_WT_Ang", "hist_Gel", "hist_Outros"]

for hist, name in zip(hists, name_hists):
    if hist.empty:
        continue
    z = pd.DataFrame(hist_mf['Young Modulus (Pa)'])
    full_hist = pd.concat([z, hist], axis=1)
    #   print(hist)
    full_hist.to_csv(name+'_all_'+mf+'.tsv', sep='\t')
    average_hist = pd.DataFrame(np.average(hist, axis=1))
    #print(average_hist)
    smooth1_average =  average_hist.rolling(10).mean()
    smooth2_average =  average_hist.rolling(5).mean()
    #q1_hist = pd.DataFrame(np.nanquantile(hist, 0.25, axis=1))
    #q3_hist = pd.DataFrame(np.nanquantile(hist, 0.75, axis=1))
    std_hist = pd.DataFrame(np.std(hist, axis=1))
    smooth1_std =  std_hist.rolling(10).mean()
    std_hist = smooth1_std
    average_hist = pd.concat([z, average_hist, std_hist, smooth1_average, smooth2_average], axis=1) #, q1_hist, q3_hist], axis=1)
    columns_name = ["Young Modulus (Pa)", name, "Error", "Smooth_1", "Smooth_2"]
    average_hist.columns = columns_name
    average_hist.to_csv(name+"_"+mf+".tsv", sep='\t')
    #print(average_hist)
    plt.errorbar(average_hist["Young Modulus (Pa)"], average_hist["Smooth_1"], yerr=average_hist["Error"], ecolor="lightgray", label="Average_Hist")
    plt.plot(average_hist["Young Modulus (Pa)"], average_hist["Smooth_1"], color="green", label="Smooth_1")
    #plt.plot(average_hist["Young Modulus (Pa)"], average_hist["Smooth_2"], color="red", label="Smooth_2")
    #plt.plot(average_hist["Young Modulus (Pa)"], average_hist["Q1"], color="green", label="Q1")
    #plt.plot(average_hist["Young Modulus (Pa)"], average_hist["Q3"], color="red", label="Q3")
    plt.legend(loc="best")
    plt.title(name+" "+mf)
    plt.xlabel("Young Modulus (Pa)")
    plt.ylabel("Frequency")
    plt.savefig(name+"_"+mf+".png")
    plt.clf()


