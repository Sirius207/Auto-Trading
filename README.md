# Auto-Trading

A Actor Critic Based Stock trader program


## Stock Data Format

| Open                | High       | Low | Close | 
| -------------------- | ----------| ---- | --- | 
| 209.894836 | 216.427353 | 207.758728 |216.208771 |
| ... | ...  |  ... |  ...  |  


## Usage

```
python trader.py --training training_data.csv --testing testing_data.csv --output output.csv
```