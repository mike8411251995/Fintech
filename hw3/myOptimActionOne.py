import numpy as np
import operator

def myOptimActionOne(priceVec, transFeeRate):
	dataLen = len(priceVec)
	actionVec = np.zeros(dataLen)
	stockVec = np.zeros(dataLen)
	cashVec = np.zeros(dataLen)
	stockDecision = np.zeros(dataLen)
	cashDecision = np.zeros(dataLen)

	cashVec[0] = 1.0
	stockVec[0] = cashVec[0] / priceVec[0]
	for i in range(dataLen):
		if i == 0:
			continue

		stockValues = [stockVec[i - 1], (cashVec[i - 1] / priceVec[i]) * (1.0 - transFeeRate)]
		stockDecision[i], stockVec[i] = max(enumerate(stockValues), key=operator.itemgetter(1))

		cashValues = [cashVec[i - 1], (stockVec[i - 1] * priceVec[i]) * (1.0 - transFeeRate)]
		cashDecision[i], cashVec[i] = max(enumerate(cashValues), key=operator.itemgetter(1))

	
	# 1: stock,  -1: cash
	indicator = 1 if stockVec[-1] > cashVec[-1] else -1
	for i in reversed(range(dataLen)):
		if indicator == 1:
			if stockDecision[i] == 0:
				actionVec[i] = 0
			elif stockDecision[i] == 1: # from cash to stock (buy)
				actionVec[i] = 1
				indicator *= -1
		elif indicator == -1:
			if cashDecision[i] == 0:
				actionVec[i] = 0
			elif cashDecision[i] == 1: # from stock to cash (sell)
				actionVec[i] = -1
				indicator *= -1

	return actionVec