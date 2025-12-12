import os
import pandas as pd
import numpy as np
from time import time
from datetime import timedelta, datetime
from io import StringIO
from types import CoroutineType
from openpyxl import workbook
import multiprocessing as mp
import Ex_Zeus_Logs as ED
import Ex_Zeus_Defs as ECA
import networkx 
from networkx.algorithms.components.connected import connected_components 
from networkx.algorithms.centrality.current_flow_betweenness import edge_current_flow_betweenness_centrality
import csv
from tqdm import tqdm
import warnings
import shutil



warnings.filterwarnings('ignore')
maxInt =  500000
csv.field_size_limit(2147483647)

folder_path = r"\\LonNTXshare.integreon.com\ProjectNottinghamRehab\Ranjeet\Development\1266_LoadFiles\csv"
for file in os.listdir(folder_path):
    Datapath_In = (os.path.join(folder_path, file))+"\\\\"
    Datapath_Out = os.path.join(Datapath_In,"Output\\\\")



    NbProcesses_int = 1
    only_tables_bool = False 



    if not os.path.exists(Datapath_In):
        print("File Location Error")
    if not os.path.exists(Datapath_Out):
        os.makedirs(Datapath_Out)
    if not os.path.exists(Datapath_Out):
        os.makedirs(Datapath_Out)



    tstart_time = time()
    tstart2_time = time() 



    def printelaps():
        global tstart_time
        global tstart2_time
        print( "Duration: " + str(timedelta(seconds=(time() - tstart_time))).split('.')[0] + " | Difference: " + str(timedelta(seconds=(time() - tstart2_time))).split('.')[0] ); tstart2_time = time()



    def printelaps2():
        global tstart_time
        global tstart2_time
        print ( "Duration: " + str(timedelta(seconds=(time() - tstart_time))).split('.')[0] + " | Difference: " + str(timedelta(seconds=(time() - tstart2_time))).split('.')[0] ); tstart2_time = time()



    def analyze_files_func(dataworker):
        Datapath_Out = dataworker["datapathOut"]
        Datapath_Out = dataworker["StatFile"]
        NbProcesses_int = dataworker["ProcessNo"]
        print("Process: " + str(NbProcesses_int) + " | Files: " + str(len(dataworker["FilesIn"])))
        filecnt_int = 0
        fileprintcnt_int = 100
        stat_dict = {}
        with open(Datapath_Out + "Basket_Set_"+ NbProcesses_int +".dat",'w') as file:
            file.write("\xfeGroupNo\xfe\x14\xfeTable_Columns\xfe\n")
        for filename in tqdm(dataworker["FilesIn"]):
            filecnt_int +=1
            processed_file = False
            #if filecnt_int % fileprintcnt_int = 0: print(filecnt_int)
            curfilename = str(filename[filename.rfind('\\')+1:filename.rfind(".",filename.rfind('\\')+1)])
            filename_value = str(curfilename)
            fileext_value = str(filename[filename.rfind('.')+1:])
            try:
                if fileext_value.lower() in ['xls','xlsx','xlsm','xlsb']:
                        temp_stat_dict = ECA.eca_excel_funct(filename,Datapath_Out,NbProcesses_int)
                        processed_file = True
                elif fileext_value.lower() in ['csv','tsv','txt']:
                        temp_stat_dict = ECA.eca_delimited_file_func(filename,Datapath_Out,NbProcesses_int)
                        processed_file = True
                elif only_tables_bool == False:
                        temp_stat_dict = ECA.eca_text_func(filename,Datapath_Out,NbProcesses_int)
                        processed_file = True
            except Exception as e:
                temp_stat_dict = {
                "FileName": filename_value
                ,"Extension": fileext_value
                ,"Sheet Name": np.nan
                ,"First Row Columns": np.nan
                ,"Table Columns": np.nan
                ,"Table Columns Mapping": np.nan
                ,"Key Columns": np.nan
                ,"Table Number of Rows": np.nan
                ,"Total Number of Columns": np.nan
                ,"Total Number of Rows": np.nan
                ,"Processing Notes": str(e)
                ,"Table Group": np.nan
                ,"Name Identifier": np.nan
                ,"Name Count": np.nan
                ,"Address Identifier": np.nan
                ,"Address Count": np.nan
                ,"DOB Identifier": np.nan
                ,"DOB Count": np.nan
                ,"SSN Identifier": np.nan
                ,"SSN Count": np.nan
                ,"TIN Identifier": np.nan
                ,"TIN Count": np.nan
                ,"Phone Number Identifier": np.nan
                ,"Phone Count": np.nan
                ,"Driver's License Identifier": np.nan
                ,"Driver's License Count": np.nan
                                    }
                print(filename,str(e))


            if processed_file == True:
                if len(stat_dict) == 0:
                        for k,v in temp_stat_dict.items():
                            stat_dict[k] = v
                else:
                        for k,v in temp_stat_dict.items():
                            for n in v:
                                stat_dict[k].append(n)
        return stat_dict



    def to_graph(l):
        G = networkx.Graph()
        for part in l:
           
            G.add_nodes_from(part)
           
            G.add_edges_from(to_edges(part))
        return G



    def to_edges(l):
        
        
        it = iter(l)
        last = next(it)

        for current in it:
            yield last, current
            last = current  



    if __name__ == "__main__":
        printelaps()
        starttime_str = str(datetime.now())
        pool = mp.Pool(NbProcesses_int)

        runn_all_files_bool = True
        files_to_do_list = []
        if runn_all_files_bool == False:
            with open(r'L:\Intrasite\iDAT - Team\Akshat\Excel_Extracted_Sets\ex_zeus\Cache_ECA_POC.txt\\','r') as file:
                for line in file:
                        files_to_do_list.append(line.strip('\n').lower())

        if not os.path.exists(Datapath_In):
            print("File Location Error")
            exit()
        if not os.path.exists(Datapath_Out):
            os.makedirs(Datapath_Out)
        if not os.path.exists(Datapath_Out):
            os.makedirs(Datapath_Out)
        filelist_dict = {} 
        
        for i in range(NbProcesses_int):
            filelist_dict[i] = []
        i = 0

        if NbProcesses_int > 1:
            print("Processing ...")
            total_bytes_int = 0
            for root, subdirs, files in os.walk(Datapath_In):
                for filename in files:
                        if (filename.lower() in files_to_do_list) or (runn_all_files_bool == True):
                            total_bytes_int += os.path.getsize(os.path.join(root, filename))
            total_bytes_ratio_int = total_bytes_int / NbProcesses_int
            print("Total bytes: ",total_bytes_int)
            print("Total bytes per process: ",total_bytes_ratio_int)
            current_bytes_int = 0
            for root, subdirs, files in os.walk(Datapath_In):
                for filename in files:
                        if (filename.lower() in files_to_do_list) or (runn_all_files_bool == True):
                            filelist_dict[i].append(os.path.join(root, filename))
                            current_bytes_int += os.path.getsize(os.path.join(root, filename))
                            if current_bytes_int > total_bytes_ratio_int and i < NbProcesses_int:
                                current_bytes_int = 0
                                i += 1
        else:
            for root, subdirs, files in os.walk(Datapath_In):
                for filename in files:
                        if (filename[0:filename.rfind(".")].lower() in files_to_do_list) or (runn_all_files_bool == True):
                            filelist_dict[i].append(os.path.join(root, filename))
                            i +=1
                            if i > NbProcesses_int-1:
                                i = 0
        dataworker = []       
        for i in range(NbProcesses_int):
            dataworker.append( {
                "FilesIn": filelist_dict[i],
                "datapathOut": Datapath_Out,
                "StatFile": Datapath_Out,
                "ProcessNo": str(i+1),
                    })

        sd = pool.map(analyze_files_func,dataworker)

        fullstat_dict = {}
        for s in sd:
            for k,v in s.items():
                if k in fullstat_dict.keys():
                        fullstat_dict[k] += v
                else:
                        fullstat_dict[k] = v

        
        df = pd.DataFrame.from_dict(fullstat_dict,orient='columns')
        groupno_dict = {}
        groupno_matching_dict = {}

        print("Creating Baskets ...")
        for i in range(1,NbProcesses_int+1):
            with open(Datapath_Out + "Basket_Set_"+ str(i) +".dat",'r') as file:
                file_opened_bool = False
                while file_opened_bool == False:
                        try:
                            csv.field_size_limit(maxInt)
                            r = csv.reader(file, delimiter='\x14', quotechar='\xfe')
                            file_opened_bool = True
                        except:
                            maxInt = int(maxInt/10)
                lncnt_int = 1
                for line in r:
                        if lncnt_int == 1:lncnt_int +=1;continue
                        lncnt_int +=1
                        if len(groupno_dict) == 0:
                            groupno_dict[line[0]] = line[1]
                            groupno_matching_dict[line[0]] = [line[0]]
                        else:
                            if not line[1] in groupno_dict.values():
                                groupno_dict[line[0]] = line[1]
                                groupno_matching_dict[line[0]] = [line[0]]
                            else:
                                for k,v in groupno_dict.items():
                                    if v == line[1]:
                                            groupno_matching_dict[k] += [line[0]]
                                            break
            os.remove(Datapath_Out + "Basket_Set_"+ str(i) +".dat")
        
        if not os.path.exists(Datapath_Out + "Baskets_Extracted"):
            os.makedirs(Datapath_Out + "Baskets_Extracted")
        started_groups_list = []

        with open(Datapath_Out + "All_Basket_Cols.dat",'w+') as file:
            file.write("\xfeGroupNo\xfe\x14\xfeTable_Columns\xfe\n")
            for key, value in groupno_dict.items():
                file.write("\xfe" + key + "\xfe\x14\xfe" + value + "\xfe\n")
       
        
        print("Moving Baskets ...")
       
        for stackedfile in os.listdir(Datapath_Out):
            if stackedfile.find("Basket_Number") > -1:
                if stackedfile.find("Basket_Number") > -1:
                    if NbProcesses_int > 1:
                        print("Combining Baskets ...")
                        curfilegroup = str(stackedfile[stackedfile.rfind('_')+1:stackedfile.rfind(".",stackedfile.rfind('_')+1)])
                        for key, value in groupno_matching_dict.items():
                                if curfilegroup in value:
                                    if key in started_groups_list:
                                        concat_df = pd.read_csv(Datapath_Out + stackedfile,delimiter=',', dtype=str, keep_default_na=False, skipinitialspace=True,encoding='utf-8')
                                        with open(Datapath_Out + "Baskets_Extracted\\" + "Basket_Number" + "_" + str(key) + ".csv", 'a+', newline ='\n',encoding='utf-16') as file:
                                            concat_df.to_csv(file,index=False,header=False,encoding='utf-16',quoting=csv.QUOTE_ALL)
                                        os.remove(Datapath_Out + stackedfile)
                                    else:
                                        concat_df = pd.read_csv(Datapath_Out + stackedfile,delimiter=',', dtype=str, keep_default_na=False, skipinitialspace=True,encoding='utf-8-sig')
                                        concat_df.to_csv(Datapath_Out + "Baskets_Extracted\\" + "Basket_Number" + "_" + str(key) + ".csv",header=True,index=False,quoting=csv.QUOTE_ALL,encoding='utf-16')
                                        os.remove(Datapath_Out + stackedfile)
                                        started_groups_list.append(key)
                                    break
                    else:
        
                        shutil.move(Datapath_Out + stackedfile, Datapath_Out + "Baskets_Extracted\\" + stackedfile)
       
        print("Processing to file")
       
        for index, row in df.iterrows():
            if row['Table Columns Mapping'] in groupno_dict.values():
                for k,v in groupno_dict.items():
                        if v == row['Table Columns Mapping']:
                            df.at[index,'Table Group'] = k
        groupcnt_col_int = df.columns.get_loc("Table Group") + 1
        df.insert(groupcnt_col_int,"Group Count",'')
        df["Group Count"] = df.groupby('Table Group')['Table Group'].transform('count')

        
        tempdf = df[['Table Group','FileName']].copy()
        tempdf['Table Group'] = tempdf['Table Group'].replace('',np.nan)
        tempdf = tempdf.dropna()
        tempdf = tempdf[tempdf['Table Group'] != ""]
        if len(tempdf) > 0:
            tempdf = tempdf.groupby(['Table Group'])['FileName'].agg(';'.join).reset_index()
            tempdf['INTT_index'] = tempdf['FileName'].apply(lambda x: x.split(';'))
            masterlist = tempdf['INTT_index'].tolist()
            tempdf2 = pd.DataFrame(columns = ['INTT_explode','INTT_index'])
            tempdf2['INTT_explode'] = masterlist
            tempdf2['INTT_explode'] = tempdf2['INTT_explode'].apply(lambda x: set(x))
            sets = tempdf2['INTT_explode'].tolist()
            G = to_graph(sets)
            sets = (list(connected_components(G)))

            df.insert(groupcnt_col_int+1,"WorkFlow Groups",'')
            df.insert(groupcnt_col_int+2,"WorkFlow Group Count",'')
            df.insert(groupcnt_col_int+3,"Files Represnted in Workflow Group",'')
            grpno = 1
            grouping_dict = {}
            for s in sets:
                for i in s:
                        if not i in grouping_dict.keys():
                            cntrl_list = df[df['FileName'] == i].index.tolist()
                            for x in cntrl_list:
                                df.at[x,'WorkFlow Groups'] = grpno
                            grouping_dict[i] = grpno
                grpno +=1
            df["WorkFlow Group Count"] = df.groupby('WorkFlow Groups')['WorkFlow Groups'].transform('count')
            filecount_dict = df.groupby('WorkFlow Groups')['FileName'].apply(list).to_dict()
            df["Files Represnted in Workflow Group"] = df["WorkFlow Groups"].apply(lambda x: len(set(filecount_dict[x])))

            del tempdf2
        del tempdf
        
        df.sort_values(['WorkFlow Groups','Table Group','FileName'], ascending=[True,True,True], inplace=True)
        df.to_excel(Datapath_Out+"!Header_Analysis.xlsx",sheet_name="Header_Analysis",header=True,index=False)
        df=pd.read_excel(Datapath_Out+"!Header_Analysis.xlsx", dtype=str)
        df=df.rename(columns={'FileName':'Doc_ID','Extension':'File_Extension','Sheet Name':'Sheet_Name','Table Columns Mapping':'Columns_Combined','Key Columns':'Columns_Identified','Total Number of Columns':'Column_Count','Total Number of Rows':'Row_Count','Processing Notes':'Comments','Table Group':'Basket_Number'})
        df=df.drop(['Group Count', 'WorkFlow Groups', 'WorkFlow Group Count', 'Files Represnted in Workflow Group', 'First Row Columns', 'Table Columns', 'Table Number of Rows', 'Name Identifier', 'Name Count', 'Address Identifier', 'Address Count', 'DOB Identifier', 'DOB Count', 'SSN Identifier', 'SSN Count', 'TIN Identifier', 'TIN Count', 'Phone Number Identifier', 'Phone Count', "Driver's License Identifier", "Driver's License Count"], axis=1)
        df.to_excel(Datapath_Out+"!Header_Analysis.xlsx",sheet_name="Header_Analysis",header=True,index=False)\
        

        os.remove(Datapath_Out+"ConCat_Columns.csv")
        os.remove(Datapath_Out+"All_Basket_Cols.dat")
       
        print (" Start Time:  " + starttime_str + "   |  End Time:  " + str(datetime.now()))
        printelaps2()