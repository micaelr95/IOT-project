from flask import Flask, render_template
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

LDR_PIN = 17
SM_PIN = 18
sm_state = 7.5

GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
GPIO.setup(LDR_PIN, GPIO.OUT)
GPIO.setup(SM_PIN, GPIO.OUT)
GPIO.output(LDR_PIN, GPIO.LOW)
GPIO.setup(LDR_PIN, GPIO.IN)
pwm=GPIO.PWM(SM_PIN, 50)
pwm.start(sm_state)

@app.route("/")
def index():
    ldr_state = GPIO.input(LDR_PIN)
    if ldr_state==0:
        sm_state = 7.5
    else:
        sm_state = 12.5

    pwm.ChangeDutyCycle(sm_state)
    templateData = {
        'ldr': ldr_state,
        'sm': sm_state
    }
    return render_template("index.html", **templateData)

if __name__ == "__main__":
    try:
        app.run(host= '0.0.0.0', debug=True)
    except KeyboardInterrupt:
        print('Key Interrupt')
    finally:
        print("STOP")
        pwm.stop()
        GPIO.cleanup()
    
