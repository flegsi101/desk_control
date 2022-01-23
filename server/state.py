import json
import pigpio

PIN_R = 3
PIN_G = 2
PIN_B = 4

class State():

    color: str = ""
    on: bool = False

    def __init__(self):
        self.pi = pigpio.pi()
        try:
            stored = json.load(open("state.json"))
            self.color = stored.get("color", "#000000")
            self.on = stored.get("on", False)
            stored.close()
        except:
            pass

    def update(self, color: str, on: bool):
        self.color = color
        self.on = on

        stored = open("state.json", "w")
        stored.write(json.dumps({"color": self.color, "on": self.on}))
        stored.close()

        self._set_state()

    def off(self): 
        self.pi.set_PWM_dutycycle(PIN_R, 0)
        self.pi.set_PWM_dutycycle(PIN_G, 0)
        self.pi.set_PWM_dutycycle(PIN_B, 0)

    def _set_state(self):
        red = int(self.color[1:3], 16)
        green = int(self.color[3:5], 16)
        blue = int(self.color[5:7], 16)
        self.pi.set_PWM_dutycycle(PIN_R, red)
        self.pi.set_PWM_dutycycle(PIN_G, green)
        self.pi.set_PWM_dutycycle(PIN_B, blue)
