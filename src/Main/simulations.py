
import simpy
import random
import timeit

class Computer:

    def __init__(self, env):
        all_the_times = []
        self.cpu = simpy.Resource(env, capacity=1)
        self.ram = simpy.Container(env, capacity=100, init=100)

    def buf(self, x):
        return self.ram.level >= x

class Resultados:
    totes = 0
    mcgoats = []

    @classmethod
    def set_totes(self, n):
        self.totes += n

    @classmethod
    def add_goats(self, n):
        self.mcgoats.append(n)

def print_stats(res):
    print('%d of %d slots are allocated.' % (res.count, res.capacity))
    print('  Users:', res.users)
    print('  Queued events:', res.queue)

def proceso(env, nram, ram, cpu, inst):   
    start = env.now #   tiempo en que instancia el proceso
    while ram.level < nram:
        #   "cola"
        yield env.timeout(1)
        #   esperar un ciclo de reloj mientras se libera memoria
        #   yield para devolver control al ciclo

    gotMem = env.now - start
    yield ram.get(nram)
    #   allocate ram
    with cpu.request() as proc:
        while inst > 2:
            inst -= 3
            yield env.timeout(1)
            #   devuelve el CPU por 1 ciclo de reloj
            
        print_stats(proc)
        Resultados.add_goats(env.now - gotMem)
        # timeout == tiempo de realizar proceso
    #   finalizado el proceso, devolver ram
    # Resultados.mcgoats(env.now - gotMem)
    yield ram.set(nram)

# ----------------------

env = simpy.Environment() 
#   ambiente de simulacion
RAM = simpy.Container(env, capacity=100, init=100)
#   100 Unidades de RAM
CPU = simpy.Resource(env, capacity=1)
#   "Podra incrementarse", significa + capacity?

random.seed(666) # fijar el inicio de random

x = 25
#   25, 50, 100, 200, 250
for i in range(x):
    #   falta setear el ritmo al que se generan
    #   es el random.expovariate(n/10)
    env.process(proceso(env, ram=RAM, cpu=CPU, nram=random.randint(1, 10), inst=random.randint(1, 10)))
    #   instanciamos el objeto a simular -> se agrega a environment 
    #   (simpy env, resource_ram, resource_cpu, cantidad de ram necesaria, cantidad de intrucciones a realizar)

env.run(until=50)  #correr la simulaci�n hasta el tiempo = 50