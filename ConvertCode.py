import pandas as pd
import re
import os
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.parse import quote

df = pd.read_excel('SICtoNAICS.xlsx')
Shape = df.shape
Limit = Shape[0]
mypath = "./Data IBIS"
#WEB = True
#driver = webdriver.Chrome()
# driver.get('https://www-mergentonline-com.proxy1.lib.uwo.ca/basicsearch.php')


def locX(SIC):
    x = 0
    flag = False
    while (x < Limit) and (flag == False):
        sic = df.iloc[x]['SIC Code']
        if(sic == SIC):
            flag = True
            return x
        x += 1
    return -1


def fileName(PName):
    name = []
    for file in os.listdir(mypath):
        if re.match("{}".format(PName), file):
            name.append(file)
    return(name)

# Will return in list ['Revenue', Wages]


def index(SIC, year, CName):
    SIC = str(SIC)
    if(len(SIC) == 3):
        SIC = '0{}'.format(SIC)
    year = int(year)
    x = locX(SIC)
    Code = df.iloc[x]['NAICS Code']
    Code = str(Code)
    CodeL = re.findall(r'(\d{5})(\d)', Code)
    NAICS = CodeL[0][0]
    FileNumber = int(CodeL[0][1])
    FileList = fileName(NAICS)
    print(NAICS[0:-1])
    if(len(FileList) == 0):
        FileList = fileName(NAICS[0:-1])
    print(FileList)
    LList = len(FileList)
    if(LList == 0):
        return([np.nan, np.nan, np.nan])
    elif(LList == 1):
        FullAdd = "{}/{}".format(mypath, FileList[0])
        da = pd.read_excel(FullAdd)
        shape = da.shape
        limit = shape[0]
        y = 0
        Found = False
        while(y < limit):
            line = da.iloc[y]['Year']
            if(line == year):
                Found = True
                break
            y += 1
        if(not Found):
            return([np.nan, np.nan, np.nan])
        Revenue = da.iloc[y]['Revenue (%)']
        EmRate = da.iloc[y]['Employment (%)']
        WagesR = da.iloc[y]['Wages (%)']
        return([Revenue, EmRate, WagesR])
    else:
        # time.sleep(15)
        '''
        try:
            Name = re.match(r"(\S+\s*\S*\s*\S*\s*\S*\s*)(?=\()", CName)
            company_name = Name[0]
            company_name = company_name[0:-1]
            url = f"https://www-mergentonline-com.proxy1.lib.uwo.ca/advancedsearchresults.php?action=basic&page=1&sector=&u=on&ui=on&i=on&ii=on&searchtext={quote(company_name)}&csrf_token_mol=2ef7350c1a"
            driver.get(url)
            path = "//a[normalize-space()='{}']".format(company_name)
            company_page_link = driver.find_element(By.LINK_TEXT, company_name)
            company_page_link.click()
            Infor = driver.find_elements(By.XPATH, "//div[@id = 'summarycol2']")
            Text = ""
            for element in Infor:
                text = element.text
                Text = Text + " " + text
            NumList = re.findall(pattern='(NAICS\s*\d{5})(\d)', string=Text)
            Num = int(NumList[0][1])
            if(Num <= len(FileList)):
                Choose = Num - 1
            else:
                Choose = len(FileList) - 1
        except:
            Choose = -1
        '''
        if(FileNumber <= len(FileList)):
            if(FileNumber == 0):
                Choose = FileNumber
            else:
                Choose = FileNumber - 1
        else:
            Choose = len(FileList) - 1
        if(Choose != -1):
            FullAdd = "{}/{}".format(mypath, FileList[Choose])
            da = pd.read_excel(FullAdd)
            shape = da.shape
            limit = shape[0]
            y = 0
            Found = False
            while(y < limit):
                line = da.iloc[y]['Year']
                if(line == year):
                    Found = True
                    break
                y += 1
            if(not Found):
                return([np.nan, np.nan, np.nan])
            Revenue = da.iloc[y]['Revenue (%)']
            EmRate = da.iloc[y]['Employment (%)']
            WagesR = da.iloc[y]['Wages (%)']
            return([Revenue, EmRate, WagesR])
        else:
            return([np.nan, np.nan, np.nan])

if __name__ == '__main__':
    print(index(831, 2013, '0187279 B C Ltd (NBB: LNXG F)'))
