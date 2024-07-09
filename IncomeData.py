import pandas as pd
import numpy as np
import re

# 'PTime','PRevenue','PCost of good sold','PGross Profit','POperationg Expense','POperationg income',
# 'PInterest expense','PIncome before tax','PIncome tax expense','PNet income']


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def Income(name, srow, nrow, CompName, SIC):
    fl = True
    df = pd.read_excel(name, skiprows=int(srow), nrows=int(nrow), header=None)
    # print(df)
    df.dropna(how='any', axis='columns', inplace=True)
    #df.to_excel('Check.xlsx', index=False)
    Col = df.columns
    NumCol = len(Col)
    x = 1
    Year = []
    Revenue = []
    GProfit = []
    OpExpense = []
    InBeTax = []
    Tax = []
    NetIn = []
    IntEx = []
    shape = df.shape
    limit = shape[0]
    #print(shape, limit)
    while(x < NumCol):
        Re = 0
        Ye = 0
        GPRo = 0
        OpEx = 0
        BeTax = 0
        Ta = 0
        NIn = 0
        y = 0
        IEx = 0
        while y < limit:
            Name = df.iloc[y][Col[0]]
            if (Name == 'Report Date'):
                date = df.iloc[y][Col[x]]
                YearNumL = re.findall(r'\d{4}', date)
                Ye = int(YearNumL[0])
            elif (re.match(r'Total Revenue.*', Name, re.I)):
                ele = df.iloc[y][Col[x]]
                check = isfloat(ele)
                if check:
                    Re = float(ele)
            elif (re.match(r'Gross profit.*', Name, re.I)):
                ele = df.iloc[y][Col[x]]
                check = isfloat(ele)
                if check:
                    GPRo = float(ele)
            elif (re.match(r'Earnings Before Tax.*', Name, re.I)):
                ele = df.iloc[y][Col[x]]
                check = isfloat(ele)
                if check:
                    BeTax = float(ele)
            elif (re.match(r'Tax.*', Name, re.I)):
                ele = df.iloc[y][Col[x]]
                check = isfloat(ele)
                if check:
                    Ta = float(ele)
            elif (Name == "Interest Expense"):
                ele = df.iloc[y][Col[x]]
                check = isfloat(ele)
                if check:
                    IEx = float(ele)
            elif (re.match(r'Net Income.*', Name, re.I)):
                ele = df.iloc[y][Col[x]]
                check = isfloat(ele)
                if check:
                    NIn = float(ele)
            y += 1
        OpEx = BeTax - GPRo
        Year.append(Ye)
        Revenue.append(Re)
        GProfit.append(GPRo)
        OpExpense.append(OpEx)
        InBeTax.append(BeTax)
        Tax.append(Ta)
        NetIn.append(NIn)
        IntEx.append(IEx)
        x += 1

    z = 0
    # Year - Revenue -  GrossProfit - Interest expene - Operation Expense - Tax - Net incoem
    data = []
    while (z < (len(Year) - 1)):
        Array = [Year[z], Revenue[z], GProfit[z], IntEx[z], OpExpense[z], Tax[z], NetIn[z], Year[z + 1], Revenue[z + 1], GProfit[z + 1], IntEx[z + 1], OpExpense[z + 1], Tax[z + 1], NetIn[z + 1], CompName, SIC]
        # print(Array)
        if(fl):
            data = [Array]
            fl = False
        else:
            data = np.append(data, [Array], axis=0)
        z += 1
        # print(data)
    return data


def YearData(name, srow, nrow, CompName, SIC):
    fl = True
    df = pd.read_excel(name, skiprows=int(srow), nrows=int(nrow), header=None)
    # print(df)
    df.dropna(how='any', axis='columns', inplace=True)
    #df.to_excel('Check.xlsx', index=False)
    Col = df.columns
    NumCol = len(Col)
    x = 1
    Year = []
    Revenue = []
    GProfit = []
    OpExpense = []
    InBeTax = []
    Tax = []
    NetIn = []
    IntEx = []
    shape = df.shape
    limit = shape[0]
    #print(shape, limit)
    while(x < NumCol):
        Re = 0
        Ye = 0
        GPRo = 0
        OpEx = 0
        BeTax = 0
        Ta = 0
        NIn = 0
        y = 0
        IEx = 0
        while y < limit:
            Name = df.iloc[y][Col[0]]
            if (Name == 'Report Date'):
                date = df.iloc[y][Col[x]]
                YearNumL = re.findall(r'\d{4}', date)
                Ye = int(YearNumL[0])
            elif (re.match(r'Total Revenue.*', Name, re.I)):
                ele = df.iloc[y][Col[x]]
                check = isfloat(ele)
                if check:
                    Re = float(ele)
            elif (re.match(r'Gross profit.*', Name, re.I)):
                ele = df.iloc[y][Col[x]]
                check = isfloat(ele)
                if check:
                    GPRo = float(ele)
            elif (re.match(r'Earnings Before Tax.*', Name, re.I)):
                ele = df.iloc[y][Col[x]]
                check = isfloat(ele)
                if check:
                    BeTax = float(ele)
            elif (re.match(r'Tax.*', Name, re.I)):
                ele = df.iloc[y][Col[x]]
                check = isfloat(ele)
                if check:
                    Ta = float(ele)
            elif (Name == "Interest Expense"):
                ele = df.iloc[y][Col[x]]
                check = isfloat(ele)
                if check:
                    IEx = float(ele)
            elif (re.match(r'Net Income.*', Name, re.I)):
                ele = df.iloc[y][Col[x]]
                check = isfloat(ele)
                if check:
                    NIn = float(ele)
            y += 1
        OpEx = BeTax - GPRo
        Year.append(Ye)
        Revenue.append(Re)
        GProfit.append(GPRo)
        OpExpense.append(OpEx)
        InBeTax.append(BeTax)
        Tax.append(Ta)
        NetIn.append(NIn)
        IntEx.append(IEx)
        x += 1

    z = 0
    data = []
    while (z < len(Year)):
        Array = [Year[z], Revenue[z], GProfit[z], IntEx[z], OpExpense[z], Tax[z], NetIn[z], CompName, SIC]
        if(fl):
            data = [Array]
            fl = False
        else:
            data = np.append(data, [Array], axis=0)
        z += 1
    return data
