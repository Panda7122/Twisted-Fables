import sys 
sys.path.append("..")
from game import *
from characters.character import *
class dorothyATKSkill(atkCard):
    def skill(self, g:game, level):
        if g.getRange()>1:
            g.cheating()
        beforeDis = g.getRange()
        g.knockback(level)
        afterDis = g.getRange()
        X = level - (afterDis-beforeDis)
        g.damage(1-g.nowid, 11, self.level + level+X)
        lastAct = lastAction(0 ,0, 0,0, [1, self.level, level])
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
        lastAct = lastAction(0 ,0, 0,0, [2, self.level, level])
        
    
class dorothyMOVSkill(movCard):
    def skill(self, g:game, level):
        g.damage(1-g.nowid,self.level+level, g.getRange()) 
        lastAct = lastAction(0 ,0, 0, 0,[3, self.level, level])
        pass
class dorothyMETASkill(metaCard):
    def skill(self, g:game, level):
        g.cheating()
class dorothyUltraSkill(ultraCard):
    def skill(self, g:game, level):
        t = g.players[g.nowid].identity.spendTOKEN(g)
        if self.cardName == '獅子':
            g.damage(1-g.nowid, 1, t)
            g.players[g.nowid].identity.energy += t
        elif self.cardName == '鐵皮人':
            g.players[g.nowid].identity.life += t
            g.players[g.nowid].identity.life = min(g.players[g.nowid].identity.maxlife, g.players[g.nowid].identity.life)
        elif self.cardName == '稻草人':
            for _ in range((t+1)//2):
                g.drawCard(g.nowid)
        pass
class dorothy(character):
    @property
    def idx(self):
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
    def __init__(self, COMBO_TOKEN=0, canCombo=0, **kwargs):
        super().__init__()
        self.setup()
        self.COMBO_TOKEN = COMBO_TOKEN
        self.canCombo = canCombo
        self.characterName = "桃樂絲"
        self.picture = "./picture/character/dorothy/character.png"
        atklv1 =  dorothyATKSkill("沒有圖片", "目標確認", 1)
        atklv2 =  dorothyATKSkill("沒有圖片", "目標鎖定", 2)
        atklv3 =  dorothyATKSkill("沒有圖片", "目標清除", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  dorothyDEFSkill("沒有圖片", "思想刺探", 1)
        deflv2 =  dorothyDEFSkill("沒有圖片", "深度搜索", 2)
        deflv3 =  dorothyDEFSkill("沒有圖片", "讀取完畢", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  dorothyMOVSkill("沒有圖片", "發現敵蹤", 1)
        movlv2 =  dorothyMOVSkill("沒有圖片", "進入視野", 2)
        movlv3 =  dorothyMOVSkill("沒有圖片", "使命終結", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  dorothyMETASkill("沒有圖片", "殺戮指令")
        meta2 =  dorothyMETASkill("沒有圖片", "超越機器")
        meta3 =  dorothyMETASkill("沒有圖片", "獲准極刑")
        meta4 =  dorothyMETASkill("沒有圖片", "無所遁形")
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  dorothyUltraSkill("沒有圖片", "獅子")
        ultra2 =  dorothyUltraSkill("沒有圖片", "鐵皮人")
        ultra3 =  dorothyUltraSkill("沒有圖片", "稻草人")
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)
    def dropCard(self, g:game):
        s = g.status
        g.status = state.DROP_CARD
        ret = svr.connectBot(g.nowid, "int32_t", g)
        if ret >= len(g.players[g.nowid].hand) or ret < 0:
            # cheat
            g.cheating()
        ret -= 1
        g.status = s
        return ret
    def spendTOKEN(self, g:game):
        s = g.status
        g.status = state.SPEND_COMBO
        c = svr.connectBot(g.nowid, 'int32_t', g)
        if c < 0 or c > self.COMBO_TOKEN:
            g.cheating()
        self.COMBO_TOKEN -= c
        g.status = s
        return c