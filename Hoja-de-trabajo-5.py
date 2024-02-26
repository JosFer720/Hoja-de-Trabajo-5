import simpy
import random
import statistics
import matplotlib.pyplot as plt

RANDOM_SEED = 42
MEMORIA_RAM = 100  
VELOCIDAD_CPU = 3  

class Proceso:
    def __init__(self, env, nombre, memoria, instrucciones_totales):
        self.env = env
        self.nombre = nombre
        self.memoria = memoria
        self.instrucciones_totales = instrucciones_totales
        self.instrucciones_restantes = instrucciones_totales

    def run(self, cpu, ram):
        instrucciones_a_realizar = min(VELOCIDAD_CPU, self.instrucciones_restantes)
        yield self.env.timeout(1)  
        self.instrucciones_restantes -= instrucciones_a_realizar
        if self.instrucciones_restantes <= 0:
            return self.env.now  
        else:
            rand = random.randint(1, 21)
            if rand == 1:
                yield self.env.timeout(1)  
                with ram.get(self.memoria) as req:
                    yield req
                    return (yield from self.run(cpu, ram))
            elif rand == 2:
                with ram.get(self.memoria) as req:
                    yield req
                    return (yield from self.run(cpu, ram))
            else:
                with cpu.request() as req:
                    yield req
                    return (yield from self.run(cpu, ram))

def llegada_proceso(env, cpus, ram, procesos, intervalo):
    for i in range(procesos):
        instrucciones_totales = random.randint(1, 10)
        memoria_necesaria = random.randint(1, 10)
        proceso = Proceso(env, f"Proceso {i+1}", memoria_necesaria, instrucciones_totales)
        env.process(proceso.run(cpus, ram)) 
        yield env.timeout(intervalo)  

def ejecutar_simulacion(procesos_lista, intervalo):
    tiempos_promedio = []
    for procesos in procesos_lista:
        tiempos = []
        for _ in range(10):  
            env = simpy.Environment()
            ram = simpy.Container(env, init=MEMORIA_RAM, capacity=MEMORIA_RAM)
            cpus = simpy.Resource(env, capacity=2)
            env.process(llegada_proceso(env, cpus, ram, procesos, intervalo))
            env.run()
            tiempos.append(env.now)
        tiempo_promedio = statistics.mean(tiempos)
        desviacion_estandar = statistics.stdev(tiempos)
        tiempos_promedio.append(tiempo_promedio)
        print(f"Procesos: {procesos}, Tiempo promedio: {tiempo_promedio}, Desviación estándar: {desviacion_estandar}")
    return tiempos_promedio

def graficar(procesos_lista, tiempos_promedio, intervalo):
    plt.plot(procesos_lista, tiempos_promedio, marker='o')
    plt.xlabel('Cantidad de Procesos')
    plt.ylabel('Tiempo Promedio')
    plt.title(f'Cantidad de Procesos vs Tiempo Promedio (Intervalo = {intervalo})')
    plt.grid(True)
    plt.show()

procesos_lista = [25, 50, 100, 150, 200]
intervalo = 10  

tiempos_promedio = ejecutar_simulacion(procesos_lista, intervalo)
graficar(procesos_lista, tiempos_promedio, intervalo)