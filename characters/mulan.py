from game import *
from character import *
class mulanATKSkill(atkCard):
    def skill(self, g:game, level):
        pass
class mulanDEFSkill(defCard):
    def skill(self, g:game, level):
        pass
class mulanMOVSkill(movCard):
    def skill(self, g:game, level):
        pass
class mulanMETASkill(metaCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class mulanUltraSkill(ultraCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class mulan(character):
    def idx():
        return 4
    def setup(self):
        self.maxlife = 34
        self.life= self.maxlife
        self.maxdefense = 3
        self.defense = 0 
        self.energy = 0
        self.specialGate = 17   
        self.KI_TOKEN = 0
    def __init__(self, KI_TOKEN = 0, **kwargs):
        self.setup()
        self.KI_TOKEN = KI_TOKEN
        self.characterName = "花木蘭"
        self.picture = "沒有圖片"
        atklv1 =  mulanATKSkill("沒有圖片", "", 1)
        atklv2 =  mulanATKSkill("沒有圖片", "", 2)
        atklv3 =  mulanATKSkill("沒有圖片", "", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  mulanDEFSkill("沒有圖片", "", 1)
        deflv2 =  mulanDEFSkill("沒有圖片", "", 2)
        deflv3 =  mulanDEFSkill("沒有圖片", "", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  mulanMOVSkill("沒有圖片", "", 1)
        movlv2 =  mulanMOVSkill("沒有圖片", "", 2)
        movlv3 =  mulanMOVSkill("沒有圖片", "", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  mulanMETASkill("沒有圖片", "", 0)
        meta2 =  mulanMETASkill("沒有圖片", "", 0)
        meta3 =  mulanMETASkill("沒有圖片", "", 0)
        meta4 =  mulanMETASkill("沒有圖片", "", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  mulanUltraSkill("沒有圖片", "", 0)
        ultra2 =  mulanUltraSkill("沒有圖片", "", 0)
        ultra3 =  mulanUltraSkill("沒有圖片", "", 0)
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)