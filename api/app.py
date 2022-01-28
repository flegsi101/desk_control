from enum import Enum
from socket import socket
from sys import int_info
from dotenv import load_dotenv
from os import path, getenv
from distutils.log import debug
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
import pigpio
import re

load_dotenv(f"{path.dirname(__file__)}/.env")
load_dotenv(f"{path.dirname(__file__)}/.env.local")


# ||================================================================================================
# || LED CONTROL
# ||================================================================================================
class ToggleState(Enum):
    OFF = 0
    ON = 1


class LedState:

    def __init__(self, color="#ffffff", state=ToggleState.OFF):
        self.__color = color
        self.__state = state

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color: str):
        if not re.match("^#[0-9,a-f]{6}$", color.lower()):
            raise Exception(f"Invalid color: {color}")
        self.__color = color

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state: ToggleState):
        self.__state = state

    @property
    def json(self):
        return {
            "color": self.__color,
            "state": self.__state.value,
        }


ENV_DUMMY_MODE = "DUMMY_MODE"
ENV_PIGPIO_HOST = "PIGPIO_HOST"

PIN_R = 3
PIN_G = 2
PIN_B = 4

in_example_mode = getenv(ENV_DUMMY_MODE, "false") == "true"
pigpio_host = getenv(ENV_PIGPIO_HOST, None)


if not in_example_mode:
    pi = pigpio.pi(host=pigpio_host)


def set_state(new_state: LedState):
    red = int(new_state.color[1:3], 16) * new_state.state.value
    green = int(new_state.color[3:5], 16) * new_state.state.value
    blue = int(new_state.color[5:7], 16) * new_state.state.value

    if in_example_mode:
        print(f"set color: r: {red}, g: {green}, b: {blue}")
    else:
        pi.set_PWM_dutycycle(PIN_R, red)
        pi.set_PWM_dutycycle(PIN_G, green)
        pi.set_PWM_dutycycle(PIN_B, blue)


# ||================================================================================================
# || WEBSERVER
# ||================================================================================================
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"

CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

current_state = LedState()

@socketio.on("connect")
def client_connect():
    global current_state
    emit("state", current_state.json)

@socketio.on("state")
def on_color(data):
    global current_state
    current_state.state = ToggleState(data.get("state"))
    current_state.color = data.get("color")
    set_state(current_state)
    emit("state", current_state.json, include_self=False, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)