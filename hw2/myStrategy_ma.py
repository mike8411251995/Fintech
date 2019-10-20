def myStrategy(pastPriceVec, currentPrice, stockType):
    # Explanation of my approach:
    # 1. Technical indicator used: MA
    # 2. if price-ma>alpha ==> buy
    #    if price-ma<-beta ==> sell
    # 3. Modifiable parameters: alpha, beta, and window size for MA
    # 4. Use exhaustive search to obtain these parameter values (as shown in bestParamByExhaustiveSearch.py)
    
    import numpy as np
    # stockType='SPY', 'IAU', 'LQD', 'DSI'
    # Set parameters for different stocks
    paramSetting={'SPY': {'alpha':35, 'beta':75, 'windowSize':56},
                    'IAU': {'alpha':21, 'beta':81, 'windowSize':35},
                    'LQD': {'alpha':45, 'beta':63, 'windowSize':176},
                    'DSI': {'alpha':18, 'beta':93, 'windowSize':17}}
    windowSize=paramSetting[stockType]['windowSize']
    # windowSize=params[0]
    alpha=paramSetting[stockType]['alpha']
    # alpha=params[1]
    beta=paramSetting[stockType]['beta']
    # beta=params[2]
    # if stockType == 'LQD' or stockType == 'SPY' or stockType == 'IAU':
    #     return 0
        
    action=0        # action=1(buy), -1(sell), 0(hold), with 0 as the default action
    dataLen=len(pastPriceVec)       # Length of the data vector
    if dataLen==0 or dataLen==1: 
        return action
    # Compute MA
    if dataLen<=windowSize:
        windowedData=np.array(pastPriceVec)
        # prevWindowedData=pastPriceVec
        # halfWindowedData=pastPriceVec[-int(len(pastPriceVec)/2):]
    else:
        windowedData=np.array(pastPriceVec[-windowSize:])     # Compute the normal MA using windowSize 
        # prevWindowedData=pastPriceVec[-windowSize-1:-1]
        # halfWindowedData=pastPriceVec[-int(windowSize/2):]
        # ma=np.mean(windowedData)
    
    diffWindow = windowedData[1:] - windowedData[:-1]
    diffWindowSize = len(diffWindow)
    SMD_u =  float(np.sum(diffWindow[diffWindow>0])) / diffWindowSize
    SMD_d = -float(np.sum(diffWindow[diffWindow<0])) / diffWindowSize
    
    if SMD_u + SMD_d == 0:
        return action
    # elif prevSMD_u + prevSMD_d == 0:
    #     return action
    # elif halfSMD_u + halfSMD_d == 0:
    #     return action
    else:
        RSI = SMD_u / (SMD_u + SMD_d) * 100.0
        # prevRSI = prevSMD_u / (prevSMD_u + prevSMD_d) * 100.0
        # halfRSI = halfSMD_u / (halfSMD_u + halfSMD_d) * 100.0
    # print(RSI)
    
    # Determine action
    # if RSI>alpha and prevRSI<=alpha:       # If price-ma > alpha ==> buy
    #     action=1
    # elif RSI<beta and prevRSI>=beta:  # If price-ma < -beta ==> sell
    #     action=-1
    if RSI>beta:
        action=-1
    elif RSI<alpha:
        action=1
    # elif halfRSI > RSI:
    #     action=1
    # elif halfRSI < RSI:
    #     action=-1

    return action
