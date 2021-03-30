def ledpwm():

    from machine import Pin, PWM
    import time

    led = PWM(Pin(14),freq=5000)

    while True:
        for cycle in range(0,100):
            led.duty(cycle)
            time.sleep_ms(20)
        for cycler in range(0,100):
            led.duty(100-cycler)
            time.sleep_ms(20)


    


