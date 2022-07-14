import pandas as pd
import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt


X_SIZE = 105.0
Y_SIZE = 68.0

BOX_HEIGHT = (16.5*2 + 7.32)/Y_SIZE*100
BOX_WIDTH = 16.5/X_SIZE*100

GOAL = 7.32/Y_SIZE*100

GOAL_AREA_HEIGHT = 5.4864*2/Y_SIZE*100 + GOAL
GOAL_AREA_WIDTH = 5.4864/X_SIZE*100

SCALERS = np.array([X_SIZE/100, Y_SIZE/100])

def draw_pitch(dpi=100):
    """Sets up field
    Returns matplotlib fig and axes objects.
    """

    fig = plt.figure(figsize=(12.8, 7.2), dpi=dpi) #(X_SIZE/10, Y_SIZE/10)
    fig.patch.set_facecolor('#a8bc95') #complementary: #80a260 e #95bbbc, opposing: #bc95a8 & #bc9f95

    axes = fig.add_subplot(1, 1, 1)
    axes.set_axis_off()
    axes.set_facecolor('#a8bc95')
    axes.xaxis.set_visible(False)
    axes.yaxis.set_visible(False)

    axes.set_xlim(0,100)
    axes.set_ylim(0,100)

    plt.xlim([-13.32, 113.32])
    plt.ylim([-5, 105])

    fig.tight_layout(pad=3)

    draw_patches(axes)

    return fig, axes

def draw_patches(axes):
    """
    Draws basic field shapes on an axes
    """
    #pitch
    axes.add_patch(plt.Rectangle((0, 0), 100, 100,
                       edgecolor="white", facecolor="none"))

    #half-way line
    axes.add_line(plt.Line2D([50, 50], [100, 0],
                    c='w'))

    #penalty areas
    axes.add_patch(plt.Rectangle((100-BOX_WIDTH, (100-BOX_HEIGHT)/2),  BOX_WIDTH, BOX_HEIGHT,
                       ec='w', fc='none'))
    axes.add_patch(plt.Rectangle((0, (100-BOX_HEIGHT)/2),  BOX_WIDTH, BOX_HEIGHT,
                               ec='w', fc='none'))

    #goal areas
    axes.add_patch(plt.Rectangle((100-GOAL_AREA_WIDTH, (100-GOAL_AREA_HEIGHT)/2),  GOAL_AREA_WIDTH, GOAL_AREA_HEIGHT,
                       ec='w', fc='none'))
    axes.add_patch(plt.Rectangle((0, (100-GOAL_AREA_HEIGHT)/2),  GOAL_AREA_WIDTH, GOAL_AREA_HEIGHT,
                               ec='w', fc='none'))

    #goals
    axes.add_patch(plt.Rectangle((100, (100-GOAL)/2),  1, GOAL,
                       ec='w', fc='none'))
    axes.add_patch(plt.Rectangle((0, (100-GOAL)/2),  -1, GOAL,
                               ec='w', fc='none'))


    #halfway circle
    axes.add_patch(Ellipse((50, 50), 2*9.15/X_SIZE*100, 2*9.15/Y_SIZE*100,
                                    ec='w', fc='none'))

    return axes


    df =pd.read_csv('mb7_df_mapped.csv')
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
plt.show()
fig , ax = draw_pitch()
#Draw the pitch on the ax figure as well as invert the axis for this specific pitch
plt.gca().invert_yaxis()
ex = newdata.plot(kind='scatter',x='average_x_pos',y='average_y_pos',title='average position' ,c=newdata.color,s=150,ax=ax)

#mx = pitch.scatter(newdata.average_x_pos,newdata.average_y_pos,ax=ax)
newdata[['average_x_pos','average_y_pos','id']].apply(lambda row: ax.text(*row),axis=1)

fig.savefig('/outpot_data/average position.jpg',facecolor=fig.get_facecolor(), transparent=True)

plt.show()

