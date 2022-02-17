from backend.utilities.grafos import Graph
from backend.utilities.dijkstra import DJS
#from utilities.grafos import Graph


class Memory_Graph():
      def __init__(self):
          self.graph=Graph()

      def add(self,data): #recive solo los fromatos de dict, de tipo "node" o "edge"
          for i in data:

              type=i["type"]

              if type=='node':
                 self.graph.add_vertex(i["value"])
                 
              
              elif type=="edge":
                  
                  value0,value1=i["value"].split("-")
                  #value0=i["conex"][0]
                  #value1=i["conex"][1]
                  
                  self.graph.add_edge(value0,value1,height=i["height"])
       
      def find(self,start,end):

          path=DJS(self.graph,start,end,all_steps=True)

          steps=path["steps"] #devuelve por todos los lados que paso(nos va mostrando los edges xon los valores de donde salen hata donde van)
          path=path["path"]
          
          print(path)
          for i in path:
              node=self.graph.get_vertex(i)
              print(i,node.get_neighs(only_values=True))

          formatted_steps,formatted_path=self.__format_dijk(steps),self.__format_dijk(path)
          

          return formatted_steps,formatted_path

      
      
      
      def __format_dijk(self,steps):
          cont=0
          formated_steps=[]
          
          for i in steps:
              
              
              if cont%2==0: #cuando es par, agregamos su nodo, y el edge al juntarlo con su vecino previo.
                            #cuando es impar, ya aparecio y solo forma parte del edge del siguiente(por eso no lo tenemos en cuenta)
                            #                                                                      (estariamos repitiendo)
                 
                 
                 if cont==0:
                    node={"type":"node","value":steps[cont]}
                    formated_steps.append(node)
                 
                 else:
                    node={"type":"node","value":steps[cont]}
                    edge={"type":"edge","value":steps[cont-1] +"-"+ steps[cont]}
                    formated_steps.append(edge)
                    formated_steps.append(node)
                    
                 
              cont+=1
          
          return formated_steps #tambien habria que devolver la distancia
        
        
      def __delete(self):
          try:
              del self.graph
          
          except:
              pass





#---------------------------------------Creacion de grafo random---------------------------------------------------------------------

from random import randint
from math import sqrt

class Rand_node():
      def __init__(self):
          self.x_cor=None
          self.y_cor=None
      
      def get_coords(self):

          return {"x":self.x_cor,"y":self.y_cor}

      def update_value(self):
          self.value=str(self.x_cor)+str(self.y_cor)
      
      def get_distance(self,obj):
          x_dist=(self.x_cor-obj.x_cor)**2
          y_dist=(self.y_cor-obj.y_cor)**2

          return int(sqrt(x_dist+y_dist))


#para un vertex o node hay que poner: value(str), coords(list(coords1,coords2))
#para un edge hay que poner: height(int), conex(list(value1,value2)), coords(list(coords1,coords2))

def Gen_rand_graph():
    
    nodes=[]
    finals=[]
    
    space_x=0
    space_y=300
    
    for i in range(20):
        new_node=Rand_node()
        new_node.x_cor=randint(space_x,space_x+20)
        new_node.y_cor=randint(space_y-100,space_y+100)
        
        new_node.update_value()
        
        space_x+=50
        
        nodes.append(new_node)
        if i>0:
           distance=new_node.get_distance(nodes[i-1])
           
           node_data={"type":"node","value":new_node.value,"coords":new_node.get_coords()}
           edge_data={"type":"edge","height":distance,"coords":[nodes[i-1].get_coords(),new_node.get_coords()],
                      "conex":[nodes[i-1].value,new_node.value]}
           
           finals.append(node_data)
           finals.append(edge_data)
        
        else:
            node_data={"type":"node","value":new_node.value,"coords":new_node.get_coords()}
            finals.append(node_data)
    

    return finals,nodes


def format_coords(coord_new,coord_conex): #formatea coordenadas en str
                                          #usado para crear formato dict de nodes y edges

    new_node=Rand_node()
    new_node.x_cor=int(coord_new[0])
    new_node.y_cor=int(coord_new[1])
    new_node.update_value()

    conex_node=Rand_node()
    conex_node.x_cor=int(coord_conex[0])
    conex_node.y_cor=int(coord_conex[1])
    conex_node.update_value()

    distance=new_node.get_distance(conex_node)

    node={"type":"node","value":new_node.value,"coords":new_node.get_coords()}
    edge={"type":"edge","height":distance,"coords":[conex_node.get_coords(),new_node.get_coords()],
          "conex":[conex_node.value,new_node.value]}
    

    return [node,edge]

