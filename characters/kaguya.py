import sys 
sys.path.append("..")
from game import *
from character import *
class kaguyaATKSkill(atkCard):
    def skill(self, g:game, level):
        defe = 1 if g.players[g.nowid].identity.defense >= 3 else 0
        g.damage(1-g.nowid, 1,self.level+level+defe)
        pass
class kaguyaDEFSkill(defCard):
    def skill(self, g:game, level):
        g.players[g.nowid].identity.defense += level+self.level
        g.players[g.nowid].identity.defense = min(g.players[g.nowid].identity.defense, g.players[g.nowid].identity.maxdefense)
        waitingQueue = []
        for i in range(level):
            top = g.players[g.nowid].deck[0]
            del g.players[g.nowid].deck[0]
            if top in [4,5,6]:
                g.players[g.nowid].hand.append(top)
            else:
                r = g.players[g.nowid].identity.droporKeepCard(top)
                if r:
                    waitingQueue.append(g, top)
        for c in reversed(waitingQueue):
            g.players[g.nowid].deck.insert(0, c)
        
        pass
class kaguyaMOVSkill(movCard):
    def skill(self, g:game, level):
        g.damage(1-g.nowid, level, self.level)
        g.players[g.nowid].identity.lostLiveRemoveCard(g)
        pass
class kaguyaMETASkill(metaCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class kaguyaUltraSkill(ultraCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class kaguya(character):
    def idx():
        return 5
    def setup(self):
        self.maxlife = 32
        self.life= self.maxlife
        self.maxdefense = 6
        self.defense = 0
        self.energy = 0
        self.specialGate = 16
    def __init__(self, **kwargs):
        self.setup()
        self.characterName = "輝夜姬"
        self.picture = "沒有圖片"
        atklv1 =  kaguyaATKSkill("沒有圖片", "", 1)
        atklv2 =  kaguyaATKSkill("沒有圖片", "", 2)
        atklv3 =  kaguyaATKSkill("沒有圖片", "", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  kaguyaDEFSkill("沒有圖片", "", 1)
        deflv2 =  kaguyaDEFSkill("沒有圖片", "", 2)
        deflv3 =  kaguyaDEFSkill("沒有圖片", "", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  kaguyaMOVSkill("沒有圖片", "", 1)
        movlv2 =  kaguyaMOVSkill("沒有圖片", "", 2)
        movlv3 =  kaguyaMOVSkill("沒有圖片", "", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  kaguyaMETASkill("沒有圖片", "", 0)
        meta2 =  kaguyaMETASkill("沒有圖片", "", 0)
        meta3 =  kaguyaMETASkill("沒有圖片", "", 0)
        meta4 =  kaguyaMETASkill("沒有圖片", "", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  kaguyaUltraSkill("沒有圖片", "", 0)
        ultra2 =  kaguyaUltraSkill("沒有圖片", "", 0)
        ultra3 =  kaguyaUltraSkill("沒有圖片", "", 0)
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)
    def useSpecialMove(self, g:game):
        pass
    def specialMove(self, g:game):
        pass
    def droporKeepCard(self, g:game, card):
        uc = g.nowUsingCardID
        s = g.status
        g.status = state.KEEP_OR_BACK
        ret = svr.connectBot(g.nowid, 'int8_t', g)
        g.status = s
        g.nowUsingCardID = uc
        return ret
    def lostLiveRemoveCard(self, g:game):
        s = g.status
        g.status = state.LOST_LIFE_FOR_REMOVECARD
        ret = svr.connectBot(g.nowid, 'int8_t', g)
        if ret == 1:
            g.lostLife(g.nowid, 1)
            where, c = g.chooseCardFromHandorGraveyard()
            if where: # hand
                del g.players[g.nowid].hand[c]
            else: # graveyard
                del g.players[g.nowid].graveyard[c]
        elif ret != 0:
            g.cheating()
        g.status = s