import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import pandas as pd
import numpy as np
import seaborn as sns


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


    df =pd.read_csv('havertz_df_mapped.csv')
df = df.drop(df[ (df['Class'] == 'Ball')].index)
dataframe=np.array(df.sort_values(['ID','frame']))


def newdataa(dataframe):
  nframe=[]
  nid=[]
  nx=[] 
  ny=[]
  dataclass=[]
  color=[]
  position=[]
  dx=[0]
  dy=[0]
  for i in range(1,len(dataframe)):
    if dataframe[i,1] == dataframe[i-1,1]:
      if (dataframe[i,0]!=dataframe[i-1,0]+1):
        newframe = (dataframe[i-1,0]*2)-1
        secondframe = (dataframe[i-1,0]*2)
        nframe.append(newframe)
        nframe.append(secondframe)
        
        #appending new ids
        id=dataframe[i-1,1]
        nid.append(id)
        nid.append(id)


        #calculate x mean between two points
        x_avg = (dataframe[i,2]+dataframe[i-1,2])/2
        nx.append(x_avg)
        nx.append(dataframe[i,2])
  
        #y array 
        y_avg = (dataframe[i,3]+dataframe[i-1,3])/2
        ny.append(y_avg)
        ny.append(dataframe[i,3])  
        

        #appending class values
        dataclass.append(dataframe[i-1,4])
        dataclass.append(dataframe[i-1,4])

        #appending color values
        color.append(dataframe[i-1,5])
        color.append(dataframe[i-1,5])
        
        #appending position values
        position.append(dataframe[i-1,6])
        position.append(dataframe[i-1,6])


      else:
        newframe = (dataframe[i-1,0]*2)-1
        secondframe = (dataframe[i-1,0]*2)
        nframe.append(newframe)
        nframe.append(secondframe)
        
        #appending new ids
        id=dataframe[i-1,1]
        nid.append(id)
        nid.append(id)


        # x array
        x_avg = (dataframe[i,2]+dataframe[i-1,2])/2
        nx.append(x_avg)
        nx.append(dataframe[i,2])
  
        #y array 
        y_avg = (dataframe[i,3]+dataframe[i-1,3])/2
        ny.append(y_avg)
        ny.append(dataframe[i,3])  
 
        #appending class values
        dataclass.append(dataframe[i-1,4])
        dataclass.append(dataframe[i-1,4])

        #appending color values
        color.append(dataframe[i-1,5])
        color.append(dataframe[i-1,5])
        
        #appending position values
        position.append(dataframe[i-1,6])
        position.append(dataframe[i-1,6])
             
  newdataframe = pd.DataFrame({'Frame':nframe,'ID':nid,'X':nx,'Y':ny,'Class':dataclass,'color':color,'position':position})
  newdddd=np.array(newdataframe.sort_values(['ID','Frame']))
  
  for i in range(1,len(newdataframe)):
    if(newdddd[i,1]==newdddd[i-1,1]):
      distancex=(newdddd[i,2]-newdddd[i-1,2])
      dx.append(distancex)
      distancey=(newdddd[i,3]-newdddd[i-1,3])
      dy.append(distancey)
    else:
      dx.append(0)
      dy.append(0)
  newdataframe.loc[:, 'dx'] = dx
  newdataframe.loc[:, 'dy'] = dy

  newdataframe['X'] = (newdataframe['X']/10.5)
  newdataframe['Y'] = (newdataframe['Y']/6.8)
  
  #newdataframe['dx'] = (newdataframe['dx']/10.5)
  #newdataframe['dy'] = (newdataframe['dy']/6.8)
  return newdataframe


  
newdataframe=newdataa(dataframe)

plt.show()
fig , ax = draw_pitch()
#Draw the pitch on the ax figure as well as invert the axis for this specific pitch
plt.gca().invert_yaxis()
x = int(input('inter player id: '))
df0 = newdataframe[newdataframe['ID'] == x ]
Title=('heat map for player with ID: '+ str(x))
ex = df0.plot(kind='scatter',x='X',y='Y',title=Title ,ax=ax)

kde = sns.kdeplot(
        df0['X'],
        df0['Y'],
        shade = True,
        shade_lowest=False,
        alpha=0.4,
        n_levels=4,
        cmap = 'magma'
)

fig.savefig('/outpot_data/average position.jpg',facecolor=fig.get_facecolor(), transparent=True)

plt.show()