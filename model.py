# Importing the modules that are needed for the model to run.
from mesa import Model
from agent import AgenteInit
from agent import dirtyAgent, AgenteInit
from mesa import time
from mesa import space
from mesa import DataCollector


def celdas_limpias(model):
    """
   Cuenta el número de movimientos realizados por todos los agentes
    """
    movements = 0
    for agent in model.schedule.agents:
        if isinstance(agent, AgenteInit):
            movements =movements+ agent.moves
    return movements

def tiempo(model):
    """
    Devuelve la hora actual del modelo.
    """
    return model.schedule.time
def clean(model):
    """
    Calcula el porcentaje de celdas limpias en la grilla
    """
    cells = model.height * model.width
    celdasSucias = 0
    for agent in model.schedule.agents:
        if isinstance(agent, dirtyAgent):
            if not agent.is_clean():
                celdasSucias += celdasSucias+1
    clean2 = (cells - celdasSucias) / cells * 100
    return clean2







# coloca agentes en la red y luego crea a data collector
class AgenteInitModel(Model):
    def __init__(self, width, height, num_agents,
                 dirty_percentage, max_steps):
      
        self.num_agents = num_agents
        self.width = width
        self.height = height
        self.dirty_percentage = dirty_percentage
        self.remaining_steps = max_steps
        self.grid = space.MultiGrid(width, height, False)
        self.schedule = time.RandomActivation(self)
        self.running = True
        num_celdasSucias = int(self.dirty_percentage * width * height)
        used_coordinates = set()

        for i in range(num_celdasSucias):
            agent = dirtyAgent(i, self)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            while (x, y) in used_coordinates:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            used_coordinates.add((x, y))

        for i in range(self.num_agents):
            agent = AgenteInit(i + num_celdasSucias, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (0, 0))

        self.datacollector = DataCollector(
            model_reporters={"% Celdas Limpias": clean,
                             "Movimientos": celdas_limpias,
                             "Tiempo": tiempo})

    def step(self):
        """
        comprobar si el número de pasos es mayor que 0 y si el número de limpieza
        celdas no es igual a 100
        """
        if self.remaining_steps > 0 and clean(self) != 100.0:
            self.datacollector.collect(self)
            self.schedule.step()
            self.remaining_steps -= 1
