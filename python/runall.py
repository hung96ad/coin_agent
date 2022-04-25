#!/usr/bin/env python
# coding: utf-8

# In[1]:


from binance.client import Client
import pandas as pd
from sqlalchemy.sql import func

import pandas as pd
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import *
from sklearn.preprocessing import MinMaxScaler

import pickle
from datetime import datetime
from modelDB import SQLALCHEMY_DATABASE_URI, Kline, Trade, CoinInfo, db

import schedule
import time
import random


# In[2]:


client = Client("api_key", "api_secret")
window_size = 20
skip = 1
layer_size = 500
output_size = 3


# In[3]:


def get_revert(df):
    predicted_stock_price = df['Close'].values[-30:].tolist()
    predicted_stock_price.reverse()
    for i in range(len(predicted_stock_price)):
        predicted_stock_price[i] *= (1+random.uniform(-0.03, 0.03))
    return predicted_stock_price


# In[4]:


class PredictModel():
    def __init__(self, df, isPredict=False, symbol='BTCUSDT'):
        self.time_pre = 180
        self.time_test = 30
        if isPredict:
            self.time_test = 0
            self.future_day = 30
        self.epoch = 20
        self.batch_size = 32
        self.df = df
        self.model = self.get_model()
        self.symbol = symbol
        self.checkpoint_filepath = f'./predictmodels/{self.symbol}/checkpoint'
        self.prep_data()

    def prep_data(self):
        self.data_target = self.df.filter(['Close'])
        target = self.data_target.values
        self.training_data_len = len(target) - self.time_test
        self.sc = MinMaxScaler(feature_range=(0,1))
        self.training_scaled_data = self.sc.fit_transform(target)
        train_data = self.training_scaled_data[0:self.training_data_len  , : ]
        X_train = []
        y_train = []
        for i in range(self.time_pre, len(train_data)):
            X_train.append(train_data[i-self.time_pre:i, 0])
            y_train.append(train_data[i, 0])

        X_train, self.y_train = np.array(X_train), np.array(y_train)
        self.X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    def get_model(self):
        model = Sequential()
        model.add(LSTM(units = 50, return_sequences=True, input_shape = (self.time_pre, 1)))
        model.add(Dropout(0.5))
        model.add(LSTM(units = 50, return_sequences = True))
        model.add(Dropout(0.5))
        model.add(LSTM(units = 50, return_sequences = True))
        model.add(Dropout(0.2))
        model.add(LSTM(units = 50))
        model.add(Dropout(0.2))
        model.add(Dense(units = 1))
        model.compile(optimizer = 'adam', loss = 'mean_squared_error')
        return model

    def predict(self):
        try:
            self.model.load_weights(self.checkpoint_filepath)
        except:
            print("need revert")
            return get_revert(self.df)
        predict_data = self.training_scaled_data[-self.time_pre: , : ]
        predicted_stock_price_pre = []
        scale = 1
        for i in range(self.future_day):
            X_test = np.array([predict_data[-self.time_pre: , : ]])
            pred = self.model.predict(X_test)
            if i == 0:
                scale = self.training_scaled_data[-1][-1]/pred[-1][-1]
            if abs(scale) > 10:
                print("need scale")
                scale = scale
            elif abs(scale) < 0.1:
                print("need revert scale")
                scale = 1/scale
            else:
                scale = 1
            predicted_stock_price_pre.append(pred[-1]*scale)
            predict_data = np.append(predict_data, [self.training_scaled_data[-i*3-1], pred[-1]*scale], axis=0)
        predicted_stock_price = self.sc.inverse_transform(predicted_stock_price_pre)
        return predicted_stock_price.flatten().tolist()


# In[5]:


def softmax(z):
    assert len(z.shape) == 2
    s = np.max(z, axis=1)
    s = s[:, np.newaxis]
    e_x = np.exp(z - s)
    div = np.sum(e_x, axis=1)
    div = div[:, np.newaxis]
    return e_x / div

def get_state(parameters, t, window_size = 20):
    outside = []
    d = t - window_size + 1
    for parameter in parameters:
        block = (
            parameter[d : t + 1]
            if d >= 0
            else -d * [parameter[0]] + parameter[0 : t + 1]
        )
        res = []
        for i in range(window_size - 1):
            res.append(block[i + 1] - block[i])
        for i in range(1, window_size, 1):
            res.append(block[i] - block[0])
        outside.append(res)
    return np.array(outside).reshape((1, -1))


# In[6]:


def save_trade_db(price, close_time, result, id_symbol, initial_money):
    db.query(CoinInfo).filter(CoinInfo.id == id_symbol).update({
        "Volume": CoinInfo.Volume + result['status_code'], 
        "initial_money": initial_money,
        "suggestionType": result['status_code'],
        "suggestionPrice": price,
        "suggestionDate": close_time
    }, synchronize_session = False)
    gain = None
    investment = None
    if 'gain' in result:
        gain = result['gain']
        investment = result['investment']
    trade = Trade(id_symbol = id_symbol,
                  close_time = close_time,
                  status = result['status_code'],
                  gain = gain,
                  price = price,
                  id_kline = result['id'],
                  investment = investment)
    db.add(trade)
    db.commit()


# In[7]:

class Deep_Evolution_Strategy:

    inputs = None

    def __init__(
        self, weights, reward_function, population_size, sigma, learning_rate
    ):
        self.weights = weights
        self.reward_function = reward_function
        self.population_size = population_size
        self.sigma = sigma
        self.learning_rate = learning_rate

    def _get_weight_from_population(self, weights, population):
        weights_population = []
        for index, i in enumerate(population):
            jittered = self.sigma * i
            weights_population.append(weights[index] + jittered)
        return weights_population

    def get_weights(self):
        return self.weights
    
    def train(self, epoch = 100, print_every = 1):
        lasttime = time.time()
        for i in range(epoch):
            population = []
            rewards = np.zeros(self.population_size)
            for k in range(self.population_size):
                x = []
                for w in self.weights:
                    x.append(np.random.randn(*w.shape))
                population.append(x)
            for k in range(self.population_size):
                weights_population = self._get_weight_from_population(
                    self.weights, population[k]
                )
                rewards[k] = self.reward_function(weights_population)
            rewards = (rewards - np.mean(rewards)) / (np.std(rewards) + 1e-7)
            for index, w in enumerate(self.weights):
                A = np.array([p[index] for p in population])
                self.weights[index] = (
                    w
                    + self.learning_rate
                    / (self.population_size * self.sigma)
                    * np.dot(A.T, rewards).T
                )
            if (i + 1) % print_every == 0:
                print(
                    'iter %d. reward: %f'
                    % (i + 1, self.reward_function(self.weights))
                )
        print('time taken to train:', time.time() - lasttime, 'seconds')

class Model:
    def __init__(self, input_size, layer_size, output_size):
        self.weights = [
            np.random.rand(input_size, layer_size)
            * np.sqrt(1 / (input_size + layer_size)),
            np.random.rand(layer_size, output_size)
            * np.sqrt(1 / (layer_size + output_size)),
            np.zeros((1, layer_size)),
            np.zeros((1, output_size)),
        ]

    def predict(self, inputs):
        feed = np.dot(inputs, self.weights[0]) + self.weights[-2]
        decision = np.dot(feed, self.weights[1]) + self.weights[-1]
        return decision

    def get_weights(self):
        return self.weights

    def set_weights(self, weights):
        self.weights = weights
        
class Agent:

    POPULATION_SIZE = 15
    SIGMA = 0.1
    LEARNING_RATE = 0.03

    def __init__(self, model, timeseries, skip, initial_money, real_trend, minmax, max_close_time = 0):
        self.max_close_time = max_close_time
        self.model = model
        self.timeseries = timeseries
        self.skip = skip
        self.real_trend = real_trend
        self.initial_money = initial_money
        self.es = Deep_Evolution_Strategy(
            self.model.get_weights(),
            self.get_reward,
            self.POPULATION_SIZE,
            self.SIGMA,
            self.LEARNING_RATE,
        )
        self.minmax = minmax
        self._id = None
        self._initiate()

    def _initiate(self):
        # i assume first index is the close value
        self.trend = self.timeseries[0]
        self._mean = np.mean(self.trend)
        self._std = np.std(self.trend)
        self._inventory = []
        self._capital = self.initial_money
        self._queue = []
        self._scaled_capital = self.minmax.transform([[self._capital, 2]])[0, 0]

    def reset_capital(self, capital):
        if capital:
            self._capital = capital
        self._scaled_capital = self.minmax.transform([[self._capital, 2]])[0, 0]
        self._queue = []
        self._inventory = []

    def trade(self, data, id=None):
        """
        you need to make sure the data is [close, volume]
        """
        if id is not None:
            self._id = id
        scaled_data = self.minmax.transform([data])[0]
        real_close = data[0]
        close = scaled_data[0]
        if len(self._queue) >= window_size:
            self._queue.pop(0)
        self._queue.append(scaled_data)
        if len(self._queue) < window_size:
            return {
                'id': id,
                'status_code': 0,
                'status': 'data not enough to trade',
                'action': 'fail',
                'balance': self._capital,
                'timestamp': str(datetime.now()),
            }
        state = self.get_state(
            window_size - 1,
            self._inventory,
            self._scaled_capital,
            timeseries = np.array(self._queue).T.tolist(),
        )
        action, prob = self.act_softmax(state)
#         print(prob)
        if action == 1 and self._scaled_capital >= close:
            self._inventory.append(close)
            self._scaled_capital -= close
            self._capital -= real_close
            return {
                'id': id,
                'status_code': 1,
                'status': 'buy 1 unit, cost %f' % (real_close),
                'action': 'buy',
                'balance': self._capital,
                'timestamp': str(datetime.now()),
            }
        elif action == 2 and len(self._inventory):
            bought_price = self._inventory.pop(0)
            self._scaled_capital += close
            self._capital += real_close
            scaled_bought_price = self.minmax.inverse_transform(
                [[bought_price, 2]]
            )[0, 0]
            try:
                invest = (
                    (real_close - scaled_bought_price) / scaled_bought_price
                ) * 100
            except:
                invest = 0
            return {
                'id': id,
                'status_code': -1,
                'status': 'sell 1 unit, price %f' % (real_close),
                'investment': invest,
                'gain': real_close - scaled_bought_price,
                'balance': self._capital,
                'action': 'sell',
                'timestamp': str(datetime.now()),
            }
        else:
            return {
                'id': id,
                'status_code': 0,
                'status': 'do nothing',
                'action': 'nothing',
                'balance': self._capital,
                'timestamp': str(datetime.now()),
            }

    def change_data(self, timeseries, skip, initial_money, real_trend, minmax):
        self.timeseries = timeseries
        self.skip = skip
        self.initial_money = initial_money
        self.real_trend = real_trend
        self.minmax = minmax
        self._initiate()

    def act(self, sequence):
        decision = self.model.predict(np.array(sequence))

        return np.argmax(decision[0])

    def act_softmax(self, sequence):
        decision = self.model.predict(np.array(sequence))

        return np.argmax(decision[0]), softmax(decision)[0]

    def get_state(self, t, inventory, capital, timeseries):
        state = get_state(timeseries, t)
        len_inventory = len(inventory)
        if len_inventory:
            mean_inventory = np.mean(inventory)
        else:
            mean_inventory = 0
        z_inventory = (mean_inventory - self._mean) / self._std
        z_capital = (capital - self._mean) / self._std
        concat_parameters = np.concatenate(
            [state, [[len_inventory, z_inventory, z_capital]]], axis = 1
        )
        return concat_parameters

    def get_reward(self, weights):
        initial_money = self._scaled_capital
        starting_money = initial_money
        invests = []
        self.model.weights = weights
        inventory = []
        state = self.get_state(0, inventory, starting_money, self.timeseries)

        for t in range(0, len(self.trend) - 1, self.skip):
            action = self.act(state)
            if action == 1 and starting_money >= self.trend[t]:
                inventory.append(self.trend[t])
                starting_money -= self.trend[t]

            elif action == 2 and len(inventory):
                bought_price = inventory.pop(0)
                starting_money += self.trend[t]
                invest = ((self.trend[t] - bought_price) / bought_price) * 100
                invests.append(invest)

            state = self.get_state(
                t + 1, inventory, starting_money, self.timeseries
            )
        invests = np.mean(invests)
        if np.isnan(invests):
            invests = 0
        score = (starting_money - initial_money) / initial_money * 100
        return invests * 0.7 + score * 0.3

    def fit(self, iterations, checkpoint):
        self.es.train(iterations, print_every = checkpoint)

    def buy(self):
        initial_money = self._scaled_capital
        starting_money = initial_money

        real_initial_money = self.initial_money
        real_starting_money = self.initial_money
        inventory = []
        real_inventory = []
        state = self.get_state(0, inventory, starting_money, self.timeseries)
        states_sell = []
        states_buy = []

        for t in range(0, len(self.trend) - 1, self.skip):
            action, prob = self.act_softmax(state)
#             print(t, prob)

            if action == 1 and starting_money >= self.trend[t] and t < (len(self.trend) - 1 - window_size):
                inventory.append(self.trend[t])
                real_inventory.append(self.real_trend[t])
                real_starting_money -= self.real_trend[t]
                starting_money -= self.trend[t]
                states_buy.append(t)
                print(
                    'day %d: buy 1 unit at price %f, total balance %f'
                    % (t, self.real_trend[t], real_starting_money)
                )

            elif action == 2 and len(inventory):
                bought_price = inventory.pop(0)
                real_bought_price = real_inventory.pop(0)
                starting_money += self.trend[t]
                real_starting_money += self.real_trend[t]
                states_sell.append(t)
                try:
                    invest = (
                        (self.real_trend[t] - real_bought_price)
                        / real_bought_price
                    ) * 100
                except:
                    invest = 0
                print(
                    'day %d, sell 1 unit at price %f, investment %f %%, total balance %f,'
                    % (t, self.real_trend[t], invest, real_starting_money)
                )
            state = self.get_state(
                t + 1, inventory, starting_money, self.timeseries
            )

        invest = (
            (real_starting_money - real_initial_money) / real_initial_money
        ) * 100
        total_gains = real_starting_money - real_initial_money
        return states_buy, states_sell, total_gains, invest
    

def update_predict_db(id_symbol, predictions):
    db.query(CoinInfo).filter(CoinInfo.id == id_symbol).update({
        "prediction": predictions[0],
        "predictions": str(predictions)
    }, synchronize_session = False)
    db.commit()


# In[8]:


def add_to_db(klines, id):
    for kline in klines:
        klineDB = Kline(id_symbol = id,
                       Close_time = kline[6],
                       Open = kline[1],
                       High = kline[2],
                       Low = kline[3],
                       Close = kline[4],
                       Volume = kline[5])
        db.add(klineDB)
    return kline[6] + 1


# In[9]:


def crawl_to_db():
    coins = db.query(CoinInfo).filter(CoinInfo.isPrediction == 1).all()
    for coin in coins:
        try:
            max_close_time = db.query(func.max(Kline.Close_time)).filter(Kline.id_symbol == coin.id).scalar()
            if max_close_time:
                start_time = max_close_time + 1
            else:
                start_time = 0

            klines = client.get_klines(symbol = coin.symbol,
                        interval = client.KLINE_INTERVAL_1DAY, 
                        limit = 1000,
                        startTime = start_time)
            if klines:
                startTime = add_to_db(klines, coin.id)
                while len(klines) == 1000:
                    klines = client.get_klines(symbol = coin.symbol,
                                interval = client.KLINE_INTERVAL_1DAY, 
                                limit = 1000,
                                startTime = startTime)
                    startTime = add_to_db(klines, coin.id)
                db.commit()
        except Exception as e:
            print("crawl_to_db faild", e, coin.symbol)


# In[10]:


def simulation_trade():
    query = """SELECT id, `Close`, Volume, Close_time FROM klines WHERE id_symbol = {0} AND Close_time > {1} ORDER BY `Close_time` ASC"""
    symbols = pd.read_sql("SELECT * FROM coin_info WHERE isPrediction = 1", SQLALCHEMY_DATABASE_URI)
    for _, symbol in symbols.iterrows():
        try:
            with open(f'trade/{symbol.symbol}.pkl', 'rb') as handle:
                agent = pickle.load(handle)
            df = pd.read_sql(query.format(symbol.id, agent.max_close_time), SQLALCHEMY_DATABASE_URI)
            if df.shape[0] == 0:
                continue
            agent.max_close_time = df['Close_time'].max()
            for index, row in df.iterrows():
                data = [row['Close'], row['Volume']]
                result = agent.trade(data, row['id'])
                if result['status_code'] != 0:
                    save_trade_db(price = row['Close'], close_time = row['Close_time'], result=result, id_symbol=symbol.id, initial_money = agent.initial_money)
            with open(f'trade/{symbol.symbol}.pkl', 'wb') as handle:
                pickle.dump(agent, handle, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print("simulation_trade falid", e, symbol.symbol)
    try:
        db.execute("""UPDATE coin_info c
        JOIN ( SELECT id_symbol, SUM( gain ) total_gain FROM trade GROUP BY id_symbol ) a ON a.id_symbol = c.id 
        SET c.totalGain =  a.total_gain""")
        db.commit()
    except Exception as e:
        print("update totalGain faild", e)


# In[11]:


def predict():
    query = """SELECT `Close` FROM klines WHERE id_symbol = {0} ORDER BY `Close_time` ASC"""
    symbols = pd.read_sql("SELECT * FROM coin_info WHERE isPrediction = 1", SQLALCHEMY_DATABASE_URI)
    for _, symbol in symbols.iterrows():
        try:
            dt = pd.read_sql(query.format(symbol.id), SQLALCHEMY_DATABASE_URI)
            if dt.shape[0] < 180:
                predicted_stock_price = get_revert(dt)
            else:
                predict_model = PredictModel(dt, isPredict=True, symbol=symbol.symbol)
                predicted_stock_price = predict_model.predict()
            if predicted_stock_price:
                update_predict_db(symbol.id, predicted_stock_price)
        except Exception as e:
            print("predict faild" ,e, symbol.symbol)


# In[12]:


def job():
    try:
        crawl_to_db()
        simulation_trade()
        predict()
    except Exception as e:
        print("job faild", e)


# In[ ]:

if __name__ == '__main__':
    schedule.every().day.at("07:00:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


# In[ ]:




