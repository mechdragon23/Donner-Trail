import random
import pygame as pg
from images import allimages

class Mapnode:
    def __init__(self, col, nextnode, icon, x, y):
        self.col = col
        self.nextnode = nextnode
        self.icon = icon
        self.x = x
        self.y = y

class mainmap:

    #generates nodes and returns the mapnode array and maplink array
    def nodecreation(length):
        mapnodes = []   # a 2d array of mapnode class used to store node information
        maplinks = []   # an array of path ids used to display the paths in between nodes
        maplength = length #the number of rows the map will have
        numberoficons = 5   #the number of icons the map can pull from

        for i in range(maplength):
            #setting number of cols baised to 3
            if random.randint(0,10) > 6:
                numofcols = 2
            else:
                numofcols = 3

            #populating mapnode with # of cols in each row
            if i%5 == 0: #sets town every x rows
                mapnodes.append([-1])
                numofcols = 1
            elif numofcols == 2: # sets 2 icons
                mapnodes.append([-1,-1])
            else: # sets 3 icons
                mapnodes.append([-1,-1,-1])

            #once # of cols in each row in known, populate mapnodes with proper information
            for j in range(numofcols):
                if numofcols == 1: #set town every x rows
                    mapnodes[i][j] = (Mapnode(0,-1,0,0,0))
                else: #set rand icons
                    mapnodes[i][j] = (Mapnode(j,-1,random.randint(1,numberoficons),0,0))
    
        #linking nodes
        for i in range(maplength-1):
            currentcols = len(mapnodes[i]) * 100
            nextcols = len(mapnodes[i+1]) * 10
            pathid = currentcols + nextcols #path id is a 3 digit num coralating to the correct path to display
                                            # the 100's place is the current number of cols
                                            # the 10's place is the next number of cols
                                            # the 1's place is the path variation
            if pathid == 330: # 3->3
                variation = random.randint(1,4)
                match variation:
                    case 1:
                        mapnodes[i][0].nextnode = [0]
                        mapnodes[i][1].nextnode = [1,2]
                        mapnodes[i][2].nextnode = [2]
                    case 2:
                        mapnodes[i][0].nextnode = [0]
                        mapnodes[i][1].nextnode = [0,1]
                        mapnodes[i][2].nextnode = [2]
                    case 3:
                        mapnodes[i][0].nextnode = [0,1]
                        mapnodes[i][1].nextnode = [1]
                        mapnodes[i][2].nextnode = [2]
                    case 4:
                        mapnodes[i][0].nextnode = [0]
                        mapnodes[i][1].nextnode = [1]
                        mapnodes[i][2].nextnode = [1,2]
            elif pathid == 320: # 3->2
                variation = random.randint(1,5)
                match variation:
                    case 1:
                        mapnodes[i][0].nextnode = [0]
                        mapnodes[i][1].nextnode = [0]
                        mapnodes[i][2].nextnode = [0,1]
                    case 2:
                        mapnodes[i][0].nextnode = [0,1]
                        mapnodes[i][1].nextnode = [1]
                        mapnodes[i][2].nextnode = [1]
                    case 3:
                        mapnodes[i][0].nextnode = [0]
                        mapnodes[i][1].nextnode = [0]
                        mapnodes[i][2].nextnode = [1]
                    case 4:
                        mapnodes[i][0].nextnode = [0]
                        mapnodes[i][1].nextnode = [1]
                        mapnodes[i][2].nextnode = [1]
                    case 5:
                        mapnodes[i][0].nextnode = [0]
                        mapnodes[i][1].nextnode = [0,1]
                        mapnodes[i][2].nextnode = [1]
            elif pathid == 230: # 2->3
                variation = random.randint(1,3)
                match variation:
                    case 1:
                        mapnodes[i][0].nextnode = [0,1]
                        mapnodes[i][1].nextnode = [1,2]
                    case 2:
                        mapnodes[i][0].nextnode = [0]
                        mapnodes[i][1].nextnode = [1,2]
                    case 3:
                        mapnodes[i][0].nextnode = [0,1]
                        mapnodes[i][1].nextnode = [2]
            elif pathid == 220: # 2->2
                variation = random.randint(1,3)
                match variation:
                    case 1:
                        mapnodes[i][0].nextnode = [0]
                        mapnodes[i][1].nextnode = [0,1]
                    case 2:
                        mapnodes[i][0].nextnode = [0,1]
                        mapnodes[i][1].nextnode = [1]
                    case 3:
                        mapnodes[i][0].nextnode = [0]
                        mapnodes[i][1].nextnode = [1]
            else:
                variation = 1
                match pathid:
                    case 130: # 1->3
                        mapnodes[i][0].nextnode = [0,1,2]
                    case 120: # 1->2
                        mapnodes[i][0].nextnode = [0,1]
                    case 310: # 3->1
                        mapnodes[i][0].nextnode = [0]
                        mapnodes[i][1].nextnode = [0]
                        mapnodes[i][2].nextnode = [0]
                    case 210: # 2->1
                        mapnodes[i][0].nextnode = [0]
                        mapnodes[i][1].nextnode = [0]

            pathid = pathid + variation #assigns the proper path id with variation
            maplinks.append(pathid)     #adds the pathid to the maplinks array
        return mapnodes, maplinks
        #end of linking nodes

    def displaymap(self, maplength, maprowindex, maplinks, mapnodes, validnodes, mouse, mapcolindex, selectionready):
        mapiconysteps = -150    #the y ammount the icons move up every new row
        mapiconx = [[568], [468,668], [368,568,768]] # x cords for 1, 2, and 3 map icons
        mapicony = 800  #the initial starting point for the map icons

        #displaying party arrow
        arrowx = mapiconx[len(mapnodes[maprowindex])-1][mapcolindex] #x position is calulated from # of cols in that row
        self.screen.blit(allimages.mappointer, (arrowx - 30, 630))

        #displays the map
        for i in range(maplength - maprowindex):
            mapicony = mapicony + mapiconysteps #increment the y value of icons for every new row
            row = maprowindex + i   #looks ahead at next row from where the player is
            if row < maplength - 1: #display paths
                self.screen.blit(allimages.pathget(maplinks[row]), (300, mapicony-158))
            for j in range(len(mapnodes[row])): #display icons
                self.screen.blit(allimages.iconget(mapnodes[row][j].icon), (mapiconx[len(mapnodes[row])-1][j], mapicony))
                mapnodes[row][j].x = mapiconx[len(mapnodes[row])-1][j]
                mapnodes[row][j].y = mapicony

        #displaying map selection icon
        if(selectionready):
            row = maprowindex + 1
            for i in range(len(validnodes)):
                selectionx = mapnodes[row][validnodes[i]].x
                selectiony = mapnodes[row][validnodes[i]].y
                if selectionx <= mouse[0] <= selectionx+64 and selectiony <= mouse[1] <= selectiony + 64: 
                    self.screen.blit(allimages.mapselecticon, (selectionx-25, selectiony-25)) #displays the button hovering image
        #display selection prompt
        if selectionready:
                     self.screen.blit(allimages.selectdest, (370, 100))
        pg.display.update()
        