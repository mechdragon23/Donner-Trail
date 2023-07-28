import pygame as pg

class allimages:
    #backgrounds
    bg  = pg.image.load("images/bg.png")
    pc  = pg.image.load("images/character creation.png") #loads background image for party creation
    bgg = pg.image.load("images/background.png") #loads background image for game
    ui = pg.image.load("images/ui.png") #loads ui
    death = pg.image.load("images/death screen.png")

    #play buttons 
    pb  = pg.image.load("images/play button.png")
    pbh = pg.image.load("images/play button hover.png")

    #settings buttons
    sb  = pg.image.load("images/settings button.png")
    sbh = pg.image.load("images/settings button hover.png") 
    
    #done buttons
    db  = pg.image.load("images/done button.png")
    dbh = pg.image.load("images/done button hover.png")

    #grey buttons
    rb  = pg.image.load("images/grey button right hollow.png")
    rbh = pg.image.load("images/grey button right.png")
    rbp = pg.image.load("images/grey button right pressed.png")
    lb  = pg.image.load("images/grey button left hollow.png")
    lbh = pg.image.load("images/grey button left.png")
    lbp = pg.image.load("images/grey button left pressed.png")

    plusonebutton       = pg.image.load("images/plusonebutton.png")
    plusonebuttonpress  = pg.image.load("images/plusonebuttonpress.png")
    plusfivebutton      = pg.image.load("images/plusfivebutton.png")
    plusfivebuttonpress = pg.image.load("images/plusfivebuttonpress.png")
    plustenbutton       = pg.image.load("images/plustenbutton.png")
    plustenbuttonpress  = pg.image.load("images/plustenbuttonpress.png")
    minusonebutton      = pg.image.load("images/minusonebutton.png")
    minusonebuttonpress = pg.image.load("images/minusonebuttonpress.png")
    minusfivebutton     = pg.image.load("images/minusfivebutton.png")
    minusfivebuttonpress= pg.image.load("images/minusfivebuttonpress.png")
    minustenbutton      = pg.image.load("images/minustenbutton.png")
    minustenbuttonpress = pg.image.load("images/minustenbuttonpress.png")

    #camp fire button
    campfire = pg.image.load("images/campfirebutton.png")
    campfirehover = pg.image.load("images/campfirebuttonhover.png")
    campfirepress = pg.image.load("images/campfirebuttonpress.png")

    #clock buttons
    clockbutton  = pg.image.load("images/clock/clock button.png") #loads clock button
    clockbuttonp = pg.image.load("images/clock/clock button pressed.png") #loads clock button pressed
    
    #map buttons
    mapbutton       = pg.image.load("images/mapbutton.png") #loads map button
    mapbuttonhover  = pg.image.load("images/mapbuttonhover.png") #loads map button

    #map assets 
    map = pg.image.load("images/map.png") #loads the map
    mapdarken     = pg.image.load("images/mapdarken.png")   #overlay to darken the background
    mapselecticon = pg.image.load("images/mapselecticon.png")
    maparrowup    = pg.image.load("images/map arrow up.png")
    mappointer    = pg.image.load("images/mappointer.png")
    selectdest    = pg.image.load("images/select a destination.png")

    #event assets
    townprompt = pg.image.load("images/townprompt.png")
    store = pg.image.load("images/store.png")
    inn = pg.image.load("images/inn.png")
    camp = pg.image.load("images/camp.png")
    hunt = pg.image.load("images/hunting.png")
    gather = pg.image.load("images/gathering.png")

    #town buttons
    storebutton = pg.image.load("images/storebutton.png")
    storebuttonhover = pg.image.load("images/storebuttonhover.png")
    innbutton = pg.image.load("images/innbutton.png")
    innbuttonhover = pg.image.load("images/innbuttonhover.png")
    leavebutton = pg.image.load("images/leavebutton.png")
    leavebuttonhover = pg.image.load("images/leavebuttonhover.png")
    buybutton = pg.image.load("images/buybutton.png")
    buybuttonhover = pg.image.load("images/buybuttonhover.png")
    restbutton = pg.image.load("images/restbutton.png") 
    restbuttonhover = pg.image.load("images/restbuttonhover.png")

    #camp buttons
    yesbutton = pg.image.load("images/yesbutton.png") 
    yesbuttonhover = pg.image.load("images/yesbuttonhover.png")
    nobutton = pg.image.load("images/nobutton.png")
    nobuttonhover = pg.image.load("images/nobuttonhover.png")

    #river buttons
    fordbutton = pg.image.load("images/fordbutton.png") 
    fordbuttonhover = pg.image.load("images/fordbuttonhover.png") 
    floatbutton = pg.image.load("images/floatbutton.png") 
    floatbuttonhover = pg.image.load("images/floatbuttonhover.png") 
    ferrybutton = pg.image.load("images/ferrybutton.png") 
    ferrybuttonhover = pg.image.load("images/ferrybuttonhover.png") 
    waitbutton = pg.image.load("images/waitbutton.png") 
    waitbuttonhover = pg.image.load("images/waitbuttonhover.png") 

    #misc
    numfill = pg.image.load("images/numfill.png")
    food = pg.image.load("images/food.png")
    supplies = pg.image.load("images/supplies.png")
    money = pg.image.load("images/money.png")
    wagon = pg.image.load("images/wagondlc.png")

    def numget(i):
        string = "images/nums/" + str(i) + ".png"
        return pg.image.load(string)
    
    def iconget(i):
        string = "images/icons/" + str(i) + ".png"
        return pg.image.load(string)

    def pathget(i):
        string = "images/paths/" + str(i) + ".png"
        return pg.image.load(string)
    
    def clockget(i):
        string = "images/clock/clock" + str(i) + ".png"
        return pg.image.load(string)
    
    def characterget(i):
        string = "images/character" + str(i) + ".png"
        return pg.image.load(string)
    
    def characterportrait(i):
        string = "images/characterportrait" + str(i) + ".png"
        return pg.image.load(string)
    
    def characterportraitui(i):
        string = "images/characterbackground" + str(i) + ".png"
        return pg.image.load(string)
    
    def characterportraituidead(i):
        string = "images/characterbackgrounddead" + str(i) + ".png"
        return pg.image.load(string)
    
    def gethealth(i):
        string = "images/healthbar" + str(i) + ".png"
        return pg.image.load(string)
    
    def getstamina(i):
        string = "images/staminabar" + str(i) + ".png"
        return pg.image.load(string)
    
    def getriver(i):
        string = "images/river" + str(i) + ".png"
        return pg.image.load(string)