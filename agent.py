# Importación de la clase Agente desde el módulo mesa.

from mesa import Agent


# La clase AgenteInit es una subclase de la clase Agent. tiene un constructor
# que toma un unique_id y un
# modelo como argumentos. También tiene un método de pasos que mueve el AgenteInit
# alrededor de la cuadrícula
class AgenteInit(Agent):
    """Un agente constructor."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.moves = 0

    def step(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        change = False
        for cellmate in cellmates:
            if isinstance(cellmate, dirtyAgent):
                #si la celda esta sucia
                if not cellmate.is_clean():
                    
                    #llamamos a nuestra función clean
                    cellmate.clean()
                    change = True
                else:
                
                    #nos movemos y continuamos buscando

                    self.move()
                    change = True
        if not change:
            self.move()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
        #establecemos nueva posicion utilizando rand
        new_pos = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_pos)
        self.moves += 1



class dirtyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dirty = True

    def step(self):
        pass

    def clean(self):
        self.dirty = False

    def is_clean(self):
        return not self.dirty
