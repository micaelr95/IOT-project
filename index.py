from flask import Flask, render_template
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

LDR_PIN = 17
SM_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LDR_PIN, GPIO.OUT)
GPIO.output(LDR_PIN, GPIO.LOW)

@app.route("/")
def index():
    GPIO.setup(LDR_PIN, GPIO.IN)
    templateData = {
        'ldr': GPIO.input(LDR_PIN)
    }
    return render_template("index.html", **templateData)

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True)
