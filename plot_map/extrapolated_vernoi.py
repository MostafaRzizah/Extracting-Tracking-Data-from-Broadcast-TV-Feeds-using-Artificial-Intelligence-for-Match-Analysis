#chage the draw_voronoi function to accept another argument: future, the number of seconds used to extrapolate predicted future positions

reception_coords = df[df.ID==3][['X','Y']]
def draw_voronoi( t, future=0):
    df=df
    fig, ax, dfFrame = draw_frame( t)
    vor, dfVor = calculate_voronoi(dfFrame, future)
    polygons = {}
    for index, region in enumerate(vor.regions):
        if not -1 in region:
            if len(region)>0:
                try:
                    pl = dfVor[dfVor['region']==index]
                    polygon = Polygon([vor.vertices[i] for i in region]/SCALERS).intersection(pitch)
                    color = pl['Color'].values[0]
                    X, Y = polygon.exterior.xy
                    plt.fill(X, Y, c=color, alpha=0.30)
                    polygons[pl.index[0]] = polygon
                except IndexError:
                    pass
                except AttributeError:
                    pass

        plt.scatter(dfVor['X'], dfVor['Y'], c=dfVor['Color'], alpha=0.2)
    return fig, ax, dfFrame, polygons

fig, ax, dfFrame, polygons = draw_voronoi(df, t=1, future=2)
plt.title('Voronoi extrapolating position from current speed and direction: 1.0 seconds')
plt.scatter(*reception_coords.values[0], c='red')


anim = VideoClip(lambda x: mplfig_to_npimage(draw_voronoi(x)[0]), duration=5)
anim.to_videofile('working with positional data - version 1.mp4', fps=8)
anim.ipython_display(fps = 8, loop = True, autoplay = True)

