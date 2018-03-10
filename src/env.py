import numpy as np

MAX_MOVING_AVG_LEN = 10


# class policy:
#     def _get_hold_type(self, hold_state, action):
#     _hold_state = hold_state + action
#     if (_hold_state > 1 || _hold_state < -1):
#       raise ValueError('action wrong') 
#     else:
#       return _hold_state

#   def _get_hold_price(self, hold_state, action, day):
#     if (action == 1):
#       if(hold_state[0] == 0):
#          _hold_price = -self.data['Open'][day+1]
#       elif(hold_state[0] == -1):
#         _hold_price = 0
#       else:
#         raise ValueError('action wrong') 

#     elif (action == -1):
#       if(hold_state[0] == 1):
#         _hold_price = 0
#       elif(hold_state[0] == 0):
#         _hold_price = self.data['Open'][day+1]
#       else:
#         raise ValueError('action wrong')

#     else:
#       _hold_price = hold_state[1]

#     return _hold_price



# s_, r, done
class env:
  def __init__(self, data):
    self.data = data


  def _cal_moving_avg(self, day):
    total = 0
    for index in range(MAX_MOVING_AVG_LEN):
      if ((day - index) < 0):
        total += self.data['Open'][0]
      else:
        total += self.data['Open'][day-index]
    
    return (total / MAX_MOVING_AVG_LEN) - self.data['Open'][0]

  def _cal_avg_change_trend(self, _avg_diff):
    if (_avg_diff > 1):
      _avg_change_period = 3
    elif(_avg_diff > 2):
      _avg_change_period = 4
    elif(_avg_diff < -2):
      _avg_change_period = 0
    elif(_avg_diff < -1):
      _avg_change_period = 1
    else:
      _avg_change_period = 2
    return _avg_change_period

  def _get_new_state(self, day, state, action):
    _moving_avg = self._cal_moving_avg(day)
    _avg_diff = _moving_avg - state[0]
    _avg_change_trend = self._cal_avg_change_trend(_avg_diff)
    
    _state = [_moving_avg, _avg_diff, _avg_change_trend]
    return np.array(_state)

  def _get_new_reword(self, day, state, action, _state):
    if (action - _state[2] > 1 or action - _state[2] < -1):
      reward = -50
    elif (action == _state[2]):
      reward = 20
    else:
      reward = 0

    return reward


  def step(self, day, state, action):
    if(day == (len(self.data['Open'])) - 1):
      done = True
      _state = 0
      reword = 0
    else:
      done = False
      _state = self._get_new_state(day, state, action)
      reword = self._get_new_reword(day, state, action, _state)
    
    return (_state, reword, done)



