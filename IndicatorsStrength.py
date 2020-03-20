###Imports
import numpy as np
#from scipy import stats
import yfinance as yf
import ta
import csv
import pandas as pd
#first we get the search criteria and the data

##GETTING STOCK SEARCH CRITERIA
def criteria(textfile):
    
    text_file = open(textfile,'r')
    string = text_file.read()
    mylist = string.split(',')
    startdate = mylist[0]
    enddate = mylist[1]
    adxthreshold = float(mylist[2])
    vortexthreshold = float(mylist[3])
    vortexrisk = float(mylist[4])
    text_file.close()#don't leave your files open--bad feng shue
    
    return startdate,enddate,adxthreshold,vortexthreshold,vortexrisk#names explain themselves

##GETTING DATA as CSV
def CSVconverter(filename):
    
    with open(filename) as f:
        reader = csv.reader(f)
        data = list(reader)
    
    data.remove(data[0])
    
    return data



#next we create the measurement tools
    

##ADX indicator
def ADXIndicator(stockname,startdate,enddate):#inputs strictly stringvalues
    
  stock = yf.download(stockname,startdate,enddate)
  stock['Adj Open'] = stock.Open * stock['Adj Close']/stock['Close']
  stock['Adj High'] = stock.High * stock['Adj Close']/stock['Close']
  stock['Adj Low'] = stock.Low * stock['Adj Close']/stock['Close']
  stock.dropna(inplace=True)
  adxstock = ta.trend.ADXIndicator(stock['Adj High'],stock['Adj Low'],stock['Adj Open'])
  adxlist = adxstock.adx()
  
  return adxlist


##Vortex Indicator
def VortexIndicator(stockname,startdate,enddate):
  stock = yf.download(stockname,startdate,enddate)
  stock['Adj Open'] = stock.Open * stock['Adj Close']/stock['Close']
  stock['Adj High'] = stock.High * stock['Adj Close']/stock['Close']
  stock['Adj Low'] = stock.Low * stock['Adj Close']/stock['Close']
  stock.dropna(inplace=True)
  vortexstock = ta.trend.VortexIndicator(stock['Adj High'],stock['Adj Low'],stock['Adj Close'])
  vortexlist = vortexstock.vortex_indicator_diff()
  return vortexlist


#we make the evaluation criteria of the measuring tools

##finding how useful adx and vortex can be used one day in advance (to be continually updated)
def ADXVortexPredictionRate(stockname,startdate,enddate,adxthreshhold,vortexrisk):

    #getting data and indicators
    
    stock = yf.download(stockname,startdate,enddate)
    vortexstock = VortexIndicator(stockname,startdate,enddate)
    adxstock = ADXIndicator(stockname,startdate,enddate)
    closing = stock['Close']
    currentprice = closing[-1]

    #dataframe management; selecting current indicators to decide whether or not to even look at given stock
    stock['vortex'] = vortexstock
    vortex = vortexstock[-1]
    stock['adx'] = adxstock
    adx = adxstock[-1]
    stock.dropna()


    ##measuring the intensity of bullishness
    PosVort = []
    for i in range(0,len(stock['vortex'])):
        a = stock['vortex'][i]
        if a > 0:
            PosVort.append(a)

    avgposvortex = np.average(PosVort)


    #counters (see loop below)
    sumx = 0
    sumincrease = 0
    gains = 0
    #checking how likely going long paid off in one-day increments (i.e., price increased) for the given vortex
    #(later) maybe give indexes for which going long paid off

    #calculating average

    for i in range(0,len(stock)-1):
        current_vortex = stock['vortex'][i]
        current_price = stock['Open'][i]
        next_price = stock['Open'][i + 1]
    
    
        if (current_vortex > 0) and (abs(current_vortex - avgposvortex) <= vortexrisk*abs(avgposvortex - vortex)):#
            sumx += 1
            gains += (next_price - current_price)

            #error checks
            #print('current vortex:',current_vortex,'\n','average-positive-vortex: ',avgposvortex,'\n','gains: ',gains,'\n')
            #print('next price: ',next_price,'\ncurrent price: ',current_price,'\n\n')
        
            if next_price >= current_price:
            
                sumincrease += 1
            
    if sumx == 0:
        sumincrease = 0
        sumx = 1
            
    averagesuccess = sumincrease / sumx
    averagereturn = gains / sumx

    return currentprice, adx, vortex, averagesuccess, averagereturn





#executing analysis and providing results
def StockFinder(stocks,searchcriteria):#both file names, 'stocklist.csv' and 'searchcritera.txt'
    
    #acquiring data
    startdate,enddate,adxthreshhold,vortexthreshhold,vortexrisk = criteria(searchcriteria)
    stocklist = CSVconverter(stocks)
    
    #empty lists to later be converted to data frame with analysis results
    currentprice = []
    adx = []
    vortex = []
    averagesuccess = []
    averagereturn = []
    #adx_applicability = []
    #vortex_applicability = []
    stocklist1 = []
    stocktype = []
    
    
    for i in range(0,len(stocklist)):
        stockname = stocklist[i][0]
        currentprice_i,adx_i,vortex_i,averagesuccess_i,averagereturn_i = ADXVortexPredictionRate(stockname,startdate,enddate,adxthreshhold,vortexrisk)
        
        #adx/vortex applicability
        """
        if adx_i >= adxthreshhold:
            adx_applicable = 'true'
        else:
            adx_applicable = 'false'
        if vortex_i >= vortexthreshhold:
            vortex_applicable = 'true'
        else:
            vortex_applicable = 'false'
            
        adx_applicability.append(adx_applicable)
        vortex_applicability.append(vortex_applicable)
        """
        
        #decision factor stats
        currentprice.append(currentprice_i)
        adx.append(adx_i)
        vortex.append(vortex_i)
        averagesuccess.append(averagesuccess_i)
        averagereturn.append(averagereturn_i)
        
        #datamanagement
        stocklist1.append(stockname)
        stocktype.append(stocklist[i][1])
    
    stocklist = stocklist1        
    dictionary = {'name':stocklist,
                  'sector':stocktype,
                  'current price':currentprice,
                  'current adx':adx,
                  'current vortex':vortex,
                  'average success':averagesuccess,
                  'average return':averagereturn}#,
                  #'adx meets threshold':adx_applicability,
                  #'vortex meets threshold':vortex_applicability}
    
    df = pd.DataFrame (dictionary, 
                       columns = ['name','sector','current price','current adx','current vortex','average success','average return'])#,'adx meets threshhold','vortex meets threshhold'])
    return df

def PresentAnalysis(stocks,criteria,outfile):
    df = StockFinder(stocks,criteria)
    df.to_csv(outfile,header=True,index=False)



#test commands
    
"""
stockrolidex = 'CommonStocks.csv'
searchcriteria = 'SearchCriteria.txt'
outfile = 'AnalysisResults.csv'

relevant commands

df[df['vortex meets threshold'] == 'true']



##other possibilities . . .

def strategysuccess(n,stock,vortexrisk):
    
    PosVort = []
    for i in range(0,len(stock['vortex'])):
        a = stock['vortex'][i]
        if a > 0:
            PosVort.append(a)

    avgposvortex = np.average(PosVort)
    

    sumx = 0
    sumincrease = 0
    gains = 0
    for i in range(0,len(stock) - n):
        
        #including all possibilities (Baysian probability)
        current_vortex = stock['vortex'][i]
        current_price = stock['Open'][i]
        
        increased_prices = []
        decreased_prices = []
        #catching increases
        for j in range(0,n):
            
            if (stock['Open'][i + j] >= current_price) or (stock['Close'][i + j] >= current_price) or (stock['High'][i + j] >= current_price) or (stock['Low'][i + j] >= current_price):
                success = bool(1)
                increased_prices.append(stock['Open'][i + j])
            else:
                success = bool(0)
                decreased_prices.append(stock['Open'][i + j])
        
                             
            


        if (current_vortex > 0) and (abs(current_vortex - avgposvortex) <= vortexrisk*abs(avgposvortex - vortex)):#
            sumx += 1
            #gains += (next_price - current_price)#need to fix this
            
            #error checks
            #print('current vortex:',current_vortex,'\n','average-positive-vortex: ',avgposvortex,'\n','gains: ',gains,'\n')
            #print('next price: ',next_price,'\ncurrent price: ',current_price,'\n\n')
            
            
            

            if success:
                gains += np.min(increased_prices)
                sumincrease += 1
            else:
                gains += np.min(decreased_prices)

    if sumx == 0:
        sumincrease = 0
        sumx = 1

    averagesuccess = sumincrease / sumx
    averagereturn = gains / sumx
    return averagesuccess,averagereturn

"""

#NEXT STEPS:(upcoming)
##fix true/false for adx and vortex applicability why are they blank in the csv?
##get program to run every morning

#NEXT STEPS:(prospective)
##make selection mechanism to decide which stocks to buy
##make make report generator
##make database of trades and success/failure rates of methodology
