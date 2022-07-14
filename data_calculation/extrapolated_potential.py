#df['dx'] = (df['dx']/10.5)
#df['dy'] = (df['dy']/6.8)
import json
#########################################################################
#loading the json file with the xT values for each zone of the pitch 
with open('open_xt_12x8_v1.json', 'r') as f:
    xTvalues = np.array(json.load(f))
    
def offset_df(df, dx, dy):
    df = df.copy()
    df.X = df.Y+dx
    df.Y = df.Y+dy  
    return df

dfxT = df.from_records(xTvalues).unstack().reset_index()
dfxT.columns = ['X', 'Y', 'xT']

dfxT = pd.concat([offset_df(dfxT, dx, dy)
                  for dx, dy
                  in [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)]
                 ])

ny, nx = xTvalues.shape

dfxT.X = dfxT.X*100/nx
dfxT.Y = dfxT.Y*100/ny

#only consider locations with better than median threat (i.e. ignore defensive positions)
dfxT.xT = np.clip(dfxT.xT-dfxT.xT.median(), 0, 1)

#flip axis if necessary (to align with attacking team)
#dfxT.X = 100-dfxT.X
#dfxT.Y = 100-dfxT.Y

points = MultiPoint(list(zip(dfxT['X'], dfxT['Y'])))
dfValues = dfxT.set_index(['X', 'Y'])

player_values = {}

attack_polygon = cascaded_union([polygon for player,polygon in polygons.items() if dfPlayers.loc[player]['Position']=='Attack'])

values = [dfValues.loc[p.x,p.y].values[0] for p in attack_polygon.intersection(points)]
area_value = np.mean(values)*attack_polygon.area

################################
df_max_frame=df['frame']
max_frame=df_max_frame.max()
##############################
def calculate_value(df, t, future=0):
    if t == 0:
       t=1*1
    f = int(t*1)
    if f > max_frame :
       f = max_frame
    else:
       f=f*1
    dfFrame = df.loc[f]

    vor, dfVor = calculate_voronoi(dfFrame, future)
    polygons = {}
    for index, region in enumerate(vor.regions):
        if not -1 in region:
            if len(region)>0:
                try:
                    pl = dfVor[dfVor['region']==index]
                    polygon = Polygon([vor.vertices[i] for i in region]/SCALERS).intersection(pitch)
                    polygons[pl.index[0]] = polygon
                except IndexError:
                    pass
                except AttributeError:
                    pass
    
    attack_polygon = cascaded_union([polygon for player,polygon in polygons.items() if dfPlayers.loc[player]['Color']=='red'])
    values = [dfValues.loc[p.x,p.y].values[0] for p in attack_polygon.intersection(points)]
    area_value = np.mean(values)*attack_polygon.area
    return area_value
values = [calculate_value(df, t=0) for t in range(22)]
##############################################
#     frame number  ^        
#calculate_value(df, 1, 0), calculate_value(df, 1, 2)
#values
#############################################



