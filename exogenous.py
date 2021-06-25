import eq_table as et
import os
import pandas as pd
import tkinter
from tkinter import filedialog
from math import ceil

root = tkinter.Tk()
root.withdraw() #use to hide tkinter window
def search_for_file_path(message = "Please select a file"):
    currdir = os.getcwd()
    tempdir = filedialog.askopenfilename(parent = root, initialdir = currdir, title = message, filetypes = (("Data files", ["*.csv*",]), ("All files", "*.*")))
    return tempdir

def  multipleResource(teamID, multiplier):
    roundData = search_for_file_path("讀取狀態")
    historicalData = search_for_file_path("讀取輸入資料")
    df_RD = pd.read_csv(roundData)
    df_HD = pd.read_csv(historicalData)
    currentRound = df_RD.loc[teamID-1]["Round"]
    log = None
    if os.path.isfile(f"Round{currentRound}\\{teamID}_exogenous.txt") == False:
        log = open(f"Round{currentRound}\\{teamID}_exogenous.txt","w")
    else:
        log = open(f"Round{currentRound}\\{teamID}_exogenous.txt","a")

    print(f"第{teamID}小隊 發動 {multiplier}倍資源卡...", file = log)

    originalFood = df_RD.loc[teamID-1]["food"]
    originalSi = df_RD.loc[teamID-1]["Si"]
    originalNi = df_RD.loc[teamID-1]["Ni"]
    originalRa = df_RD.loc[teamID-1]["Ra"]
    originalCo = df_RD.loc[teamID-1]["Co"]
    originalCr = df_RD.loc[teamID-1]["Cr"]
    originalScore = df_RD.loc[teamID-1]["score"]
    print(f"初始資源：[food, Si, Ni, Ra, Co, Cr] = [{originalFood}, {originalSi}, {originalNi}, {originalRa}, {originalCo}, {originalCr}]", file = log)
    print(f"初始分數：{originalScore}", file = log)

    df_RD.loc[teamID-1,["food"]] = originalFood * multiplier
    df_RD.loc[teamID-1,["Si"]] = originalSi * multiplier
    df_RD.loc[teamID-1,["Ni"]] = originalNi * multiplier
    df_RD.loc[teamID-1,["Ra"]] = originalRa * multiplier
    df_RD.loc[teamID-1,["Co"]] = originalCo * multiplier
    df_RD.loc[teamID-1,["Cr"]] = originalCr * multiplier
    df_RD.loc[teamID-1,["score"]] = newScore = et.compute_score(df_RD.iloc[teamID-1])

    newRes = [df_RD.loc[teamID-1][x] for x in et.legalContent]
    print(f"更新後資源：[food, Si, Ni, Ra, Co, Cr] = {newRes}", file = log)
    print(f"更新後分數：{newScore}\n ", file = log)

    df_RD.to_csv(roundData, sep= ",", index = False, encoding="utf_8_sig")

    df_HD.loc[currentRound - 1,["food"]] = df_HD.loc[currentRound - 1,["food"]] + originalFood * (multiplier - 1)
    df_HD.loc[currentRound - 1,["Si"]] = df_HD.loc[currentRound - 1,["Si"]] + originalSi * (multiplier - 1)
    df_HD.loc[currentRound - 1,["Ni"]] = df_HD.loc[currentRound - 1,["Ni"]] + originalNi * (multiplier - 1)
    df_HD.loc[currentRound - 1,["Ra"]] = df_HD.loc[currentRound - 1,["Ra"]] + originalRa * (multiplier - 1)
    df_HD.loc[currentRound - 1,["Co"]] = df_HD.loc[currentRound - 1,["Co"]] + originalCo * (multiplier - 1)
    df_HD.loc[currentRound - 1,["Cr"]] = df_HD.loc[currentRound - 1,["Cr"]] + originalCr * (multiplier - 1)

    df_HD.to_csv(historicalData, sep= ",", index = False, encoding="utf_8_sig")
    print(f"Team {teamID}\'s resource has been updated.")
    log.close()


def techUpgrade(teamID):
    roundData = search_for_file_path("讀取狀態")
    df_RD = pd.read_csv(roundData)
    currentRound = df_RD.loc[teamID-1]["Round"]
    log = None
    if os.path.isfile(f"Round{currentRound}\\{teamID}_exogenous.txt") == False:
        log = open(f"Round{currentRound}\\{teamID}_exogenous.txt","w")
    else:
        log = open(f"Round{currentRound}\\{teamID}_exogenous.txt","a")

    print(f"第{teamID}小隊 發動技術升級卡...", file = log)

    originalTech = df_RD.loc[teamID-1]["tech"]
    print(f"初始技術等級：{originalTech}", file = log)

    newTech = originalTech
    if newTech >= 10:
        print(f"技術已達上限", file = log)
        print(f"Team {teamID}\'s tech + 0.")
    else:
        newTech = originalTech + 1
        df_RD.loc[teamID-1,["tech"]] = newTech
        print(f"Team {teamID}\'s tech + 1.")
    
    print(f"更新後技術等級：{newTech}\n ", file = log)

    df_RD.to_csv(roundData, sep= ",", index = False, encoding="utf_8_sig")
    log.close()
    

def addMoney(teamList, toAddMoneyList):
    print(f"teamList = {teamList}")
    print(f"toAddMoneyList = {toAddMoneyList}")
    roundData = search_for_file_path("讀取狀態")
    df_RD = pd.read_csv(roundData)
    currentRound = df_RD.loc[0]["Round"]

    log = []
    for i in range(10):
        if os.path.isfile(f"Round{currentRound}\\{i+1}_exogenous.txt") == False:
            log.append(open(f"Round{currentRound}\\{i+1}_exogenous.txt","w"))
        
        else:
            log.append(open(f"Round{currentRound}\\{i+1}_exogenous.txt","a"))
            
    for i in range(len(teamList)):
        teamIndex = teamList[i] - 1
        toAddMoney = toAddMoneyList[i]
        print(f"第{teamIndex + 1}小隊 調整金錢...", file = log[teamIndex])
        originalMoney = df_RD.loc[teamIndex]["money"]
        originalScore = df_RD.loc[teamIndex]["score"]

        print(f"原有：{originalMoney}元；分數 = {originalScore}", file = log[teamIndex])

        df_RD.loc[teamIndex,["money"]] = newMoney =  originalMoney + toAddMoney
        df_RD.loc[teamIndex,["score"]] = newScore = et.compute_score(df_RD.iloc[teamIndex])
        print(f"獲得{toAddMoney}元", file = log[teamIndex])
        print(f"現有：{newMoney}元；分數 = {newScore}\n ", file = log[teamIndex])
    

    df_RD.to_csv(roundData, sep= ",", index = False, encoding="utf_8_sig")
    print("Money has been updated.")
    for i in log:
        i.close()

def actionDeductMoney(teamID, money):
    roundData = search_for_file_path("讀取狀態")
    df_RD = pd.read_csv(roundData)
    currentRound = df_RD.loc[teamID-1]["Round"]

    log = None
    if os.path.isfile(f"Round{currentRound}\\{teamID}_exogenous.txt") == False:
        log= open(f"Round{currentRound}\\{teamID}_exogenous.txt","w")
    else:
        log = open(f"Round{currentRound}\\{teamID}_exogenous.txt","a")
            
    print(f"第{teamID}小隊 競標成功...", file = log)
    originalMoney = df_RD.loc[teamID-1]["money"]
    originalScore = df_RD.loc[teamID-1]["score"]

    print(f"原有：{originalMoney}元；分數 = {originalScore}", file = log)
    df_RD.loc[teamID-1,["money"]] = newMoney =  originalMoney - money
    df_RD.loc[teamID-1,["score"]] = newScore = et.compute_score(df_RD.iloc[teamID-1])

    print(f"消費{money}元", file = log)
    print(f"現有：{newMoney}元；分數 = {newScore}\n ", file = log)
    
    df_RD.to_csv(roundData, sep= ",", index = False, encoding="utf_8_sig")
    print("Money has been updated.")
    log.close()

def addResource(teamID, **kwargs):
    for k,v in kwargs.items():
        if k not in et.legalContent:
            raise Exception("input error")

    
    roundData = search_for_file_path("讀取狀態")
    historicalData = search_for_file_path("讀取輸入資料")
    df_RD = pd.read_csv(roundData)
    df_HD = pd.read_csv(historicalData)
    currentRound = df_RD.loc[teamID-1]["Round"]
    log = None
    if os.path.isfile(f"Round{currentRound}\\{teamID}_exogenous.txt") == False:
        log = open(f"Round{currentRound}\\{teamID}_exogenous.txt","w")
    else:
        log = open(f"Round{currentRound}\\{teamID}_exogenous.txt","a")

    print(f"第{teamID}小隊 得到禮包資源...", file = log)
    print(f"內容物：", file = log)
    for k,v in kwargs.items():
        print(f"{k}：{v}個", file = log)
    

    originalFood = df_RD.loc[teamID-1]["food"]
    originalSi = df_RD.loc[teamID-1]["Si"]
    originalNi = df_RD.loc[teamID-1]["Ni"]
    originalRa = df_RD.loc[teamID-1]["Ra"]
    originalCo = df_RD.loc[teamID-1]["Co"]
    originalCr = df_RD.loc[teamID-1]["Cr"]
    originalScore = df_RD.loc[teamID-1]["score"]
    print(f"初始資源：[food, Si, Ni, Ra, Co, Cr] = [{originalFood}, {originalSi}, {originalNi}, {originalRa}, {originalCo}, {originalCr}]", file = log)
    print(f"初始分數：{originalScore}", file = log)

    for k,v in kwargs.items():
        df_RD.loc[teamID-1,[k]] = df_RD.loc[teamID-1][k] + v

    df_RD.loc[teamID-1,["score"]] = newScore = et.compute_score(df_RD.iloc[teamID-1])
    newRes = [df_RD.loc[teamID-1][x] for x in et.legalContent]
    print(f"更新後資源：[food, Si, Ni, Ra, Co, Cr] = {newRes}", file = log)
    print(f"更新後分數：{newScore}\n ", file = log)

    df_RD.to_csv(roundData, sep= ",", index = False, encoding="utf_8_sig")

    for k,v in kwargs.items():
        df_HD.loc[currentRound-1,[k]] = df_RD.loc[currentRound-1][k] + v

    df_HD.to_csv(historicalData, sep= ",", index = False, encoding="utf_8_sig")
    print(f"Team {teamID}\'s resource has been updated.")
    log.close()

def starvation(sr):
    """
    if availPopulation of a team is less than 15% * maxPopulation\n
    adjust to 15% 
    """
    currentRound = sr["Round"]   
    teamID = sr["ID"] 
    log = None
    if os.path.isfile(f"Round{currentRound}\\{teamID}_exogenous.txt") == False:
        log= open(f"Round{currentRound}\\{teamID}_exogenous.txt","w")
    else:
        log = open(f"Round{currentRound}\\{teamID}_exogenous.txt","a")
    
    originalAvlpopu = sr["available_popu"]
    maxpopu = sr["max_popu"]

    print(f"第{teamID}小隊 快餓死...", file = log)
    print(f"次回合可用人口：{originalAvlpopu} < 次回合人口上限的15%：{maxpopu * 0.15}", file = log)

    sr["available_popu"] = newAvlpopu = ceil(maxpopu * 0.15)
    print(f"調整次回合可用人口至：{newAvlpopu}，請加加油^_^...", file = log)
    log.close()
    return sr

def addPopulation(teamID, population):
    roundData = search_for_file_path("讀取狀態")
    df_RD = pd.read_csv(roundData)
    currentRound = df_RD.loc[teamID-1]["Round"]
    log = None
    if os.path.isfile(f"Round{currentRound}\\{teamID}_exogenous.txt") == False:
        log = open(f"Round{currentRound}\\{teamID}_exogenous.txt","w")
    else:
        log = open(f"Round{currentRound}\\{teamID}_exogenous.txt","a")

    print(f"第{teamID}小隊 發動人口增加卡...", file = log)

    originalMaxPopu = df_RD.loc[teamID-1]["max_popu"]
    originalAvlPopu = df_RD.loc[teamID-1]["available_popu"]
    print(f"初始人口上限：{originalMaxPopu}\n初始可用人口：{originalAvlPopu}", file = log)

    newMaxPopu = originalMaxPopu + population
    newAvlPopu = originalAvlPopu + population
    
    df_RD.loc[teamID-1,["max_popu"]] = newMaxPopu
    df_RD.loc[teamID-1,["available_popu"]] = newAvlPopu
    print(f"Team {teamID}\'s population has been updated.")

    print(f"更新後人口上限：{newMaxPopu}\n更新後可用人口：{newAvlPopu}\n ", file = log)

    df_RD.to_csv(roundData, sep= ",", index = False, encoding="utf_8_sig")
    log.close()


