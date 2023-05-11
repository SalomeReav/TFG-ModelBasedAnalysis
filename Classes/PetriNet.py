from abc import ABC, abstractmethod
#añadir las clases de node  y arc para poder poner las
#funciones que añadan esos nodos en nodes o arcs dependiendo.
#no me cuadra porque en la composicion petrinet deberia usar objetos de
#la clase node o arc, y estan declarados en el mismo fichero por lo que no 
#necesutan importar. pero en este caso no puedo poner las 3 clases en el mismo 
#fichero. o si? ?¿?¿


class PetriNet:
    def __init__(self):
        self.nodes = []
        self.arcs = []
    








