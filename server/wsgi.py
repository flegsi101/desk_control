from app import app
import led_controller

if __name__ == "__main__":
    led_controller.run()
    app.run()