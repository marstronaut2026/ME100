import time
import math as m
import matplotlib.pyplot as plt
import numpy as np


f = open("polyfit.txt","r")
coef = []
for i in f:
    coef.append(float(i))

# for j in range(len(coef)):
#     print("Coef {0}: {1}\n".format(j,coef[j]))
t0 = time.time()

t = (time.time()-t0)
data = (coef[0]*t[-1]**6+coef[1]*t[-1]**5+coef[2]*t[-1]**4+coef[3]*t[-1]**3+coef[4]*t[-1]**2+coef[5]*t[-1]+coef[6])

# while True:

#     t = []
#     data = []

    
    # for i in range(150):
    #     t.append(time.time()-t0)
    #     data.append(coef[0]*t[-1]**6+coef[1]*t[-1]**5+coef[2]*t[-1]**4+coef[3]*t[-1]**3+coef[4]*t[-1]**2+coef[5]*t[-1]+coef[6])

    #     print("{},{},{}".format(t[-1],data[-1],len(t)))

    #     plt.ion()
    #     plt.cla()
    #     plt.plot(t,data,'b',label='data')
    #     plt.legend()
    #     plt.pause(0.05)
    # break
        

