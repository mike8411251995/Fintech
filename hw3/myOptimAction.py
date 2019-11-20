import numpy as np
import operator

def myOptimAction(priceMat, transFeeRate):
    # Explanation of my approach:
    # 1. Technical indicator used: dynamic programming
    # 2. For each day, record the "best previous actions" 
    #    for each stock (from cash or other stocks) by
    #    choosing maximized profit
    # 3. Choose the maximum profit achieved on the last
    #    day and select it as the starting point
    # 4. Follow the record of "best previous actions" to
    #    decide how to sell/buy stocks
    
    dataLen, stockCount = priceMat.shape
    actionMat = []
    stockVec = np.zeros((dataLen, stockCount + 1))
    stockDecision = np.zeros((dataLen, stockCount + 1))

    stockVec[0][stockCount] = 1000 # initialize cash
    for j in range(stockCount):
        stockVec[0][j] = 0 # initialize stock
    
    for i in range(dataLen):
        if i == 0:
            continue

        for j in range(stockCount): # stocks
            stockValues = np.zeros(stockCount + 1)
            for k in range(stockCount):
                if k == j: # no buy or sell
                    stockValues[k] = stockVec[i-1][j]
                else: # sell k to buy j
                    stockValues[k] = (stockVec[i-1][k] * priceMat[i][k] / priceMat[i][j]) * (1.0 - transFeeRate) * (1.0 - transFeeRate)
            stockValues[stockCount] = (stockVec[i-1][stockCount] / priceMat[i][j]) * (1.0 - transFeeRate) # use cash to buy j
            stockDecision[i][j], stockVec[i][j] = max(enumerate(stockValues), key=operator.itemgetter(1))

        stockValues = np.zeros(stockCount + 1) # cash
        for k in range(stockCount):
            # sell k to get cash
            stockValues[k] = (stockVec[i-1][k] * priceMat[i][k]) * (1.0 - transFeeRate)
        stockValues[stockCount] = stockVec[i-1][stockCount] # no buy or sell
        stockDecision[i][stockCount], stockVec[i][stockCount] = max(enumerate(stockValues), key=operator.itemgetter(1))

    stockDecision = stockDecision.astype(int)

    # 1: stock,  -1: cash
    indicator, _ = max(enumerate(stockVec[-1]), key=operator.itemgetter(1))
    for i in reversed(range(dataLen)):
        if i == 0:
            continue
        indicator = int(indicator)
        if indicator == stockCount: # ... to cash
            if stockDecision[i][indicator] == stockCount: # from cash to cash
                indicator = stockCount
            else: # from stock to cash (sell)
                actionMat.insert(0, [i, stockDecision[i][indicator], -1, float("inf")])
                indicator = stockDecision[i][indicator]
        else: # ... to stock
            if stockDecision[i][indicator] == stockCount: # from cash to stock
                actionMat.insert(0, [i, -1, indicator, float("inf")])
                indicator = stockCount
            elif stockDecision[i][indicator] == indicator:
                indicator = stockDecision[i][indicator]
            else: # from stock to stock
                actionMat.insert(0, [i, stockDecision[i][indicator], indicator, float("inf")])
                indicator = stockDecision[i][indicator]      
    
    return actionMat