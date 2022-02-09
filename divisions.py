from backend.utilities.grafos import Graph,Vertex,Edges_list
from random import choice
from math import sqrt

class Division(Graph,Vertex):
      def __init__(self,value,coords,max_nodes,p):
          #attrs propios
          self.value=value
          self.limits=coords
          self.max_nodes=max_nodes
          self.p=p

          #cosas de clases padre que necesitamos poner si o si
          self.neighs=Edges_list()# igual revisar esto esta mal hacerlo asi
          self.vertexs={}

          #new funcional attrs
          
          #completarrrrrrrr----------------------------------------------------------------------------------------
      
      def add_vertex(self,obj,format_back=False):
          if self.vertexs.get(obj.value)!=None:
             pass
          else:
             self.vertexs[obj.value]=obj

          if format_back==True:
             new={"type":"node","value":obj.value}
             return new                   #vamos devolviendo formatos a medida que los creamos
      
      def add_edge(self, v1, v2, height=0,format_back=False):
          super().add_edge(v1, v2, height)
          
          new={"type":"edge","value":v1+"-"+v2,"height":height}
          if format_back==True:
             return new        #lo mismo aca.

      def create_rand_conex(self):#mallllll, hay que hacerlo en Division_Graph
          neigh=choice(self.get_neighs())
          neigh_node=choice(neigh.vertexs_keys)
          node=choice(self.vertexs_keys)
          
          dist=neigh_node.get_distance(self.vertexs[node])
          
          return {"type":"edge","value":neigh_node.value+"-"+node,"height":dist}

      def create_rand_edge(self,root,n_conex,format_back=False):#Hay mucho para mejorar aca, hicmos una O() como el culo
          curr_node=self.vertexs[root]
          posible_neighs=self.vertexs_keys 
          new_edges=[]

          
          
          sel_node=curr_node.value
          
          conex_cont=0
          while ((self.max_nodes-1)-curr_node.total_neighs)>0 and conex_cont<n_conex:

              while sel_node==curr_node.value or (curr_node.has(sel_node)==True):#mientras no sea el mismo, ni este en sus vecinos
                    sel_node=choice(posible_neighs)
        
        

              dist=curr_node.get_distance(self.vertexs[sel_node])

              new_edge=self.add_edge(curr_node.value,sel_node,height=dist,format_back=True)
              
              new_edges.append(new_edge)

              #print("choice_cont:"+str(cont))
              conex_cont+=1

          if format_back==True:
             #print(conex_cont)
             return new_edges
      
      def get_nodes(self):
          self.vertexs_keys=list(self.vertexs.keys())
          return self.vertexs_keys

      def __descr(self):
          pass
          """#Hereda de Graph y de Vertex
          #Es un vertex de Division_Graph, y un grafo que contiene los div_nodes
          #Fundamental en la creacion de nodos y su posteriro union en Rand_Graph
          #Cada vez que crea un nodo o edge, si se pasa un param(format_back), devuelve su format
          
          #Node:"type":"node", "value":value (ya fue formateado en Gen_Vertex)
          #Edge: "type":"edge" , "value": ------> v1 +"-" + v2 (ya es str por el valor del vertex)"""
      


          



class Gen_div_neighs():
      def __init__(self):
          self.touch_coords={}


      def find_neighs(self,division):
          coords_x=division["coords"]["x"]
          coords_y=division["coords"]["y"]

          top_left=str(coords_x[0])+str(coords_y[0])
          bot_left=str(coords_x[0])+str(coords_y[1])
          top_right=str(coords_x[1])+str(coords_y[0])
          bot_right=str(coords_x[1])+str(coords_y[1])

          all_coords=[top_left,bot_left,top_right,bot_right]
          
          final_neighs=[]

          for i in all_coords:
              neighs=self.touch_coords.get(i)
              
              if neighs!=None:
                 for j in neighs:
                     if j not in final_neighs:
                        final_neighs.append(j)
                 
                 self.touch_coords[i].append(division["value"])
              
              else:
                 self.touch_coords[i]=[division["value"]]
              
          return final_neighs
      
      def descr(self):
          pass
          """#Va encontrando los vecinos de las divisiones, una por una
          #Recibe una division (solo usa sus coords)
          #Return List----> values de divisiones vecinas"""



class Gen_div():
      def __init__(self,screen_size,div_size,n_nodes,p):
          self.screen_size=screen_size
          self.div_size=div_size
          self.n_nodes=n_nodes
          self.p=p
      

      def generate(self):
          
          rest_nodes=self.n_nodes
          cursor_x=0
          cursor_y=0
          x1,y1,x2,y2=0,0,0,0

          limit=self.screen_size
          
          div_size={"x":None,"y":None} #este es uno que usamos por si cambia en las divisiones que se cortan
                                       #el fijo es el de self.div_size

          control_value=[0,0]
          final_value=""
          division_list=[]
          neighs_generator=Gen_div_neighs()
          
          while x2!=limit["x"] or y2!=limit["y"]:
              x1=cursor_x
              y1=cursor_y
              
              x2=cursor_x+self.div_size
              y2=cursor_y+self.div_size
              
              control_value[0]+=1
              
              final_value=str(control_value[1]) +","+ str(control_value[0])
              if x2>limit["x"]:
                 div_size["x"]=limit["x"]-x1
                 x2=limit["y"]
                 
                 cursor_x=0
                 cursor_y=y2

                 control_value[1]+=1
                 control_value[0]=0
              
              else:
                 cursor_x=x2

                 div_size["x"]=self.div_size
                 div_size["y"]=self.div_size
              
              if y2>limit["y"]:
                 div_size["y"]=limit["y"]-y1

                 y2=limit["y"]

              max_nodes=round((div_size["x"]*div_size["y"])/self.p["max"]**2,0)
              
              #if max_nodes<1:#si es uno solo o menos no nos sirve(es una division muy chica). Salteamos a la prox vuelta
                 #continue

              if rest_nodes>0:#si quedan nodos restantes
                 if rest_nodes<max_nodes: #si la division pide mas de los que tenemos
                    max_nodes=max_nodes-(max_nodes%rest_nodes) #les damos solo los que nos quedan
                 rest_nodes-=max_nodes
              
              else: #sino, cortamos(corte gaspi)
                  break

              #creamos nuestro formato de divison
              division={"type":"division","value":final_value,"coords":{"x":[x1,x2],"y":[y1,y2]},"size":div_size,"max_nodes":int(max_nodes),"p":self.p}
              
              #aprovechamos para averiguar los vecinos tmb ,para que no lo tenga que hacer otra clase
              division["neighs"]=neighs_generator.find_neighs(division)

              division_list.append(division)
          
          return division_list

      
      def descr(self):
          pass
          """#Hace los calculos para fitear las divisiones en pantalla
          #Define bien sus coords y cuantos nodes entran en c/u
          #Encuentra vecinos de cada una
          #Genera el formato dict de cada division----> "type":"division","value","coords":{"x":[0,1],"y":[0,1]},"size","max_nodes","p"

          #Return List---> divisiones en el formato de arriba"""
            




#possible_neighs------> Vecinos que puede llegar a tener
#actual_neighs -------> Valores


"""6v  9conex

while rest_conex<(div.max_nodes-node.neighs)

while (div.max_nodes-1-node.neighs)<0 and cont<=n_conex

1 (9-6)
2 (9-7)
3 (9-8)
4 (9-3)"""


#tiempo:

#(generando 100 nodos)
#Con 4 prints ---> 0,1
#Sin prints   ---> 0,00(3 a 9)
#Sin hacer grafico ----> 0,000(algo) recien llega a 0,1 arriba de 9000

#con grafico---> recien llega en los 3200
