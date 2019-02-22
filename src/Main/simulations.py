
import simpy
import random


totalDia = None
def process(env, ram, cpu):
    #   definir como va a fucionar la cola
    #   pedir la ram si hay hacer el proceso si no esperar
    #   devolver resultado

    # if RAM
    
    pass
           

# ----------------------

env = simpy.Environment() 
#   ambiente de simulacion
RAM = simpy.Container(env, capacity=100, init=100)
#   100 Unidades de RAM
CPU = simpy.Resource(env, capacity=1)
#   1 Core
Queue = simpy.Resource(env, capacity=1) # ?
random.seed(10) # fijar el inicio de random

x = 25
#   25, 50, 100, 200, 250
for i in range(x):
    env.process(process(env, RAM, CPU))

env.run(until=50)  #correr la simulaci�n hasta el tiempo = 50

print ("tiempo promedio por vehiculo es: ", totalDia/x)