import pandas as pd
import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from google.colab import files

########################################

data = files.upload()
#################################
def analytics(df):    
###################################################
    df =pd.read_csv('filtered_data.csv')
############################################3
    df = df.drop(df[ (df['Color'] == 'white')].index)

    dataframe=np.array(df)


    playerid=[]
    euc=[]
    class_=[]
    color=[]
    position=[]
    x=[]
    y=[]    
    for i in range(1,len(dataframe)): 
      
      if(dataframe[i,1]==dataframe[i-1,1]):
          #count euclidean distance for values in 2rd to 4th columns (x,y,z)
          eucdist=np.linalg.norm(dataframe[i,2:4]-dataframe[i-1,2:4])
          
          #check if the value does already excist or not to add it
          if eucdist not in euc:
              euc.append(eucdist)
              playerid.append(dataframe[i,1])
              class_.append(dataframe[i,4])
              color.append(dataframe[i,5])
              position.append(dataframe[i,6])      
              x.append(dataframe[i,2])
              y.append(dataframe[i,3])  
      else:
        euc.append(0)
        playerid.append(dataframe[i,1])
        class_.append(dataframe[i,4])
        color.append(dataframe[i,5])
        position.append(dataframe[i,6])      
        x.append(dataframe[i,2])
        y.append(dataframe[i,3]) 
       
    newd = pd.DataFrame({'id':playerid,'distance':euc,'x':x,'y':y,'class':class_,'color':color,'position':position})
    newdd = newd.groupby(['id','class','color','position'])['distance','x','y'].agg(number_of_frames=('distance','count' ),total_distance=('distance','sum'),average_x_pos=('x','mean'),average_y_pos=('y','mean')).reset_index(drop = False )
    newdd['number_of_frames'] = newdd.loc[:,'number_of_frames']= newdd['number_of_frames']+1
    newdd['average_speed'] = newdd['total_distance']/(newdd['number_of_frames']*10)
    newdd['average_x_pos'] = (newdd['average_x_pos']/10.5)
    newdd['average_y_pos'] = (newdd['average_y_pos']/6.8)
    
    return newdd
newdata = analytics(dataframe)
newdata