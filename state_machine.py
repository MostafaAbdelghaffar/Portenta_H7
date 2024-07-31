# Define states with integers
STATE_INIT = 0
STATE_DETECT = 1
STATE_CALCULATE = 2
STATE_ANALYZE = 3
STATE_DRAW = 4
STATE_FINISH = 5

class StateMachine:
    def __init__(self):
        self.state = STATE_INIT

    def next_state(self):
        if self.state == STATE_INIT:
            self.state = STATE_DETECT
        elif self.state == STATE_DETECT:
            self.state = STATE_CALCULATE
        elif self.state == STATE_CALCULATE:
            self.state = STATE_ANALYZE
        elif self.state == STATE_ANALYZE:
            self.state = STATE_DRAW
        elif self.state == STATE_DRAW:
            self.state = STATE_FINISH
        elif self.state == STATE_FINISH:
            self.state = STATE_INIT  # Loop back to SETUP or handle as needed

    def reset(self):
        self.state = STATE_INIT
    def get_state(self):
        return self.state
    def detect_state(self):
        self.state = STATE_DETECT
    def calculate_state(self):
        self.state = STATE_CALCULATE
