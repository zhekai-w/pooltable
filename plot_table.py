import matplotlib.pyplot as plt
import random
import cv2
import numpy as np
import math

# define table height width
tablewidth = 1920
tableheight = 914

# radius of balls (30cm: 1.6cm = 914pixels : 97.5pixels)
R = 1.6/30*tableheight
r = round(R) #97
#radius of holes (63cm : 1920pixels = 2cm : 60pixels)
RB = 1920/63*2
rb = round(RB)

#define hole locations and aiming point
holex = [0, 0,           tablewidth/2, tablewidth/2, tablewidth, tablewidth]
holey = [0, tableheight, 0,            tableheight,  0,          tableheight]
aimpointx = [r, r,             tablewidth/2,  tablewidth-r,   tablewidth-r, tablewidth/2]
aimpointy = [r, tableheight-r, tableheight-r, tableheight-r,  r,            r]

# DISTANCE BETWEEN TWO BALLS
def disandvec(toballx, tobally, fromballx, frombally):
    x = toballx-fromballx
    y = tobally-frombally
    d = math.sqrt(abs(x)**2+abs(y)**2)
    d = round(d,2)
    return d, x, y

# GENERATE RANDOM NUMBER TO SIMULATE BALL LOCATION
def generateballs(numberofballs, r):
    print("number of balls:",numberofballs)

    # generate mother ball
    Motherx = random.randint(0+r, tablewidth-r)
    Mothery = random.randint(0+r, tableheight-r)

    # generate cue ball location
    cueballx = []
    cuebally = []
    for i in range(0,numberofballs):
        x = random.randint(0+r, tablewidth-r)
        cueballx.append(x)
        y = random.randint(0+r, tableheight-r)
        cuebally.append(y)
    return Motherx, Mothery, cueballx, cuebally, numberofballs

#CHECK IF BALL IS IN HOLE
def ballinhole(ballx, bally):
    balltohole = []
    for i in range(0,6):
        x, y, z= disandvec(holex[i], holey[i], ballx, bally)
        balltohole.append(x)
    mindis = min(balltohole)
    return mindis 

#CALCULATE VOCTOR TO DOT DISTANCE
def dottovector(fromdotx, fromdoty, todotx, todoty, dotx, doty):
    dis, vectorx, vectory = disandvec(todotx, todoty, fromdotx, fromdoty)
    balltoballx = dotx-fromdotx
    balltobally = doty-fromdoty
    dotproduct = vectorx*balltoballx + vectory*balltobally
    if dotproduct > 0:
        shadowlengh = dotproduct/dis
        ratio = shadowlengh/dis
        shadowx = fromdotx+vectorx*ratio
        shadowy = fromdoty+vectory*ratio
        normallengh, normalvectorx, normalvectory = disandvec(dotx, doty, shadowx, shadowy)

        return normallengh
                            #return normalvectorx, normalvectory, shadowx, shadowy
    else:
        return 0


if __name__ == '__main__':


    illogical = 1
    while illogical:
        Motherx, Mothery, cueballx, cuebally, n = generateballs(8, r)
        #cueball[-1] is mother ball
        cueballx.append(Motherx)
        cuebally.append(Mothery)
        print("cueball x axis:",cueballx)
        print("cueball y axis:",cuebally)

        # check if distance and vectors between balls are logical
        dis = []
        balltoballx = []
        balltobally = []
        k = 0
        for i in range(0,n):
            for j in range(0+k,n):
                d, x, y = disandvec(cueballx[j+1], cuebally[j+1], cueballx[i], cuebally[i])
                dis.append(d)
                balltoballx.append(x)
                balltobally.append(y)
            k=k+1
        print("distance between each balls:",dis)

        flag = 0
        lengh = len(dis)
        mindis = min(dis)
        print("minimum in distance:",mindis)
        for i in range(0,lengh):
            if dis[i] < 2*r:
                flag = flag + 1
        if flag == 0:
            illogical = 0
        else:
            illogical = 1
    
    inhole = ballinhole(Motherx, Mothery)
    print("distance from motherball to closest hole:", inhole)

    for i in range(0,n+1): #because mother ball is in cueball[-1]
        distohole = ballinhole(cueballx[i], cuebally[i])
        if distohole < rb:
            print("cueball[%d] is in hole"%i)    
        else:
            print("cueball[%d] is out of hole"%i) 

    # Plot vector from each cueballs to each aiming point
    balltoholedis = []*6
    Vx = []*6
    Vy = []*6
    all_balltoholedis = []*n
    all_vectors_BHx = []*n
    all_vectors_BHy = []*n
    c=['red','orange','black','green','blue','purple']
    for j in range(0,n):
        for i in range(0,6):
            dis, vx, vy = disandvec(aimpointx[i],aimpointy[i],cueballx[j],cuebally[j])
            balltoholedis.append(dis)
            Vx.append(vx)
            Vy.append(vy)
        all_balltoholedis.append(balltoholedis)
        all_vectors_BHx.append(Vx)
        all_vectors_BHy.append(Vy)
        balltoholedis = []*6
        Vx = []*6
        Vy = []*6
    print(all_vectors_BHx)
    #Draw vector from ball to aiming point
    for j in range(0,n):
        for i in range(0,6):
            plt.quiver(cueballx[j],cuebally[j],all_vectors_BHx[j][i],all_vectors_BHy[j][i],color=c[i],units="xy",angles="xy",scale_units="xy",scale=1, width=3)

    #Plot table boundry
    plt.plot([holex[0],holex[0]],[holey[0],holey[1]],[holex[0],holex[4]],[holey[0],holey[0]],
             [holex[0],holex[5]],[holey[1],holey[1]],[holex[5],holex[5]],[holey[0],holey[1]],color='black')
    
    #plot aim point
    for j in range(len(aimpointx)):
        aimpoint = plt.Circle((aimpointx[j], aimpointy[j]),
                            r, color="red", alpha=0.5)
        plt.gca().add_patch(aimpoint)

    #PLOT ALL BALLS AND HOLES
        #plot cueballs
    cueballcolor = ['r','orange','yellow','green','purple','black','brown','cyan']
    for i in range(len(cueballx)-1):
        cueball = plt.Circle((cueballx[i], cuebally[i]),
                            r, color=cueballcolor[i], alpha=0.5)
        plt.gca().add_patch(cueball)
    
    #plot mother ball
    plt.gca().add_patch(plt.Circle((Motherx, Mothery), r, color='red'))

    #plot holes
    for j in range(len(holex)):
        hole = plt.Circle((holex[j], holey[j]),
                            rb, color="black", alpha=0.7)
        plt.gca().add_patch(hole)

    plt.title("sim pool table") 
    plt.axis([0, tablewidth, tableheight, 0])
    plt.axis("equal")
    plt.show()

    # #plot cueballs' and mother ball's center
    # plt.scatter(cueballx, cuebally, c='blue', edgecolors='black',alpha=0.5)  #plot cue balls
    # plt.scatter(Motherx, Mothery, c='red', edgecolors='black', alpha=0.5)   

    # normallengh, normalvectorx, normalvectory, shadowx, shadowy = dottovector(cueballx[0], cuebally[0], aimpointx[0], aimpointy[0], cueballx[1], cuebally[1])
    # plt.scatter(shadowx, shadowy, c='black')
    # plt.quiver(shadowx, shadowy, normalvectorx, normalvectory,color='black',units="xy",angles="xy",scale_units="xy",scale=1, width=5)
    #check if there are balls in between cueball and aiming point 
    btball = []*n
    all_btball = []*6
    count = 0
    for i in range(0,n):
        for j in range(0,6):
            for k in range(0,n):
                btbdis = dottovector(cueballx[i], cuebally[i], aimpointx[j], aimpointy[j], cueballx[k], cuebally[k])
                #add fucntion to compare cueball[i] to aimpoint distance and cueball[i] to cueball[k] distance
                # if the previous distance is lesser than the later distance then cueball[k] is not in the way of cueball[i] to aimpoint   
                if 0 < btbdis < 2*r:
                    count = count+1
                    #if count = 1 or 2, record cueball[k]s is in way of vector cueball[i] to aimpoint[j] 
            btball.append(count)
            count = 0
        all_btball.append(btball)
        btball = []*6
    print(all_btball)

    #plot vectors from cueballs to holes which have no balls between 
    for j in range(0,n):
        for i in range(0,6):
            if all_btball[j][i] == 0:
                plt.quiver(cueballx[j],cuebally[j],all_vectors_BHx[j][i],all_vectors_BHy[j][i],color=c[i],units="xy",angles="xy",scale_units="xy",scale=1, width=3)
            #else if all_btball[j][i] == 1:
                


    #Plot table boundry
    plt.plot([holex[0],holex[0]],[holey[0],holey[1]],[holex[0],holex[4]],[holey[0],holey[0]],
             [holex[0],holex[5]],[holey[1],holey[1]],[holex[5],holex[5]],[holey[0],holey[1]],color='black')
    
    #plot aim point
    for j in range(len(aimpointx)):
        aimpoint = plt.Circle((aimpointx[j], aimpointy[j]),
                            r, color="red", alpha=0.2)
        plt.gca().add_patch(aimpoint)

    #PLOT ALL BALLS AND HOLES
        #plot cueballs
    for i in range(len(cueballx)-1):
        cueball = plt.Circle((cueballx[i], cuebally[i]),
                            r, color=cueballcolor[i], alpha=0.5)
        plt.gca().add_patch(cueball)
    
    #plot mother ball
    plt.gca().add_patch(plt.Circle((Motherx, Mothery), r, color='red'))

    #plot holes
    for j in range(len(holex)):
        hole = plt.Circle((holex[j], holey[j]),
                            rb, color="black", alpha=0.7)
        plt.gca().add_patch(hole)

    plt.title("sim pool table") 
    plt.axis([0, tablewidth, tableheight, 0])
    plt.axis("equal")
    plt.show()
    # #Draw vector from cueball n to the rest of the cueballs
    # plt.quiver(cueballx[0],cuebally[0],balltoballx[0],balltobally[0],color='black',units="xy",angles="xy",scale_units="xy",scale=1, width=5)

    # #shadow of ball1 to ball2 vector on ball1 to hole1 vector
    # dotproduct = Vx[0]*balltoballx[0]+Vy[0]*balltobally[0] 
    # if dotproduct > 0:
    #     shadowlengh = dotproduct/balltoholedis[0]
    #     ratio = shadowlengh/balltoholedis[0]
    #     shadowx = cueballx[0]+Vx[0]*ratio
    #     shadowy = cuebally[0]+Vy[0]*ratio
    #     dotproduct1 = Vx[0]*(cueballx[1]-shadowx)+Vy[0]*(cuebally[1]-shadowy)
    #     plt.quiver(shadowx,shadowy,cueballx[1]-shadowx,cuebally[1]-shadowy,color='brown',units="xy",angles="xy",scale_units="xy",scale=1, width=5)
    #     plt.scatter(shadowx,shadowy,c='black',edgecolors='black')
    #     print("shadow x:",shadowx)
    #     print("shadow y:",shadowy)
    #     print("dot product:",dotproduct)
    #     print("shadow lengh:",shadowlengh)
    #     print("shadow point to ball 1:",dotproduct1)
    # print("Vx:",Vx[0])
    # print("Vy",Vy[0])
    # print("ball to ball x:",balltoballx[0])
    # print("ball to ball y:",balltobally[0])
    # print("ball to hole dis:",balltoholedis[0])