# data analysis and wrangling
import pandas as pd
import numpy as np
import random as rnd



# machine learning
# from sklearn.linear_model import LogisticRegression
# from sklearn.svm import SVC, LinearSVC
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.naive_bayes import GaussianNB
# from sklearn.linear_model import Perceptron
# from sklearn.linear_model import SGDClassifier
# from sklearn.tree import DecisionTreeClassifier
train_df = pd.read_csv('./data/training_data.csv', names = ["Open", "High", "Low", "Close"])
test_df = pd.read_csv('./data/testing_data.csv', names = ["Open", "High", "Low", "Close"])

# print(train_df.columns)
# train_df.head(2)
# MAX_MOVING_AVG_LEN = 10


# def _cal_moving_avg(day):
#     total = 0
#     for index in range(MAX_MOVING_AVG_LEN):
#       if ((day - index) < 0):
#         total += train_df['Open'][0]
#       else:
#         total += train_df['Open'][day-index]
    
#     return (total / MAX_MOVING_AVG_LEN) - train_df['Open'][0]

# moving_avg = 0
# for day in range(100):
#   _moving_avg = _cal_moving_avg(day)
#   diff = _moving_avg - moving_avg
#   print(day," -- ",train_df['Open'][day], ": ", diff ," = ", _moving_avg, " - ", moving_avg)
#   moving_avg = _moving_avg


# Testing
predict = Env(Test_df)
s = np.array([0,0,0])
t = 0
track_r = []
while True:
    a = actor.choose_action(s)

    s_, r, done = predict.step(t, s, a)

    if done:
        ep_rs_sum = sum(track_r)
        print("final - reward: ", int(ep_rs_sum))
        break
    else:
        track_r.append(r)
        s = s_
        t += 1

