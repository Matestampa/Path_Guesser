from random import randint,choice


class General():
      def __init__(self):
          self.already_connected={}
      
      def choose_nodes(self,div_obj,n_nodes):#devuelve values de los nodos elegidos
          pass
      

      def choose_div(self,div_obj):#solo puede devolver values,este es comun para todos
          possible_div_neighs=div_obj.get_neighs(only_values=True)

          if possible_div_neighs==None:
             return None
          else:
             return choice(possible_div_neighs)
      
      def choose_neigh(div_obj):#le pasamos el obj de la div elegida, y el node que queremos conectar
                                #devuelve obj
          pass


class Full_Random(General):
      
      def choose_nodes(self, div_obj, n_nodes):
          
          possible_nodes=div_obj.get_nodes()
          
          final_nodes=[]
          
          node=""
          
          for i in range(n_nodes):
              
              while (node in final_nodes) or node=="":
                    node=choice(possible_nodes)
              
              final_nodes.append(node)
          
          return final_nodes

      def choose_neigh(self,div_obj,node):
          possible_neighs=div_obj.get_nodes()

          neigh=""
          
          while (node.has(neigh)==True) or neigh=="":
                neigh=choice(possible_neighs)
          
          return div_obj.get_vertex(neigh)
          



            




