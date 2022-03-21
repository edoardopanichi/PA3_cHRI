import numpy as np

def save_score(gun,kpm,bpm,sme,score):
    file = open('leaderboard.txt','a')
    if gun == 'rifle':
        string = "\n" + gun + "       " + str(kpm) + "      "  + str(bpm) + "     " + str(sme) + "        " + str(score) 
    else:
        string = "\n" + gun + "      " + str(kpm) + "      "  + str(bpm) + "     " + str(sme) + "        " + str(score)
    file.write(string)

    file.close()


def smth_else():
    file = open('leaderboard.txt','r')
    lines = file.readlines()
    pistol_avg=rifle_avg=sniper_avg = np.array([0,0,0])
    print(lines[2:])
    
    for line in lines[:2]:
        line_list = np.array(line.split())
        print(line_list[1:])
        if line_list != []:
            if line_list[0]=='pistol':
               pistol_avg+= line_list[1:]
            elif line_list[0]=='rifle':
                rifle_avg+= line_list[1:]
            elif line_list[0]=='sniper':
                sniper_avg+= line_list[1:]
    
    print(pistol_avg)

    