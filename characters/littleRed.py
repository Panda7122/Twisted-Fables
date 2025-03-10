import sys 
sys.path.append("..")
from game import *
from character import *
class littleRedATKSkill(atkCard):
    def skill(self, g:game, level):
        if g.getRange()> self.level:
            g.cheating()
        g.damage(1-g.nowid, self.level, self.level+level)
class littleRedDEFSkill(defCard):
    def skill(self, g:game, level):
        if g.getRange()> self.level:
            g.cheating()
        g.damage(1-g.nowid, self.level, self.level)
        g.players[g.nowid].defense+=1
        g.players[g.nowid].defense = min(g.players[g.nowid].maxdefense, g.players[g.nowid].defense)
class littleRedMOVSkill(movCard):
    def skill(self, g:game, level):
        if g.getRange()> self.level:
            g.cheating()
        g.damage(1-g.nowid, self.level, self.level)
        g.status = state.KNOCKBACK
        dis = svr.connectBot(g.nowid, 'int32_t', g)
        if dis > self.level or dis < 0:
            g.cheating()
        g.knockback(dis)
class littleRedMETASkill(metaCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class littleRedUltraSkill(ultraCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class littleRed(character):
    def idx():
        return 0
    def setup(self):
        self.maxlife = 30
        self.life= self.maxlife
        self.maxdefense = 6
        self.defense = 0 
        self.energy = 0
        self.specialGate = 15  
    def __init__(self, **kwargs):
        self.setup()
        self.characterName = "小紅帽"
        self.picture = "沒有圖片"
        atklv1 =  littleRedATKSkill("沒有圖片", "快速射擊", 1)
        atklv2 =  littleRedATKSkill("沒有圖片", "精準射擊", 2)
        atklv3 =  littleRedATKSkill("沒有圖片", "致命狙擊", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  littleRedDEFSkill("沒有圖片", "能量護盾", 1)
        deflv2 =  littleRedDEFSkill("沒有圖片", "電流護盾", 2)
        deflv3 =  littleRedDEFSkill("沒有圖片", "終極護盾", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  littleRedMOVSkill("沒有圖片", "彈道噴射", 1)
        movlv2 =  littleRedMOVSkill("沒有圖片", "火力噴射", 2)
        movlv3 =  littleRedMOVSkill("沒有圖片", "暴怒噴射", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  littleRedMETASkill("沒有圖片", "過載燃燒", 0)
        meta2 =  littleRedMETASkill("沒有圖片", "兜帽系統", 0)
        meta3 =  littleRedMETASkill("沒有圖片", "兜帽系統", 0)
        meta4 =  littleRedMETASkill("沒有圖片", "板載緩存", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  littleRedUltraSkill("沒有圖片", "餓狼吞噬", 0)
        ultra2 =  littleRedUltraSkill("沒有圖片", "系統入侵", 0)
        ultra3 =  littleRedUltraSkill("沒有圖片", "復仇之雨", 0)
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)
    def specialMove(self, g:game):
        g.cheating()