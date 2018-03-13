# Auto-Trading

An Actor Critic Based stock trader program


## Usage

```
python trader.py --training training_data.csv --testing testing_data.csv --output output.csv
```


## Strategy

Use [Actor Critic  Algorithms](http://rll.berkeley.edu/deeprlcourse/f17docs/lecture_5_actor_critic_pdf.pdf) ([Source](https://morvanzhou.github.io/tutorials/machine-learning/reinforcement-learning/6-1-actor-critic/)) to predict stock trend of tomorrow, and use simple judge policy to do action according to the predict trend.

### State of Actor Critic
- Moving average (10 days)
- Difference of today moving average & yesterday moving average
- Magnitude of difference of moving average: [0,1,2,3]  (means fall, decline, flat, rise)

### Predict Trend 
(As Action of Actor Critic) 
(Should equal to the Magnitude of difference of moving average tomorrow)
Value
- 0: fall
- 1: decline
- 2: flat
- 3: rise

### Hold State
- -1: short 1 stock
- 0: no stock
- 1: hold 1 stock

### Action
- 1: buy
- 0: no action
- -1: sold (or short)

### Action Strategy
```
if(hold == 0):
  if(trend_of_tomorrow > 1):
    action = 1
  else:
    action = -1
elif(hold == 1):
  if(trend_of_tomorrow > 1):
    action = 0
  else:
    action = -1
else:
  if(trend_of_tomorrow < 3):
    action = 0
  else:
    action = 1
```

---

## Stock Data Format

| Open                | High       | Low | Close | 
| -------------------- | ----------| ---- | --- | 
| 209.894836 | 216.427353 | 207.758728 |216.208771 |
| ... | ...  |  ... |  ...  |  


## Action Type

The action should be one of these three types:
1 → means to “Buy” the stock. If you short 1 unit, you will return to 0 as the open price in the next day. If you did not have any unit, you will have 1 unit as the open price in the next day. “If you already have 1 unit, your code will be terminated due to the invalid status.“

0 → means to “NoAction”. If you have 1-unit now, hold it. If your slot is available, the status continues. If you short 1 unit, the status continues.

-1 → means to “Sell” the stock. If you hold 1 unit, your will return to 0 as the open price in the next day. If you did not have any unit, we will short 1 unit as the open price in the next day. “If you already short 1 unit, your code will be terminated due to the invalid status.“

In the final day, if you hold/short the stock, we will force your slot empty as the close price of the final day in the testing period. Finally, your account will be settled and your profit will be calculated.


## Input Sample:

- training data: https://www.dropbox.com/s/2lzkd5oj6pm6zk9/training_data.csv?dl=0
- testing data: https://www.dropbox.com/s/0p6mx922eafy6tm/testing_data.csv?dl=0


## Output Sample:
1. Each line in output file contains the action type which will be executed in the opening of the next day.

2. If the testing data contains 300 lines, the output would include 299 lines. But the last day will be settled without executing the specified action, and the calculator will use the close price of the last day as the settled price.
