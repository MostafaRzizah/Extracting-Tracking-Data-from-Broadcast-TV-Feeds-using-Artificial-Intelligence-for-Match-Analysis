
def xt_gained():
    #calculating threats
    threats = [(calculate_value(df, t, 0), calculate_value(df, t, 1)) for t in np.arange(0, max(df.index)/20, 0.05)]

    #plot xt gained movement
    cur_threat, fut_threat = list(zip(*threats))
    plt.plot(np.array(fut_threat)-np.array(cur_threat))

    plt.xticks(np.arange(0, 300, 20), np.arange(0, 15))
    plt.xlabel('Time (s)')
    plt.ylabel('xT gained from movement')
    plt.ylim(bottom=0)
    plt.xlim(0, 160)

    plt.axvline(6.5*20, color='blue')

