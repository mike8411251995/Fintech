import random
import numpy as np

def myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPrice, params):
    action = 0
    windowSize, alpha, beta = params

    # pastPriceVec = np.array(minutelyOhlcvFile["open"])
    pastPriceVec = np.array(dailyOhlcvFile["open"])
    dataLen=len(pastPriceVec)        # Length of the data vector
    if dataLen==0: 
        return action
    # Compute MA
    if dataLen<windowSize:
        ma=np.mean(pastPriceVec)    # If given price vector is small than windowSize, compute MA by taking the average
    else:
        windowedData=pastPriceVec[-windowSize:]        # Compute the normal MA using windowSize 
        ma=np.mean(windowedData)
    # Determine action
    if (openPrice-ma)>alpha:        # If price-ma > alpha ==> buy
        action=1
    elif (openPrice-ma)<-beta:    # If price-ma < -beta ==> sell
        action=-1

    return action

    # a = [-1, 0, 1]
    # return a[random.randint(0, 2)]