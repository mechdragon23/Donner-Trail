import math
class character:
    def __init__(self, playerattributes):
        #attributes
        self.str    = playerattributes[0]
        self.dex    = playerattributes[1]
        self.con    = playerattributes[2]
        self.intel  = playerattributes[3]
        self.intu   = playerattributes[4]
        self.rizz   = playerattributes[5]
        self.points = playerattributes[6]

        self.strmult    = 0.01
        self.dexmult    = 0.01
        self.conmult    = 0.01
        self.intelmult  = 0.01
        self.intumult   = 0.01
        self.rizzmult   = 0.01

        #stats
        self.health = 100
        self.stamina = 100
        self.moral = 100

        #flags
        self.alive = True
        

class Party:
    #calculates the multiplier for a given attribute value
    def multcalc(attribute):
        if attribute > 33:
            attribute = 33
        return math.log(attribute+2,40)
    
    #creates 4 chacters in a party in returns the party array
    def partycreation():
        party = []
        playerattributes = [10,10,10,10,10,10,12]
        for i in range(4):
            party.append(character(playerattributes))
        return party

    def getattributes(party, i):
        attribues = []
        attribues.append(party[i].str)
        attribues.append(party[i].dex)
        attribues.append(party[i].con)
        attribues.append(party[i].intel)
        attribues.append(party[i].intu)
        attribues.append(party[i].rizz)
        attribues.append(party[i].points)
        return attribues
    
    def setattributes(party, i, playerattributes):
        #setting attribute values
        party[i].str    = playerattributes[0]
        party[i].dex    = playerattributes[1]
        party[i].con    = playerattributes[2]
        party[i].intel  = playerattributes[3]
        party[i].intu   = playerattributes[4]
        party[i].rizz   = playerattributes[5]
        party[i].points = playerattributes[6]

        #setting attribute multipliers
        party[i].strmult    = Party.multcalc(playerattributes[0])
        party[i].dexmult    = Party.multcalc(playerattributes[1])
        party[i].conmult    = Party.multcalc(playerattributes[2])
        party[i].intelmult  = Party.multcalc(playerattributes[3])
        party[i].intumult   = Party.multcalc(playerattributes[4])
        party[i].rizzmult   = Party.multcalc(playerattributes[5])