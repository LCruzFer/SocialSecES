import numpy as np 
import pandas as pd 
import os 


"""
this file creates two CSVs -> see README
average is constructed for column "GENERAL"
if interested in other values, replace "GENERAL" with column name of interest 
exchange below to local path of project folder
"""
wd = "Path to yoour project folder"
os.chdir(wd) 


#functions 
def get_date(string): 
    """
    Get date from a filename of format "AfiliadosMuni-01-2003"
    """
    month = string[-7:-5]
    if int(month[0]) == 0: 
        month = int(month[1])
    else: 
        month = int(month)
    year = int(string[-4:])
    return(year, month)


def get_muni_code(df_muni): 
    """
    df_muni is df element which contains names of municipio and code
    """
    code = []
    df_muni = df_muni[df_muni.isnull() == False]
    df_muni = df_muni[df_muni != "SIN DISTRIBUCIÓN (*)"]
    for x in df_muni.tolist():
        code.append(int(x.split()[0]))
    return(code)

#CREATE DATASET
#read in data to initialize columns 
#code below that is turned to comment must be run once to save a csv 
#including all data, afterwards can be turned back to comment 
"""

#CREATE DATASET
#read in data to initialize columns 

data_init = pd.reader_excel("src_data/" + os.listdir("src_data")[0], header = 1)
#get columns
columns = list(data_init.columns)
#append a year and month column
columns.append("year")
columns.append("month")
#intiliaze empty df with columns
data_total = pd.DataFrame(columns = columns)
#only add files to file list that are .xlsx (otherwise invisible files might be added, eg. .DS_Store)
file_list = [f for f in os.listdir("src_data") if f.endswith(".xlsx")]
#loop over all 
for file in file_list:
    data = pd.read_excel("src_data/" + file, header = 1)
    file = file[:-5]
    year, month = get_date(file)
    data["year"] = year
    data["month"] = month 
    if "Reg. General(1)" in list(data.columns):
        data = data.rename(columns = {"Reg. General(1)": "GENERAL"})
    data_total = data_total.append(data, ignore_index = True)
    print(year, month)
#write total df to csv such that processing all files is not necessary 
data_total.to_csv("out_data/all_data.csv")
"""

data_total = pd.read_csv("out_data/all_data.csv")
#exchange GENERAL "<5" is substituted with 4 (for now, ask Laura what to do about it)
data_total["GENERAL"][data_total["GENERAL"] == "<5"] = np.nan
data_total["GENERAL"] = data_total["GENERAL"].astype(float)


#CREATE PANEL 
#create dataset for municipios of interest (data_moi) 
# or all municipios


#only keep columns of interest (interested in "GENERAL")
data_reduc = data_total[["PROVINCIA", "MUNICIPIO", "GENERAL", "year", "month"]]
#drop obs where Municipio is missing
data_reduc = data_reduc[data_reduc["MUNICIPIO"].isnull() == False]
#drop where no municipio available
data_reduc = data_reduc[data_reduc["MUNICIPIO"] != "SIN DISTRIBUCIÓN (*)"]
#drop provincial total level 
data_reduc = data_reduc[data_reduc["MUNICIPIO"] != "PROVINCIAL"]

data_reduc["MUNI_CODE"] = get_muni_code(data_reduc["MUNICIPIO"])

"""
UNCOMMENT BELOW ONLY WHEN FILE TO FILTER MUNICIPIOS EXISTS
#get municipios of interest using list from muni 
#read in municipios
#file below is a list of pre-defined municipios of interest 
#if non available, then ignore 
muni = pd.read_stata("src_data/samplemunis_pollution.dta")
data_moi = data_reduc.merge(muni, left_on = "MUNI_CODE", right_on = "municipality", how = "inner")
#keep Municipio code as identifier
data_moi = data_moi.drop(["municipality", "MUNICIPIO"], axis = 1)
"""

#average by municipilaity and year
averages = data_moi.groupby(["MUNI_CODE", "year"]).mean().reset_index().drop("month", axis = 1)
averages.to_csv("out_data/averages_muni.csv")

#create dataset for NACIONAL
data_nacional = data_total[data_total["PROVINCIA"] == "NACIONAL"]
data_nacional = data_nacional[["PROVINCIA", "GENERAL", "year", "month"]]
averages_nacional = data_nacional.groupby(["year"]).mean().reset_index().drop("month", axis = 1)
averages_nacional.to_csv("out_data/averages_nacional.csv")

