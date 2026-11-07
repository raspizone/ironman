from machine import Pin, PWM
import time

# --- CONFIGURACIÓN DE PINES Y PWM ---
pwm_top = PWM(Pin(26), freq=50)
pwm_bottom = PWM(Pin(25), freq=50)
action_pin = Pin(17, Pin.IN, Pin.PULL_UP)

# --- CONSTANTES DE POSICIÓN ---
TOP_CERRADO = 167
BOTTOM_CERRADO = 107

TOP_ABIERTO = 110
BOTTOM_ABIERTO = 30

# Variable de estado (False = Cerrado, True = Abierto)
estado_abierto = False

def angulo_a_duty(angulo):
    us = 500 + (2500 - 500) * angulo / 180
    return int(us * 65535 / 20000)

def mover_servos_directo(top, bottom):
    pwm_top.duty_u16(angulo_a_duty(top))
    pwm_bottom.duty_u16(angulo_a_duty(bottom))

def ejecutar_apertura():
    global estado_abierto
    print("Iniciando secuencia de apertura...")
    mover_servos_directo(TOP_ABIERTO, BOTTOM_ABIERTO)
    estado_abierto = True
    print("Apertura completada.")

def ejecutar_cierre():
    global estado_abierto
    print("Iniciando secuencia de cierre...")
    mover_servos_directo(TOP_CERRADO, BOTTOM_CERRADO)
    estado_abierto = False
    print("Cierre completado.")

# --- INICIALIZACIÓN ---
# Al encender, se coloca directamente en estado CERRADO
ejecutar_cierre()

# --- BUCLE PRINCIPAL ---
while True:
    if action_pin.value() == 0:  # Al presionar el botón (PULL_UP detecta LOW)
        if estado_abierto:
            ejecutar_cierre()
        else:
            ejecutar_apertura()
            
        time.sleep_ms(500)  # Antirrebote para evitar múltiples disparos al presionar
    
    time.sleep_ms(20)