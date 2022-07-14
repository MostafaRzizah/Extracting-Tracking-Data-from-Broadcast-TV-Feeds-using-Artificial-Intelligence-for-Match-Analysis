import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.patheffects as path_effects
from scipy.spatial import Voronoi
import random
from shapely.ops import cascaded_union
from shapely.geometry import Polygon, MultiPoint
from shapely import affinity

%matplotlib inline
plt.style.use('ggplot')


df = pd.read_csv('df_dup.csv',index_col=0)


dataframe=np.array(df)

df['X'] = (df['X']/10.5)
df['Y'] = (df['Y']/6.8)
df


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


def draw_frame( t,display_num=False ,text_color='black'):
    f = int(t*1)
    fig, ax = draw_pitch()
    
    if f == 0:
      f= 1 * 1
    else:
      f=f*1

#Stop condition at the maximum frame but not very accurate (need better solution) 

    if f > max_frame:
      f = max_frame
    
    
    dfFrame = df.loc[f].copy()
    plt.gca().invert_yaxis()

    for i, row in dfFrame.iterrows():
        if row['ID']==0:
            try:
                z = row['z']
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
            edge =  row['Color']

            color = row['Color']
            if row['Position']=='attack':
                zorder = 21
            else:
                zorder = 20

        ax.add_artist(Ellipse((row['X'],
                               row['Y']),
                              size/X_SIZE*100, size/Y_SIZE*100,
                              edgecolor=edge,
                              linewidth=lw,
                              facecolor=color,
                              alpha=0.8,
                              zorder=zorder))

        # s = row['ID']
        # if not(pd.isnull(s)):
        #     if isinstance(s, float):
        #         s=int(s)
        #     text = plt.text(row['X'],row['Y'],str(s),
        #                     horizontalalignment='center', verticalalignment='center',
        #                     fontsize=8, color=text_color, zorder=22, alpha=0.8)

        #     text.set_path_effects([path_effects.Stroke(linewidth=1, foreground=text_color, alpha=0.8),
        #                            path_effects.Normal()])

    return fig, ax, dfFrame


# anim = VideoClip(lambda x: mplfig_to_npimage(draw_frame(x)[0]), duration= 44)

# #Save the animation to a file
# anim.to_videofile('working with positional data - version 1.mp4', fps=5)

# #Display out videop
# #anim.ipython_display(fps = 5, loop = True, autoplay = True)
# ##draw_frame(df, 2)

# #Import everything needed to edit video clips
# from moviepy.editor import *

# # loading video gfg
# clip = VideoFileClip("working with positional data - version 1.mp4")
  
# # applying speed effect
# final = clip.fx( vfx.speedx, 4)

# # showing final clip
# final.ipython_display()
# final.to_videofile('5sec_filtered.mp4', fps=5)



direction = -1

def calculate_voronoi(dfFrame, future=0):
    dfTemp = dfFrame.copy().set_index('ID').drop(0, errors='ignore')
    dfTemp.x = dfTemp.X+dfTemp.dx*future*2
    dfTemp.y = dfTemp.Y+dfTemp.dy*future*2
    #7 becuase our data every 7 frame

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

def draw_voronoi( t):
    fig, ax, dfFrame = draw_frame( t)
    vor, dfVor = calculate_voronoi(dfFrame)
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



#     #fig, ax, dfFrame, polygons = draw_voronoi(df, t=1)


# anim = VideoClip(lambda x: mplfig_to_npimage(draw_voronoi(x)[0]), duration=40)

# #Save the animation to a file
# anim.to_videofile('working with positional data - version 1.mp4', fps=8)

# #Display out videop
# # anim.ipython_display(fps = 20, loop = True, autoplay = True)




# #Display out videop
# #anim.ipython_display(fps = 5, loop = True, autoplay = True)

# # Import everything needed to edit video clips
# from moviepy.editor import *

# # loading video gfg
# clip = VideoFileClip("working with positional data - version 1.mp4")
  
# # applying speed effect
# final = clip.fx( vfx.speedx, 8)

# # showing final clip
# final.ipython_display()
# final.to_videofile('5sec_filtered.mp4', fps=8)



fig, ax, dfFrame, polygons = draw_voronoi(current_time=1)
reception_coords = df[df.ID==3][['X','Y']]