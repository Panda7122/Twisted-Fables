from game import *
from character import *
class mermaidATKSkill(atkCard):
    def skill(self, g:game, level):
        pass
class mermaidDEFSkill(defCard):
    def skill(self, g:game, level):
        pass
class mermaidMOVSkill(movCard):
    def skill(self, g:game, level):
        pass
class mermaidMETASkill(metaCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class mermaidUltraSkill(ultraCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class mermaid(character):
    def idx():
        return 6
    def setup(self):
        self.maxlife = 36
        self.life= self.maxlife
        self.maxdefense = 3
        self.defense = 0
        self.energy = 0
        self.specialGate = 18
    def __init__(self, **kwargs):
        self.setup()
        self.characterName = "小美人魚"
        self.picture = "沒有圖片"
        atklv1 =  mermaidATKSkill("沒有圖片", "", 1)
        atklv2 =  mermaidATKSkill("沒有圖片", "", 2)
        atklv3 =  mermaidATKSkill("沒有圖片", "", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  mermaidDEFSkill("沒有圖片", "", 1)
        deflv2 =  mermaidDEFSkill("沒有圖片", "", 2)
        deflv3 =  mermaidDEFSkill("沒有圖片", "", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  mermaidMOVSkill("沒有圖片", "", 1)
        movlv2 =  mermaidMOVSkill("沒有圖片", "", 2)
        movlv3 =  mermaidMOVSkill("沒有圖片", "", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  mermaidMETASkill("沒有圖片", "", 0)
        meta2 =  mermaidMETASkill("沒有圖片", "", 0)
        meta3 =  mermaidMETASkill("沒有圖片", "", 0)
        meta4 =  mermaidMETASkill("沒有圖片", "", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  mermaidUltraSkill("沒有圖片", "", 0)
        ultra2 =  mermaidUltraSkill("沒有圖片", "", 0)
        ultra3 =  mermaidUltraSkill("沒有圖片", "", 0)
        self.moveSkill.append(ultra1)
        self.moveSkill.append(ultra2)
        self.moveSkill.append(ultra3)