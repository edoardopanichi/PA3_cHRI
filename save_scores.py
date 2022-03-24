import numpy as np

def save_score(gun,kpm,bpm,sme,score):
    file = open('leaderboard.txt','a')
    if gun == 'rifle':
        string = "\n" + gun + "       " + str(kpm) + "      "  + str(bpm) + "     " + str(sme) + "        " + str(score) 
    else:
        string = "\n" + gun + "      " + str(kpm) + "      "  + str(bpm) + "     " + str(sme) + "        " + str(score)
    file.write(string)

    file.close()




    