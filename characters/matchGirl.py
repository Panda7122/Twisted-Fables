import sys 
sys.path.append("..")
from game import *
from character import *
class matchGirlATKSkill(atkCard):
    def skill(self, g:game, level):
        pass
class matchGirlDEFSkill(defCard):
    def skill(self, g:game, level):
        pass
class matchGirlMOVSkill(movCard):
    def skill(self, g:game, level):
        pass
class matchGirlMETASkill(metaCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class matchGirlUltraSkill(ultraCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class matchGirl(character):
    def idx():
        return 7
    def setup(self):
        self.maxlife = 36
        self.life= self.maxlife
        self.maxdefense = 6
        self.defense = 0
        self.energy = 0
        self.specialGate = 18
        self.remindMatch = 12
    def __init__(self, remindMatch, **kwargs):
        self.setup()
        self.remindMatch = remindMatch
        self.characterName = "火柴女孩"
        self.picture = "沒有圖片"
        atklv1 =  matchGirlATKSkill("沒有圖片", "", 1)
        atklv2 =  matchGirlATKSkill("沒有圖片", "", 2)
        atklv3 =  matchGirlATKSkill("沒有圖片", "", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  matchGirlDEFSkill("沒有圖片", "", 1)
        deflv2 =  matchGirlDEFSkill("沒有圖片", "", 2)
        deflv3 =  matchGirlDEFSkill("沒有圖片", "", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  matchGirlMOVSkill("沒有圖片", "", 1)
        movlv2 =  matchGirlMOVSkill("沒有圖片", "", 2)
        movlv3 =  matchGirlMOVSkill("沒有圖片", "", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  matchGirlMETASkill("沒有圖片", "", 0)
        meta2 =  matchGirlMETASkill("沒有圖片", "", 0)
        meta3 =  matchGirlMETASkill("沒有圖片", "", 0)
        meta4 =  matchGirlMETASkill("沒有圖片", "", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  matchGirlUltraSkill("沒有圖片", "", 0)
        ultra2 =  matchGirlUltraSkill("沒有圖片", "", 0)
        ultra3 =  matchGirlUltraSkill("沒有圖片", "", 0)
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)