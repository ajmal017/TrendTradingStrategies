"""
Trend Strength Measures

"""

###Imports
import numpy as np
from scipy import stats
#import DirectionalIndexTools as DITools #Note: This assumes that ADX file is in the same directory as the current program.
import yfinance as yf
import ta

### Logarithmic Return

def log_get_returns(prices):
  returns = []
  for i in range(prices):
    #print(i,'\n') making sure the loop iterates over the right number of elements
 
    price_final = prices[i+1]
    price_initial = prices[i]
    log_return = np.log(price_final/price_initial) #logreturns; see documents for explanation
    returns.append(log_return)   
    
  #index update for 'count' after operations but before break statement~~ need to stop iteration from going to 12th index because there are n - 1 intervals given n elements in a list, but updating index before operations would skip the first element and ask for a list index out of range

    if i == len(prices) - 2:
      break
  return returns



### Simple Linear Regression Predictor (within 1/n * standard deviations, where n is selected by the user)
def lin_reg_predictor(prices,n=1): #prices array-like, n > 0

    x = np.linspace(0.0,float(len(prices) - 1), len(prices))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,prices)
    prediction = slope*(len(prices)) + intercept #extrapolating values stock price for the following day/week/month

    #note to self, if regression is provided in terms of days, the x vector will not work since it treats days as evenly spaced; to be dealt with later
    prediction_upper_bound = prediction + std_err/n
    prediction_lower_bound = prediction - std_err/n #actual value of following stock price should be within range of upper/lower bound; else lin_reg_predictor is not predictive

    return prediction_upper_bound, prediction_lower_bound, r_value, p_value #potentially useful for subsequent analysis


### ADX indicator
def ADXIndicator(stockname,startdate,enddate):#inputs strictly stringvalues
  stock = yf.download(stockname,startdate,enddate)
  stock['Adj Open'] = stock.Open * stock['Adj Close']/stock['Close']
  stock['Adj High'] = stock.High * stock['Adj Close']/stock['Close']
  stock['Adj Low'] = stock.Low * stock['Adj Close']/stock['Close']
  stock.dropna(inplace=True)
  adxstock = ta.trend.ADXIndicator(stock['Adj High'],stock['Adj Low'],stock['Adj Close'])
  stock['adx'] = adxstock.adx()
  return stock


### Vortex Indicator
def VortexIndicator(stockname,startdate,enddate):
  stock = yf.download(stockname,startdate,enddate)
  stock['Adj Open'] = stock.Open * stock['Adj Close']/stock['Close']
  stock['Adj High'] = stock.High * stock['Adj Close']/stock['Close']
  stock['Adj Low'] = stock.Low * stock['Adj Close']/stock['Close']
  stock.dropna(inplace=True)
  vortexstock = ta.trend.VortexIndicator(stock['Adj High'],stock['Adj Low'],stock['Adj Close'])
  stock['vortex'] = vortexstock.vortex_indicator_diff()
  return stock



###ADXindictator (experimental modifications using exponential moving average as opposed to smoothed average)
"""

def CurrentADX(final,list1,list2,period,NumLargePeriod):
  initial = final - NumLargePeriod*period*14 #possibly some index issues
  DM_high = DITools.DM(list1)
  DM_low = DITools.DM(list2)
  DX_vector = []
  ADX_vector = []
  i = initial
  j = 0 #for dx vector
  k = 0 #for adx vector
  N = NumLargePeriod*13

  #getting initial ADX

  while i < 14*period*NumLargePeriod - 2:#potential indexing issues, to be worked out later
    High_list = []
    Low_list = []
    count = 0
    initialDXVECTORlength = len(DX_vector)
    while count < period:
      High_list.append(DM_high[i + count])
      Low_list.append(DM_low[i + count])
      count += 1
      
    DX_i = DITools.DX_initiator(High_list,Low_list)
    DX_vector.append(DX_i)#dx vector stuff
    j += 1
    updatedDXVECTORlength = len(DX_vector)

    if i == initial + period*14 - 2:#double check for indexing
      currentADX = np.average(DX_vector)
      ADX_vector.append(currentADX)
      k += 1
    elif (i > initial + period*14 - 1) and (updatedDXVECTORlength > initialDXVECTORlength):
      prevADX = ADX_vector[int(k) - 1]
      currentADX = DX_i*(2//(N + 1)) + prevADX(1 - (2//(N + 1))) #N = NumLargePeriods813 could possibly be wrong, but this is a relatively easy fix; more problematic would be if this formula is incorrectly implemented
      ADX_vector.append(currentADX)
      k += 1
      
    #changing index by three
    i += count + 1

  return ADX_vector,ADX_vector[len(ADX_vector)-1]
  #still in progress 1

"""

