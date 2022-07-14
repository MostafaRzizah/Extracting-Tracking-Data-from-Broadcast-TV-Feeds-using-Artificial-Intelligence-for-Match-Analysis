import numpy as np
import pandas as pd
from shapely.geometry import Polygon, MultiPoint
import matplotlib
from matplotlib.patches import Ellipse
from matplotlib import pyplot as plt
from scipy.spatial import Voronoi


df= pd.read_csv('calma_df_mapped_final.csv')
dfPlayers = pd.read_csv('calma_df_mapped_final.csv')

#Getting The max frame value
df_max_frame=df['frame']
max_frame=df_max_frame.max()
first_frame = df['frame'].iat[0]

#Get the data again and apply coordinates operation to adjust players position
df=pd.read_csv('calma_df_mapped_final.csv',index_col=(0,1))

df['X']=df['X'].apply(lambda x: ((x/10)*105/100)-11 if(x>500) else (x/10)*105/100) 
df['Y']=df['Y'].apply(lambda y: (y/10)*100/68)

#Drop some unessential cloumns
df = df.drop(columns=['Class', 'Color','Position'])

#Show our data

df
#print(first_frame)


# Using one color of each unqiue ID
dfPlayers=dfPlayers.groupby('ID').first()
dfPlayers.reset_index()  

#Show our data
dfPlayers 


#This Box of code help to draw our pitch and player
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
    axes.set_ylim(100,0)

    plt.xlim([-13.32, 113.32])
    plt.ylim([105, -5])

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
def draw_frame(df, dfPlayers, t, text_color='black'):
    f = int(t*1)
    fig, ax = draw_pitch()
    dfFrame = df.loc[f]

    for pid in dfFrame.index:
        if dfPlayers.loc[pid]['Position']=='Ball':
            #formatting for ball (id==0)
            try:
                z = dfFrame.loc[pid]['z']
            except:
                z = 0
            size = 1.3+z
            lw = 0.7
            color='black'
            edge='white'
            zorder = 100
        else:
            #formatting for players
            size = 3
            lw = 2
            
            color = dfPlayers.loc[pid]['Color']
            if dfPlayers.loc[pid]['Color']=='red':
                zorder = 21
            else:
                zorder = 20

        ax.add_artist(Ellipse((dfFrame.loc[pid]['X'],
                               dfFrame.loc[pid]['Y']),
                              size/X_SIZE*100, size/Y_SIZE*100,
                              linewidth=lw,
                              facecolor=color,
                              alpha=0.8,
                              zorder=zorder))
        
        #if pid!=0:
         #   s = dfPlayers.loc[pid]['player_num']
          #  if not(pd.isnull(s)):
           #     if isinstance(s, float):
            #        s=int(s)
             #   text = plt.text(dfFrame.loc[pid]['X'],dfFrame.loc[pid]['Y'],str(s),
              #                 horizontalalignment='center', verticalalignment='center',
               #                 fontsize=8, color=text_color, zorder=22, alpha=0.8)

                #text.set_path_effects([path_effects.Stroke(linewidth=1, foreground=text_color, alpha=0.8),
                #                       path_effects.Normal()])

    return fig, ax, dfFrame

direction = -1

def calculate_voronoi(dfFrame, dfPlayers):
    dfTemp = dfFrame.copy().drop(0, errors='ignore').join(dfPlayers, rsuffix='_dup')

    values = np.vstack((dfTemp[['X', 'Y']].values*SCALERS,
                        [-1000,-1000],
                        [+1000,+1000],
                        [+1000,-1000],
                        [-1000,+1000]
                       ))

    vor = Voronoi(values)

    dfTemp['region'] = vor.point_region[:-4]
    
    return vor, dfTemp

pitch = Polygon(((0,0), (0,100), (100,100), (100,0)))

def draw_voronoi(df, dfPlayers, t=1):
    fig, ax, dfFrame = draw_frame(df, dfPlayers, t)
    vor, dfVor = calculate_voronoi(dfFrame, dfPlayers)
    polygons = {}
    for index, region in enumerate(vor.regions):
        if not -1 in region:
            if len(region)>0:
                try:
                    pl = dfVor[dfVor['region']==index]
                    polygon = Polygon([vor.vertices[i] for i in region]/SCALERS).intersection(pitch)
                    color = pl['Color'].values[0]
                    x, y = polygon.exterior.xy
                    plt.fill(x, y, c=color, alpha=0.30)
                    polygons[pl.index[0]] = polygon
                except IndexError:
                    pass
                except AttributeError:
                    pass

        plt.scatter(dfVor['X'], dfVor['Y'], c=dfVor['Color'], alpha=0.2)
    return fig, ax, dfFrame, polygons

# showing result
fig, ax, dfFrame, polygons = draw_voronoi(df, dfPlayers, t=6)
dfFrame


