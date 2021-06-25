import math
import pandas as pd
advantageRatio = 1.5
populationGrowthRate = 1.35
legalContent = ["food", "Si", "Ni", "Ra", "Co", "Cr"]


def rounding(numlist):
    r = [round(n) for n in numlist]
    return r

def elementProduction(A, tech, labor):
    Y = A * math.log(10*tech**2+2)*6*labor**0.6
    return Y


foodProduction = lambda labor: labor*5

def cumulativeDamage(df):
    """
    df : \n
    a dataframe containing cumulative production for each team\n
    format: 5 columns(elements) x 10 rows(teams) \n
    return a list containing "cumulative damage for each team"
    """
    cumulativeDamList = [] #storing cumulative damage for each team

    for i in range(10):
        s = list(df.iloc[i])   # series of elements for team i
        dam = list(map(lambda element: 10000*1.01**(element/100)-10000, s)) #compute the damage
        cumulativeDamList.append(sum(dam))
    
    return rounding(cumulativeDamList)

upgradeRequired = [[0,0],
                   [100, 30],
                   [225, 50],
                   [400, 80],
                   [625, 120],
                   [900, 170],
                   [1225, 230],
                   [1600, 300],
                   [2025, 380],
                   [2500, 470],
                   [3025, 570]]

cumUpgradeRequired = [[0,0], 
                      [100, 30],
                      [325,	80],
                      [725,	160],
                      [1350, 280],
                      [2250, 450],
                      [3475, 680],
                      [5075, 980],
                      [7100, 1360],
                      [9600, 1830],
                      [12625, 2400]]


def upgrade(currentLevel, inputResources, remain_avl_popu, inventory, cumData = cumUpgradeRequired):
    """
    inputResources: a list of int, length = 5, containing the resources & labors wants to input 
    invertory: a list containing the inventory imformation of this teams
    return a tuple containing:\n
    \t(how many resources should be used,
    \t how many labors should be used, 
    \t the tech level the team achieves)
    """
    remain_avl_popu_backup = remain_avl_popu
   
    if inputResources == [0]:
        return ([0, 0, 0, 0, 0], 0, currentLevel)

    for i in range(5):
        if inputResources[i] > inventory[i]:
            inputResources[i] = inventory[i]

    if sum(inputResources) == 0:
        return ([0, 0, 0, 0, 0], 0, currentLevel)
    
    remain_resources = sum(inputResources)
    RatioOfInput = [int(i)/remain_resources for i in inputResources]
    toLevel = currentLevel
    
    while (remain_resources >= cumData[toLevel+1][0] - cumData[toLevel][0]) and (remain_avl_popu_backup >= cumData[toLevel+1][1] - cumData[toLevel][1]) and (toLevel <= 10):
        remain_resources -= (cumData[toLevel+1][0] - cumData[toLevel][0])
        remain_avl_popu_backup -= (cumData[toLevel+1][1] - cumData[toLevel][1])
        toLevel += 1
    
    to_deduct_resources = [i*(cumData[toLevel][0] - cumData[currentLevel][0]) for i in RatioOfInput]
    to_deduct_population = cumData[toLevel][1] - cumData[currentLevel][1]
    return (to_deduct_resources, to_deduct_population , toLevel)


advantageForTeam = [["Si", "Ni"],
                    ["Ra", "Co"], 
                    ["Cr", "Si"], 
                    ["Ni", "Ra"], 
                    ["Co", "Cr"], 
                    ["Si", "Ni"], 
                    ["Ra", "Co"], 
                    ["Cr", "Si"], 
                    ["Ni", "Ra"], 
                    ["Co", "Cr"]]

spaceshipRequired = [[0 ,0, 0, 0, 0],
             [300, 300, 0, 0, 0], 
             [300, 0, 300, 0, 0],
             [0, 300, 0, 300, 0],
             [0, 0, 300, 0, 300],
             [500, 0, 0, 500, 500],
             [0, 500, 0, 500, 500],
             [0, 0, 500, 500, 500],
             [700, 700, 700, 700, 0],
             [700, 700, 700, 0, 700],
             [1200, 1200, 1200, 1200, 1200]]

spaceshipScore = [8100, 8100, 8100, 8100, 25000, 25000, 25000, 50400, 50400, 150000]
"""
spaceship = ["",
             AB,
             AC,
             BD,
             CE,
             ADE,
             BDE,
             CDE,
             ABCD,
             ABCE,
             ABCDE]
"""
def build_spaceship(demandList, remain_avl_popu, series, spaceshipRequired = spaceshipRequired):
    """
    demandList: a list of int, containing the index of the spaceship that you want to build\n
    series: a pandas.core.series.Series containing the imformation of this teams\n
    return a tuple containing:\n
    \t(how many resources should be used,
    \t how many labors should be used),
    \t a list of spaceships has been built)
    """
    def populationRequired(index):
        if index == 10:
            return 200
        elif 9 >= index >= 8 :
            return 150
        elif 7 >= index >= 5:
            return 100
        elif 4 >= index >= 1:
            return 50
        else:
            return 0
    remain_avl_popuBackup = remain_avl_popu
    
    canBuildSpaceships = [0]*11
    inventory = list(series[6:11])
    inventoryBackup = list(series[6:11])
    for i in reversed(demandList):
        acceptDemand = True
        for j in range(5):
            if spaceshipRequired[i][j] > inventory[j]:
                acceptDemand = False
        if populationRequired(i) > remain_avl_popu:
            acceptDemand = False
        
        if acceptDemand:
            canBuildSpaceships[i] += 1
            for j in range(5):
                inventory[j] -= spaceshipRequired[i][j]
            remain_avl_popu -= populationRequired(i)
    
    to_deduct_resources = [ (inventoryBackup[i]- inventory[i]) for i in range(5) ]
    return (to_deduct_resources, remain_avl_popuBackup - remain_avl_popu, canBuildSpaceships[1:11])


def compute_score(series):
    sumOfShipScore = 0
    product = series[18:28]
    for i in range(10):  # 10種產品
        sumOfShipScore += product[i] * spaceshipScore[i]
    return ( series["money"] + series["food"] + sum(series[6:11]) + sumOfShipScore - series["hurt"] )



def inventroyPrice(df):
    def price_to_proportion(proportion):
      #  p =  ( 20 - (225*(1-(1-proportion)**2))**0.5 )
        p = 2.7/proportion
        return p
    inventory = df.iloc(1)[6:11]
    AdjustedSumList = [sum(df["food"])+1] + [sum(inventory.iloc(1)[i])+1 for i in range(5)]
    inventoryRatio = [i/sum(AdjustedSumList) for i in AdjustedSumList]
    price = [price_to_proportion(i) for i in inventoryRatio] 
    return price

def modifyTradeInput(df):
    df = df.drop(df.columns[0],axis = 1) # remove timeTag
    df = df.rename(columns={df.columns[0]:"ID", df.columns[1]: "netBuyFood",df.columns[2]:"netBuySi", df.columns[3]:"netBuyNi", df.columns[4]:"netBuyRa", df.columns[5]:"netBuyCo", df.columns[6]:"netBuyCr"})
    return df

def modifyProductionInput(df):
    df = df.drop(df.columns[0],axis = 1) # remove timeTag
    df = df.rename(columns={df.columns[0]:"ID", df.columns[1]:"labor_on_food", df.columns[2]:"labor_on_Si", df.columns[3]:"labor_on_Ni" ,df.columns[4]: "labor_on_Ra", df.columns[5]: "labor_on_Co", df.columns[6]: "labor_on_Cr", df.columns[7]:"upgrade_input", df.columns[8]:"production_set"})
    return df
