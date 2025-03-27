import sys 
sys.path.append("..")
from game import *
from character import *
class mulanATKSkill(atkCard):
    def skill(self, g:game, level):
        K = 0
        if 151 in g.players[g.nowid].metamorphosis:
            K = g.players[g.nowid].identity.spendKIforATK(g)
            if K>3 or K<0:
                g.cheating()
            if K > g.players[g.nowid].identity.KI_TOKEN:
                g.cheating()
            g.players[g.nowid].identity.KI_TOKEN -= K
        g.damage(1-g.nowid, 1, self.level+level+K)
        g.players[g.nowid].identity.putAnotherSide(g)
        if g.players[1-g.nowid].locate in [1,9]:
            cid = random.randint(0,len(g.players[1-g.nowid].hand-1))
            card = g.players[1-g.nowid].hand[cid]
            del g.players[1-g.nowid].hand[cid]
            g.players[1-g.nowid].graveyard.append(card)
            if card == 134:
                eneragy = 1
                for i in range(g.players[1-g.nowid].metamorphosis):
                    if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                        eneragy+=1
                g.players[1-g.nowid].energy += eneragy
            if card in [131, 132, 133]:
                posion = card-131
                for i in range(len(g.players[1-g.nowid].metamorphosis)):
                    if g.players[1-g.nowid].metamorphosis[i] == 142:
                        posion+=1
                g.lostLife( g.nowid, posion)
class mulanDEFSkill(defCard):
    def skill(self, g:game, level):
        g.players[g.nowid].identity.defense += level
        g.players[g.nowid].identity.defense = min(g.players[g.nowid].identity.maxdefense, g.players[g.nowid].identity.defense)
        g.players[g.nowid].identity.extraCard += self.level
class mulanMOVSkill(movCard):
    def skill(self, g:game, level):
        g.damage(1-g.nowid, 1, self.level)
        g.knockback(level)
        g.status = state.CHOOSE_MOVE_NEARBY
        side = svr.connectBot(g.nowid, "int8_t", g)
        if side == 1:
            if(g.players[g.nowid].locate-1>9):
                g.cheating()
            g.setLocate(g.players[g.nowid].locate+1)
        elif side == -1:
            if(g.players[g.nowid].locate-1<1):
                g.cheating()
            g.setLocate(g.players[g.nowid].locate-1)
        elif side != 0:
            g.cheating()
        if g.players[1-g.nowid].locate in [1,9]:
            cid = random.randint(0,len(g.players[1-g.nowid].hand-1))
            card = g.players[1-g.nowid].hand[cid]
            del g.players[1-g.nowid].hand[cid]
            g.players[1-g.nowid].graveyard.append(card)
            if card == 134:
                eneragy = 1
                for i in range(len(g.players[1-g.nowid].metamorphosis)):
                    if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                        eneragy+=1
                g.players[1-g.nowid].energy += eneragy
            if card in [131, 132, 133]:
                posion = card-131
                for i in range(len(g.players[1-g.nowid].metamorphosis)):
                    if g.players[1-g.nowid].metamorphosis[i] == 142:
                        posion+=1
                g.lostLife( g.nowid, posion)
class mulanMETASkill(metaCard):
    def skill(self, g:game, level):
        g.cheating()

class mulanUltraSkill(ultraCard):
    def skill(self, g:game, level):
        if self.cardName == '氣沖雲霄':
            g.players[g.nowid].identity.extraDraw = 4
        elif self.cardName == '直面混沌':
            s = g.status
            g.status = state.CHOOSE_MOVE_NEARBY
            loc = svr.connectBot(g.nowid, 'int32_t', g)
            if loc not in [-1, 1]:
                g.cheating()
            if g.players[1-g.nowid].locate + loc > 9 or g.players[1-g.nowid].locate + loc < 1:
                g.cheating()
            g.players[g.nowid].locate = g.players[1-g.nowid].locate + loc
            g.status = s
            g.players[g.nowid].identity.KI_TOKEN +=3
        elif self.cardName == '雷霆一擊':
            X = g.players[g.nowid].identity.KI_TOKEN
            g.players[g.nowid].identity.KI_TOKEN = 0
            g.damage(1-g.nowid, 1, X)
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
        self.extraCard = 0
        self.extraDraw = 0
    def __init__(self, KI_TOKEN = 0, extraCard = 0, extraDraw = 0, **kwargs):
        self.setup()
        self.KI_TOKEN = KI_TOKEN
        self.extraCard = extraCard
        self.extraDraw = extraDraw
        self.characterName = "花木蘭"
        self.picture = "沒有圖片"
        atklv1 =  mulanATKSkill("沒有圖片", "不容小覷", 1)
        atklv2 =  mulanATKSkill("沒有圖片", "勢不可擋", 2)
        atklv3 =  mulanATKSkill("沒有圖片", "堅不可摧", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  mulanDEFSkill("沒有圖片", "以靜制動", 1)
        deflv2 =  mulanDEFSkill("沒有圖片", "以柔克剛", 2)
        deflv3 =  mulanDEFSkill("沒有圖片", "以弱勝強", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  mulanMOVSkill("沒有圖片", "永不退縮", 1)
        movlv2 =  mulanMOVSkill("沒有圖片", "毫不留情", 2)
        movlv3 =  mulanMOVSkill("沒有圖片", "絕不饒恕", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  mulanMETASkill("沒有圖片", "氣慣全身", 0)
        meta2 =  mulanMETASkill("沒有圖片", "主宰命運", 0)
        meta3 =  mulanMETASkill("沒有圖片", "長驅直入", 0)
        meta4 =  mulanMETASkill("沒有圖片", "暴風前夕", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  mulanUltraSkill("沒有圖片", "氣沖雲霄", 0)
        ultra2 =  mulanUltraSkill("沒有圖片", "直面混沌", 0)
        ultra3 =  mulanUltraSkill("沒有圖片", "雷霆一擊", 0)
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)
    def spendKIforDraw(self, g:game):
        s = g.status
        g.status = state.SPEND_KI_FOR_DRAW
        ret = svr.connectBot(g.nowid, 'int32_t', g)
        if ret > self.KI_TOKEN:
            g.cheating()
        g.status= s
        return ret
    def spendKIforATK(self, g:game):
        s = g.status
        g.status = state.SPEND_KI_FOR_ATK
        ret = svr.connectBot(g.nowid, 'int32_t', g)
        g.status= s
        if ret > self.KI_TOKEN:
            g.cheating()
        return ret
    def spendKIforATK(self, g:game):
        s = g.status
        g.status = state.SPEND_KI_FOR_MOV
        ret = svr.connectBot(g.nowid, 'int32_t', g)
        g.status= s
        if ret > self.KI_TOKEN:
            g.cheating()
        return ret