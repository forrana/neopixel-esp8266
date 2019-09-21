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
    
    @property
    def led_color_hex(self):
        return "%0.2X%0.2X%0.2X" % (self.state['led_color'][0], self.state['led_color'][1], self.state['led_color'][2])
    
    @led_color.setter 
    def led_color(self, value):
        if isinstance(value, tuple):
            self.state['led_color'] = value
        elif isinstance(value, str):
            new_color = value.replace("#", "")
            color_array_hex = [new_color[i:i+2] for i in range(0, len(new_color), 2)]
            color_array_hex.append('00')
            color_array_decimal = map(lambda  x:int(x,16), color_array_hex)
            self.state['led_color'] = tuple(color_array_decimal)
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

