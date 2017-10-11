import os
import sys
import numpy as np
import requests
from keras.models import Sequential
from keras.layers import Dense
from get_tweets import stock_sentiment

#get csv file
hist_data_file = 'WEED.csv'


def stock_prediction():
    # Collect data points from csv
    dataset = []

    with open(hist_data_file) as f:
        for n, line in enumerate(f):
            if n != 0:
                dataset.append(float(line.split(',')[1]))

    dataset = np.array(dataset)
    print(dataset)

    # Create dataset matrix (X=t and Y=t+1)
    def create_dataset(dataset):
        dataX = [dataset[n + 1] for n in range(len(dataset) - 2)]
        return np.array(dataX), dataset[2:]

    trainX, trainY = create_dataset(dataset)

    # Create and fit Multilinear Perceptron model
    model = Sequential()
    model.add(Dense(8, input_dim=1, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, nb_epoch=200, batch_size=2, verbose=2)

    # Prediction for tomorrow
    prediction = model.predict(np.array([dataset[0]]))

    # print(prediction)
    result = 'The price will move from %s to %s' % (dataset[0], prediction[0][0])

    return result


# set stock quote
stock_ticker = '$WEED'

# Check if the stock sentiment is positve
if stock_sentiment(stock_ticker, num_tweets=100) is False:
    print('Things are not looking too good.')
    sys.exit()

# create the nn and get the prediction
print(stock_prediction())