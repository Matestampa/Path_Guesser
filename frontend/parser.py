






from tkinter import StringVar


class Param_parser():
      def __init__(self):

          self.params={}
          self.param_values={}
      
      def add(self,name=None,obj=None,type="str",default="0"):
          if name==None or obj==None:
             raise Exception("The name or object can't be None")
          
          var=StringVar()
          obj.config(textvariable=var)#le ponemos una stringvar para poder interactuar con el 
          self.params[name]={"obj":obj,"type":type,"default":default,"var":var}
      
      
      def get(self,name):
          
          value=self.__parse(name)
          
          return value
      
      def sett(self,name,new_value):
          param=self.params[name]
          param["var"].set(str(new_value))
      
      
      def ___parse(self,name):
              
          param=self.params[name]
              
          #verificamos si no tiene nada y ponemos el default
          value=param["obj"].get()

          if value=="":
             value=param["default"]
              
          #lo pasamos al tipo correspondiente
          type=param["type"]
              
          if type=="str":
             value=str(value)
          elif type=="int":
             value=int(value)
          elif type=="float":
             value=float(value)

          return value

      """def get_all(self):
          for i in self.params.keys():
              print(i,self.parse(i))"""
      
      def descr(self):
          pass
          """-Sirve para al hacer get de un entry, que este ya venga formateado a un valor especificado
             -Tmb para setear valores nuevos simplemente pasando el nombre,new_value
             -Cada uno se identifica con el nombre que se pasa en add"""
             
