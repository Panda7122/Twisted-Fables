import sys 
sys.path.append("..")
from game import *
from character import *
class snowWhiteATKSkill(atkCard):
    def skill(self, g:game, level):
        if g.getRange()> 1:
            g.cheating()
        dam = g.damage(1-g.nowid, 1, self.level+level)
        if dam >=2 and vectorHave(g.players[g.nowid].metamorphosis, [139]):
            g.putPosion(1-g.nowid)
        for _ in range(self.level):
            g.dropDeck(1-g.nowid)
class snowWhiteDEFSkill(defCard):
    def skill(self, g:game, level):
        if g.getRange()> 1:
            g.cheating()
        g.damage(1-g.nowid, 1, self.level)
        s = g.status
        g.status = state.PUTTARGETPOSITION
        p = svr.connectBot(g.nowid, 'int32_t', g)
        use = 0
        for _ in range(p):
            if not use:
                s = g.status
                g.status = state.SHUFFLEPOSIONTODECK
                ask = svr.connectBot(g.nowid, 'int8_t', g)
                if ask not in [0,1]:
                    g.cheating()
                g.status = s
                if ask == 1:
                    use = 1
            else :
                ask = 0
            if not ask:
                g.putPosion(1-g.nowid)
            else:
                now = g.players[g.nowid].identity.remindPosion[0]
                del g.players[g.nowid].identity.remindPosion[0]
                g.players[1-g.nowid].deck.append(now)
                random.shuffle(g.players[1-g.nowid].deck)
        g.status = s
class snowWhiteMOVSkill(movCard):
    def skill(self, g:game, level):
        if g.getRange()> level+self.level-1:
            g.cheating()
        g.damage(1-g.nowid, level+self.level-1, self.level)
        g.putTargetPosition()
class snowWhiteMETASkill(metaCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class snowWhiteUltraSkill(ultraCard):
    def skill(self, g:game, level):
        if self.cardName == "七蛇之怒":
            if g.getRange()>1:
                g.cheating()
            count = sum(1 for card in g.players[1-g.nowid].graveyard if card in [131, 132, 133])
            g.lostLife(1-g.nowid, count)
        elif self.cardName =="魔鏡之雨":
            g.damage(1-g.nowid, 1, 3)
            for _ in range(len(g.players[1-g.nowid].hand)):
                id = 0
                g.players[1-g.nowid].graveyard.append(g.players[1-g.nowid].hand[id])
                if g.players[1-g.nowid].hand[id] == 134:
                    eneragy = 1
                    for i in range(len(self.players[self.nowid].metamorphosis)):
                        if self.players[1-self.nowid].metamorphosis[i] in [166,167,168]:
                            eneragy+=1
                    self.players[self.nowid].energy += eneragy
                if g.players[1-g.nowid].hand[id] in [131, 132, 133]:
                    posion = g.players[1-g.nowid].hand[id]-131
                    for i in range(len(self.players[self.nowid].metamorphosis)):
                        if self.players[self.nowid].metamorphosis[i] == 142:
                            posion+=1
                    self.lostLife( self.nowid, posion)    
                del g.players[1-g.nowid].hand[id]
            for _ in range(4):
                g.drawCard(1-g.nowid)
        elif self.cardName =="醞釀之災":
            cnt = 0
            for _ in range(3):
                g.status = state.CHOOSE_CARD_BACK
                id = svr.connectBot(g.nowid, 'int32_t', g)
                if id == 0:
                    break
                id -= 1
                if id<0 or id>= len(g.players[1-g.nowid].graveyard):
                    g.cheating()
                cnt += 1
                g.players[1-g.nowid].deck.append(g.players[1-g.nowid].graveyard[id])
                del g.players[1-g.nowid].graveyard[id]
            if cnt > 0:
                random.shuffle(g.players[1-g.nowid].deck)
class snowWhite(character):
    def idx():
        return 1
    def setup(self):
        self.maxlife = 34
        self.life= self.maxlife
        self.maxdefense = 6
        self.defense = 0 
        self.energy = 0
        self.specialGate = 17
        self.remindPosion = [131+(i//6) for i in range(18)]
    def __init__(self, remindPosion = [131+(i//6) for i in range(18)], **kwargs):
        self.setup()
        self.remindPosion = remindPosion
        self.characterName = "白雪公主"
        self.picture = "沒有圖片"
        atklv1 =  snowWhiteATKSkill("沒有圖片", "", 1)
        atklv2 =  snowWhiteATKSkill("沒有圖片", "", 2)
        atklv3 =  snowWhiteATKSkill("沒有圖片", "", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  snowWhiteDEFSkill("沒有圖片", "", 1)
        deflv2 =  snowWhiteDEFSkill("沒有圖片", "", 2)
        deflv3 =  snowWhiteDEFSkill("沒有圖片", "", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  snowWhiteMOVSkill("沒有圖片", "", 1)
        movlv2 =  snowWhiteMOVSkill("沒有圖片", "", 2)
        movlv3 =  snowWhiteMOVSkill("沒有圖片", "", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  snowWhiteMETASkill("沒有圖片", "", 0)
        meta2 =  snowWhiteMETASkill("沒有圖片", "", 0)
        meta3 =  snowWhiteMETASkill("沒有圖片", "", 0)
        meta4 =  snowWhiteMETASkill("沒有圖片", "", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  snowWhiteUltraSkill("沒有圖片", "", 0)
        ultra2 =  snowWhiteUltraSkill("沒有圖片", "", 0)
        ultra3 =  snowWhiteUltraSkill("沒有圖片", "", 0)
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)
    def specialMove(self, g:game):
        g.cheating()