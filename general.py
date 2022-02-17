from tkinter import *
from random import randint
from math import sqrt

from frontend.main_draws import Screen
from frontend.formatters import Classic
from frontend.parser import Param_parser

from backend.graph_actions import Memory_Graph, format_coords
from backend.graph_actions import Gen_rand_graph

from rand_graph import Rand_Graph

#Formatos importantes:
              #Type: node----> "value": str(x)+","+str(i)
              #Type: edge----> "value": ------> v1 +"-" + v2 (ya es str por el valor del vertex)
              #Type: division-----> "value","coords":{"x":[0,1],"y":[0,1]},"size","max_nodes","p"

import time



def generate():
    
    start=time.time()
    rand_graph=Rand_Graph(screen_size={"x":700,"y":700},n_nodes=parser.get("n_nodes"),conex_x_node=parser.get("conex_complex"))
    
    #se puede usar rand_graph.params + el parser.sett() para mostrar todos los parametros de la creacion del grafo

    graph_data,divisions=rand_graph.create()


    screen.clean()

    mem_graph.add(graph_data)
    screen.render(graph_data)
    screen.render(divisions)
    end=time.time()
    print("Time:"+str(end-start))


#necesitariamos tener una lista con los objetos del canvas(para poder seleccionarlas)
#de momento lo lo hacemos "random"
def run_search():
    
    start=parser.get("startpoint")
    end=parser.get("endpoint")

    steps,path=mem_graph.find(start,end)

    screen.perform(steps,color="white")
    screen.perform(path,color="yellow",restart=False)

#---------------Extras que hay que mejorar----------------------------(el posta es con el mouse)    
def add_node(new,conex):
    
    new,conex=new.split(","),conex.split(",")

    new_data=format_coords(new,conex)

    mem_graph.add(new_data)
    screen.render(new_data)
#------------------------------------------------------------------------------------------------


raiz=Tk()


parser=Param_parser()#hacemos un parser que nos convierte los parametros al tipo que queremos
                    #se agregan con .add()--> hay que poner name,objetotk,tipo al que se quiere convertir,un valor default
                    #tambien sirve para updatearlos solo pasando el name,new_value

frame_actions=Frame(raiz,width=700,height=700,bg="white")
frame_actions.pack()

frame_canvas=Frame(raiz)
frame_canvas.pack()


button=Button(frame_actions,text="generate",command=generate)
button.grid(rowspan=3,column=0)

#-------------------------------------------------------------------------------

label=Label(frame_actions,text="Startpoint")
label.grid(row=0,column=2)
entry_start=Entry(frame_actions)
entry_start.grid(row=1,column=2)

parser.add("startpoint",entry_start,"str",default="0.0")

label=Label(frame_actions,text="Endpoint")
label.grid(row=2,column=2)
entry_end=Entry(frame_actions)
entry_end.grid(row=3,column=2)

parser.add("endpoint",entry_end,"str",default="0.0")

button=Button(frame_actions,text="run",command=lambda:run_search())
button.grid(rowspan=3,column=3)


"""entry_new=Entry(frame_actions)
entry_new.grid(row=0,column=2)

entry_conex=Entry(frame_actions)
entry_conex.grid(row=1,column=2)

button=Button(frame_actions,text="add",command=lambda:add_node())
button.grid(row=2,column=2)"""

#-----------------------------------------------------------------------

label=Label(frame_actions,text="Nro.Nodes:")
label.grid(row=0,column=1)
entry_nodes=Entry(frame_actions)
entry_nodes.grid(row=1,column=1)

parser.add("n_nodes",entry_nodes,"int",default="20")

label=Label(frame_actions,text="Nro_conex x node:")
label.grid(row=2,column=1)
entry_conex_x_node=Entry(frame_actions)
entry_conex_x_node.grid(row=3,column=1)

parser.add("conex_complex",entry_conex_x_node,"int",default="1")

#---------------------------------------------------------------------------------------

screen=Screen(parent=frame_canvas,size={"width":700,"height":700},formatter=Classic)
mem_graph=Memory_Graph()


raiz.mainloop()

