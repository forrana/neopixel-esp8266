import json


class GlobalVars(object):
    def __init__(self, program_number, led_color):
        self.state = {}
        if program_number:
            self.state['program_number'] = program_number
        if led_color:
            self.state['led_color'] = led_color

    @property
    def program_number(self): 
        return self.state.get('program_number')

    @property
    def led_color(self): 
        return self.state.get('led_color')
    
    @led_color.setter 
    def led_color(self, value):
        self.state['led_color'] = value
        self.save_state()
    
    @program_number.setter
    def program_number(self, value):
        self.state['program_number'] = value
        self.save_state()
    
    def save_state(self):
        f = open('state.txt', 'w')
        f.write(json.dumps(self.state))
        f.close()
    
    def load_state(self):
        f = None
        try:
            f = open('state.txt')
            state_string = f.readline()
            if state_string:
                self.state = json.loads(state_string)
        except:
            print('File does not exist')
            pass
        finally:
            if f:
                f.close()
           

manager = GlobalVars(1, (166, 16, 30, 100))
manager.load_state()

