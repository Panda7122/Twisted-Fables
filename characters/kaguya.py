from game import *
from character import *
class kaguyaATKSkill(atkCard):
    def skill(self, g:game, level):
        pass
class kaguyaDEFSkill(defCard):
    def skill(self, g:game, level):
        pass
class kaguyaMOVSkill(movCard):
    def skill(self, g:game, level):
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
        self.moveSkill.append(ultra1)
        self.moveSkill.append(ultra2)
        self.moveSkill.append(ultra3)