from matplotlib import pyplot as plt

def voronoi_pic():
    reception_coords = dfFrame[dfFrame.player==12][['x','y']]        
    #saving versions assuming different time periods to the extrapolation
    for i in range(40):
        fig, ax, dfFrame, polygons = draw_voronoi(df, t=8, future=i)
        plt.title('Voronoi extrapolating position from current speed and direction: {:.2f} seconds'.format(i))
        plt.scatter(*reception_coords.values[0], c='black')
        fig.savefig('frame{}.jpg'.format(i+100), facecolor='#a8bc95')
        
    plt.close('all')
