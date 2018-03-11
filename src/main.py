import pandas as pd
import numpy as np
import tensorflow as tf

from env import Env
from predict import predict
Train_df = pd.read_csv('../data/training_data.csv', names = ["Open", "High", "Low", "Close"])
Test_df = pd.read_csv('../data/testing_data.csv', names = ["Open", "High", "Low", "Close"])
env = Env(Train_df)
predict = predict()

np.random.seed(2)
tf.set_random_seed(2)  # reproducible

# Superparameters
OUTPUT_GRAPH = False
MAX_EPISODE = 30
DISPLAY_REWARD_THRESHOLD = 200  # renders environment if total episode reward is greater then this threshold
MAX_EP_STEPS = 1000   # maximum time step in one episode
RENDER = False  # rendering wastes time
GAMMA = 0.9     # reward discount in TD error
LR_A = 0.001    # learning rate for actor
LR_C = 0.01     # learning rate for critic

N_F = 3 # mean & curve & block
N_A = 5 # 0, 1, 2, 3, 4

class Actor(object):
    def __init__(self, sess, n_features, n_actions, lr=0.001):
        self.sess = sess

        self.s = tf.placeholder(tf.float32, [1, n_features], "state")
        self.a = tf.placeholder(tf.int32, None, "act")
        self.td_error = tf.placeholder(tf.float32, None, "td_error")  # TD_error

        with tf.variable_scope('Actor'):
            l1 = tf.layers.dense(
                inputs=self.s,
                units=20,    # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),    # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='l1'
            )

            self.acts_prob = tf.layers.dense(
                inputs=l1,
                units=n_actions,    # output units
                activation=tf.nn.softmax,   # get action probabilities
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='acts_prob'
            )

        with tf.variable_scope('exp_v'):
            log_prob = tf.log(self.acts_prob[0, self.a])
            self.exp_v = tf.reduce_mean(log_prob * self.td_error)  # advantage (TD_error) guided loss

        with tf.variable_scope('train'):
            self.train_op = tf.train.AdamOptimizer(lr).minimize(-self.exp_v)  # minimize(-exp_v) = maximize(exp_v)

    def learn(self, s, a, td):
        s = s[np.newaxis, :]
        feed_dict = {self.s: s, self.a: a, self.td_error: td}
        _, exp_v = self.sess.run([self.train_op, self.exp_v], feed_dict)
        return exp_v

    def choose_action(self, s):
        s = s[np.newaxis, :]
        probs = self.sess.run(self.acts_prob, {self.s: s})   # get probabilities for all actions
        return np.random.choice(np.arange(probs.shape[1]), p=probs.ravel())   # return a int

class Critic(object):
    def __init__(self, sess, n_features, lr=0.01):
        self.sess = sess

        self.s = tf.placeholder(tf.float32, [1, n_features], "state")
        self.v_ = tf.placeholder(tf.float32, [1, 1], "v_next")
        self.r = tf.placeholder(tf.float32, None, 'r')

        with tf.variable_scope('Critic'):
            l1 = tf.layers.dense(
                inputs=self.s,
                units=20,  # number of hidden units
                activation=tf.nn.relu,  # None
                # have to be linear to make sure the convergence of actor.
                # But linear approximator seems hardly learns the correct Q.
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='l1'
            )

            self.v = tf.layers.dense(
                inputs=l1,
                units=1,  # output units
                activation=None,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='V'
            )

        with tf.variable_scope('squared_TD_error'):
            self.td_error = self.r + GAMMA * self.v_ - self.v
            self.loss = tf.square(self.td_error)    # TD_error = (r+gamma*V_next) - V_eval
        with tf.variable_scope('train'):
            self.train_op = tf.train.AdamOptimizer(lr).minimize(self.loss)

    def learn(self, s, r, s_):
        s, s_ = s[np.newaxis, :], s_[np.newaxis, :]

        v_ = self.sess.run(self.v, {self.s: s_})
        td_error, _ = self.sess.run([self.td_error, self.train_op],
                                          {self.s: s, self.v_: v_, self.r: r})
        return td_error

sess = tf.Session()

actor = Actor(sess, n_features=N_F, n_actions=N_A, lr=LR_A)
critic = Critic(sess, n_features=N_F, lr=LR_C)     # we need a good teacher, so the teacher should learn faster than the actor

sess.run(tf.global_variables_initializer())



if OUTPUT_GRAPH:
    tf.summary.FileWriter("logs/", sess.graph)

# Training
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


s = np.array([0,0,0])

error = 0
correct = 0
error_1 = 0
error_2 = 0

# user state
hold = 0
money = 0

for day in range(len(Test_df['Open'])):
    # Predict Trend
    trend = actor.choose_action(s)

    # Buy or Sold
    action = predict.action(hold, trend)
    #
    # New Day
    #
    price = Test_df['Open'][day]
    predict.push_data(price)

    # Check money after day 0 (day start from 0)
    if(day > 0):
        print("day: ", day, "state: ", s, " ------ today: ", (s[2] - 2) ,"predict tomorrow: ", (trend - 2) , " ------- hold: ", hold, " action: ", action, "money: ", money)
        money, hold = predict.check_money(hold, action, money, price)

    s = predict.get_new_state(day, s)

    if(day + 1 == len(Test_df['Open'])):
        if (hold == 1):
            money += Test_df['Close'][day]
        elif (hold == -1):
            money -= Test_df['Close'][day]
        print("final money: ", money)

    # error check    
    if(np.absolute(trend - s[2]) == 0):
        correct += 1
    elif(np.absolute(trend - s[2]) == 1):
        error_1 += 1
    else:
        error_2 += 2

print("correct: ", correct)
print("error_1: ", error_1)
print("error_2: ", error_2)
