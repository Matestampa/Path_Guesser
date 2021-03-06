from backend.utilities.grafos import Graph,Vertex
from divisions import Gen_div,Division
import interdiv_conex
from math import sqrt
from random import randint,choice

class Rand_Vertex(Vertex):
      def __init__(self, value):
          super().__init__(value) #ya tenemos self.value
          
          self.x_cor,self.y_cor=value.split(",")
          self.x_cor,self.y_cor=int(self.x_cor),int(self.y_cor)

          self.neighs_values={}
          self.total_neighs=0  


      def get_distance(self,obj):
          x_dist=(self.x_cor-obj.x_cor)**2
          y_dist=(self.y_cor-obj.y_cor)**2

          return int(sqrt(x_dist+y_dist))

      def connect(self, value, height):#override
          super().connect(value, height)
          self.neighs_values[value]=value
          self.total_neighs+=1
      
      def disconnect(self, value):#override
          super().disconnect(value)
          del self.neighs_values[value]
          self.total_neighs-=1
      
      def has(self, value):#override (we should change it in the origin Vertex to)
          try:
              h=self.neighs_values[value]
              return True
          except KeyError:
              return False

class Gen_Vertex():
      def __init__(self,division):
          self.limits=division.limits
          self.p=division.p

          self.tree=[]
      
      def generate(self):
          range_x=self.limits["x"]
          range_y=self.limits["y"]

          coords_x=randint(int(range_x[0]),int(range_x[1]))
          coords_y=randint(int(range_y[0]),int(range_y[1]))

          final_value=str(coords_x) +","+ str(coords_y)

          return Rand_Vertex(final_value)
      
      def descr(self):
          pass
          """#Generar vertices, uno x uno random
          #Return: Solo el valor en formato -----> str(x)+","+str(y) <-----"""



class Division_Graph(Graph):
      

      def create(self,divisions):
          for div in divisions:
              
              div_value=div["value"]
              self.add_vertex(div)
              
              for neigh in div["neighs"]:
                  
                  self.add_edge(div_value,neigh)
      
      def create_div_conex(self,from_div,generator,n_nodes,n_conex):
          #print(from_div)
          div_obj=self.get_vertex(from_div)
          nodes=generator.choose_nodes(div_obj,n_nodes)#eelgimos nodos del curr div
          
          already_connected={}
          new_edges=[]
          
          for node in nodes:
              node=div_obj.get_vertex(node)
              #print("node",node.value)
              for j in range(n_conex):
                  neigh_div=generator.choose_div(div_obj)#elegimos a que div se va a conectar
                  neigh_div_obj=self.get_vertex(neigh_div)
                  #print("div",neigh_div)
                  neigh=generator.choose_neigh(neigh_div_obj,node)#elegimos el nodo de esa div
                  #print("neigh")
                  dist=node.get_distance(neigh)
            
                  edge=self.add_interdiv_edge(div_obj,neigh_div_obj,node,neigh,height=dist,format_back=True)
                  
                  neigh_div_obj.remove_vertex(node.value)
            
                  already_connected[neigh_div]="" #agregamos la div aca, para que aparezaca en ya visitadas
                 

                  new_edges.append(edge)
    
          for neigh_div in already_connected:#las ya visistadas, las desconecta para que no puedan volver a la curr
              self.remove_edge(div_obj.value,neigh_div)
          
          return new_edges

      
      def add_interdiv_edge(self,div1,div2,v1,v2,height=0,format_back=False):
          div1.add_vertex(v2)
          new=div1.add_edge(v1.value,v2.value,height=height,format_back=True)

          div2.add_vertex(v1)
          div2.add_edge(v2.value,v1.value,height=height)

          if format_back==True:
             return new
       
      def add_vertex(self,div): #modificamos el add_vertex de la clase Graph
          self.vertexs[div["value"]]=Division(div["value"],coords=div["coords"],max_nodes=div["max_nodes"],p=div["p"])
      
      def add_edge(self, v1, v2, height=0):
          super().add_edge(v1, v2, height)
        
      def get_divisions(self):
          return self.vertexs.keys()
      
      def descr(self):
          pass
          """#Hereda de Graph
          #Es un grafo, cuyos vertices son divisiones
          #Recibe formatos dict de tipo "division" (usa todo menos "size")
          #Hace un objeto Division con eso, y lo agrega como vertice
          #Encargado de operaciones entre divisiones"""


 
class Rand_Graph():
      
      def __init__(self,screen_size,n_nodes,conex_x_node):
          self.screen_size=screen_size
          self.screen_area=screen_size["x"] * screen_size["y"]
          self.n_nodes=n_nodes

          self.conex_complex=conex_x_node

          self.__gen_params()
      
      def __gen_params(self):
          self.p={"min":30,"max":None}

          self.p["max"]=int(sqrt(self.screen_area/self.n_nodes))

          self.n_divisions=int(self.n_nodes * 0.1)
          
          self.div_nodes=int(self.n_nodes/self.n_divisions)

          self.div_size=sqrt((self.n_nodes/self.n_divisions) * (self.p["max"])**2)
          self.div_size=int(self.div_size)

          self.params={"screen":self.screen_area,"n_divisions":self.n_divisions,"n_nodes":self.n_nodes,
                       "conex_complex":self.conex_complex,"p":self.p,"div_size":self.div_size,"p_nodes":self.div_nodes}

      def create(self):
          self.div_graph=Division_Graph()
          
          #hacemos divisiones
          div_generator=Gen_div(screen_size=self.screen_size,div_size=self.div_size,n_nodes=self.n_nodes,p=self.p)

          divisions=div_generator.generate()
          
          #las metemos en un grafo
          
          self.div_graph.create(divisions)

          #hacer nodes de c/u ------------------------------------------------
          formatted_objs=[]
          for div_value in self.div_graph.get_divisions():
              div=self.div_graph.get_vertex(div_value) #accedemos al obj

              vertex_generator=Gen_Vertex(division=div) #creamos un generador especifico para esa div

              for i in range(div.max_nodes):#vamos generando
                  new_vertex=vertex_generator.generate() #ver esta func x dentro
                  f_node=div.add_vertex(new_vertex,format_back=True)
                  
                  formatted_objs.append(f_node)

          
          #hacer conexiones de nodos(dentro de cada div) ------------------------------------------
          for div_value in self.div_graph.get_divisions():
              div=self.div_graph.get_vertex(div_value)
              
              for node_value in div.get_nodes():
                  n_conex=randint(1,self.conex_complex)
                  new_edges=div.create_rand_edge(root=node_value,n_conex=n_conex,format_back=True)#aca tenemos un param para variar
                  

                  if new_edges!=None:
                     formatted_objs+=new_edges
              
              #This particulary connects the divisions
              if len(div.get_neighs())!=0:
                 n_nodes,n_conex=self.make_conex_params(div)
                 
                 new_edges=self.div_graph.create_div_conex(div_value,generator=interdiv_conex.Full_Random(),n_nodes=n_nodes,n_conex=n_conex)
                 formatted_objs+=new_edges

              
          return formatted_objs,divisions

      def make_conex_params(self,div):
          cant_nodes=len(div.get_nodes())

          if cant_nodes<self.conex_complex:
             max_nodes=cant_nodes
          
          else:
              max_nodes=int(cant_nodes/2)

          n_nodes=randint(1,max_nodes)
          #n_conex=randint(1,self.conex_complex)
          n_conex=1

          return n_nodes,n_conex    

      
      def descr(self):
          pass
          """#Genera todos los parametros que podemos usar para el ui
          #Usa todos esos para hacer el grafo random:
                     #Pasos:
                          #Crea las divisiones(todos los calculos graficos) y devuelve su frmato dict -> Class: Gen_Div
                          #Crea el grafo con las divisiones--> Class: Division_Graph
                          #Hace nodos(random) para cada division, devuelve ya el objeto --> Class: Gen_Vertex
                          #Establece conexiones entre todos(primero nodos, despues div) ---> Class: Gen_Conex
          
          #Return: List---> objetos de type "node" y "edge" en formato dict"""