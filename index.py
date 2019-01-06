from flask import Flask, render_template
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Guarda os pinos onde estao conetados os sensores e os atuadores
LDR_PIN = 17
SM_PIN = 18

# Guarda o estado do atuador
sm_state = 7.5

# Iniciação do GPIO
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(LDR_PIN, GPIO.OUT)
GPIO.setup(SM_PIN, GPIO.OUT)
GPIO.output(LDR_PIN, GPIO.LOW)
GPIO.setup(LDR_PIN, GPIO.IN)
pwm=GPIO.PWM(SM_PIN, 50)
pwm.start(sm_state)

@app.route("/")
def index():
    '''Função principal que retorna o index'''
    ldr_state = GPIO.input(LDR_PIN)
    # Se não houver luz fecha o servomotor senao abre
    if ldr_state==0:
        sm_state = 7.5
    else:
        sm_state = 12.5

    # Muda o valor do servomotor
    pwm.ChangeDutyCycle(sm_state)
    # Dicionario que guarda as variaveis para a página
    templateData = {
        'ldr': ldr_state,
        'sm': sm_state
    }
    return render_template("index.html", **templateData)

@app.route("/<devicename>/<action>")
def control(devicename, action):
    '''Função para controlar os atuadores. Recebe o nome do atuador e o valor'''
    if devicename == "sm":
        sm_state = (float(action))
        # Muda o valor do servomotor
        pwm.ChangeDutyCycle(sm_state)
    # Dicionario que guarda as variaveis para a página
    templateData = {
        'ldr': GPIO.input(LDR_PIN),
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
