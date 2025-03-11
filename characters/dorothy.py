import sys 
sys.path.append("..")
from game import *
from character import *
class dorothyATKSkill(atkCard):
    def skill(self, g:game, level):
        if g.getRange()>1:
            g.cheating()
        beforeDis = g.getRange()
        g.knockback(level)
        afterDis = g.getRange()
        X = level - (afterDis-beforeDis)
        g.damage(1-g.nowid, 11, self.level + level+X)
        pass
class dorothyDEFSkill(defCard):
    def skill(self, g:game, level):
        cnt = 1
        while(1):
            drop = g.players[g.nowid].identity.dropCard(g)
            if drop == -1:
                break
            cnt += 1
            if g.players[g.nowid].hand[drop]not in [1,2,3,4,5,6,7,8,9,10]:
                g.cheating()
            g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[drop])
            del g.players[g.nowid].hand[drop]
        for _ in range(cnt):
            g.drawCard(g.nowid)
        pass
    
class dorothyMOVSkill(movCard):
    def skill(self, g:game, level):
        g.damage(1-g.nowid,self.level+level, g.getRange()-1)
        pass
class dorothyMETASkill(metaCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class dorothyUltraSkill(ultraCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class dorothy(character):
    def idx():
        return 8
    def setup(self):
        self.maxlife = 40
        self.life= self.maxlife
        self.maxdefense = 6
        self.defense = 0
        self.energy = 0
        self.specialGate = 18
        self.COMBO_TOKEN = 0
        self.canCombo = 0
    def __init__(self, COMBO_TOKEN, canCombo, **kwargs):
        self.setup()
        self.COMBO_TOKEN = COMBO_TOKEN
        self.canCombo = canCombo
        self.characterName = "桃樂絲"
        self.picture = "沒有圖片"
        atklv1 =  dorothyATKSkill("沒有圖片", "", 1)
        atklv2 =  dorothyATKSkill("沒有圖片", "", 2)
        atklv3 =  dorothyATKSkill("沒有圖片", "", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  dorothyDEFSkill("沒有圖片", "", 1)
        deflv2 =  dorothyDEFSkill("沒有圖片", "", 2)
        deflv3 =  dorothyDEFSkill("沒有圖片", "", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  dorothyMOVSkill("沒有圖片", "", 1)
        movlv2 =  dorothyMOVSkill("沒有圖片", "", 2)
        movlv3 =  dorothyMOVSkill("沒有圖片", "", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  dorothyMETASkill("沒有圖片", "", 0)
        meta2 =  dorothyMETASkill("沒有圖片", "", 0)
        meta3 =  dorothyMETASkill("沒有圖片", "", 0)
        meta4 =  dorothyMETASkill("沒有圖片", "", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  dorothyUltraSkill("沒有圖片", "", 0)
        ultra2 =  dorothyUltraSkill("沒有圖片", "", 0)
        ultra3 =  dorothyUltraSkill("沒有圖片", "", 0)
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)
    def dropCard(self, g:game):
        s = self.status
        g.status = state.DROP_CARD
        ret = svr.connectBot(g.nowid, "int32_t", g)
        if ret >= len(g.players[g.nowid].hand) or ret < 0:
            # cheat
            g.cheating()
        ret -= 1
        g.status = s
        return ret