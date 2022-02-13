from tkinter import *
from random import randint
from math import sqrt

from frontend.main_draws import Screen
from frontend.formatters import Classic
from backend.graph_actions import Memory_Graph, format_coords
from backend.graph_actions import Gen_rand_graph
from backend.graph_actions import format_coords

from rand_graph import Rand_Graph

#Formatos importantes:
              #Type: node----> "value": str(x)+","+str(i)
              #Type: edge----> "value": ------> v1 +"-" + v2 (ya es str por el valor del vertex)
              #Type: division-----> "value","coords":{"x":[0,1],"y":[0,1]},"size","max_nodes","p"

import time

def generate(n_nodes,conex_x_node=1):
    start=time.time()
    rand_graph=Rand_Graph(screen_size={"x":700,"y":700},n_nodes=int(n_nodes),conex_x_node=int(conex_x_node))
      

    graph_data,divisions=rand_graph.create()


    screen.clean()

    mem_graph.add(graph_data)
    screen.render(graph_data)
    screen.render(divisions)
    end=time.time()
    print("Time:"+str(end-start))



"""def generate():
    global only_nodes
    
    screen.clean() #limpiamos pantalla

    graph_data,only_nodes=Gen_rand_graph() #data en dict para construir grafo tanto en la pantalla como en memoria

    mem_graph.add(graph_data) #hacemos grafo en memoria
    screen.render(graph_data)#hacemos grafo en pantalla"""




#necesitariamos tener una lista con los objetos del canvas(para poder seleccionarlas)
#de momento lo lo hacemos "random"
def run_search(start=None,end=None):
    
    start=start
    end=end

    steps=mem_graph.find(start,end)

    screen.perform(steps)

#---------------Extras que hay que mejorar----------------------------(el posta es con el mouse)    
def add_node(new,conex):
    
    new,conex=new.split(","),conex.split(",")

    new_data=format_coords(new,conex)

    mem_graph.add(new_data)
    screen.render(new_data)
#------------------------------------------------------------------------------------------------


raiz=Tk()

frame_actions=Frame(raiz,width=700,height=700,bg="white")
frame_actions.pack()

frame_canvas=Frame(raiz)
frame_canvas.pack()


button=Button(frame_actions,text="generate",command=lambda:generate(entry_nodes.get(),entry_conex_x_node.get()))
button.grid(row=0,column=0)


entry_start=Entry(frame_actions)
entry_start.grid(row=0,column=1)

entry_end=Entry(frame_actions)
entry_end.grid(row=1,column=1)


button=Button(frame_actions,text="run",command=lambda:run_search(entry_start.get(),entry_end.get()))
button.grid(row=2,column=1)


entry_new=Entry(frame_actions)
entry_new.grid(row=0,column=2)

entry_conex=Entry(frame_actions)
entry_conex.grid(row=1,column=2)

button=Button(frame_actions,text="add",command=lambda:add_node(entry_new.get(),entry_conex.get()))
button.grid(row=2,column=2)

entry_nodes=Entry(frame_actions)
entry_nodes.grid(row=0,column=3)

entry_conex_x_node=Entry(frame_actions)
entry_conex_x_node.grid(row=0,column=4)

screen=Screen(parent=frame_canvas,size={"width":700,"height":700},formatter=Classic)
mem_graph=Memory_Graph()


raiz.mainloop()

