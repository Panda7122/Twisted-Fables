import sys 
sys.path.append("..")
from game import *
from characters.character import *
class sleepingBeautyATKSkill(atkCard):
    def skill(self, g:game, level):
        if g.getRange() > 1:
            g.cheating()
        s = g.status
        g.status = state.SLEEP_ATK_HERTSELF
        h = svr.connectBot(g.nowid, 'int32_t', g)
        if h < 0 or h >  self.level:
            g.cheating()
        atk = (self.level)*level+h
        g.damage(g.nowid, 11, h)
        g.damage(1-g.nowid, 1, atk)        
        g.status = s
class sleepingBeautyDEFSkill(defCard):
    def skill(self, g:game, level):
        if g.players[g.nowid].identity.AWAKEN == 1:
            q = g.players[g.nowid].identity.askUSE_AWAKEN_TOKEN(g)
        else:
            q = 0
        g.players[g.nowid].identity.atkRiseTime = q+level
        g.players[g.nowid].identity.atkRise = self.level
        pass
class sleepingBeautyMOVSkill(movCard):
    def skill(self, g:game, level):
        if g.getRange() > self.level+1:
            g.cheating()
        if g.players[g.nowid].identity.AWAKEN == 1:
            q = g.players[g.nowid].identity.askUSE_AWAKEN_TOKEN(g)
        else:
            q = 0
        g.damage(1-g.nowid, self.level+1, level + q)
        g.knockback(-min(g.getRange()-1, level))
        pass
class sleepingBeautyMETASkill(metaCard):
    def skill(self, g:game, level):
        g.cheating()
        pass
class sleepingBeautyUltraSkill(ultraCard):
    def skill(self, g:game, level):
        if self.cardName == '喚醒沉睡':
            g.players[g.nowid].identity.AWAKEN_TOKEN += 3
            self.AWAKEN = 1
        elif self.cardName == '血脈重鑄':
            g.players[g.nowid].identity.life += g.players[g.nowid].identity.AWAKEN_TOKEN
            g.players[g.nowid].identity.life = min(g.players[g.nowid].identity.life, g.players[g.nowid].identity.maxlife)
class sleepingBeauty(character):
    @property
    def idx(self):
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
        self.atkRise = 0
        self.atkRiseTime = 0
        self.usedmeta1 = 0
        self.usedmeta2 = 0
    def __init__(self, AWEAKEN = 0, AWAKEN_TOKEN = 0, dayNightmareDrawRemind = 0, atkRise = 0, atkRiseTime = 0, usedmeta1 = 0, usedmeta2 = 0, **kwargs):
        super().__init__()
        self.setup()
        self.AWAKEN_TOKEN = AWAKEN_TOKEN
        self.AWAKEN = AWEAKEN
        self.dayNightmareDrawRemind = dayNightmareDrawRemind
        self.atkRise = atkRise
        self.atkRiseTime = atkRiseTime
        self.usedmeta1 = usedmeta1
        self.usedmeta2 = usedmeta2
        self.characterName = "睡美人"
        self.picture = "./picture/character/sleepingBeauty/character.png"
        self.picture_awakend = "./picture/character/sleepingBeauty/character_awakend.png"
        atklv1 =  sleepingBeautyATKSkill("沒有圖片", "心靈震顫", 1)
        atklv2 =  sleepingBeautyATKSkill("沒有圖片", "心靈之怒", 2)
        atklv3 =  sleepingBeautyATKSkill("沒有圖片", "心靈狂怒", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  sleepingBeautyDEFSkill("沒有圖片", "爆裂之鎖", 1)
        deflv2 =  sleepingBeautyDEFSkill("沒有圖片", "爆裂之骨", 2)
        deflv3 =  sleepingBeautyDEFSkill("沒有圖片", "爆裂之魂", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  sleepingBeautyMOVSkill("沒有圖片", "黑暗碰觸", 1)
        movlv2 =  sleepingBeautyMOVSkill("沒有圖片", "黑暗糾纏", 2)
        movlv3 =  sleepingBeautyMOVSkill("沒有圖片", "黑暗絞殺", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  sleepingBeautyMETASkill("沒有圖片", "放血療法")
        meta2 =  sleepingBeautyMETASkill("沒有圖片", "血祭之禮")
        meta3 =  sleepingBeautyMETASkill("沒有圖片", "精神屏障")
        meta4 =  sleepingBeautyMETASkill("沒有圖片", "強制治療")
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  sleepingBeautyUltraSkill("沒有圖片", "喚醒沉睡")
        ultra2 =  sleepingBeautyUltraSkill("沒有圖片", "白日夢魘")
        ultra3 =  sleepingBeautyUltraSkill("沒有圖片", "血脈重鑄")
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)
    def askUSE_AWAKEN_TOKEN(self, g:game):
        if self.AWAKEN == 1:
            return 0
        g.status = state.USE_AWAKEN_TOKEN
        t = svr.connectBot(g.nowid, "int8_t", g)
        if t > 3 or t < 0:
            g.cheating()
        return t
    def specialMove(self, g:game):
        g.cheating()