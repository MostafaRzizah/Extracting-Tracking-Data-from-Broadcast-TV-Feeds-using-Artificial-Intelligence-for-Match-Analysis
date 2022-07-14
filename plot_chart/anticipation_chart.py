import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from celluloid import Camera
from IPython.display import HTML


df = pd.read_csv('calma_df_mapped_final.csv',index_col=0)
df=df.reset_index()  
df = df.drop_duplicates(subset=["ID", "frame"], keep=False)
first_frame = df['frame'].iat[0]
df['frame']=df['frame']/first_frame
df=df.set_index('frame')

df['X'] = (df['X']/10.5)
df['Y'] = (df['Y']/6.8)
df


dataframe=np.array(df.sort_values(['ID','frame']))

dx=[0]
dy=[0]
for i in range(1,len(dataframe)):
  if(dataframe[i,0]==dataframe[i-1,0]):
    distancex=(dataframe[i,1]-dataframe[i-1,1])
    dx.append(distancex)
    distancey=(dataframe[i,2]-dataframe[i-1,2])
    dy.append(distancey)
  else:
    dx.append(0)
    dy.append(0)
df.loc[:, 'dx'] = dx
df.loc[:, 'dy'] = dy
#df['dx'] = (df['dx']/10.5)
#df['dy'] = (df['dy']/6.8)
df
df.to_csv('df_with_dx_dy.csv')



players = [3, 4, 5] # player_id 12 is the attacker; ids 7347 and 7346 the two defenders closest to the attacker
df['d'] = np.sqrt(np.square(df.dx)+np.square(df.dy))

#creating new array for each given id
d1 = df.loc[df.ID == 3 , 'd']
d2 = df.loc[df.ID == 4 , 'd']
d3 = df.loc[df.ID == 5 , 'd']


fig , ax = plt.subplots( figsize= (15,5))
camera = Camera(fig)
for i in range(0,len(d1)):
    z1 = d1[:i]
    plt.plot(z1, color = 'red')

    z2 = d2[:i]
    plt.plot(z2, color = 'black')

    z3 = d3[:i]
    plt.plot(z3, color = 'black')

    #take camera snap 
    #fig.tight_layout()
    camera.snap()  
    plt.xlim(0, 20)


#xticks arrange have limit time of the video to arrange second

plt.xticks(np.arange(0, 20, 4 ), np.arange(0, 4))
# 0 is starting 20 is the last 4 for step value
plt.xlabel('Time (s)')
plt.ylabel('Speed (m)')

plt.axvline(0.5*4, color='blue')    
# 4 frame per second

#animating data 
animation = camera.animate()
HTML(animation.to_html5_video())

# for p in players:
#     if p!=0:
#         if p==3:
#             color='red'
#         else:
#             color='black'
#         dfPlot = df.loc[df.ID==p]
#         plt.plot(dfPlot.d, color=color)
