# Importar los módulos que se necesitan para ejecutar el modelo.import mesa

import mesa

from mesa.visualization.modules import ChartModule

from model import AgenteInitModel
from agent import dirtyAgent



def agent_portrayal(agent):
    """
    Si el agente es un agente sucio, entonces es un círculo, y si es

    """
    dirty = {"Shape": "circle", "Filled": "true", "r": 0.7}
    agentee = {"Shape": "rect", "Filled": "true", "w": 1, "h": 1}
    if type(agent) is dirtyAgent:
        if not agent.is_clean():
            dirty["Color"] = "purple"
            dirty["Layer"] = 5
        else:
            dirty["Color"] = "black"
            dirty["Layer"] = 5
    else:
        agentee["Color"] = "green"
        agentee["Layer"] = 10
    return dirty if type(agent) is dirtyAgent else agentee


# It's the main function of the program.
if __name__ == '__main__':
    width: int = 24
    height: int = 24
    grid = mesa.visualization.CanvasGrid(
        agent_portrayal, width, height, 500, 500)
    movimientos = ChartModule(
        [{
            "Label": "movements",
            "Color": "Green",
        }],
        data_collector_name='datacollector'
            )
    compute_clean_cells = ChartModule(
        [{
            "Label": "% Celdas Limpias",
            "Color": "Red"
        }],
        data_collector_name='datacollector'
            )
    tiempo = ChartModule(
        [{
            "Label": "Tiempo",
            "Color": "Purple"
        }],
        data_collector_name='datacollector'
            )
    model_params = {
        "num_agents": mesa.visualization.Slider(
            "Total de agentes",4,1, 50,1,
        ),
        "dirty_percentage": mesa.visualization.Slider(
            "% dirty",0.3, 0,1,0.01,
        ),
        "max_steps": mesa.visualization.Slider(
            "Pasos",100,40,10000,1,
        ),
        "width": width,
        "height": height,
    }
    server = mesa.visualization.ModularServer(
        AgenteInitModel, [grid, tiempo, compute_clean_cells, movimientos],
        "AgenteInitModel", model_params)
    # It's launching the server.
    server.port = 8521
    server.launch()
