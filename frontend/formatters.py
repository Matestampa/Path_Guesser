
class Classic():
      def __init__(self):
          pass
      
      def transform(self,data):
          cont=0
          for i in data:

              curr=i
              type=i["type"]

              if type=="node":
                 coord_x,coord_y=i["value"].split(",")
                 i["coords"]={"x":int(coord_x),"y":int(coord_y)}
                 i["type"]="rectangle"
              
              if type=="edge":
                 value1,value2=i["value"].split("-")
                 coords_1,coords_2=value1.split(","),value2.split(",")
                 i["coords"]=[{"x":coords_1[0],"y":coords_1[1]},{"x":coords_2[0],"y":coords_2[1]}]
                 i["conex"]=[value1,value2]

                 #en el tag quedaria tag=value1-value2 -------> 72,63-98,90
                                     #tag=value2-value1 ------> 98,90-72,63
              
              if type=="division":
                 i["value"]=""
              
              data[cont]=i

              cont+=1
          return data
                 
