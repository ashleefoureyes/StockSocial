import os
import sys
import numpy as np
import requests
from keras.models import Sequential
from keras.layers import Dense
from get_tweets import stock_sentiment


# create a temp csv to store historical data
hist_data_file = 'historical_data.csv'


def get_historical(quote):
    # Download file from google finance
    url = 'http://www.google.com/finance/historical?q=NASDAQ%3A' + quote + '&output=csv'
    r = requests.get(url, stream=True)

    if r.status_code != 400:
        with open(hist_data_file, 'wb') as f:
            for content in r:
                f.write(content)

        return True

def stock_prediction():
    # Collect data from csv
    open_price = []

    with open(hist_data_file) as f:
        for n, line in enumerate(f):
            if n != 0:
                open_price.append(float(line.split(',')[1]))

    open_price = np.array(open_price)




    # Create dataset matrix (X=t and Y=t+1)
    def create_dataset(open_price):
        dataX = [open_price[n + 1] for n in range(len(open_price) - 2)]
        return np.array(dataX), open_price[2:]

    trainX, trainY = create_dataset(open_price)

    # Create and fit Multilinear Perceptron model
    model = Sequential()
    model.add(Dense(8, input_dim=1, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, nb_epoch=200, batch_size=2, verbose=2)

    # Prediction for tomorrow
    prediction = model.predict(np.array([open_price[0]]))

    # print(prediction)
    result = 'The price will move from %s to %s' % (open_price[0], prediction[0][0])

    return result

# Ask user for a stock quote
stock_ticker = input('Enter a NASDAQ listed symbol: ').upper()

# Check if the stock sentiment is positve
if stock_sentiment(stock_ticker, num_tweets=50) is False:
    print('Things are not looking too good.')
    sys.exit()

# Check historical data is acquirable
if get_historical(stock_ticker) is False:
    print('404 Error')
    sys.exit()

# create the neural net and get the prediction
print(stock_prediction())

# Delete file
os.remove(hist_data_file)