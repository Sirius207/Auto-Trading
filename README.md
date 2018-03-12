# Auto-Trading

An Actor Critic Based stock trader program


## Usage

```
python trader.py --training training_data.csv --testing testing_data.csv --output output.csv
```


## Predict Algorithm



## Stock Policy



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

training data:
https://www.dropbox.com/s/2lzkd5oj6pm6zk9/training_data.csv?dl=0
testing data:
https://www.dropbox.com/s/0p6mx922eafy6tm/testing_data.csv?dl=0


## Output Sample:
1. Each line in output file contains the action type which will be executed in the opening of the next day.

2. If the testing data contains 300 lines, the output would include 299 lines. But the last day will be settled without executing the specified action, and the calculator will use the close price of the last day as the settled price.
