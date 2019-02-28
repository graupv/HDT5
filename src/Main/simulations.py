'''
Hoja de Trabajo 5   -   Simulaciones discretas en Simpy

Kristen Brandt - 171482
Gerardo Pineda - 18848

'''
import simpy
import random
from math import sqrt

class Data:
    res = []
    avg = 0
    rams = []
    #   variables estaticas

    @classmethod
    def set_avg(self):
        self.avg = sum(self.res) / len(self.res)

    @classmethod
    def get_avg(self):
        return self.avg

    def __str__(self):
        return f'Procesos: {len(self.res)}\nPromedio: {self.avg}\nDesviacion: {self.get_stdv()}\nTiempo Max: {max(self.res)}\nMin RAM: {min(self.rams)}'

    @classmethod
    def get_stdv(self):
        total = 0
        for x in self.res:
            total += ((x - self.avg)**2)
        return str(sqrt(total / len(self.res)))

def print_stats(res):
    print(f'{res.count} of {res.capacity} slots are allocated.')
    print(f'\tUsers: {res.users}')
    print(f'\tQueued events: {res.queue}')

def proceso(env, nram, ram, cpu, inst):
    print(f'Instructions: {inst}')
    print(f'RAM Needed: {nram}')
    print(f'RAM Available: {ram.level}')
    Data.rams.append(ram.level)
    start = env.now #   tiempo en que instancia el proceso
    # while ram.level < nram:
        #   "cola"
        # yield env.timeout(1)
        #   esperar un ciclo de reloj mientras se libera memoria
        #   yield para devolver control al ciclo

    yield ram.get(nram)
    #   allocate ram
    #   new -> Ready
    # print('***Before cpu request:\n'.upper())
    # print_stats(cpu)

    if inst > 2:
        while inst > 2:
            with cpu.request() as proc:
                # print('***Requested CPU:\n'.upper())
                # print_stats(cpu)
                yield proc
                yield env.timeout(1)    
                inst -= 3
                #   simula procesamiento de 3 instrucciones
                # print('***Post Yield, inst -3:'.upper())
                # print('***inst left:', inst, '\n')
                #   fin with devuelve el CPU 
                
            # print('***Outside WITH, releasing cpu:\n'.upper())
            # print_stats(cpu)
            #   random int para ver si va a cola de waiting o regresa a ready
            if random.randint(1, 2) == 2:
                yield env.timeout(1)
                #   simular operaciones I/O, regresa a cola para pedir cpu luego de 1 ciclo
    else:
        #   2 o menos instrucciones,
        #   si el proceso tiene 2 o menos instrucciones simula un solo ciclo
        #   ya que si tiene mas al llegar a 2 se libera anticipadamente.
        with cpu.request() as proc:
                # print('***Requested CPU:\n'.upper())
                # print_stats(cpu)
                yield proc
                yield env.timeout(1)  
    # print('***Outside while, process Terminated:\n'.upper())
    print('final time:', (env.now))
    Data.res.append(env.now - start)
    yield ram.put(nram) #   devolver memoria utilizada
    env.exit()  #   finalizado proceso, terminado.
    
def get_int():
    p = input()
    while not p.isdigit():
        p = input()
    return int(p)

def process_gen(env, RAM, CPU, procesos=25, rate=10):
    for x in range(procesos):
        yield env.timeout(random.expovariate(1/rate))
        print("\nProcess #", x + 1)
        print('Time:', env.now, '\n')
        env.process(proceso(env, ram=RAM, cpu=CPU, nram=random.randint(1, 10), inst=random.randint(1, 10)))

#   fin setup.
random.seed(3716) 
# fijar seed de random


def run():
    Data.res = []
    env = simpy.Environment()
    #   ambiente de simulacion
    RAM = simpy.Container(env, capacity=100, init=100)
    #   100 Unidades de RAM, 
    # en algunos casos se cambia capacity e init a 200
    CPU = simpy.Resource(env, capacity=1)
    #   Para algunas simulaciones hay que cambiar capacity de CPU a 2
    print('Ingresar numero de procesos: ')
    p = get_int()
    print('Ingresar ritmo de generacion: ')
    r = get_int()
    env.process(process_gen(env, RAM, CPU, p, rate=r))
    
    env.run()
    Data.set_avg()
    d = Data()
    print("\nResumen:\n")
    print(d)

#   25, 50, 100, 200, 250
#   100 procesos necesita 800 simulation time
if __name__ == '__main__':
    run()
