from machine import Pin, PWM
import array as arr
import time
import math as m

def ctrl():
    servo = PWM(Pin(14),freq=50,duty=7)
    duty_cycle = arr.array('i',[3,7,11])
    time.sleep(1) #give time to get to center position

    try:
        while True:
            # servo.duty(int(input("Enter servo position: ")))
            # for i in range(3):
            #     servo.duty(duty_cycle[i])
            #     time.sleep(2)
            
            for i in range(60):
                du = float(m.sin(i/30*m.pi)*4+7)
                servo.duty(du)
                print(du)
                time.sleep_ms(50)


#3-11 in 50 steps

    except KeyboardInterrupt:
        print("\nReturning to sleep position...")
        servo.duty(3)
        time.sleep(1)
        servo.deinit()
        print("\nGoodbye.")