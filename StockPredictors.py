"""
Statistical Methods of Predicting Stock Prices

"""
###Imports
import numpy as np
from scipy import stats


### Logarithmic Return

def log_get_returns(prices):
  returns = []
  count = 0
  for i in enumerate (prices,0):
    #print(i,'\n') making sure the loop iterates over the right number of elements
 
    price_final = prices[count+1]
    price_initial = prices[count]
    log_return = np.log(price_final/price_initial) #logreturns; see documents for explanation
    returns.append(log_return)   
    
  #index update for 'count' after operations but before break statement~~ need to stop iteration from going to 12th index because there are n - 1 intervals given n elements in a list, but updating index before operations would skip the first element and ask for a list index out of range

    count += 1
    if count == len(prices) -1:
      break
  return returns



### Simple Linear Regression Predictor (within 1 standard deviation)
def lin_reg_predictor(prices,n): #prices array-like, n > 0

    x = np.linspace(0.0,float(len(prices) - 1), len(prices))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,prices)
    prediction = slope*(len(prices)) + intercept #extrapolating values stock price for the following day/week/month

    #note to self, if regression is provided in terms of days, the x vector will not work since it treats days as evenly spaced; to be dealt with later
    #could instead have a vector consisting of 
    prediction_upper_bound = prediction + std_err/n
    prediction_lower_bound = prediction - std_err/n #actual value of following stock price should be within range of upper/lower bound; else lin_reg_predictor is not predictive

    return prediction_upper_bound, prediction_lower_bound, r_value, p_value #potentially useful for subsequent analysis



### ADX INDICATOR

####components of adx in function formatt
#####Directional Movement List Generator
def DM(listprice):
    DM_list = []
    for count in enumerate(listprice,0):
        if count > 0:
            DM = listprice[count] - listprice[count - 1]
            DM_list.append(DM)
    return DM_list

#Example for test run: high list
#HDMList = DM(highlist)

#####True Range
def TR(listprice1,listprice2): #listprice1,2 have to be the same size.
    TR_list = [] #further, listprice1 should be the high DM, listprice2 should be the low DM (subject to modification)
    for count in enumerate(listprice1,0):
        if count > 0:
            Op1 = listprice1[count] - listprice1[count-1]
            Op2 = listprice2[count] - listprice2[count-1]
            TR = min(Op1,Op2)
            TR_list.append(TR)
    return TR_list

#####Moving Average Types
"""
def SmoothAverage(list_len_14): #list length is strictly 14 in this function
    for count in enumerate(list_len_14,0):
        heavyterm = 0 #smoothed averages are weighted more heavily towards previous 13 indexes
        lightterm = list_len_14[13] #current index in whichever metric
        if count <= 12:
            heavyterm += list_len_14[count]
    smoothAverage = (13*heavyterm + lightterm)/14
    return smoothAverage#returns scalar
"""

######Exponential Moving Average  
def ExponentialMovingAverage(list):#if applied to ADX, should have the same length the total interval of analysis; gives a specific number
  EMA_0 = list[0]
  EMA_y = EMA_0 #for the sake of mathematical coherence
  N = len(list)

  for i in range(list):
    EMA_t = list[i]*(2//(N + 1)) + EMA_y(1 - (2//(N + 1)))#see documentation
    #print(EMA)
    EMA_y = EMA_t
  
  return EMA_t#returns scalar

#Standard Directional Index Measures
def DI(DM,ATR): #DM, ATR float, not list
    return 100*DM/ATR

def DX(DI1,DI2,ATR): #DI1,DI2,ATR must be a float, not a list
    return (100*(abs(DI1 - DI2)//abs(DI1 + DI2)))
    #alternative versions of DX also could be used. . . projects for later

def DX_initiator(list1,list2):#lists should be same length, n should be integer

  #everything below assembles most of the previous code to give initial dx value, where subsequent adx values are defined by either a smoothed average
  #or an exponential moving average

  True_Range_Vector = TR(list1,list2)
  ATR = np.average(True_Range_Vector)
  DM_high = DM(list1)
  DM_low = DM(list2)
  Smoothed_DM_high = ExponentialMovingAverage(DM_high)
  Smoothed_DM_low = ExponentialMovingAverage(DM_low)
  high_DI = DI(Smoothed_DM_high,ATR)
  low_DI = DI(Smoothed_DM_low,ATR)
  Simple_DX = DX(high_DI,low_DI,ATR)
  #N = len(list1)

  return Simple_DX #N,Simple_DX

###### ADX functions

### the following loop should apply ADX_initiator to first N entries and then iterate for as many N-length periods as the user demands (provided there is enough data)

def CurrentADX(final,list1,list2,period,numLargePeriods):
  initial = final - period*numLargePeriods*14 #possibly some index issues
  DM_high = DM(list1)
  DM_low = DM(list2)
  TR_index = TR(list1,list2)
  DX = 0
  i = 0

  #getting initial ADX

  while i < 14*period - 2:
    High_list = []
    Low_list = []
    Range_list = []
    count = 0
    while count < period:
      High_list.append(DM_high[i + count])
      Low_list.append(DM_low[i + count])
      Range_list.append(TR_index[i + count])
      
    N,DX_i = DX_initiator(High_list,Low_list)
    i += count + 1 #count is (period - 1) at this point--I need to move period indexes away to calculate ADX
    DX += DX_i
     
  
  i = initial + 14*period - 1
  ADX_i = DX // 14.0
  
  while i < final - 1:
    j = i
    DX = 0
    while i < j + 14*period - 2:
      High_list = []
      Low_list = []
      Range_list = []
      count = 0
      while count < period:
        High_list.append(DM_high[i + count])
        Low_list.append(DM_low[i + count])
        Range_list.append(TR_index[i + count])
      
      DX_update = DX_initiator(High_list,Low_list)
      DX += DX_update

      i += count + 1 #count is (period - 1) at this point--I need to move period indexes away to calculate ADX
      
    ADX_current = DX // 14.0

    current_ADX = ADX_current(2//(numLargePeriods + 1)) - ADX_i*(1 - 2//(numLargePeriods + 1))
    ADX_i = current_ADX

  return current_ADX

  ### 

