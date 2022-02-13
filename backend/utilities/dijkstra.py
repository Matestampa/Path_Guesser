from .grafos import Graph
from .dijk_help import P_Queue

#from grafos import Graph
#from dijk_help import P_Queue

#el poped, es el objeto que contiene los datos de distancia, y trackea el anteriro(es independiente del grafo)
#el actual es el objeto concreto del vertice (corresponde directamente al grafo)

class First():
      def __init__(self):
          self.value="finish"
          self.prev=None


def path(vertex):
    lista=[]

    actual=vertex
    while actual!=None:
          
          lista.insert(0,actual.value)
          actual=actual.prev
     
    return lista[1:]
          
    
def DJS(grafo,s,f,all_steps=False):
    
    cola=P_Queue()
    
    cola.add(value=s)
    cola.update(s,distance=0,prev=First())
    
    steps=[]

    while True:
          poped=cola.pop() #elimina del queue y devuelve objeto
          #print(poped.value)
          steps.append(poped.prev.value)
          steps.append(poped.value)

          actual=grafo.get_vertex(poped.value)

          if poped.value==f:
             if all_steps==False:
                return {"steps":path(poped),"distance":poped.distance}
             
             else:
                return {"steps":steps[1:],"distance":poped.distance}

          for i in actual.get_neighs():#recorremos los vecinos
        
              if i.value==poped.prev.value:
                 pass

              else:
                 curr=cola.get(i.value)

                 if curr==None: #verificamos si estan o no en el queue
                    curr=cola.add(value=i.value,send_back=True) #sino, lo agregamos y el p_queue se encarga de ordenarlo

                 if (i.height+poped.distance)<curr.distance: #si se cumple la regla de la distancia menor y eso:
       
                    cola.update(i.value,distance=i.height+poped.distance,prev=poped) #actualizamos(tambien el p_queue se encarga de ordenar nuevamente)
                    #print(poped.value)