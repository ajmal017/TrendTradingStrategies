# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 05:02:27 2020

@author: Gabriel Dennery
"""
#imports
import numpy as np
import yfinance as yf
import ta
import csv
import pandas as pd

##GETTING STOCK SEARCH CRITERIA
def criteria(textfile):
    
    text_file = open(textfile,'r')
    string = text_file.read()
    mylist = string.split(',')
    startdate = mylist[0]
    enddate = mylist[1]
    iterations = int(mylist[2])
    period = int(mylist[3])
    text_file.close()#don't leave your files open--bad feng shue
    
    return startdate,enddate,iterations,period


##GETTING List of Stock Names as CSV
def CSVconverter(filename):
    
    with open(filename) as f:
        reader = csv.reader(f)
        data = list(reader)
    
    data.remove(data[0])
    
    return data


##GETTING stock data and indicators from yahoo finance, putting in dataframe
def Indicators(stockname,startdate,enddate):
    stock_df = yf.download(stockname,startdate,enddate)
    adx = ta.trend.ADXIndicator(stock_df.High,stock_df.Low,stock_df.Close)
    stock_df['adx'] = adx.adx()
    vortex = ta.trend.VortexIndicator(stock_df.High,stock_df.Low,stock_df.Close)
    stock_df['vortex'] = vortex.vortex_indicator_diff()
    stock_df.dropna()
    return stock_df


#definitions for neural network computation
def sigmoid(x):
    return 1/(1 + np.exp(-x))

def sigmoid_derivative(x):
    return x*(1 - x)

#neural network
def Perceptron(training_data,training_outputs,num_param,training_iteration):#num_param is an integer, training data must have num_param columns
    
    np.random.seed(1)
    synaptic_weights = 2*np.random.random((num_param,1)) - 1
    
    
    for i in range(training_iteration):
        input_layer = training_data
        outputs = sigmoid(np.dot(input_layer, synaptic_weights))
        error = training_outputs - outputs
        adjustments = error*sigmoid_derivative(outputs)
        synaptic_weights += np.dot(input_layer.T, adjustments)

    
    return synaptic_weights


#how often does the neural network predict price changes?
def PerceptronEfficacy(stock_df,period_length,training_iteration):
    n = len(stock_df)
    param = 4#parameters/activations used to predict stock
    
    #building and evaluating perceptrons of given period_length over entire stock
    #should result in efficacy of perceptron method using period_length's worth of data 
    #on the given stock

    for i in range(0,n - period_length - 2):#minus 2 is to keep the loop from iterating out of range
        diff = []
        inputs = []
        error_vector = []
        for j in range(0,period_length):
            #gathering inputs
            inputs.append(stock_df.adx[i + j])
            inputs.append(stock_df.vortex[i + j])
            inputs.append(stock_df.Volume[i + j])
            inputs.append(stock_df.High[i + j])
    
            #deriving outputs
            init_high = stock_df.High[i + j]
            final_high = stock_df.High[i + j + 1]
            price_diff = final_high - init_high
            diff.append(price_diff)
        
        
        prediction_date_inputs = np.array([[inputs.append(stock_df.adx[i + j + 1]),inputs.append(stock_df.vortex[i + j + 1]),inputs.append(stock_df.Volume[i + j + 1]),inputs.append(stock_df.High[i + j + 1])]])
        
        inputs = np.array(inputs)
        training_inputs = inputs.reshape((period_length,param))
        training_outputs = np.array([diff]).T
        
        weights = Perceptron(training_inputs,training_outputs,param,training_iteration)
        predicted_price_vector = sigmoid(np.dot(prediction_date_inputs,weights))
        actual_price_vector = stock_df.High[i + j + 2] - stock_df.High[i + j + 1]
        
        error = abs(actual_price_vector - predicted_price_vector)/actual_price_vector
        error_vector.append(error)
    
    average_error = np.average(error_vector)
    
    return average_error

#Giving Summary Stats for All Stocks in form of data frame
def StockFinder(stocks,searchcriteria):#both file names, 'stocklist.csv' and 'searchcritera.txt'
    
    #acquiring data
    startdate,enddate,training_iteration,period_length = criteria(searchcriteria)
    stocklist = CSVconverter(stocks)
    
    #empty lists to later be converted to data frame with analysis results
    stocklist1 = []
    stock_type = []
    
    price_changes = []
    adx = []
    vortex = []
    volume = []
    error = []
    #adx_applicability = []
    #vortex_applicability = [] specific to trading strategy/criteria
    
    for i in range(1,len(stocklist) - 1):
        
        stockname = stocklist[i][0]
        stocktype = stocklist[i][1]
        
        stock_df = Indicators(stockname,startdate,enddate)
        
        price_vector = stockname.High[-1] - stockname.High[-2]
        current_adx = stockname.adx[-1]
        current_vortex = stockname.vortex[-1]
        current_volume = stockname.Volume[-1]
        perceptron_error = PerceptronEfficacy(stock_df,period_length,training_iteration)
        
        stocklist1.append(stockname)
        stock_type.append(stocktype)
        price_changes.append(price_vector)
        adx.append(current_adx)
        vortex.append(current_vortex)
        volume.append(current_volume)
        error.append(perceptron_error)
    
    
    stocklist = stocklist1        
    dictionary = {'name':stocklist,
                  'sector':stocktype,
                  'price change':price_vector,
                  'current adx':adx,
                  'current vortex':vortex,
                  'current volume':volume,
                  'Perceptron error':error}#,
                  #'adx meets threshold':adx_applicability,
                  #'vortex meets threshold':vortex_applicability}
    
    df = pd.DataFrame (dictionary, 
                       columns = ['name','sector','price change','current adx','current vortex','current volume','perceptron error'])#,'adx meets threshhold','vortex meets threshhold'])
    return df



#prints dataframe analysis results on csv in working directory
def PresentAnalysis(stocks,criteria,outfile):
    df = StockFinder(stocks,criteria)
    df.to_csv(outfile,header=True,index=False)
        



'''
test commands:



debuggers:

print('Random starting synaptic weights: ')
print(synaptic_weights)

print('Synaptic weights after training')
print(synaptic_weights)
print('outputs')
print(outputs)

'''