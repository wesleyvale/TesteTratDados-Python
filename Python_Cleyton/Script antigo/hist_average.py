import pandas as pd
import numpy as np
import re

def mf_hist(data_file, file_name, mf, media_hist, hist_mc_KO_Control, hist_mc_KO_ROCKi, hist_mc_KO_Ang, hist_mc_WT_Control, hist_mc_WT_ROCKi, hist_mc_WT_Ang, hist_ac_KO_Control, hist_ac_KO_ROCKi, hist_ac_KO_Ang, hist_ac_WT_Control, hist_ac_WT_ROCKi, hist_ac_WT_Ang):#, hist_Gel, hist_Outros):
    #Parâmetros
    YMlim1 = 150E3 #Young Modulus limite 1
    YMlim2 = 50E3 #Young Modulus limite 2

    z=data_file[data_file.maxforce==mf]
    freq, x = np.histogram(z.YM, bins=int(YMlim2/200), range=(0, YMlim2))
    #direcionar o dataframe_hist para um dataframe de sua categoria (amostra, ex: KO_Control) e concatenar estes dados em grupos comuns
    hist_mf = pd.DataFrame([x, freq]).transpose()
    hist_mf.columns = ['Young Modulus (Pa)', file_name]
    #hist_mf = pd.DataFrame([x, z.YM]).transpose()
    #hist_mf.columns = ['Young Modulus (Pa)', file_name]

    z = pd.DataFrame(hist_mf[file_name])
    YMmax = z.max()
    z = z*100/YMmax
    
    
    if re.search(r'manual_calib', file_name):
        if re.search(r'KO', file_name):
            if re.search(r'Control', file_name):
                #final_dir = 'Trat_Data/Manual_Calib/KO/Control/'
                hist_mc_KO_Control = pd.concat([hist_mc_KO_Control, z], axis=1)

                #print(hist_mc_KO_Control)

            elif re.search(r'ROCKi', file_name):
                #final_dir = 'Trat_Data/Manual_Calib/KO/ROCKi/'
                hist_mc_KO_ROCKi = pd.concat([hist_mc_KO_ROCKi, z], axis=1)
                #print(hist_mc_KO_ROCKi)

            elif re.search(r'Ang', file_name):
                #final_dir = 'Trat_Data/Manual_Calib/KO/Ang/'
                hist_mc_KO_Ang = pd.concat([hist_mc_KO_Ang, z], axis=1)
                #print(hist_mc_KO_Ang)

        elif re.search(r'WT', file_name):
            if re.search(r'Control', file_name):
                #final_dir = 'Trat_Data/Manual_Calib/WT/Control/'
                hist_mc_WT_Control = pd.concat([hist_mc_WT_Control, z], axis=1)
                #print(hist_mc_WT_Control)

            elif re.search(r'ROCKi', file_name):
                #final_dir = 'Trat_Data/Manual_Calib/WT/ROCKi/'
                hist_mc_WT_ROCKi = pd.concat([hist_mc_WT_ROCKi, z], axis=1)
                #print(hist_mc_WT_ROCKi)

            elif re.search(r'Ang', file_name):
                #final_dir = 'Trat_Data/Manual_Calib/WT/Ang/'
                hist_mc_WT_Ang = pd.concat([hist_mc_WT_Ang, z], axis=1)
                #print(hist_mc_WT_Ang)

    elif re.search(r'auto_calib', file_name):
        if re.search(r'KO', file_name):
            if re.search(r'Control', file_name):
                #final_dir = 'Trat_Data/Manual_Calib/KO/Control/'
                hist_ac_KO_Control = pd.concat([hist_ac_KO_Control, z], axis=1)
                #print(hist_ac_KO_Control)

            elif re.search(r'ROCKi', file_name):
                #final_dir = 'Trat_Data/Manual_Calib/KO/ROCKi/'
                hist_ac_KO_ROCKi = pd.concat([hist_ac_KO_ROCKi, z], axis=1)
                #print(hist_ac_KO_ROCKi)
                
            elif re.search(r'Ang', file_name):
                #final_dir = 'Trat_Data/Manual_Calib/KO/Ang/'
                hist_ac_KO_Ang = pd.concat([hist_ac_KO_Ang, z], axis=1)
                #print(hist_ac_KO_Ang)

        elif re.search(r'WT', file_name):
            if re.search(r'Control', file_name):
                #final_dir = 'Trat_Data/Manual_Calib/WT/Control/'
                hist_ac_WT_Control = pd.concat([hist_ac_WT_Control, z], axis=1)
                #print(hist_ac_WT_Control)

            elif re.search(r'ROCKi', file_name):
                #final_dir = 'Trat_Data/Manual_Calib/WT/ROCKi/'
                hist_ac_WT_ROCKi = pd.concat([hist_ac_WT_ROCKi, z], axis=1)
                #print(hist_ac_WT_ROCKi)

            elif re.search(r'Ang', file_name):
                #final_dir = 'Trat_Data/Manual_Calib/WT/Ang/'
                hist_ac_WT_Ang = pd.concat([hist_ac_WT_Ang, z], axis=1)
                #print(hist_ac_WT_Ang)
    #elif re.search(r'Gel', file_name):
        #final_dir = 'Trat_Data/Gel/'
    #    hist_Gel = pd.concat([hist_Gel, z], axis=1)

    #else:
        #final_dir = 'Outros/'
    #    hist_Outros = pd.concat([hist_Outros, z], axis=1)



    #media_hist = pd.concat([media_hist, z], axis=1)
    #print(hist_mc_KO_Control, hist_mc_KO_ROCKi, hist_mc_KO_Ang, hist_mc_WT_Control, hist_mc_WT_ROCKi, hist_mc_WT_Ang, hist_ac_KO_Control, hist_ac_KO_ROCKi, hist_ac_KO_Ang, hist_ac_WT_Control, hist_ac_WT_ROCKi, hist_ac_WT_Ang)
    #numpy.average(lista, axis=0)
    return hist_mf, z, hist_mc_KO_Control, hist_mc_KO_ROCKi, hist_mc_KO_Ang, hist_mc_WT_Control, hist_mc_WT_ROCKi, hist_mc_WT_Ang, hist_ac_KO_Control, hist_ac_KO_ROCKi, hist_ac_KO_Ang, hist_ac_WT_Control, hist_ac_WT_ROCKi, hist_ac_WT_Ang#, hist_Gel, hist_Outros
