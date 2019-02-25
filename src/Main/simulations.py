'''
Hoja de Trabajo 5   -   Simulaciones discretas en Simpy

Kristen Brandt - 1
Gerardo Pineda - 18848

'''

import simpy
import random

class Data:
    res = []
    std = 0
    avg = 0

    @classmethod
    def get_avg(self):
        self.avg = sum(self.res) / len(self.res)
        return self.avg

    @classmethod
    def get_stdv(self):

        return

def print_stats(res):
    print('%d of %d slots are allocated.' % (res.count, res.capacity))
    print('  Users:', res.users)
    print('  Queued events:', res.queue)

def proceso(env, nram, ram, cpu, inst):
    print('Instructions:', inst)
    start = env.now #   tiempo en que instancia el proceso
    while ram.level < nram:
        #   "cola"
        yield env.timeout(1)
        #   esperar un ciclo de reloj mientras se libera memoria
        #   yield para devolver control al ciclo

    yield ram.get(nram)
    gotMem = env.now - start
    print('got mem:', gotMem)
    #   allocate ram
    #   new -> Ready
    print('***Before cpu request:\n'.upper())
    print_stats(cpu)

    while inst > 2:
        with cpu.request() as proc:
        
            print('***Requested CPU:\n'.upper())
            print_stats(cpu)
            yield proc
            yield env.timeout(1)    
            inst -= 3
            #   simula procesamiento de 3 instrucciones
            print('***Post Yield, inst -3:'.upper())
            print('***inst left:', inst, '\n')
            print_stats(cpu)
            #   fin with devuelve el CPU por ciclo de reloj
            
        print('***Outside WITH, releasing cpu:\n'.upper())
        print_stats(cpu)
        #   random int para ver si va a cola de waiting o regresa a ready
        if random.randint(1, 2) == 2:
            yield env.timeout(1)
            #   simular operaciones I/O, regresa a cola para pedir cpu luego de 1 ciclo
    print('***Outside while, process Terminated:\n'.upper())
    print('final time:', (env.now))
    Data.res.append(env.now - start)
    yield ram.put(nram) #   devolver memoria utilizada
    env.exit()  #   finalizado proceso, terminado.
    

def process_gen(env, RAM, CPU, procesos=25):
    for x in range(procesos):
        yield env.timeout(random.expovariate(1/10))
        print("Process #", x + 1)
        env.process(proceso(env, ram=RAM, cpu=CPU, nram=random.randint(1, 10), inst=random.randint(1, 10)))

# ----------------------



random.seed(666) # fijar el inicio de random

from math import sqrt
def run():
    Data.res = []
    env = simpy.Environment()
    #   ambiente de simulacion
    RAM = simpy.Container(env, capacity=100, init=100)
    #   100 Unidades de RAM
    CPU = simpy.Resource(env, capacity=1)
    #   "Podra incrementarse", significa + capacity?
    p = int(input("Cuantos procesos desea simular: "))
    env.process(process_gen(env, RAM, CPU, p))
    x = int(input("Simulation time: "))
    env.run(until=x)
    Data.avg = sum(Data.res) / p
    print('Promedio:', Data.get_avg())
    # std = 0
    # for val in Data.res:
    #     sqrt((val - Data.avg)**2)
    # print('Desviacion estandar:', sum(Data.res) / p)
#   25, 50, 100, 200, 250
#   100 procesos necesita 800 simulation time

#   instanciamos el objeto a simular -> se agrega a environment 
#   (simpy env, container_ram, resource_cpu, cantidad de ram necesaria, cantidad de intrucciones a realizar)

# env.run(until=50)
# print('final time', t)