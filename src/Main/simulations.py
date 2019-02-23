
import simpy
import random
import timeit



class Resultado:
    totes = 0

    @classmethod
    def set_totes(self, n):
        self.totes = n



def thing(env, nram, ram, cpu, inst):
    ready = False
    #   definir como va a fucionar la cola
    #   pedir la ram si hay hacer el proceso si no esperar
    #   devolver resultado
    
    # if RAM
    start = env.now
    with ram.request() as mem:
        if mem > 0:
            ready = True
            yield mem
        
    pass
           

# ----------------------

env = simpy.Environment() 
#   ambiente de simulacion
RAM = simpy.Container(env, capacity=100, init=100)
#   100 Unidades de RAM
CPU = simpy.Resource(env, capacity=1)   
#   "Podra incrementarse", significa + capacity?
#   simpy.Resource == Shared resources inside environment
random.seed(666) # fijar el inicio de random

x = 25
#   25, 50, 100, 200, 250
for i in range(x):
    env.process(thing(env, ram=RAM, cpu=CPU, nram=random.randint(1, 10), inst=random.randint(1, 3)))
    #   instanciamos el objeto a simular -> se agrega a environment 
    #   (simpy env, resource_ram, resource_cpu, cantidad de ram necesaria, cantidad de intrucciones a realizar)

env.run(until=50)  #correr la simulaci�n hasta el tiempo = 50