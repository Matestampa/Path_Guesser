from backend.utilities.grafos import Graph,Vertex
from divisions import Gen_div,Division
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
      
      def create_rand_conex(self,fromm_value):
          fromm_div=self.get_vertex(fromm_value)#obj div from
          
          div_neigh=choice(fromm_div.get_neighs())#seleccionamos vecino al que vamos a conectar
          div_neigh=self.get_vertex(div_neigh.value) #obj del vecino

          fromm_node=choice(fromm_div.get_nodes())#seleccionamos value del nodo de div from
          to_node=choice(div_neigh.get_nodes()) #seleccionamos value del nodo del vecino elegido

          fromm_node=fromm_div.get_vertex(fromm_node) #obj del nodo de div from
          to_node=div_neigh.get_vertex(to_node) #obj del nodo del vecino

          dist=fromm_node.get_distance(to_node)#distancia
          
          new_edge=self.add_interdiv_edge(fromm_div,div_neigh,fromm_node,to_node,height=dist,format_back=True)

          return new_edge
          
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
                       "p":self.p,"div_size":self.div_size,"p_nodes":self.div_nodes}

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
                  
                  #print(node_value+":"+str(n_conex))
                  #print(new_edges)

                  if new_edges!=None:
                     formatted_objs+=new_edges
              
              new_edge=self.div_graph.create_rand_conex(div_value)
              formatted_objs.append(new_edge)

              
          
          

          return formatted_objs,divisions

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



                 