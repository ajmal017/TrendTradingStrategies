#ADXPredictor components
import numpy as np
from scipy import stats

####components of adx
#####Directional Movement List Generator
def DM(listprice):
    DM_list = []
    for i in range(listprice):
        if count > 0:
            DM = listprice[i] - listprice[i - 1]
            DM_list.append(DM)
    return DM_list

#Example for test run: high list
#HDMList = DM(highlist)

#####True Range
def TR(listprice1,listprice2): #listprice1,2 have to be the same size.
    TR_list = [] #further, listprice1 should be the high DM, listprice2 should be the low DM (subject to modification)
    for i in range(listprice1):
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
#suspicion is that exponential moving average is more accurate predictor using ADX than smooth moving average. Subject to modification.


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
