from tkinter import *

from time import sleep


class Screen():
      def __init__(self,parent,size,formatter):
          self.parent=parent
          self.width=size["width"]
          self.height=size["height"]
          
          self.formatter=formatter()
          self.__new_screen()


      def clean(self):
          self.cv.destroy()
          self.__new_screen()
      

      def render(self,data):
          data=self.formatter.transform(data)
          for i in data:

              if i["type"]=="rectangle":
                 
                 self.__new_rectangle(i)
              
              elif i["type"]=="edge":
                  self.__new_line(i)
              
              elif i["type"]=="division":
                   self.__new_division(i)
      
      def perform(self,steps):
          
          self.animator=Animator(self.cv)
          self.animator.run(steps)
       

      def __new_screen(self):#Limpiamos la pantalla
          self.cv=Canvas(self.parent,width=self.width,height=self.height,bg="grey")
          self.cv.pack()

      def __new_division(self,fig):
          coords=fig["coords"]

          self.cv.create_rectangle(coords["x"][0],coords["y"][0],coords["x"][1],coords["y"][1])
          self.cv.create_text(coords["x"][0]+30,coords["y"][0]+30,text=str(fig["value"]))


      def __new_rectangle(self,fig):
           coords=fig["coords"]

           self.cv.create_rectangle(coords["x"]-10,coords["y"]-10,coords["x"]+10,coords["y"]+10,fill="red",tags=("rectangle",fig["value"]))
           self.cv.create_text(coords["x"],coords["y"],text=fig["value"],fill="black",tags=("text",fig["value"]+"-"+"text"))

           #self.cv.tag_bind("hi","<Button-1>",self.change) tema para despues



      def __new_line(self,fig):
           coords=fig["coords"]
           cord0=coords[0]
           cord1=coords[1]
           
           self.cv.create_line(cord0["x"],cord0["y"],cord1["x"],cord1["y"],fill="black",tags=("line",fig["conex"][0]+"-"+fig["conex"][1],
                                                                                       fig["conex"][1]+"-"+fig["conex"][0]))



#----------------------------------------- Animator----------------------------------------------


class Animator():
      def __init__(self,cv):
          self.cv=cv
      

      def run(self,steps):
          self.__restart()

          for i in steps:
              self.cv.itemconfig(i["value"],fill="white")
              #self.cv.itemconfigure(i["value"]+"-"+"text",fill="green")

              if i["type"]=="node":
                 #sleep(0.05)
                 self.cv.update()
      
      def __restart(self):

          self.cv.itemconfigure("line",fill="black")
          self.cv.itemconfigure("rectangle",fill="red")
          self.cv.itemconfigure("text",fill="black")