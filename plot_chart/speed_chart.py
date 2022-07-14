import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df =pd.read_csv('havertz_df_mapped.csv')
df = df.drop(df[ (df['Class'] == 'Ball')].index)
dataframe=np.array(df.sort_values(['ID','frame']))

def avg_speed_pos(dataframe):    
    
    playerid=[]
    euc=[]
    class_=[]
    color=[]
    position=[]
    x=[]
    y=[]    
    for i in range(1,len(dataframe)): 
      
      if(dataframe[i,1]==dataframe[i-1,1]):
          #count euclidean distance for values in 2rd to 4th columns (x,y)
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

    newdd['average_speed'] = newdd['total_distance']/(newdd['number_of_frames']*5)
    newdd['average_x_pos'] = (newdd['average_x_pos']/10.5)
    newdd['average_y_pos'] = (newdd['average_y_pos']/6.8)
    return newdd



newdata = avg_speed_pos(dataframe)
speed_chart = newdata.plot.bar(x='id',y='average_speed', rot=0 ,xlabel='player_id',ylabel='speed',title='Average speed')
plt.show()
plt.savefig('speed chart.jpg', dpi=300, bbox_inches='tight')