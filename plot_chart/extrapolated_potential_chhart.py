def extrapolated_potential():
    #calculating threats
    threats = [(calculate_value(df, t, 0), calculate_value(df, t, 1)) for t in np.arange(0, max(df.index)/20, 0.05)]

    #ploting current and extrapolated threats
    cur_threat, fut_threat = list(zip(*threats))
    plt.plot(cur_threat, label='current')
    plt.plot(fut_threat, label='extrapolated')

    plt.xticks(np.arange(0, 200, 20), np.arange(0, 9))
    plt.xlabel('Time (s)')
    plt.ylabel('potential xT')
    plt.ylim(bottom=0)
    plt.legend()
    plt.axvline(6.5*20, color='blue')
    plt.xlim(0, 160)
    plt.ylim(0, 85)
