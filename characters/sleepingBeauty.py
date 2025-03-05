from game import *
from character import *
class sleepingBeautyATKSkill(atkCard):
    def skill(self, g:game, level):
        s = g.status
        g.status = state.SLEEPATKHERTSELF
        h = svr.connectBot(g.nowid, 'int32_t', g)
        if h < 0 or h >  self.level:
            g.cheating()
        atk = (self.level)*level+h
        g.damage(g.nowid, 11, h)
        g.damage(1-g.nowid, 1, atk)        
        g.status = s
class sleepingBeautyDEFSkill(defCard):
    def skill(self, g:game, level):
        pass
class sleepingBeautyMOVSkill(movCard):
    def skill(self, g:game, level):
        pass
class sleepingBeautyMETASkill(metaCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class sleepingBeautyUltraSkill(ultraCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class sleepingBeauty(character):
    def idx():
        return 2
    def setup(self):
        self.maxlife = 42
        self.life= self.maxlife
        self.maxdefense = 6
        self.defense = 0 
        self.energy = 0
        self.specialGate = 21  
        self.AWAKEN_TOKEN = 0
        self.AWAKEN = 0
        self.dayNightmareDrawRemind = 0
    def __init__(self, AWEAKEN = 0, AWAKEN_TOKEN = 0, dayNightmareDrawRemind = 0, **kwargs):
        self.setup()
        self.AWAKEN_TOKEN = AWAKEN_TOKEN
        self.AWAKEN = AWEAKEN
        self.dayNightmareDrawRemind = dayNightmareDrawRemind
        self.characterName = "睡美人"
        self.picture = "沒有圖片"
        atklv1 =  sleepingBeautyATKSkill("沒有圖片", "", 1)
        atklv2 =  sleepingBeautyATKSkill("沒有圖片", "", 2)
        atklv3 =  sleepingBeautyATKSkill("沒有圖片", "", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  sleepingBeautyDEFSkill("沒有圖片", "", 1)
        deflv2 =  sleepingBeautyDEFSkill("沒有圖片", "", 2)
        deflv3 =  sleepingBeautyDEFSkill("沒有圖片", "", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  sleepingBeautyMOVSkill("沒有圖片", "", 1)
        movlv2 =  sleepingBeautyMOVSkill("沒有圖片", "", 2)
        movlv3 =  sleepingBeautyMOVSkill("沒有圖片", "", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  sleepingBeautyMETASkill("沒有圖片", "", 0)
        meta2 =  sleepingBeautyMETASkill("沒有圖片", "", 0)
        meta3 =  sleepingBeautyMETASkill("沒有圖片", "", 0)
        meta4 =  sleepingBeautyMETASkill("沒有圖片", "", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  sleepingBeautyUltraSkill("沒有圖片", "", 0)
        ultra2 =  sleepingBeautyUltraSkill("沒有圖片", "", 0)
        ultra3 =  sleepingBeautyUltraSkill("沒有圖片", "", 0)
        self.moveSkill.append(ultra1)
        self.moveSkill.append(ultra2)
        self.moveSkill.append(ultra3)