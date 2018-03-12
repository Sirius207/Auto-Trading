import pandas as pd
import numpy as np
import tensorflow as tf

from env import Env
from predict import predict

from rl import (Actor, Critic)

LR_A = 0.001    # learning rate for actor
LR_C = 0.01     # learning rate for critic
MAX_EPISODE = 25
N_F = 3         # mean & curve & block
N_A = 5         # 0, 1, 2, 3, 4

if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
    args = parser.parse_args()

    Train_df = pd.read_csv('../data/training_data.csv', names = ["Open", "High", "Low", "Close"])

    #
    # Training
    #
    env = Env(Train_df)
    sess = tf.Session()

    actor = Actor(sess, n_features=N_F, n_actions=N_A, lr=LR_A)
    critic = Critic(sess, n_features=N_F, lr=LR_C)     # we need a good teacher, so the teacher should learn faster than the actor

    sess.run(tf.global_variables_initializer())

    for i_episode in range(MAX_EPISODE):
        s = np.array([0,0,0])
        t = 0
        track_r = []
        while True:
            a = actor.choose_action(s)

            s_, r, done = env.step(t, s, a)

            if (done):
                ep_rs_sum = sum(track_r)
                print("episode:", i_episode, "  reward:", int(ep_rs_sum))
                break

            else:
                track_r.append(r)

                td_error = critic.learn(s, r, s_)  # gradient = grad[r + gamma * V(s_) - V(s)]
                actor.learn(s, a, td_error)     # true_gradient = grad[logPi(s,a) * td_error]

                s = s_
                t += 1

    #
    # Testing
    #
    Test_df = pd.read_csv('../data/testing_data.csv', names = ["Open", "High", "Low", "Close"])
    predict = predict()

    # Initial State
    s = np.array([0,0,0])
    hold = 0
    money = 0

    with open(args.output, 'w') as output_file:
        for day in range(len(Test_df['Open'])):
            # Predict Trend
            trend = actor.choose_action(s)

            # Action Type
            action = predict.action(hold, trend)
            print("day: ", day, "state: ", s, " ------ today: ", (s[2] - 2) ,"predict tomorrow: ", (trend - 2) , " ------- hold: ", hold, " action: ", action, "money: ", money)

            #
            # New Day
            #
            price = Test_df['Open'][day]
            if (day > 0):
                money, hold = predict.check_money(hold, action, money, price)

            # Last day should not output action
            if (day + 1 != len(Test_df['Open'])):
                output_file.write(str(action) + "\n")

            # Change State
            predict.push_data(price)
            s = predict.get_new_state(day, s)






