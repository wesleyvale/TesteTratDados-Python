import pandas as pd
import os
import re

# Abrir os arquivos
# main_folder = 'C:\\Users\\cleyt\\Desktop\\Tratamento Python\\Untitled Folder\\Visual Code'
main_folder = 'C:\\Users\\cleyt\\Desktop\\JPK Dados\\INCor\\Originais'

def sep_col_YMR(root):

    df = pd.read_csv(root, sep='\t', index_col='Position Index')

    if not len(df.T)==150:
        print(len(df.T))
        print("Este arquivo não é compatível com o programa:" + root)
        return

    #Separar as colunas de interesse
    #datafilter = df.iloc[0:, [11, 20, 27, 34, 41, 48, 55, 62, 69, 76, 83, 26, 33, 40, 47, 54, 61, 68, 75, 82, 89]]
    datafilter = df.iloc[0:, [11, 20, 26, 27, 33, 34, 40, 41, 47, 48, 54, 55, 61, 62, 68, 69, 75, 76, 82, 83, 89]]
    #rt = ["Height_ref_5%", "YM_MaxF_0100pN", "YM_MaxF_0200pN", "YM_MaxF_0300pN", "YM_MaxF_0400pN", "YM_MaxF_0500pN", "YM_MaxF_0600pN", "YM_MaxF_0800pN", "YM_MaxF_1000pN", "YM_MaxF_1200pN", "YM_MaxF_1500pN", "Rrms_MaxF_0100pN", "Rrms_MaxF_0200pN", "Rrms_MaxF_0300pN", "Rrms_MaxF_0400pN", "Rrms_MaxF_0500pN", "Rrms_MaxF_0600pN", "Rrms_MaxF_0800pN", "Rrms_MaxF_1000pN", "Rrms_MaxF_1200pN", "Rrms_MaxF_1500pN"]
    rt = ["Height_ref_5%", "YM_MaxF_0100pN", "Rrms_MaxF_0100pN", "YM_MaxF_0200pN", "Rrms_MaxF_0200pN", "YM_MaxF_0300pN", "Rrms_MaxF_0300pN", "YM_MaxF_0400pN", "Rrms_MaxF_0400pN", "YM_MaxF_0500pN", "Rrms_MaxF_0500pN", "YM_MaxF_0600pN", "Rrms_MaxF_0600pN", "YM_MaxF_0800pN", "Rrms_MaxF_0800pN", "YM_MaxF_1000pN", "Rrms_MaxF_1000pN", "YM_MaxF_1200pN", "Rrms_MaxF_1200pN", "YM_MaxF_1500pN", "Rrms_MaxF_1500pN"]
    datafilter.columns=rt

    #print('Foram separadas as colunas')

    #Reconstrução do nome
    old_name = root.split(sep='\\')
    #print(old_name)
    sample_name = old_name[-5].split(sep='_')
    new_name = sample_name[1] + '_' + old_name[-4] + '_' + sample_name[0] + '_' + old_name[-6] + '_' + old_name[-3]
    if re.search(r'-1\.tsv', root):
        new_name = new_name + "_manual_calib"
        #print(new_name)
    else:
        new_name = new_name + "_auto_calib"
    #print(new_name)

    #Como verificar se o diretório já existe e criar um novo + index?
    if re.search(r'manual_calib', new_name):
        if re.search(r'KO', new_name):
            final_dir = 'Trat_Data\\Manual_Calib\\KO\\'
        elif re.search(r'WT', new_name):
            final_dir = 'Trat_Data\\Manual_Calib\\WT\\'
    elif re.search(r'auto_calib', new_name):
        if re.search(r'KO', new_name):
            final_dir = 'Trat_Data\\Auto_Calib\\KO\\'
        elif re.search(r'WT', new_name):
            final_dir = 'Trat_Data\\Auto_Calib\\WT\\'
    #print(final_dir+'dataYM\\'+new_name+'_dataYM.tsv')

    #Exportando como arquivo tsv
    pathfilter = final_dir+'datafilter\\'+new_name+'_datafilter.tsv'
    datafilter.to_csv(pathfilter, sep='\t')

    print('Foram criados os arquivos separados: '+new_name)

for roots, dirs, files in os.walk(main_folder):
    for file in files:
        if not re.search(r'\.tsv', file):
            continue
        elif re.search(r'Trat_Data', roots):
            continue
        root = u"\\\\?\\" + os.path.join(roots, file)
        #print(root)
        sep_col_YMR(root)

print("Fim! (=")