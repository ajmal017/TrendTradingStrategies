"""
codeacademy project of financial analysis, do not execute

"""
import numpy as np
from scipy import stats

def display_as_percentage(val):
  return '{:.1f}%'.format(val * 100)

amazon_prices = [1699.8, 1777.44, 2012.71, 2003.0, 1598.01, 1690.17, 1501.97, 1718.73, 1639.83, 1780.75, 1926.52, 1775.07, 1893.63]
ebay_prices = [35.98, 33.2, 34.35, 32.77, 28.81, 29.62, 27.86, 33.39, 37.01, 37.0, 38.6, 35.93, 39.5]

# Write code here

def get_returns(prices):
  returns = []
  count = 0
  for i in enumerate (prices,0):
    #print(i,'\n') making sure the loop iterates over the right number of elements
 
    price_final = prices[count+1]
    price_initial = prices[count]
    log_return = np.log(price_final/price_initial)  
    returns.append(log_return)   
    
  #index update for 'count' after operations but before break statement~~ need to stop iteration from going to 12th index because there are n - 1 intervals given n elements in a list, but updating index before operations would skip the first element and ask for a list index out of range

    count += 1
    if count == len(prices) -1:
      break
  return returns


amazon_returns = get_returns(amazon_prices)
ebay_returns = get_returns(ebay_prices)

average_amazon_returns = np.average(amazon_returns)
average_ebay_returns = np.average(ebay_returns)

amazon_std = np.std(amazon_returns)
ebay_std = np.std(ebay_returns)


print('AMAZON ANNUAL RETURNS: ',display_as_percentage(average_amazon_returns),'\nEBAY ANNUAL RETURNS: ', display_as_percentage(average_ebay_returns),'\n')
print('AMAZON STD: ',display_as_percentage(amazon_std),'\nEBAY STD: ',display_as_percentage(ebay_std))

slope, intercept, r_value, p_value, std_err = stats.linregress(amazon_returns, ebay_returns)

print('Slope: ',slope,'\n','Intercept: ',intercept,'\n','r_value: ',r_value,'\n','p_value: ',p_value,'\n','Standard Error:',std_err,' \n')
