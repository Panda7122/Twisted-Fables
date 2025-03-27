import sys 
sys.path.append("..")
from game import *
from character import *
class matchGirlATKSkill(atkCard):
    def skill(self, g:game, level):
        ra = 0    
        if 163 in g.players[g.nowid].metamorphosis:
            r = g.players[g.nowid].identity.recycle_match(g, 1)
            if r == 1:
                ra = 2
        cost = g.players[g.nowid].identity.spendEnergy(g)
        g.damage(1-g.nowid, 1, self.level+level+(cost//3) + ra)
        pass
class matchGirlDEFSkill(defCard):
    def skill(self, g:game, level):
        if 164 in g.players[g.nowid].metamorphosis:
            r = g.players[g.nowid].identity.recycle_match(g, 1)
            if r == 1:
                g.drawCard(g.nowid)
        g.players[g.nowid].identity.defense += 1
        g.players[g.nowid].identity.defense = min(g.players[g.nowid].identity.defense , g.players[g.nowid].identity.maxdefense)
        lost = g.players[g.nowid].identity.spendLife(g)
        g.lostLife(g.nowid, lost)
        for _ in range(lost):
            g.drawCard(g.nowid)
class matchGirlMOVSkill(movCard):
    def skill(self, g:game, level):
        g.damage(1-g.nowid,self.level, self.level)
        rec = g.players[g.nowid].identity.recycle_match(g, level)
        g.players[g.nowid].identity.energy += self.level * rec
        g.players[g.nowid].identity.life += (self.level-1) * rec
        g.players[g.nowid].identity.life = min(g.players[g.nowid].identity.maxlife,g.players[g.nowid].identity.life)
class matchGirlMETASkill(metaCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class matchGirlUltraSkill(ultraCard):
    def skill(self, g:game, level):
        if self.cardName == '地獄烈焰':
            g.damage(1-g.nowid, 1, (g.players[g.nowid].identity.energy+1)>>1)
        elif self.cardName == '厄運降臨':
            for _ in range(6):
                t = g.dropDeck(1-g.nowid)
                if t == 134:
                    g.damage(1-g.nowid, 3, 1)
        elif self.cardName == '貪婪詛咒':
            for _ in range(3):
                g.players[g.nowid].identity.pushMatch()
            
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
        self.pushedMatch = 0
    def __init__(self, remindMatch, pushedMatch, **kwargs):
        self.setup()
        self.remindMatch = remindMatch
        self.pushedMatch = pushedMatch
        self.characterName = "火柴女孩"
        self.picture = "沒有圖片"
        atklv1 =  matchGirlATKSkill("沒有圖片", "虛幻的願望", 1)
        atklv2 =  matchGirlATKSkill("沒有圖片", "隱密的期望", 2)
        atklv3 =  matchGirlATKSkill("沒有圖片", "無厭的奢望", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  matchGirlDEFSkill("沒有圖片", "惡魔的祭品", 1)
        deflv2 =  matchGirlDEFSkill("沒有圖片", "惡魔的賭注", 2)
        deflv3 =  matchGirlDEFSkill("沒有圖片", "惡魔的契約", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  matchGirlMOVSkill("沒有圖片", "失重的靈魂", 1)
        movlv2 =  matchGirlMOVSkill("沒有圖片", "虧欠的靈魂", 2)
        movlv3 =  matchGirlMOVSkill("沒有圖片", "殘破的靈魂", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  matchGirlMETASkill("沒有圖片", "痛苦的儀式", 0)
        meta2 =  matchGirlMETASkill("沒有圖片", "放縱的渴望", 0)
        meta3 =  matchGirlMETASkill("沒有圖片", "魔鬼的凝視", 0)
        meta4 =  matchGirlMETASkill("沒有圖片", "火焰的捉弄", 0)
        meta5 =  matchGirlMETASkill("沒有圖片", "欲望的捉弄", 0)
        meta6 =  matchGirlMETASkill("沒有圖片", "命運的捉弄", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        self.metamorphosisSkill.append(meta5)
        self.metamorphosisSkill.append(meta6)
        ultra1 =  matchGirlUltraSkill("沒有圖片", "地獄烈焰", 0)
        ultra2 =  matchGirlUltraSkill("沒有圖片", "厄運降臨", 0)
        ultra3 =  matchGirlUltraSkill("沒有圖片", "貪婪詛咒", 0)
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)
    def pushMatch(self, g:game):
        if(self.remindMatch>0):
            g.players[1-g.nowid].deck.insert(0, 134)
            self.remindMatch -= 1
    def specialMove(self, g:game):
        if g.getRange() == 1 and not self.pushedMatch == 0:
            self.pushMatch(g)
            self.pushedMatch = 1
    def spendEnergy(self, g:game):
        s = g.status
        g.status = state.SPEND_ENERGY
        cost = svr.connectBot(g.nowid, 'int32_t', g)
        if cost < 0 or cost > g.players[g.nowid].identity.energy:
            g.cheating()
        g.status = s
        return cost
    def spendLife(self, g:game):
        s = g.status
        g.status = state.SPEND_ENERGY
        cost = svr.connectBot(g.nowid, 'int32_t', g)
        if cost < 0 or cost > g.players[g.nowid].identity.life:
            g.cheating()
        g.status = s
        return cost
    def recycle_match(self, g:game, atmost):
        count = 0
        for i in range(len(g.players[1-g.nowid].graveyard)):
            if g.players[1-g.nowid].graveyard[i] == 134:
                count += 1
        maxi = min(count, atmost)
        s = g.status
        g.status = state.RECYCLE_MATCH
        cost = svr.connectBot(g.nowid, 'int32_t', g)
        if cost < 0 or cost > maxi:
            g.cheating()
        g.status = s
        idx = []
        for i in range(len(g.players[1-g.nowid].graveyard)):
            if len(idx) == cost:
                break
            if g.players[1-g.nowid].graveyard[i] == 134:
                idx.append(i)
        for i in reversed(idx):
            del g.players[1-g.nowid].graveyard[i]
        self.remindMatch += cost
        return cost