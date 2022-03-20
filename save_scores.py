import numpy as np

def save_score(gun,kpm,bpm,sme):
    file = open('leaderboard.txt','a')
    if gun == 'rifle':
        string = "\n" + gun + "       " + str(kpm) + "      "  + str(bpm) + "     " + str(sme)
    else:
        string = "\n" + gun + "      " + str(kpm) + "      "  + str(bpm) + "     " + str(sme)
    file.write(string)

    file.close()
