import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

stocks = ['https://finance.yahoo.com/quote/VTI/','https://finance.yahoo.com/quote/VGK/','https://finance.yahoo.com/quote/VPL/','https://finance.yahoo.com/quote/VWO/','https://finance.yahoo.com/quote/BWX/','https://finance.yahoo.com/quote/IEF/']
currentHoldings = [1,1,1,1,1,1]
"""Vanguard total Stock Market (VTI) = [1]
Vanguard FTSE Europe (VGK) = [2]
Vanguard FTSE Pacific (VPL) = [3]
Vangaurd FTSE Emerging Market (VWO) = [4]
SPDR Bloomberg Barclays Int (BWX) = [5]
iShares 7-10Y T-BOND (IEF) = [6]
"""

totalAssetListUSD = []
totalAssetListSGD = []

def getUrl(stockURL):
    url = urlopen(stockURL)
    return url
    
def beautifulSoup(url):
    soup = BeautifulSoup(url, 'html.parser')
    return soup
    
def getName(soup):
    name_box = soup.find('h1',attrs = {'class':'D(ib) Fz(16px) Lh(18px)'})
    name = name_box.text.strip()
    return name
    
def getPrice(soup):
    price_box = soup.find('span', attrs = {'class':'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)'})
    price = price_box.text.strip()
    return round(float(price),2)
    
def getExchangeRate():
    url = urlopen('https://finance.yahoo.com/quote/SGD%3DX/')
    soup = BeautifulSoup(url, 'html.parser')
    rate_box = soup.find('span', attrs = {'class':'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)'})
    rate = float(rate_box.text.strip())
    return rate
    
def exportCSV(name, price, now):
    with open('record.csv', 'a') as csv_file:
        write = csv.writer(csv_file)
        write.writerow([name, price, now])
        
def main():
    now =  datetime.now()
    timeDate = now.strftime("%m/%d/%Y, %H:%M:%S")
    sgdRate = getExchangeRate()
    totalAssetUSD = 0
    totalAssetSGD = 0
    for i in range(0,len(stocks)):
        url = getUrl(stocks[i])
        soup = beautifulSoup(url)
        name = getName(soup)
        price = getPrice(soup)
        sgdPrice = round((price*sgdRate),2)
        print("@",timeDate)
        print(name, "\nCurrent price in USD:", price, "\nCurren price in SGD:", sgdPrice)
        addUSD = price * currentHoldings[i]
        addSGD = sgdPrice * currentHoldings[i]
        totalAssetListUSD.append(addUSD)
        totalAssetListSGD.append(addSGD)
        exportCSV(name, price, timeDate)
    for i in range(0, len(totalAssetListUSD)):
        totalAssetUSD = totalAssetUSD + totalAssetListUSD[i]
        totalAssetSGD = totalAssetSGD + totalAssetListSGD[i]
    print("Total Asset in USD: ", totalAssetUSD)
    print("Total Asset in SGD: ", totalAssetSGD)
    exportCSV("Total Asset in USD", totalAssetUSD, timeDate)

if __name__ == "__main__":
    main()
