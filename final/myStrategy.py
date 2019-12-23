import keras
from keras.models import Model
from keras.layers import Dense, Dropout, LSTM, Input, Activation
from keras import optimizers
import numpy as np
np.random.seed(4)
import tensorflow
tensorflow.random.set_seed(4)
import pandas as pd
from sklearn import preprocessing

history_points = 50
alpha = 0
beta = 0

def csv_to_dataset(dailyOhlcvFile, openPrice):
    data = dailyOhlcvFile.drop('trading_point', axis=1)

    data = data.values
    new_data = np.zeros_like(data)
    new_data[:, :3] = data[:, 1:4]
    new_data[:, 4] = data[:, 4]
    new_data[:-1, 3] = data[1:, 0]
    new_data[-1, 3] = openPrice
    last_ohlcv_history = new_data[None, -history_points:]
    data = new_data

    data_normaliser = preprocessing.MinMaxScaler()
    data_normalised = data_normaliser.fit_transform(data)

    # using the last {history_points} open close high low volume data points, predict the next open value
    ohlcv_histories_normalised = np.array([data_normalised[i:i + history_points].copy() for i in range(len(data_normalised) - history_points)])
    next_day_open_values_normalised = np.array([data_normalised[:, 3][i + history_points].copy() for i in range(len(data_normalised) - history_points)])
    next_day_open_values_normalised = np.expand_dims(next_day_open_values_normalised, -1)
    next_day_open_higher = (next_day_open_values_normalised - ohlcv_histories_normalised[:, -1, 3, None] > 0)

    next_day_open_values = np.array([data[:, 3][i + history_points].copy() for i in range(len(data) - history_points)])
    next_day_open_values = np.expand_dims(next_day_open_values, -1)

    y_normaliser = preprocessing.MinMaxScaler()
    y_normaliser.fit(next_day_open_values)

    def calc_ema(values, time_period):
        # https://www.investopedia.com/ask/answers/122314/what-exponential-moving-average-ema-formula-and-how-ema-calculated.asp
        # sma = np.mean(values[:, 3])
        sma = np.mean(values[:, 2])
        ema_values = [sma]
        k = 2 / (1 + time_period)
        for i in range(len(his) - time_period, len(his)):
            # close = his[i][3]
            close = his[i][2]
            ema_values.append(close * k + ema_values[-1] * (1 - k))
        return ema_values[-1]

    technical_indicators = []
    for his in ohlcv_histories_normalised:
        # note since we are using his[3] we are taking the SMA of the closing price
        # sma = np.mean(his[:, 3])
        sma = np.mean(his[:, 2])
        macd = calc_ema(his, 12) - calc_ema(his, 26)
        technical_indicators.append(np.array([sma]))
        # technical_indicators.append(np.array([sma,macd,]))

    technical_indicators = np.array(technical_indicators)

    tech_ind_scaler = preprocessing.MinMaxScaler()
    technical_indicators_normalised = tech_ind_scaler.fit_transform(technical_indicators)

    assert ohlcv_histories_normalised.shape[0] == next_day_open_values_normalised.shape[0] == technical_indicators_normalised.shape[0]
    return last_ohlcv_history, ohlcv_histories_normalised, technical_indicators_normalised, next_day_open_values_normalised, next_day_open_values, next_day_open_higher, y_normaliser


def myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPrice):
    action = 0
    
    # dataset

    last_ohlcv_history, ohlcv_histories, _, next_day_open_values, unscaled_y, next_day_open_higher, y_normaliser = csv_to_dataset(dailyOhlcvFile, openPrice)

    ohlcv_train = ohlcv_histories
    y_train = next_day_open_values

    # model architecture

    lstm_input = Input(shape=(history_points, 5), name='lstm_input')
    x = LSTM(50, name='lstm_0')(lstm_input)
    x = Dropout(0.2, name='lstm_dropout_0')(x)
    x = Dense(64, name='dense_0')(x)
    x = Activation('sigmoid', name='sigmoid_0')(x)
    x = Dense(1, name='dense_1')(x)
    output = Activation('linear', name='linear_output')(x)

    model = Model(inputs=lstm_input, outputs=output)
    adam = optimizers.Adam(lr=0.0005)
    model.compile(optimizer=adam, loss='mse')
    model.fit(x=ohlcv_train, y=y_train, batch_size=32, epochs=50, shuffle=True, validation_split=0.1)

    # evaluation

    y_test_predicted = model.predict(last_ohlcv_history)
    y_test_predicted = y_normaliser.inverse_transform(y_test_predicted)

    if y_test_predicted > openPrice + alpha:
        action = 1
    elif y_test_predicted < openPrice - beta:
        action = -1
    
    return action