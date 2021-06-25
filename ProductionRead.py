import pygsheets
import pandas as pd
import os
import tkinter
from tkinter import filedialog

def save():
    currdir = os.getcwd()
    tempdir = filedialog.asksaveasfilename(initialdir = currdir, initialfile = "生產組合", title = "",defaultextension='.txt', filetypes= (("csv files", ".csv"), ("All files", "*.*")))
    return tempdir

gc = pygsheets.authorize(service_account_file = "econcamp.json")

survey_url = 'https://docs.google.com/spreadsheets/d/1nKHlDQdWWImRnbrCdhs0Kt2iGXUgmDOhHnAbb7FxbGQ'
sh = gc.open_by_url(survey_url).sheet1
df = pd.DataFrame(sh.get_all_values())
df = df.iloc(1)[1:10]
start = 1

while(True):
    if df.iloc[start][1] == "":
        start += 1
    else:
        break
df = df.iloc[start:start+10]
df = df.rename(columns={1: "ID", 2: "labor_on_food",3: "labor_on_Si", 4:"labor_on_Ni", 5: "labor_on_Ra", 6: "labor_on_Co", 7: "labor_on_Cr", 8: "upgrade_input", 9:"production_set"})
df.index = [0,1,2,3,4,5,6,7,8,9]

root = tkinter.Tk()
root.withdraw() #use to hide tkinter window
df.to_csv(save(), sep= ",", index = False, encoding="utf_8_sig")


