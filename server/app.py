from socket import socket
from sys import int_info
from dotenv import load_dotenv
from os import path, getenv
from distutils.log import debug
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
import pigpio

load_dotenv(f"{path.dirname(__file__)}/.env")
load_dotenv(f"{path.dirname(__file__)}/.env.local")

# ||================================================================================================
# || LED CONTROL
# ||================================================================================================
ENV_DUMMY_MODE = "DUMMY_MODE"

in_example_mode = getenv(ENV_DUMMY_MODE, "false") == "true"

PIN_R = 3
PIN_G = 2
PIN_B = 4

current_color = ""

if not in_example_mode:
    pi = pigpio.pi()


def set_color(color):
    global current_color

    red = int(color[1:3], 16)
    green = int(color[3:5], 16)
    blue = int(color[5:7], 16)

    if in_example_mode:
        print(f"set color: r: {red}, g: {green}, b: {blue}")
    else:
        pi.set_PWM_dutycycle(PIN_R, red)
        pi.set_PWM_dutycycle(PIN_G, green)
        pi.set_PWM_dutycycle(PIN_B, blue)

    current_color = color
    return current_color


def led_off():
    pi.set_PWM_dutycycle(PIN_R, 0)
    pi.set_PWM_dutycycle(PIN_G, 0)
    pi.set_PWM_dutycycle(PIN_B, 0)


def led_on():
    global current_color
    if not current_color or current_color == "":
        set_color("#ffffff")
    else:
        set_color(current_color)


# ||================================================================================================
# || WEBSERVER
# ||================================================================================================
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"

CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/desk_control/api/state", methods=["GET"])
def state():
    return {"color": current_color}


@app.route("/desk_control/api/on", methods=["GET"])
def on():
    led_on()
    socketio.emit("color", current_color)
    return {"color": current_color}


@app.route("/desk_control/api/off", methods=["GET"])
def off():
    led_off()
    socketio.emit("color", current_color)
    return {"color": current_color}


@app.route("/desk_control/api/color", methods=["POST"])
def color():
    set_color(request.form.get("color"))
    socketio.emit("color", current_color)
    return {"color": current_color}


@socketio.on("color")
def on_color(data):
    set_color(data)
    emit("color", current_color, include_self=False, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True, port=5000)