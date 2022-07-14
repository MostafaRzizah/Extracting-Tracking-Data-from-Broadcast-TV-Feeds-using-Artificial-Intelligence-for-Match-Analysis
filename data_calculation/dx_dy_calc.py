
def dx_dy_calc(df):

    df.groupby(['ID'])

    df['frame']=df['frame']/7
    dataframe=np.array(df.sort_values(['ID','frame']))

    dx=[0]
    dy=[0]
    for i in range(1,len(dataframe)):
    if(dataframe[i,1]==dataframe[i-1,1]):
        if (dataframe[i,0])== (dataframe[i-1,0]+7):
            distancex=(dataframe[i,2]-dataframe[i-1,2])
            dx.append(distancex)
            distancey=(dataframe[i,3]-dataframe[i-1,3])
            dy.append(distancey)
        else:
            dx.append(0)
            dy.append(0) 
    else:
        dx.append(0)
        dy.append(0)
    df.loc[:, 'dx'] = dx
    df.loc[:, 'dy'] = dy

    return df
