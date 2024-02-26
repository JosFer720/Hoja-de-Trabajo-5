"""
Fernando Ruiz 23065 
2016 - Algoritmos y Estructuras de Datos
Sección 40
"""

import simpy
import random
import statistics
import matplotlib.pyplot as plt

RANDOM_SEED = 42
MEMORIA_RAM = 100  
VELOCIDAD_CPU = 3  

class Proceso:
    def __init__(self, env, nombre, memoria, instrucciones_totales):
        """
        Inicializa un proceso con sus atributos.
        Args:
            env (simpy.Environment): Entorno de simulación.
            nombre (str): Nombre del proceso.
            memoria (int): Cantidad de memoria requerida por el proceso.
            instrucciones_totales (int): Número total de instrucciones que debe ejecutar el proceso.
        """
        self.env = env
        self.nombre = nombre
        self.memoria = memoria
        self.instrucciones_totales = instrucciones_totales
        self.instrucciones_restantes = instrucciones_totales

    def run(self, cpu, ram):
        """
        Ejecuta el proceso.
        Realiza la ejecución de las instrucciones del proceso y gestiona su interacción con el CPU y la RAM.
        Args:
            cpu (simpy.Resource): Recurso que representa el CPU.
            ram (simpy.Container): Contenedor que representa la memoria RAM.
        """
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
    """
    Genera la llegada de procesos al sistema.
    Args:
        env (simpy.Environment): Entorno de simulación.
        cpus (simpy.Resource): Recurso que representa el CPU.
        ram (simpy.Container): Contenedor que representa la memoria RAM.
        procesos (int): Número total de procesos a generar.
        intervalo (int): Intervalo de llegada de los procesos.
    """
    for i in range(procesos):
        instrucciones_totales = random.randint(1, 10)
        memoria_necesaria = random.randint(1, 10)
        proceso = Proceso(env, f"Proceso {i+1}", memoria_necesaria, instrucciones_totales)
        env.process(proceso.run(cpus, ram)) 
        yield env.timeout(intervalo)  

def ejecutar_simulacion(procesos_lista, intervalo):
    """
    Ejecuta la simulación con diferentes cantidades de procesos.
    Args:
        procesos_lista (list): Lista que contiene las cantidades de procesos a simular.
        intervalo (int): Intervalo de llegada de los procesos.
    Returns:
        list: Lista con los tiempos promedio de ejecución de los procesos para cada cantidad de procesos simulada.
    """
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
    """
    Genera una gráfica de los resultados de la simulación.
    Args:
        procesos_lista (list): Lista que contiene las cantidades de procesos simuladas.
        tiempos_promedio (list): Lista que contiene los tiempos promedio de ejecución de los procesos.
        intervalo (int): Intervalo de llegada de los procesos.
    """
    plt.plot(procesos_lista, tiempos_promedio, marker='o')
    plt.xlabel('Cantidad de Procesos')
    plt.ylabel('Tiempo Promedio')
    plt.title(f'Cantidad de Procesos vs Tiempo Promedio (Intervalo = {intervalo})')
    plt.grid(True)
    plt.show()

# Parámetros de la simulación
procesos_lista = [25, 50, 100, 150, 200]
intervalo = 10  

# Ejecución de la simulación y generación de la gráfica
tiempos_promedio = ejecutar_simulacion(procesos_lista, intervalo)
graficar(procesos_lista, tiempos_promedio, intervalo)