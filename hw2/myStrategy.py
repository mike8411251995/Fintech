def myStrategy(pastPriceVec, currentPrice, stockType):
    # Explanation of my approach:
    # 1. Technical indicator used: MA & RSI
    # 2. For MA:
    #    if price-ma>alpha ==> buy
    #    if price-ma<-beta ==> sell
    # 3. For RSI:
    #    if RSI>beta  ==> sell
    #    if RSI<alpha ==> buy
    # 4. Modifiable parameters: alpha, beta, and window size for both MA and RSI
    # 5. Use exhaustive search to obtain these parameter values (as shown in bestParamByExhaustiveSearch.py)
    # 6. After some experiments, LQD and IAU exhibits better results using MA, while SPY and DSI performs better using RSI.
    
    import numpy as np
    # stockType='SPY', 'IAU', 'LQD', 'DSI'
    # Set parameters for different stocks
    paramSetting={'SPY': {'alpha':35, 'beta':75, 'windowSize':56},
                    'IAU': {'alpha':0, 'beta':1, 'windowSize':468},
                    'LQD': {'alpha':0, 'beta':1, 'windowSize':12},
                    'DSI': {'alpha':18, 'beta':93, 'windowSize':17}}
    windowSize=paramSetting[stockType]['windowSize']
    alpha=paramSetting[stockType]['alpha']
    beta=paramSetting[stockType]['beta']
    
    action=0        # action=1(buy), -1(sell), 0(hold), with 0 as the default action
    
    # Use MA if stockType is LQD or IAU
    if stockType == 'LQD' or stockType == 'IAU':
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
        if (currentPrice-ma)>alpha:        # If price-ma > alpha ==> buy
            action=1
        elif (currentPrice-ma)<-beta:    # If price-ma < -beta ==> sell
            action=-1
    # Use RSI if stockType is SPY or DSI
    else:
        dataLen=len(pastPriceVec)       # Length of the data vector
        if dataLen==0 or dataLen==1: 
            return action
        # Compute MA
        if dataLen<=windowSize:
            windowedData=np.array(pastPriceVec)
        else:
            windowedData=np.array(pastPriceVec[-windowSize:])     # Compute the normal MA using windowSize 
        
        diffWindow = windowedData[1:] - windowedData[:-1]
        diffWindowSize = len(diffWindow)
        SMD_u =  float(np.sum(diffWindow[diffWindow>0])) / diffWindowSize
        SMD_d = -float(np.sum(diffWindow[diffWindow<0])) / diffWindowSize
        
        if SMD_u + SMD_d == 0:
            return action
        else:
            RSI = SMD_u / (SMD_u + SMD_d) * 100.0
        
        # Determine action
        if RSI>beta:
            action=-1
        elif RSI<alpha:
            action=1

    return action