from tkinter.tix import ButtonBox
import pygame as pg
from settings import Settings
from map import mainmap
from images import allimages
from party import Party
import random
import time

from sound import Sound
from scoreboard import Scoreboard

class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Donner Trail")

        #bg music
        #self.sound = Sound(bg_music="sounds/*fillin*.wav")
        self.scoreboard = Scoreboard(game=self)  

        self.updated = False

    def reset(self):
        print('Resetting game...')
        self.updated = False

    def game_over(self):
        self.screen.blit(allimages.death, (0,0))
        pg.display.update()
        time.sleep(5)
        print('party has died!')
        self.scoreboard.reset()
        pg.quit()
        main()

    def displaynum(self, num, x, y):
        if num > 99:
            hundred = allimages.numget(int(num/100))
            self.screen.blit(hundred, (x, y))
        if num > 9:
            ten = allimages.numget(int((num - (int(num/100)*100))/10))
            self.screen.blit(ten, (x+30, y))
        if num >= 0:
            one = allimages.numget(int(num%10))
            self.screen.blit(one, (x+60, y))


    #---------------------------------------------------------------------
    #                           MAIN GAME 
    #---------------------------------------------------------------------
    def play(self):
        #self.sound.play_bg()
        self.updated = False

        clockx = 0
        clocky = 535
        clockbuttonx = allimages.clockbutton.get_width()/2 - 32
        clockbuttony = clocky

        campfirex = 300
        campfirey = 720

        storebuttonx = 300
        storebuttony = 470

        buybuttonsx = 380
        buybuttonsy = 300

        #standeredized button width and height for event prompt
        menubuttonwidth = allimages.storebutton.get_width()
        menubuttonheight = allimages.storebutton.get_height()  

        mapx = 1050
        mapwidth = allimages.mapbutton.get_width()  
        mapy = 650
        mapheight = allimages.mapbutton.get_height()

        mainmapx = 263
        inmapscreen = False #determines if the user should be in the map screen or not
        selectionready = False  # True when the user needs to select a new path
        eventready = False # True when a new event needs to take place
        startup = False
        tick = 1 
        buttonpresstime = 0.1
        distance = 0

        #used for party position
        maprowindex = 0 
        mapcolindex = 0

        maplength = 21
        validnodes = [0]

        mapnodes = []
        maplinks = []

        mapnodes, maplinks = mainmap.nodecreation(length = maplength)

        #party creation
        party = Party.partycreation()
        for i in range(4):
            file = open('p'+str(i)+'.txt','r')
            playerattributes = [int(line.rstrip()) for line in file]
            file.close()
            Party.setattributes(party, i, playerattributes)


        #food and supplies
        food = 200
        supplies = 200
        money = 500
        wagonhealth = 100
        inncost = 0
        tempdeathcounter = 0
        wagonalive = True

        #--------------------------------------
        #           UI ELEMENTS
        #--------------------------------------
        #display upper right ui elements
        def upperright():
            #food and supplies
            self.screen.blit(allimages.food, (970, 10))
            self.screen.blit(allimages.supplies, (880, 50))
            self.screen.blit(allimages.money, (945, 90))
            self.displaynum(food,1080,0)
            self.displaynum(supplies,1080,42)
            self.displaynum(money,1080,84)

        #displays characters
        def characters():
            if wagonalive:
                self.screen.blit(allimages.wagon, (20, 430))
            for i in range(4):
                if party[i].alive:
                    self.screen.blit(allimages.characterget(i+1), (350 - (i*50), 500))
            self.screen.blit(allimages.ui, (0, 0))

        #displays character portraits
        def characterportraits():
            for i in range(4):
                if party[i].alive:
                    self.screen.blit(allimages.characterportraitui(i+1), (30, 30 + (100 * i)))
                else:
                    self.screen.blit(allimages.characterportraituidead(i+1), (30, 30 + (100 * i)))
                health = int((party[i].health+19)/20)
                self.screen.blit(allimages.gethealth(health), (130, 40 + (100 * i)))
                stamina = int((party[i].stamina+19)/20)
                self.screen.blit(allimages.getstamina(stamina), (130, 70 + (100 * i)))

        def displayhoverbutton(mouse, x, y, width, height, image, imagehover):
            #display store button
            if x <= mouse[0] <= x+width  and y <= mouse[1] <= y+height: 
                self.screen.blit(imagehover, (x, y)) #displays the button hovering image 
            else: 
                self.screen.blit(image, (x, y)) #displays the regular button
        
        def partystaminadecrease():
            if wagonalive:
                for i in range(4):
                    if party[i].alive:
                        if party[i].stamina < 0:
                            party[i].health = party[i].health - ((1 - (((party[i].conmult * 2) + party[i].strmult)/3)) * 20)
                            party[i].moral = party[i].moral - ((1 - (((party[i].conmult * 2) + party[i].intumult)/3)) * 10)
                        else:
                            party[i].stamina = party[i].stamina - ((1 - (((party[i].conmult * 2) + party[i].strmult)/3)) * 10)
                    #health regen
                    if party[i].health < 100 and party[i].stamina > 0:
                        party[i].health = party[i].health + (party[i].conmult * 5)
            else:
                for i in range(4):
                    if party[i].alive:
                        if party[i].stamina < 0:
                            party[i].health = party[i].health - ((1 - (((party[i].conmult * 2) + party[i].strmult)/3)) * 30)
                            party[i].moral = party[i].moral - ((1 - (((party[i].conmult * 2) + party[i].intumult)/3)) * 15)
                        else:
                            party[i].stamina = party[i].stamina - ((1 - (((party[i].conmult * 2) + party[i].strmult)/3)) * 15)
                    #health regen
                    if party[i].health < 100 and party[i].stamina > 0:
                        party[i].health = party[i].health + (party[i].conmult * 5)

        #------------------------------------------------
        #                   MAIN LOOP
        #------------------------------------------------

        #building the background and ui
        self.screen.blit(allimages.bgg, (0, 0))
        characters()
        characterportraits()
        upperright()

        self.screen.blit(allimages.clockget(tick), (clockx, clocky))
        self.screen.blit(allimages.clockbutton, (clockx, clocky))
        self.screen.blit(allimages.mapbutton, (mapx, mapy))
        self.screen.blit(allimages.campfire, (campfirex, campfirey))

        while True:    
            for ev in pg.event.get(): 
                mouse = pg.mouse.get_pos()     
                if ev.type == pg.QUIT: 
                    pg.quit() 
                #checks if a mouse is clicked 
                if ev.type == pg.MOUSEBUTTONDOWN: 
                    #------------------------------
                    #           CLOCK
                    #------------------------------
                    if clockbuttonx <= mouse[0] <= clockbuttonx+64 and clockbuttony <= mouse[1] <= clockbuttony+36 and selectionready != True:
                        tick = tick + 1
                        if wagonhealth > 0: 
                            wagonhealth = wagonhealth - random.randint(1,3)
                        if wagonhealth <= 0:
                            wagonalive = False
                        partystaminadecrease()

                        self.screen.blit(allimages.bgg, (0, 0))
                        characters()
                        characterportraits()
                        upperright()
                                    
                        #clock button press update
                        self.screen.blit(allimages.ui, (0, 0))
                        self.screen.blit(allimages.clockbuttonp, (clockx, clocky))
                        self.screen.blit(allimages.clockget(tick), (clockx, clocky))

                        displayhoverbutton(mouse,mapx,mapy,mapwidth,mapheight,allimages.mapbutton,allimages.mapbuttonhover)
                        displayhoverbutton(mouse,campfirex,campfirey,64,64,allimages.campfire,allimages.campfirehover)  

                        #clock rollover
                        if tick >= 13:
                            tick = 1
                            selectionready = True
                            inmapscreen = True
                        pg.display.update()
                        time.sleep(buttonpresstime)
                    #----------------end of clock-----------------

                    #map button    
                    if mapx <= mouse[0] <= mapx+mapwidth and mapy <= mouse[1] <= mapy+mapheight:
                        validnodes = mapnodes[maprowindex][mapcolindex].nextnode
                        inmapscreen = True #sets map screen to true
                        self.screen.blit(allimages.mapdarken, (0, 0)) #darkens background
                        pg.display.update()
                        time.sleep(buttonpresstime)

                    #-------------------------------
                    #              MAP
                    #------------------------------
                    while(inmapscreen):
                        #displaying images
                        self.screen.blit(allimages.map, (mainmapx, 0))
                        mainmap.displaymap(self, maplength, maprowindex, maplinks, mapnodes, validnodes, mouse, mapcolindex, selectionready)
                        row = maprowindex + 1
            
                        #checking for click events
                        for ev in pg.event.get():
                            if ev.type == pg.QUIT: 
                                pg.quit()
                            mouse = pg.mouse.get_pos()
                            if ev.type == pg.MOUSEBUTTONDOWN:
                                #exiting map
                                if mainmapx > mouse[0] or mouse[0] > mainmapx + allimages.map.get_width():
                                    inmapscreen = False
                                #checking for map selection
                                for i in range(len(validnodes)):
                                    selectionx = mapnodes[row][validnodes[i]].x
                                    selectiony = mapnodes[row][validnodes[i]].y
                                    #checks if selection is valid
                                    if selectionx <= mouse[0] <= selectionx + 64 and selectiony <= mouse[1] <= selectiony + 64 and selectionready:
                                        maprowindex = row 
                                        mapcolindex = mapnodes[row][validnodes[i]].col
                                        inmapscreen = False
                                        selectionready = False
                                        eventready = True
                    #---------END OF MAP-----------
                    validnodes = mapnodes[maprowindex][mapcolindex].nextnode #sets the valid node array to that of the next valid nodes

                    #---------------------------------
                    #           EVENTS
                    #---------------------------------
                    if eventready:
                        startup = True
                    while(eventready):
                        if startup:
                            #building the background and ui
                            self.screen.blit(allimages.bgg, (0, 0))
                            characters()
                            characterportraits()
                            upperright()
                            self.screen.blit(allimages.clockget(tick), (clockx, clocky))
                            self.screen.blit(allimages.clockbutton, (clockx, clocky))
                            displayhoverbutton(mouse,mapx,mapy,mapwidth,mapheight,allimages.mapbutton,allimages.mapbuttonhover)
                            displayhoverbutton(mouse,campfirex,campfirey,64,64,allimages.campfire,allimages.campfirehover) 
                            self.screen.blit(allimages.mapdarken, (0, 0)) #darkens background
                            pg.display.update()
                            foodcost = random.randint(1,5)
                            supplycost = random.randint(1,5)
                            riverdanger = random.randint(0,3)
                            total = 0
                            for i in range(4):
                                total = total + party[i].str + party[i].intu + party[i].dex + party[i].intel
                            wagoncost = int((100 - wagonhealth)/(total/80)) 
                            startup = False
                            matchcase = mapnodes[maprowindex][mapcolindex].icon

                        match matchcase:
                            #-------------------------------
                            #           TOWN EVENT
                            #-------------------------------
                            case 0:
                                for ev in pg.event.get():
                                    self.screen.blit(allimages.townprompt, (250, 150))
                                    if ev.type == pg.QUIT: 
                                        pg.quit()
                                    mouse = pg.mouse.get_pos()
                                    if ev.type == pg.MOUSEBUTTONDOWN:
                                        #store button
                                        if storebuttonx <= mouse[0] <= storebuttonx + menubuttonwidth and storebuttony <= mouse[1] <= storebuttony + menubuttonheight:
                                            instore = True
                                            foodtobuy = 0
                                            suppliestobuy = 0
                                            while(instore):
                                                for ev in pg.event.get():
                                                    self.screen.blit(allimages.store, (250, 150))
                                                    #plus minus buttons
                                                    self.screen.blit(allimages.minusonebutton, (buybuttonsx, buybuttonsy))          #food -1
                                                    self.screen.blit(allimages.minusonebutton, (buybuttonsx, buybuttonsy+120))      #supplies -1
                                                    self.screen.blit(allimages.plusonebutton, (buybuttonsx+230, buybuttonsy))       #food +1
                                                    self.screen.blit(allimages.plusonebutton, (buybuttonsx+230, buybuttonsy+120))   #supplies +1
                                                    self.screen.blit(allimages.minustenbutton, (buybuttonsx-80, buybuttonsy))       #food -10
                                                    self.screen.blit(allimages.minustenbutton, (buybuttonsx-80, buybuttonsy+120))   #supplies -10
                                                    self.screen.blit(allimages.plustenbutton, (buybuttonsx+310, buybuttonsy))       #food +10
                                                    self.screen.blit(allimages.plustenbutton, (buybuttonsx+310, buybuttonsy+120))   #supplies +10
                                                    #display food and supply numbers
                                                    self.displaynum(foodtobuy, buybuttonsx+100, buybuttonsy)
                                                    self.displaynum(suppliestobuy, buybuttonsx+100, buybuttonsy+120)
                                                    #food and supply costs
                                                    self.displaynum(foodtobuy*foodcost, buybuttonsx+400, buybuttonsy)
                                                    self.displaynum(suppliestobuy*supplycost, buybuttonsx+400, buybuttonsy+120)
                                                    self.displaynum(suppliestobuy*supplycost+foodtobuy*foodcost, buybuttonsx+400, buybuttonsy+220)
                                                    if ev.type == pg.QUIT: 
                                                        pg.quit()
                                                    mouse = pg.mouse.get_pos()
                                                    if ev.type == pg.MOUSEBUTTONDOWN:
                                                        #food
                                                        if foodtobuy>0:
                                                            if buybuttonsx <= mouse[0] <= buybuttonsx + 64 and buybuttonsy <= mouse[1] <= buybuttonsy + 64:
                                                                foodtobuy = foodtobuy - 1
                                                            if buybuttonsx-80 <= mouse[0] <= buybuttonsx-80 + 64 and buybuttonsy <= mouse[1] <= buybuttonsy + 64:
                                                                foodtobuy = foodtobuy - 10
                                                        if foodtobuy<1000:
                                                            if buybuttonsx+230 <= mouse[0] <= buybuttonsx+230 + 64 and buybuttonsy <= mouse[1] <= buybuttonsy + 64:
                                                                foodtobuy = foodtobuy + 1
                                                            if buybuttonsx+310 <= mouse[0] <= buybuttonsx+310 + 64 and buybuttonsy <= mouse[1] <= buybuttonsy + 64:
                                                                foodtobuy = foodtobuy + 10
                                                        #supplies
                                                        if suppliestobuy>0:
                                                            if buybuttonsx <= mouse[0] <= buybuttonsx + 64 and buybuttonsy+120 <= mouse[1] <= buybuttonsy+120 + 64:
                                                                suppliestobuy = suppliestobuy - 1
                                                            if buybuttonsx-80 <= mouse[0] <= buybuttonsx-80 + 64 and buybuttonsy+120 <= mouse[1] <= buybuttonsy+120 + 64:
                                                                suppliestobuy = suppliestobuy - 10
                                                        if suppliestobuy<1000:
                                                            if buybuttonsx+230 <= mouse[0] <= buybuttonsx+230 + 64 and buybuttonsy+120 <= mouse[1] <= buybuttonsy+120 + 64:
                                                                suppliestobuy = suppliestobuy + 1
                                                            if buybuttonsx+310 <= mouse[0] <= buybuttonsx+310 + 64 and buybuttonsy+120 <= mouse[1] <= buybuttonsy+120 + 64:
                                                                suppliestobuy = suppliestobuy + 10
                                                        #buy button
                                                        if storebuttonx+140 <= mouse[0] <= storebuttonx+140 + menubuttonwidth and storebuttony+40 <= mouse[1] <= storebuttony+40 + menubuttonheight:
                                                            money = money - (suppliestobuy*supplycost+foodtobuy*foodcost)
                                                            food = food + foodtobuy
                                                            supplies = supplies + suppliestobuy
                                                            suppliestobuy = 0
                                                            foodtobuy = 0
                                                        #leave button
                                                        if storebuttonx+440 <= mouse[0] <= storebuttonx+440 + menubuttonwidth and storebuttony-300<= mouse[1] <= storebuttony-300 + menubuttonheight:
                                                            instore = False
                                                    displayhoverbutton(mouse,storebuttonx+140,storebuttony+40,menubuttonwidth,menubuttonheight,allimages.buybutton,allimages.buybuttonhover)
                                                    displayhoverbutton(mouse,storebuttonx+440,storebuttony-300,menubuttonwidth,menubuttonheight,allimages.leavebutton,allimages.leavebuttonhover)
                                                    pg.display.update()
                                        #inn button
                                        if storebuttonx+220 <= mouse[0] <= storebuttonx+220 + menubuttonwidth and storebuttony <= mouse[1] <= storebuttony + menubuttonheight:
                                            ininn = True
                                            for i in range(4):
                                                inncost = inncost + (100 - party[i].stamina) / 10
                                            while ininn:
                                                for ev in pg.event.get():
                                                    self.screen.blit(allimages.inn, (250, 150))
                                                    self.displaynum(inncost, 600, 375)
                                                    if ev.type == pg.QUIT: 
                                                        pg.quit()
                                                    mouse = pg.mouse.get_pos()
                                                    if ev.type == pg.MOUSEBUTTONDOWN:
                                                        #leave button
                                                        if storebuttonx+220 <= mouse[0] <= storebuttonx+220 + menubuttonwidth and storebuttony<= mouse[1] <= storebuttony + menubuttonheight:
                                                            ininn = False
                                                            inncost = 0
                                                        #rest button
                                                        if storebuttonx <= mouse[0] <= storebuttonx + menubuttonwidth and storebuttony<= mouse[1] <= storebuttony + menubuttonheight:
                                                            money = money - inncost
                                                            inncost = 0
                                                            for i in range(4):
                                                                if party[i].alive:
                                                                    party[i].stamina = 100
                                                                    party[i].health = 100
                                                            ininn = False
                                                    displayhoverbutton(mouse,storebuttonx,storebuttony,menubuttonwidth,menubuttonheight,allimages.restbutton,allimages.restbuttonhover)
                                                    displayhoverbutton(mouse,storebuttonx+220,storebuttony,menubuttonwidth,menubuttonheight,allimages.leavebutton,allimages.leavebuttonhover)
                                                    pg.display.update()
                                                    time.sleep(buttonpresstime)
                                        #leave button
                                        if storebuttonx+440 <= mouse[0] <= storebuttonx+440 + menubuttonwidth and storebuttony <= mouse[1] <= storebuttony + menubuttonheight:
                                            eventready = False
                                    displayhoverbutton(mouse,storebuttonx,storebuttony,menubuttonwidth,menubuttonheight,allimages.storebutton,allimages.storebuttonhover)
                                    displayhoverbutton(mouse,storebuttonx+220,storebuttony,menubuttonwidth,menubuttonheight,allimages.innbutton,allimages.innbuttonhover)
                                    displayhoverbutton(mouse,storebuttonx+440,storebuttony,menubuttonwidth,menubuttonheight,allimages.leavebutton,allimages.leavebuttonhover)
                                    pg.display.update()
                            #-------------------------------
                            #         CAMP EVENT   
                            #-------------------------------
                            case 1:
                                for ev in pg.event.get():
                                    self.screen.blit(allimages.camp, (250, 150))
                                    displayhoverbutton(mouse,storebuttonx,storebuttony,menubuttonwidth,menubuttonheight,allimages.yesbutton,allimages.yesbuttonhover)
                                    displayhoverbutton(mouse,storebuttonx+440,storebuttony,menubuttonwidth,menubuttonheight,allimages.leavebutton,allimages.leavebuttonhover)
                                    self.displaynum(wagoncost, 550, 375)
                                    if ev.type == pg.QUIT: 
                                        pg.quit()
                                    mouse = pg.mouse.get_pos()
                                    if ev.type == pg.MOUSEBUTTONDOWN:
                                        #leave button
                                        if storebuttonx+440 <= mouse[0] <= storebuttonx+440 + menubuttonwidth and storebuttony <= mouse[1] <= storebuttony + menubuttonheight:
                                            eventready = False
                                        #yes button
                                        if storebuttonx <= mouse[0] <= storebuttonx + menubuttonwidth and storebuttony <= mouse[1] <= storebuttony + menubuttonheight:
                                            supplies = supplies - wagoncost
                                            wagonhealth = 100
                                            eventready = False
                                    pg.display.update()

                            #-------------------------------
                            #         RANDOM EVENT  
                            #-------------------------------
                            case 2:
                                matchcase = random.randint(1,5)

                            #-------------------------------
                            #         RIVER EVENT
                            #-------------------------------
                            case 3:
                                for ev in pg.event.get():
                                    self.screen.blit(allimages.getriver(riverdanger), (250, 150))
                                    displayhoverbutton(mouse,storebuttonx+50,storebuttony,menubuttonwidth,menubuttonheight,allimages.fordbutton,allimages.fordbuttonhover)
                                    displayhoverbutton(mouse,storebuttonx+390,storebuttony,menubuttonwidth,menubuttonheight,allimages.floatbutton,allimages.floatbuttonhover)
                                    displayhoverbutton(mouse,storebuttonx+50,storebuttony-80,menubuttonwidth,menubuttonheight,allimages.ferrybutton,allimages.ferrybuttonhover)
                                    displayhoverbutton(mouse,storebuttonx+390,storebuttony-80,menubuttonwidth,menubuttonheight,allimages.waitbutton,allimages.waitbuttonhover)
                                    if ev.type == pg.QUIT: 
                                        pg.quit()
                                    mouse = pg.mouse.get_pos()
                                    if ev.type == pg.MOUSEBUTTONDOWN:
                                        #wait button
                                        if storebuttonx+390 <= mouse[0] <= storebuttonx+390 + menubuttonwidth and storebuttony-80 <= mouse[1] <= storebuttony-80 + menubuttonheight and tick < 12:
                                            riverdanger = riverdanger + random.randint(-1,1)
                                            if riverdanger > 3:
                                                riverdanger = 3
                                            if riverdanger < 0:
                                                riverdanger = 0
                                            tick = tick + 1
                                            partystaminadecrease()
                                        #ford button
                                        if storebuttonx+50 <= mouse[0] <= storebuttonx+50 + menubuttonwidth and storebuttony <= mouse[1] <= storebuttony + menubuttonheight:
                                            total = 0
                                            rivercost = random.randint(10,25) * (riverdanger + 1)
                                            for i in range(4):
                                                total = total + party[i].str + party[i].intu
                                            if total < rivercost:
                                                supplies = supplies - rivercost/2
                                                food = food - rivercost/2
                                            eventready = False
                                        #float button
                                        if storebuttonx+390 <= mouse[0] <= storebuttonx+390 + menubuttonwidth and storebuttony <= mouse[1] <= storebuttony + menubuttonheight:
                                            total = 0
                                            rivercost = random.randint(10,25) * (riverdanger + 1)
                                            for i in range(4):
                                                total = total + party[i].intel + party[i].dex
                                            if total < rivercost:
                                                supplies = supplies - rivercost/2
                                                food = food - rivercost/2
                                            eventready = False
                                        #ferry button
                                        if storebuttonx+50 <= mouse[0] <= storebuttonx+50 + menubuttonwidth and storebuttony-80 <= mouse[1] <= storebuttony-80 + menubuttonheight:
                                            if money > 100:
                                                money = money - 100
                                                eventready = False
                                    pg.display.update()

                            #-------------------------------
                            #         HUNTING EVENT  
                            #-------------------------------
                            case 4:
                                for ev in pg.event.get():
                                    self.screen.blit(allimages.hunt, (250, 150))
                                    displayhoverbutton(mouse,storebuttonx,storebuttony,menubuttonwidth,menubuttonheight,allimages.yesbutton,allimages.yesbuttonhover)
                                    displayhoverbutton(mouse,storebuttonx+440,storebuttony,menubuttonwidth,menubuttonheight,allimages.nobutton,allimages.nobuttonhover)
                                    if ev.type == pg.QUIT: 
                                        pg.quit()
                                    mouse = pg.mouse.get_pos()
                                    if ev.type == pg.MOUSEBUTTONDOWN:
                                        #no button
                                        if storebuttonx+440 <= mouse[0] <= storebuttonx+440 + menubuttonwidth and storebuttony <= mouse[1] <= storebuttony + menubuttonheight:
                                            eventready = False
                                        #yes button
                                        if storebuttonx <= mouse[0] <= storebuttonx + menubuttonwidth and storebuttony <= mouse[1] <= storebuttony + menubuttonheight:
                                            total = 0
                                            for i in range(4):
                                                total = total + party[i].dex
                                            huntcost = random.randint(35,80) - total
                                            if supplies > huntcost:
                                                supplies = supplies - huntcost
                                                food = food + (random.randint(3,7)*int(total/4))
                                                eventready = False
                                    pg.display.update()

                            #-------------------------------
                            #         GATHERING EVENT  
                            #-------------------------------
                            case 5:
                                for ev in pg.event.get():
                                    self.screen.blit(allimages.gather, (250, 150))
                                    displayhoverbutton(mouse,storebuttonx,storebuttony,menubuttonwidth,menubuttonheight,allimages.yesbutton,allimages.yesbuttonhover)
                                    displayhoverbutton(mouse,storebuttonx+440,storebuttony,menubuttonwidth,menubuttonheight,allimages.nobutton,allimages.nobuttonhover)
                                    if ev.type == pg.QUIT: 
                                        pg.quit()
                                    mouse = pg.mouse.get_pos()
                                    if ev.type == pg.MOUSEBUTTONDOWN:
                                        #no button
                                        if storebuttonx+440 <= mouse[0] <= storebuttonx+440 + menubuttonwidth and storebuttony <= mouse[1] <= storebuttony + menubuttonheight:
                                            eventready = False
                                        #yes button
                                        if storebuttonx <= mouse[0] <= storebuttonx + menubuttonwidth and storebuttony <= mouse[1] <= storebuttony + menubuttonheight:
                                            total = 0
                                            for i in range(4):
                                                total = total + party[i].intu + party[i].intel
                                            food = food + int(total / random.randint(1,5))
                                            eventready = False
                                    pg.display.update()

                        pg.display.update()

                    #campfire button    
                    if campfirex <= mouse[0] <= campfirex+mapwidth and campfirey <= mouse[1] <= campfirey+mapheight and tick < 10 and selectionready != True:
                        if food > 0:
                            tick = tick + 3
                            for i in range(4):
                                if party[i].alive:
                                    foodused = int((100 - party[i].stamina)/10)
                                    if foodused > 0:
                                        party[i].stamina = 100
                                        food = food - foodused
                        self.screen.blit(allimages.campfirepress, (campfirex, campfirey))
                        pg.display.update()
                        time.sleep(buttonpresstime)

                #building the background and ui
                self.screen.blit(allimages.bgg, (0, 0))
                characters()
                characterportraits()
                upperright()

                self.screen.blit(allimages.clockget(tick), (clockx, clocky))
                self.screen.blit(allimages.clockbutton, (clockx, clocky))
                displayhoverbutton(mouse,mapx,mapy,mapwidth,mapheight,allimages.mapbutton,allimages.mapbuttonhover)
                displayhoverbutton(mouse,campfirex,campfirey,64,64,allimages.campfire,allimages.campfirehover)    

                #display selection prompt
                if selectionready:
                    self.screen.blit(allimages.selectdest, (370, 100))       

            #-----end of mouse click events--------

            
            deathcounter = 0
            for i in range(4):
                if party[i].health < 0:
                    deathcounter = deathcounter + 1
                    party[i].alive = False

            if tempdeathcounter < deathcounter:
                tempdeathcounter = deathcounter
                for i in range(4):
                    if party[i].alive:
                        party[i].moral = party[i].moral - 30 
                        print(party[i].moral)           

            pg.display.update()

            #-----------------------
            #       GAME OVER
            #-----------------------
            if validnodes == -1:
                g = Game()
                g.win()
            if deathcounter >= 4:
                self.game_over()
            
            

        
    #---------------------------------------------------------------------
    #                       PARTY CREATION
    #---------------------------------------------------------------------
    def partycreate(self):
        #self.sound.play_bg()
        self.updated = False
        notdone = True

        dbuttonwidth = allimages.db.get_width()
        dbuttonheight = allimages.db.get_height()  
        dbuttonx = 1200/2 - dbuttonwidth/2 + 480
        dbuttony = 800/2 + 300
        party = []
        playerattributes = []
        playernum = 0
        buttonx = [130,850,850,850,850,850,850,375,1000,1000,1000,1000,1000,1000]
        buttony = [210,140,215,290,365,440,520,210,140,215,290,365,440,520]
        buttonpresstime = 0.1

        #initilizing party 
        party = Party.partycreation()
        playerattributes = Party.getattributes(party, playernum)

        #main loop
        while notdone:    
            for ev in pg.event.get():      
                if ev.type == pg.QUIT: 
                    pg.quit() 
                #checks if a mouse is clicked 
                if ev.type == pg.MOUSEBUTTONDOWN: 
                    #done button
                    if dbuttonx <= mouse[0] <= dbuttonx+dbuttonwidth and dbuttony <= mouse[1] <= dbuttony+dbuttonheight:
                        for i in range(4):
                            file = open('p'+str(playernum)+'.txt','w')
                            for pa in playerattributes:
                                file.write(str(pa)+"\n")
                            file.close()
                        notdone = False 
                        g = Game()
                        g.play()
                    
                    i = 0 #character left button index
                    if buttonx[i] <= mouse[0] <= buttonx[i]+64 and buttony[i] <= mouse[1] <= buttony[i]+64:
                        if playernum > 0: # if valid
                            self.screen.blit(allimages.lbp, (buttonx[i], buttony[i]))
                            self.screen.blit(allimages.numget(playernum+1), (210,215))
                            pg.display.update()

                            #setting attributes
                            Party.setattributes(party, playernum, playerattributes)
                            playernum = playernum - 1 # decriment to previous player
                            #getting attributes
                            playerattributes = Party.getattributes(party, playernum)

                            time.sleep(buttonpresstime)
                        else:
                            self.screen.blit(allimages.lbp, (buttonx[i], buttony[i]))
                            pg.display.update()
                            time.sleep(buttonpresstime) 

                    i = 7 #character right button index
                    if buttonx[i] <= mouse[0] <= buttonx[i]+64 and buttony[i] <= mouse[1] <= buttony[i]+64:
                        if playernum < 3: # if valid
                            self.screen.blit(allimages.rbp, (buttonx[i], buttony[i]))
                            self.screen.blit(allimages.numget(playernum+1), (210,215))
                            pg.display.update()

                            #setting attributes
                            Party.setattributes(party, playernum, playerattributes)
                            playernum = playernum + 1 # increment to next player
                            #getting attributes
                            playerattributes = Party.getattributes(party, playernum)

                            time.sleep(buttonpresstime)
                        else:
                            self.screen.blit(allimages.rbp, (buttonx[i], buttony[i]))
                            pg.display.update()
                            time.sleep(buttonpresstime)    

                    #lefthand decriment attribute buttons
                    for i in range(6):
                        if buttonx[i + 1] <= mouse[0] <= buttonx[i + 1]+64 and buttony[i + 1] <= mouse[1] <= buttony[i + 1]+64:
                            if playerattributes[i] > 0: #if valid
                                self.screen.blit(allimages.lbp, (buttonx[i+1], buttony[i+1]))
                                playerattributes[i] = playerattributes[i] - 1 #decriment attribute
                                playerattributes[6] = playerattributes[6] + 1 #increment points
                                self.screen.blit(allimages.numfill, (930,150+i*75)) #blacks out previous num
                                self.screen.blit(allimages.numget(playerattributes[i]), (930,150+i*75))
                                self.screen.blit(allimages.numfill, (930,150+6*75)) #blacks out previous num
                                self.screen.blit(allimages.numget(playerattributes[6]), (930,150+6*75)) #display remaning points
                                pg.display.update()
                                time.sleep(buttonpresstime)
                            else:
                                self.screen.blit(allimages.lbp, (buttonx[i+1], buttony[i+1]))
                                pg.display.update()
                                time.sleep(buttonpresstime) 

                    #righthand increment attribute buttons
                    for i in range(6):
                        if buttonx[i + 8] <= mouse[0] <= buttonx[i + 8]+64 and buttony[i + 8] <= mouse[1] <= buttony[i + 8]+64:
                            if playerattributes[6] > 0: #if valid
                                self.screen.blit(allimages.rbp, (buttonx[i+8], buttony[i+8]))
                                playerattributes[i] = playerattributes[i] + 1 #increment attribute
                                playerattributes[6] = playerattributes[6] - 1 #decriment points
                                self.screen.blit(allimages.numfill, (930,150+i*75)) #blacks out previous num
                                self.screen.blit(allimages.numget(playerattributes[i]), (930,150+i*75))
                                self.screen.blit(allimages.numfill, (930,150+6*75)) #blacks out previous num
                                self.screen.blit(allimages.numget(playerattributes[6]), (930,150+6*75)) #display remaning points
                                pg.display.update()
                                time.sleep(buttonpresstime)
                            else:
                                self.screen.blit(allimages.rbp, (buttonx[i+8], buttony[i+8]))
                                pg.display.update()
                                time.sleep(buttonpresstime)  
                #END OF MOUSE CLICK CHECK
                
            # display background onto screen
            self.screen.blit(allimages.pc, (0, 0))
            self.screen.blit(allimages.numget(playernum+1), (210,215)) #display player number
            for i in range (7):
                self.screen.blit(allimages.numget(playerattributes[i]), (930,150+i*75))
            mouse = pg.mouse.get_pos()

            # display character portraits
            self.screen.blit(allimages.characterportrait(playernum+1), (179,304))

            #display grey buttons
            for i in range(14):
                if buttonx[i] <= mouse[0] <= buttonx[i]+64 and buttony[i] <= mouse[1] <= buttony[i]+64:
                    if i > 6: 
                        self.screen.blit(allimages.rbh, (buttonx[i], buttony[i]))
                    else:
                        self.screen.blit(allimages.lbh, (buttonx[i], buttony[i]))
                else: 
                    if i > 6: 
                        self.screen.blit(allimages.rb, (buttonx[i], buttony[i]))
                    else:
                        self.screen.blit(allimages.lb, (buttonx[i], buttony[i]))

            #done button
            if dbuttonx <= mouse[0] <= dbuttonx+dbuttonwidth and dbuttony <= mouse[1] <= dbuttony+dbuttonheight: 
                self.screen.blit(allimages.dbh, (dbuttonx, dbuttony)) #displays the button hovering image 
            else: 
                self.screen.blit(allimages.db, (dbuttonx, dbuttony)) #displays the regular button 

            pg.display.update()


def main():
    pg.init() 
    res = (1200,800) 
    screen = pg.display.set_mode(res)       
    
    width = screen.get_width()  
    height = screen.get_height()
    
    playbuttonwidth = allimages.pb.get_width()
    playbuttonheight = allimages.pb.get_height()  
    playbuttonx = width/2 - playbuttonwidth/2
    playbuttony = height/2 + 200

    sbuttonwidth = allimages.sb.get_width()
    sbuttonheight = allimages.sb.get_height()  
    sbuttonx = width/2 - sbuttonwidth/2
    sbuttony = height/2 + 280
    
    f = open("highscores.txt", "r+")
    high_score = f.readline()
    f.close()
    
    while True: 
        for ev in pg.event.get():      
            if ev.type == pg.QUIT: 
                pg.quit() 
            #checks if a mouse is clicked 
            if ev.type == pg.MOUSEBUTTONDOWN: 
                #if the mouse is clicked on the 
                # button the game is terminated 
                if playbuttonx <= mouse[0] <= playbuttonx+playbuttonwidth and playbuttony <= mouse[1] <= playbuttony+playbuttonheight: 
                    g = Game()
                    g.partycreate() 
        # display background onto screen
        screen.blit(allimages.bg, (0, 0))
        
        mouse = pg.mouse.get_pos() 
        # if mouse is hovered on a button it 
        # changes to lighter shade 
        if playbuttonx <= mouse[0] <= playbuttonx+playbuttonwidth and playbuttony <= mouse[1] <= playbuttony+playbuttonheight: 
            screen.blit(allimages.pbh, (playbuttonx, playbuttony)) #displays the button hovering image 
        else: 
            screen.blit(allimages.pb, (playbuttonx, playbuttony)) #displays the regular button

        #settings button
        if sbuttonx <= mouse[0] <= sbuttonx+sbuttonwidth and sbuttony <= mouse[1] <= sbuttony+sbuttonheight: 
            screen.blit(allimages.sbh, (sbuttonx, sbuttony)) #displays the button hovering image 
        else: 
            screen.blit(allimages.sb, (sbuttonx, sbuttony)) #displays the regular button
        
        # updates the frames of the game 
        pg.display.update()


if __name__ == '__main__':
    main()
