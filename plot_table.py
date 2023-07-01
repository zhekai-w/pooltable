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
holex =     [0, 0,             tablewidth/2, tablewidth,    tablewidth,   tablewidth/2]
holey =     [0, tableheight,   tableheight,  tableheight,   0,            0]
aimpointx = [r, r,             tablewidth/2, tablewidth-r,  tablewidth-r, tablewidth/2]
aimpointy = [r, tableheight-r, tableheight-r,tableheight-r, r,            r]
aimtoholex = [-r,-r,0,r,r,0]
aimtoholey = [-r,r,r,r,-r,-r]

# DISTANCE BETWEEN TWO BALLS
def disandvec(toballx, tobally, fromballx, frombally):
    x = toballx-fromballx
    y = tobally-frombally
    d = math.sqrt(abs(x)**2+abs(y)**2)
    #round for the sake of visual, don't round it for accuracy
    d = round(d,2)
    return d, x, y

# GENERATE RANDOM NUMBER TO SIMULATE BALL LOCATION
def generateballs(numberofballs, r):
    print("number of balls:",numberofballs)

    # generate cue ball
    cuex = random.randint(0+r, tablewidth-r)
    cuey = random.randint(0+r, tableheight-r)

    # generate cue ball location
    objectballx = []
    objectbally = []
    for i in range(0,numberofballs):
        x = random.randint(0+r, tablewidth-r)
        objectballx.append(x)
        y = random.randint(0+r, tableheight-r)
        objectbally.append(y)
    return cuex, cuey, objectballx, objectbally, numberofballs

#CHECK IF BALL IS IN HOLE
def ballinhole(ballx, bally):
    balltohole = []
    for i in range(0,6):
        x, y, z= disandvec(holex[i], holey[i], ballx, bally)
        balltohole.append(x)
    mindis = min(balltohole)
    return mindis 

#CALCULATE VOCTOR TO DOT DISTANCE
def dottovector(fromdotx, fromdoty, vectorx, vectory, dotx, doty):
    disoto = math.sqrt(abs(vectorx)**2+abs(vectory)**2)
    balltoballx = dotx-fromdotx
    balltobally = doty-fromdoty
    dotproduct = vectorx*balltoballx + vectory*balltobally
    if dotproduct > 0:
        shadowlengh = dotproduct/disoto
        ratio = shadowlengh/disoto
        shadowx = fromdotx+vectorx*ratio
        shadowy = fromdoty+vectory*ratio
        #normallengh, normalvectorx, normalvectory = disandvec(dotx, doty, shadowx, shadowy)
        normallengh = disandvec(dotx, doty, shadowx, shadowy)[0]

        return normallengh#, normalvectorx, normalvectory, shadowx, shadowy
    else:
        return -1
    
def findhitpoint(ballx, bally, vectorx, vectory):
    vectorlengh = math.sqrt(abs(vectorx)**2+abs(vectory)**2)
    x = vectorx*2*r/vectorlengh
    y = vectory*2*r/vectorlengh
    hitpointx = ballx-x
    hitpointy = bally-y
    return hitpointx, hitpointy


if __name__ == '__main__':


    illogical = 1
    while illogical:
        cuex, cuey, objectballx, objectbally, n = generateballs(10, r)
        #objectball[-1] is cue ball
        # objectballx = [1180,203,936,439,478]
        # objectbally = [53,758,148,223,795]
        # cuex = 288
        # cuey = 195
        # n = 5
        objectballx.append(cuex)
        objectbally.append(cuey)
        print("number of balls:",n)
        print("objectball x axis:",objectballx)
        print("objectball y axis:",objectbally)

        # check if distance and vectors between balls are logical(meaning they are not stacked)
        dis = []
        balltoballx = []
        balltobally = []
        k = 0
        for i in range(0,n):
            for j in range(0+k,n):
                d, x, y = disandvec(objectballx[j+1], objectbally[j+1], objectballx[i], objectbally[i])
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
    
    inhole = ballinhole(cuex, cuey)
    print("distance from cueball to closest hole:", inhole)

    for i in range(0,n+1): #because cue ball is in objectball[-1]
        distohole = ballinhole(objectballx[i], objectbally[i])
        if distohole < rb:
            print("objectball[%d] is in hole"%i)    
        else:
            print("objectball[%d] is out of hole"%i) 

    # Plot vector from each objectballs to each aiming point
    balltoholedis = []*6
    Vx = []*6
    Vy = []*6
    all_balltoholedis = []*n
    all_vectors_BHx = []*n
    all_vectors_BHy = []*n
    cuetohitx = []*6
    cuetohity = []*6
    all_cuetohitx = []*n
    all_cuetohity = []*n
    c=['red','orange','black','green','blue','purple']

    for j in range(0,n):
        for i in range(0,6):
            dis, vx, vy = disandvec(aimpointx[i],aimpointy[i],objectballx[j],objectbally[j])
            balltoholedis.append(dis)
            Vx.append(vx)
            Vy.append(vy)

            hitx, hity = findhitpoint(objectballx[j],objectbally[j],vx,vy)
            _,tempcuetohitx, tempcuetohity = disandvec(hitx,hity,cuex,cuey)
            cuetohitx.append(tempcuetohitx)
            cuetohity.append(tempcuetohity)

        all_balltoholedis.append(balltoholedis)
        all_vectors_BHx.append(Vx)
        all_vectors_BHy.append(Vy)
        all_cuetohitx.append(cuetohitx)
        all_cuetohity.append(cuetohity)
        balltoholedis = []*6
        Vx = []*6
        Vy = []*6
        cuetohitx = []*6
        cuetohity = []*6
    
    print("all vectors ball to hole x:\n",all_vectors_BHx)
    print("all vectors ball to hole y:\n",all_vectors_BHy)

    #plot vector from aiming point to hole
    for i in range(0,6):
        plt.quiver(aimpointx[i],aimpointy[i],aimtoholex[i],aimtoholey[i],color='red',units="xy",angles="xy",scale_units="xy",scale=1, width=3)

    #Draw vector from ball to aiming point and cueball to hitpoitn 
    for i in range(0,n):
        for j in range(0,6):
            plt.quiver(objectballx[i],objectbally[i],all_vectors_BHx[i][j],all_vectors_BHy[i][j],color=c[j],units="xy",angles="xy",scale_units="xy",scale=1, width=3)
            plt.quiver(cuex,cuey,all_cuetohitx[i][j],all_cuetohity[i][j],color='black',units="xy",angles="xy",scale_units="xy",scale=1, width=2,alpha=0.5)
    


    #Plot table boundry
    plt.plot([holex[0],holex[1]],[holey[0],holey[1]],[holex[1],holex[2]],[holey[1],holey[2]],
             [holex[2],holex[3]],[holey[2],holey[3]],[holex[3],holex[4]],[holey[3],holey[4]],
             [holex[4],holex[5]],[holey[4],holey[5]],[holex[5],holex[0]],[holey[5],holey[0]],color='black')
    
    #plot aim point
    for j in range(len(aimpointx)):
        aimpoint = plt.Circle((aimpointx[j], aimpointy[j]),
                            r, color="red", alpha=0.2)
        plt.text(aimpointx[j],aimpointy[j],j,color='red',fontsize=15)
        plt.gca().add_patch(aimpoint)

    #PLOT ALL BALLS AND HOLES
        #plot objectballs
    objectballcolor = ['r','orange','blue','green','purple','black','brown','cyan']
    for i in range(len(objectballx)-1):
        objectball = plt.Circle((objectballx[i], objectbally[i]),
                            r, color='blue', alpha=0.5)
        plt.text(objectballx[i],objectbally[i],i,fontsize=15)
        plt.gca().add_patch(objectball)
    
    #plot cue ball
    plt.gca().add_patch(plt.Circle((cuex, cuey), r, color='red'))
    

    #plot holes
    for j in range(len(holex)):
        hole = plt.Circle((holex[j], holey[j]),
                            rb, color="black", alpha=0.7)
        #plt.text(holex[j],holey[j],j,color='white',fontsize=15)
        plt.gca().add_patch(hole)

    plt.title("sim pool table") 
    plt.axis([0, tablewidth, tableheight, 0])
    plt.axis("equal")
    plt.show()

    # #plot objectballs' and cue ball's center
    # plt.scatter(objectballx, objectbally, c='blue', edgecolors='black',alpha=0.5)  #plot cue balls
    # plt.scatter(cuex, cuey, c='red', edgecolors='black', alpha=0.5)   

    # normallengh, normalvectorx, normalvectory, shadowx, shadowy = dottovector(objectballx[0], objectbally[0], aimpointx[0], aimpointy[0], objectballx[1], objectbally[1])
    # plt.scatter(shadowx, shadowy, c='black')
    # plt.quiver(shadowx, shadowy, normalvectorx, normalvectory,color='black',units="xy",angles="xy",scale_units="xy",scale=1, width=5)

    #check if there are balls in between objectball and aiming point / cueball to hit point
    btball = []*n
    all_btball = []*6
    count = 0
    KinwayofI = []*n
    all_KinwayofI = []*6
    whoinway = []
    for i in range(0,n):
        for j in range(0,6):
            for k in range(0,n):
                btvdis = dottovector(objectballx[i], objectbally[i], all_vectors_BHx[i][j],all_vectors_BHy[i][j], objectballx[k], objectbally[k])
                # compare objectball[i] to aimpoint distance and objectball[i] to objectball[k] distance
                # if the previous distance is lesser than the later distance then objectball[k] is not in the way of objectball[i] to aimpoint   
                disota = disandvec(aimpointx[j],aimpointy[j],objectballx[i],objectbally[i])[0]
                disoto = disandvec(objectballx[k],objectbally[k],objectballx[i],objectbally[i])[0]
                if 0 <= btvdis < 2*r and disota > disoto+2*r:
                    count = count+1
                    #if count = 1 or 2, record objectball[k]s is in way of vector objectball[i] to aimpoint[j](index)
                    # Better solution ? just record k and let the index of all_KinwayofI do the rest(meaning k is in who's way) 
                    whoinway.append(k)

            btball.append(count)
            count = 0
            KinwayofI.append(whoinway)
            whoinway = []
        all_btball.append(btball)
        btball = []*n
        all_KinwayofI.append(KinwayofI)
        KinwayofI = []*n

    print("how many ball(s) is in way of object to hole:\n",all_btball)
    print("who is in way of this vector:\n",all_KinwayofI)
    
    #plot vectors from objectballs to holes which have no balls between 
    for i in range(0,n):
        for j in range(0,6):
            if all_btball[i][j] == 0: 
                #check if there is ball in way of cueball to hitpoint/check hitpoint out of bound ?
                hitx,hity = findhitpoint(objectballx[i],objectbally[i],all_vectors_BHx[i][j],all_vectors_BHy[i][j])
                temx = hitx-cuex
                temy = hity-cuey
                dotproduct = all_vectors_BHx[i][j]*temx + all_vectors_BHy[i][j]*temy
                #check hit point out of bound
                checkhitxplus = hitx + r
                checkhityplus = hity + r
                checkhitxminus = hitx - r 
                checkhityminus = hity - r 
                if checkhitxplus > 1920 or checkhityplus > 914 or checkhitxminus < 0 or checkhityminus < 0:
                    hitoutbound = 1
                else:
                    hitoutbound = 0
                #check if there is/are ball(s) in between cue to hit point
                for k in range(0,n):
                    CtoIdis = dottovector(cuex,cuey,temx,temy,objectballx[k],objectbally[k])
                    disCtoI = math.sqrt(abs(temx)**2+abs(temy)**2)
                    disCtoK = disandvec(objectballx[k],objectbally[k],cuex,cuey)[0]
                    if 0 <= CtoIdis < 2*r and disCtoK < disCtoI+R:
                        ballinwayCI0 = 1
                        break
                    else: 
                        ballinwayCI0 = 0
                #if no ball in cue to hitpoint and both vectors' angle smaller than 90 degrees and hitpoint is not out of bound
                if ballinwayCI0 == 0 and dotproduct > 0 and hitoutbound == 0:
                    plt.quiver(objectballx[i],objectbally[i],all_vectors_BHx[i][j],all_vectors_BHy[i][j],color='green',units="xy",angles="xy",scale_units="xy",scale=1, width=3)
                    plt.quiver(cuex,          cuey,          all_cuetohitx[i][j],all_cuetohity[i][j],color='green',units="xy",angles="xy",scale_units="xy",scale=1, width=3)


            if all_btball[i][j] == 1:
                #draw objectball[k] to aimpoint[j] vector and objectball[j] to shadow of objectball[k]'s vector 
                k = all_KinwayofI[i][j][0]
                #plt.quiver(objectballx[k],objectbally[k],all_vectors_BHx[k][j],all_vectors_BHy[k][j],color='black',units="xy",angles="xy",scale_units="xy",scale=1, width=5)
                #check objectball[k] to hitpoint (ball_btball[k][j])
                if all_btball[k][j] == 0:
                    #draw objectball[j] to objectball[k]'s hitpoint
                    hitkx,hitky = findhitpoint(objectballx[k],objectbally[k],all_vectors_BHx[k][j],all_vectors_BHy[k][j])
                    temkx = hitkx-objectballx[i]
                    temky = hitky-objectbally[i]
                    dotproductk = all_vectors_BHx[k][j]*temkx + all_vectors_BHy[k][j]*temky
                    for l in range(0,n):
                        tempItoKdis = dottovector(objectballx[i],objectbally[i],temkx,temky,objectballx[l],objectbally[l])
                        disItoK = math.sqrt(abs(temkx)**2+abs(temky)**2)
                        disItoL = disandvec(objectballx[l],objectbally[l],objectballx[i],objectbally[i])[0]
                        if 0 <= tempItoKdis < 2*r and disItoL < disItoK+R:
                            ballinwayIK = 1
                            break
                        else: 
                            ballinwayIK = 0
                    if  ballinwayIK == 0 and dotproductk > 0:
                        #plt.quiver(objectballx[i],objectbally[i],temkx,temky,color='blue',units="xy",angles="xy",scale_units="xy",scale=1, width=5)
                        #draw cue to objectball[i]'s hitpoint 
                        hitix, hitiy = findhitpoint(objectballx[i],objectbally[i],temkx,temky)
                        temix = hitix - cuex
                        temiy = hitiy - cuey
                        dotproducti = temix*temkx + temiy*temky
                        for m in range(0,n):
                            tempCtoKdis = dottovector(cuex,cuey,temix,temiy,objectballx[m],objectbally[m])
                            disCtoI = math.sqrt(abs(temix)**2+abs(temiy)**2)
                            disCtoM = disandvec(cuex,cuey,objectballx[m],objectbally[m])[0]
                            if 0 <= tempCtoKdis < 2*r and disCtoM < disCtoI+R:
                                ballinwayCI1 = 1
                                break
                            else: 
                                ballinwayCI1 = 0
                        if  ballinwayCI1 == 0 and dotproducti > 0:
                            plt.quiver(objectballx[k],objectbally[k],all_vectors_BHx[k][j],all_vectors_BHy[k][j],color='blue',units="xy",angles="xy",scale_units="xy",scale=1, width=5)
                            plt.quiver(objectballx[i],objectbally[i],temkx,temky,color='blue',units="xy",angles="xy",scale_units="xy",scale=1, width=5)
                            plt.quiver(cuex,cuey,temix,temiy,color='blue',units="xy",angles="xy",scale_units="xy",scale=1, width=3)
                        

            if all_btball[i][j] == 2:
                k1 = all_KinwayofI[i][j][0]
                k2 = all_KinwayofI[i][j][1]

                #to decide who is closer to objectball[j]. Need to compare (k1 to i dis) and (k2 to i dis) otherwise the vector could be reversed
                #DEFINE k1 is closer to hole and k2 is closer to j
                k1dis = disandvec(objectballx[k1],objectbally[k1],objectballx[i],objectbally[i])[0]
                k2dis = disandvec(objectballx[k2],objectbally[k2],objectballx[i],objectbally[i])[0]
                if k1dis > k2dis:
                    k1 = k1
                    k2 = k2
                elif k1dis < k2dis:
                    temp = k1 
                    k1 = k2
                    k2 = temp
                elif k1dis == k2dis:
                    #compare (k1 to hole dis) and (k2 to hole dis), use the shortest   
                    k1toadis = disandvec(aimpointx[j],aimpointy[j],objectballx[k1],objectbally[k1])
                    k2toadis = disandvec(aimpointx[j],aimpointy[j],objectballx[k2],objectbally[k2])
                    if k1toadis >= k2toadis:
                        temp = k1 
                        k1 = k2
                        k2 = temp
                    elif k1toadis < k2toadis:
                        k1 = k1
                        k2 = k2
                #start to find valid route
                if all_btball[k1][j] == 0:
                    hitk1x, hitk1y = findhitpoint(objectballx[k1],objectbally[k1],all_vectors_BHx[k1][j],all_vectors_BHy[k1][j])
                    temk1x = hitk1x-objectballx[k2]
                    temk1y = hitk1y-objectbally[k2]
                    dotproductk1 = all_vectors_BHx[k1][j]*temk1x + all_vectors_BHy[k1][j]*temk1y
                    
                    #before checking if any ball(s) in K2 to K1, check cueball to K1 


                    for l in range(0,n):
                        tempK2toK1dis = dottovector(objectballx[k2],objectbally[k2],temk1x,temk1y,objectballx[l],objectbally[l])
                        disK2toK1 = math.sqrt(abs(temk1x)**2+abs(temk1y)**2)
                        disK2toL = disandvec(objectballx[l],objectbally[l],objectballx[k2],objectbally[k2])[0]
                        if 0 <= tempK2toK1dis < 2*r and disK2toL < disK2toK1+R:
                            ballinwayIK1 = 1
                            break
                        else: 
                            ballinwayIK1 = 0
                    if ballinwayIK1 == 0 and dotproductk1 > 0:
                        hitk2x, hitk2y = findhitpoint(objectballx[k2],objectbally[k2],temk1x,temk1y)
                        temk2x = hitk2x-objectballx[i]
                        temk2y = hitk2y-objectbally[i]
                        dotproductk2 = temk1x*temk2x + temk1y*temk2y
                        for m in range(0,n):
                            tempItoK2dis = dottovector(objectballx[i],objectbally[i],temk2x,temk2y,objectballx[m],objectbally[m])
                            disItoK2 = math.sqrt(abs(temk2x)**2+abs(temk2y)**2)
                            disItoM = disandvec(objectballx[m],objectbally[m],objectballx[k2],objectbally[k2])[0]
                            if 0 <= tempK2toK1dis < 2*r and disItoM < disItoK2+R:
                                ballinwayIK2 = 1
                                break
                            else: 
                                ballinwayIK2 = 0
                        if  ballinwayIK2 == 0 and dotproductk2 > 0:
                            #plt.quiver(objectballx[i],objectbally[i],temkx,temky,color='blue',units="xy",angles="xy",scale_units="xy",scale=1, width=5)
                            #draw cue to objectball[i]'s hitpoint 
                            hitix, hitiy = findhitpoint(objectballx[i],objectbally[i],temk2x,temk2y)
                            temix = hitix - cuex
                            temiy = hitiy - cuey
                            dotproducti = temix*temk2x + temiy*temk2y
                            for o in range(0,n):
                                tempCtoKdis = dottovector(cuex,cuey,temix,temiy,objectballx[o],objectbally[o])
                                disCtoI = math.sqrt(abs(temix)**2+abs(temiy)**2)
                                disCtoO = disandvec(cuex,cuey,objectballx[o],objectbally[o])[0]
                                if 0 <= tempCtoKdis < 2*r and disCtoO < disCtoI+R:
                                    ballinwayCI2 = 1
                                    break
                                else: 
                                    ballinwayCI2 = 0
                            if  ballinwayCI2 == 0 and dotproducti > 0:
                                plt.quiver(objectballx[k1],objectbally[k1],all_vectors_BHx[k1][j],all_vectors_BHy[k1][j],color='red',units="xy",angles="xy",scale_units="xy",scale=1, width=5)
                                plt.quiver(objectballx[k2],objectbally[k2],temk1x,temk1y,color='red',units="xy",angles="xy",scale_units="xy",scale=1, width=5)
                                plt.quiver(objectballx[i],objectbally[i],temk2x,temk2y,color='red',units="xy",angles="xy",scale_units="xy",scale=1, width=5)
                                plt.quiver(cuex,cuey,temix,temiy,color='red',units="xy",angles="xy",scale_units="xy",scale=1, width=3)   


    #Plot table boundry
    plt.plot([holex[0],holex[1]],[holey[0],holey[1]],[holex[1],holex[2]],[holey[1],holey[2]],
             [holex[2],holex[3]],[holey[2],holey[3]],[holex[3],holex[4]],[holey[3],holey[4]],
             [holex[4],holex[5]],[holey[4],holey[5]],[holex[5],holex[0]],[holey[5],holey[0]],color='black')
    
    #plot aim point
    for j in range(len(aimpointx)):
        aimpoint = plt.Circle((aimpointx[j], aimpointy[j]),
                            r, color="red", alpha=0.2)
        plt.text(aimpointx[j],aimpointy[j],j,color='red',fontsize=15)
        plt.gca().add_patch(aimpoint)

    #plot vector from aiming point to hole
    for i in range(0,6):
        plt.quiver(aimpointx[i],aimpointy[i],aimtoholex[i],aimtoholey[i],color='red',units="xy",angles="xy",scale_units="xy",scale=1, width=3)

    #PLOT ALL BALLS AND HOLES
        #plot objectballs
    for i in range(len(objectballx)-1):
        objectball = plt.Circle((objectballx[i], objectbally[i]),
                            r, color='blue', alpha=0.5)
        plt.text(objectballx[i],objectbally[i],i,fontsize=15)
        plt.gca().add_patch(objectball)
    
    #plot cue ball
    plt.gca().add_patch(plt.Circle((cuex, cuey), r, color='red'))

    #plot holes
    for j in range(len(holex)):
        hole = plt.Circle((holex[j], holey[j]),
                            rb, color="black", alpha=0.7)
        #plt.text(holex[j],holey[j],j,color='white',fontsize=15)
        plt.gca().add_patch(hole)

    plt.title("sim pool table") 
    plt.axis([0, tablewidth, tableheight, 0])
    plt.axis("equal")
    plt.show()
