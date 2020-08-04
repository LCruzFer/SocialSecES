import numpy as np 
import pandas as pd 
import os 

#exchange below to local path of project folder
wd_lc = "/Users/llccf/OneDrive/Dokumente/Hiwi_Jobs_Master/QuantEcon/Felix/Social Security Spain/"

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

def calc_missings(info_missing, data): 
    """
    Info_missing is a row of a df that contains the info on the NACIONAL value that is missing.
    data is the souce of the total data which is used to calculate the sum for nacional.
    """ 
    month = info_missing["month"]
    year = info_missing["year"]
    missing = data[["GENERAL", "year", "month"]].groupby(["year", "month"]).sum().reset_index()
    data[(data["GENERAL"] == "NACIONAL") & (data["year"] == year) & (data["month"] == month)] = missing[(missing["year"] == year) & (missing["month"] == month)] 
    data = data["GENERAL"]
    return(data)

def get_nacional(df):
    nacional = df[df["PROVINCIA"] == "NACIONAL"]
    nacional = nacional[["PROVINCIA", "GENERAL", "year", "month"]]
    missings = nacional["GENERAL"].isnull() 
    missings = nacional[missings]
    data = missings.apply(calc_missings)
    return(data)

#CREATE DATASET
#read in data to initialize columns 
data_init = pd.read_excel("src_data/" + os.listdir("src_data")[0], header = 1)
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
    data_total = data_total.append(data, ignore_index = True)
    print(year, month)
data_total.to_csv("out_data/all_data.csv")
#exchange GENERAL "<5" is substituted with 4 (for now, ask Laura what to do about it)
#data_total["GENERAL"][data_total["GENERAL"].apply(isinstance, args = [str])] = 4
truth = data_total["GENERAL"][data_total["PROVINCIA"] == "NACIONAL"].isnull() == True
truth = truth[truth == True]
truth_index = list(truth.index)
missings = data_total.loc[truth_index, ["GENERAL", "year", "month"]]
data_total.loc[truth_index, "GENERAL"] = missings.apply(calc_missings, args = [data_total])