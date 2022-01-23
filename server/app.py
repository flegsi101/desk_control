
from flask import Flask, request

# ||================================================================================================
# || LED CONTROL
# ||================================================================================================




def set_color(color):
    global last_color

    red = int(color[1:3], 16)
    green = int(color[3:5], 16)
    blue = int(color[5:7], 16)

    print(f"set r:{red} g:{green} b:{blue}")

    pi.set_PWM_dutycycle(PIN_R, red)
    pi.set_PWM_dutycycle(PIN_G, green)
    pi.set_PWM_dutycycle(PIN_B, blue)

    last_color = color


def led_off():
    pi.set_PWM_dutycycle(PIN_R, 0)
    pi.set_PWM_dutycycle(PIN_G, 0)
    pi.set_PWM_dutycycle(PIN_B, 0)


def led_on():
    if not last_color or last_color == "":
        set_color("#ffffff")
    set_color(last_color)


# ||================================================================================================
# || WEBSERVER
# ||================================================================================================
app = Flask(__name__)


@app.route("/desk_control/api/state", methods = ["GET"])
def state():
    global last_color
    return {
        "color": last_color
    }


@app.route("/desk_control/api/on", methods = ["GET"])
def on():
    led_on()
    return ""


@app.route("/desk_control/api/off", methods = ["GET"])
def off():
    led_off()
    return ""


@app.route("/desk_control/api/color", methods = ["POST"])
def color():
    set_color(request.form.get("color"))
    return ""