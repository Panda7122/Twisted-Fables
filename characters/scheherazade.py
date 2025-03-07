from game import *
from character import *
class scheherazadeATKSkill(atkCard):
    def skill(self, g:game, level):
        pass
class scheherazadeDEFSkill(defCard):
    def skill(self, g:game, level):
        pass
class scheherazadeMOVSkill(movCard):
    def skill(self, g:game, level):
        pass
class scheherazadeMETASkill(metaCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class scheherazadeUltraSkill(ultraCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class scheherazade(character):
    def idx():
        return 9
    def setup(self):
        self.maxlife = 36
        self.life= self.maxlife
        self.maxdefense = 6
        self.defense = 0
        self.energy = 0
        self.specialGate = 18
    def __init__(self, **kwargs):
        self.setup()
        self.characterName = "山魯佐德"
        self.picture = "沒有圖片"
        atklv1 =  scheherazadeATKSkill("沒有圖片", "", 1)
        atklv2 =  scheherazadeATKSkill("沒有圖片", "", 2)
        atklv3 =  scheherazadeATKSkill("沒有圖片", "", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  scheherazadeDEFSkill("沒有圖片", "", 1)
        deflv2 =  scheherazadeDEFSkill("沒有圖片", "", 2)
        deflv3 =  scheherazadeDEFSkill("沒有圖片", "", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  scheherazadeMOVSkill("沒有圖片", "", 1)
        movlv2 =  scheherazadeMOVSkill("沒有圖片", "", 2)
        movlv3 =  scheherazadeMOVSkill("沒有圖片", "", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  scheherazadeMETASkill("沒有圖片", "", 0)
        meta2 =  scheherazadeMETASkill("沒有圖片", "", 0)
        meta3 =  scheherazadeMETASkill("沒有圖片", "", 0)
        meta4 =  scheherazadeMETASkill("沒有圖片", "", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  scheherazadeUltraSkill("沒有圖片", "", 0)
        ultra2 =  scheherazadeUltraSkill("沒有圖片", "", 0)
        ultra3 =  scheherazadeUltraSkill("沒有圖片", "", 0)
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)