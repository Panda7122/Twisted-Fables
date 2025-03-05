from game import *
from character import *
class aliceATKSkill(atkCard):
    def skill(self, g:game, level):
        pass
class aliceDEFSkill(defCard):
    def skill(self, g:game, level):
        pass
class aliceMOVSkill(movCard):
    def skill(self, g:game, level):
        pass
class aliceMETASkill(metaCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class aliceUltraSkill(ultraCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class alice(character):
    def idx():
        return 3
    def setup(self):
        self.maxlife = 32
        self.life= self.maxlife
        self.maxdefense = 6
        self.defense = 0 
        self.energy = 0
        self.specialGate = 16   
    def __init__(self, identity = 0, **kwargs):
        self.setup()
        self.identity = identity
        self.characterName = "愛麗絲"
        self.picture = "沒有圖片"
        atklv1 =  aliceATKSkill("沒有圖片", "", 1)
        atklv2 =  aliceATKSkill("沒有圖片", "", 2)
        atklv3 =  aliceATKSkill("沒有圖片", "", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  aliceDEFSkill("沒有圖片", "", 1)
        deflv2 =  aliceDEFSkill("沒有圖片", "", 2)
        deflv3 =  aliceDEFSkill("沒有圖片", "", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  aliceMOVSkill("沒有圖片", "", 1)
        movlv2 =  aliceMOVSkill("沒有圖片", "", 2)
        movlv3 =  aliceMOVSkill("沒有圖片", "", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  aliceMETASkill("沒有圖片", "", 0)
        meta2 =  aliceMETASkill("沒有圖片", "", 0)
        meta3 =  aliceMETASkill("沒有圖片", "", 0)
        meta4 =  aliceMETASkill("沒有圖片", "", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  aliceUltraSkill("沒有圖片", "", 0)
        ultra2 =  aliceUltraSkill("沒有圖片", "", 0)
        ultra3 =  aliceUltraSkill("沒有圖片", "", 0)
        self.moveSkill.append(ultra1)
        self.moveSkill.append(ultra2)
        self.moveSkill.append(ultra3)