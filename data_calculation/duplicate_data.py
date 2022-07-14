import csv
import pandas as pd
import numpy as np
from google.colab import files

data = files.upload()

#df.drop(columns=df.columns[:1],axis=1, inplace=True,)

def newdataa(dataframe):
##############################################################
    df.reset_index(drop=True)
    dataframe=np.array(df.sort_values(['ID','frame']))

    df =pd.read_csv('filtered_data.csv',ignore_index=True)

    df['frame']=df['frame']/7
###############################################################

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
            #x_avg = (dataframe[i,2]+dataframe[i-1,2])/2
            nx.append(dataframe[i-1,2])
            nx.append(dataframe[i-1,2])
            
            #y array 
            #y_avg = (dataframe[i,3]+dataframe[i-1,3])/2
            ny.append(dataframe[i-1,3])  
            ny.append(dataframe[i-1,3])
            

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
                
    newdataframe = pd.DataFrame({'frame':nframe,'ID':nid,'X':nx,'Y':ny,'Class':dataclass,'Color':color,'Position':position})
    #newdataframe=newdataframe.groupby(['ID']) 

    newdddd=np.array(newdataframe.sort_values(['ID','frame']))
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

    #newdataframe['X'] = (newdataframe['X']/10.5)
    #newdataframe['Y'] = (newdataframe['Y']/6.8)
    
    #newdataframe['dx'] = (newdataframe['dx']/10.5)
    #newdataframe['dy'] = (newdataframe['dy']/6.8)
    newdataframe.to_csv('/outpot_data/duplicated_df.csv')

    return newdataframe
newdataframe=newdataa(dataframe)
newdataframe
