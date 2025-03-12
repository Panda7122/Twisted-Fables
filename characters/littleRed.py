import sys 
sys.path.append("..")
from game import *
from character import *
class littleRedATKSkill(atkCard):
    def skill(self, g:game, level,X=-1,Y=-1):
        if g.getRange()> self.level:
            g.cheating()
        if X == -1 and Y == -1:
            if 135 in g.players[g.nowid].metamorphosis:
                s = g.status
                us = g.nowUsingCardID
                g.nowUsingCardID = 135
                g.status = state.DROP_CARD
                drop = svr.connectBot(g.nowid, "int32_t", g)
                if drop >= len(g.players[g.nowid].hand) or drop < 0:
                    # cheat
                    g.cheating()
                drop -= 1
                g.status = s
                if drop != -1:
                    if g.players[g.nowid].hand[drop] in [20,21,22,1,2,3,4,5,6,7,8,9,10,131,132,133,134]:
                        g.cheating()
                    X = (g.players[g.nowid].hand[drop]-11)%3+1
                    g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[drop])
                    del g.players[g.nowid].hand[drop]
                else:
                    X=0
                g.nowUsingCardID = us
            else:
                X = 0
            if 137 in g.players[g.nowid].metamorphosis:
                s = g.status
                us = g.nowUsingCardID
                g.nowUsingCardID = 137
                g.status = state.DROP_CARD
                drop = svr.connectBot(g.nowid, "int32_t", g)
                if drop > len(g.players[g.nowid].hand) or drop < 0:
                    # cheat
                    g.cheating()
                drop -= 1
                g.status = s
                if drop != -1:
                    if g.players[g.nowid].hand[drop] in [20,21,22,1,2,3,4,5,6,7,8,9,10,131,132,133,134]:
                        g.cheating()
                    Y = (g.players[g.nowid].hand[drop]-11)%3+1
                    g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[drop])
                    del g.players[g.nowid].hand[drop]
                else:
                    Y=0
                g.nowUsingCardID = us
            else:
                Y = 0
        g.damage(1-g.nowid, self.level+Y, self.level+level+X)
        lastAct = lastAction(0 ,0, 0, [1, self.level, X, Y])
class littleRedDEFSkill(defCard):
    def skill(self, g:game, level):
        if g.getRange()> self.level:
            g.cheating()
        g.damage(1-g.nowid, self.level, self.level)
        g.players[g.nowid].defense+=1
        g.players[g.nowid].defense = min(g.players[g.nowid].maxdefense, g.players[g.nowid].defense)
class littleRedMOVSkill(movCard):
    def skill(self, g:game, level, X=-1, Y=-1):
        if g.getRange()> self.level:
            g.cheating()
        if X == -1 and Y == -1:
            if 135 in g.players[g.nowid].metamorphosis:
                s = g.status
                us = g.nowUsingCardID
                g.nowUsingCardID = 135
                g.status = state.DROP_CARD
                drop = svr.connectBot(g.nowid, "int32_t", g)
                if drop > len(g.players[g.nowid].hand) or drop < 0:
                    # cheat
                    g.cheating()
                drop -= 1
                g.status = s
                if drop != -1:
                    if g.players[g.nowid].hand[drop] in [20,21,22,1,2,3,4,5,6,7,8,9,10,131,132,133,134]:
                        g.cheating()
                    X = (g.players[g.nowid].hand[drop]-11)%3+1
                    g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[drop])
                    del g.players[g.nowid].hand[drop]
                else:
                    X=0
                g.nowUsingCardID = us
            else:
                X = 0
            if 137 in g.players[g.nowid].metamorphosis:
                s = g.status
                us = g.nowUsingCardID
                g.nowUsingCardID = 137
                g.status = state.DROP_CARD
                drop = svr.connectBot(g.nowid, "int32_t", g)
                if drop > len(g.players[g.nowid].hand) or drop < 0:
                    # cheat
                    g.cheating()
                drop -= 1
                g.status = s
                if drop != -1:
                    if g.players[g.nowid].hand[drop] in [20,21,22,1,2,3,4,5,6,7,8,9,10,131,132,133,134]:
                        g.cheating()
                    Y = (g.players[g.nowid].hand[drop]-11)%3+1
                    g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[drop])
                    del g.players[g.nowid].hand[drop]
                else:
                    Y=0
                g.nowUsingCardID = us
            else:
                Y = 0
        g.damage(1-g.nowid, self.level+Y, self.level+X)
        g.status = state.KNOCKBACK
        dis = svr.connectBot(g.nowid, 'int32_t', g)
        if dis > self.level or dis < 0:
            g.cheating()
        g.knockback(dis)
        lastAct = lastAction(0 ,0, 0, [3, self.level, X,Y])
class littleRedMETASkill(metaCard):
    def skill(self, g:game, level):
        if self.cardName == '板載緩存':
            ls = []
            for i in range(len(g.players[g.nowid].metamorphosis)):
                if g.players[g.nowid].metamorphosis[i] == 138:
                    ls.append(i)
            idx = 0
            for i in range(len(ls)):
                if ls[i] == level:
                    idx = i
            if g.players[g.nowid].identity.saveCard[idx] == -1:
                us = g.nowUsingCardID
                s = g.status
                g.nowUsingCardID = 138
                g.status = state.DROP_CARD
                ret = svr.connectBot(g.nowid, 'int32_t', g)
                if ret > len(g.players[g.nowid].hand) or ret < 0:
                    # cheat
                    g.cheating()
                g.status = s
                g.nowUsingCardID = us
                ret -= 1
                g.players[g.nowid].identity.saveCard[idx]=g.players[g.nowid].hand[ret]
                del g.players[g.nowid].hand[ret]
                pass
            else:
                g.players[g.nowid].hand.append(g.players[g.nowid].identity.saveCard[idx])
class littleRedUltraSkill(ultraCard):
    def skill(self, g:game, level):
        if self.cardName == "餓狼吞噬":
            for _ in range(2):
                g.nowShowingCards = []
                if len(g.players[g.nowid].attackSkill):
                    g.nowShowingCards.append(g.players[g.nowid].attackSkill[-1])
                if len(g.players[g.nowid].defenseSkill):
                    g.nowShowingCards.append(g.players[g.nowid].defenseSkill[-1])
                if len(g.players[g.nowid].moveSkill):
                    g.nowShowingCards.append(g.players[g.nowid].moveSkill[-1])
                g.status = state.CHOOSECARDS
                c = svr.connectBot(g.nowid, "int32_t", g)
                if c not in g.nowShowingCards:
                    g.cheating()
                if (c-11)%12 in [0,1,2]:
                    if len(g.players[g.nowid].attackSkill) == 0:
                        g.cheating()
                    del g.players[g.nowid].attackSkill[0]
                elif (c-11)%3 in [3,4,5]:
                    if len(g.players[g.nowid].defenseSkill) == 0:
                        g.cheating()
                    del g.players[g.nowid].defenseSkill[0]
                elif (c-11)%3 in [6,7,8]:
                    if len(g.players[g.nowid].moveSkill) == 0:
                        g.cheating()
                    del g.players[g.nowid].moveSkill[0]
                g.players[g.nowid].hand.append(c)
            g.nowShowingCards = []
        elif self.cardName == "系統入侵":
            # TODO 重複你在本回合內剛使用過得一個行動或是一個攻擊技能、移動技能的效果（包含蛻變牌的效果）
            if lastAct.atk != 0:
                g.damage(1-g.nowid, 1, lastAct.atk)
                g.players[g.nowid].identity.energy+=lastAct.atk
            elif lastAct.defense != 0:
                g.players[g.nowid].identity.defense = min(g.players[g.nowid].identity.maxdefense,
                                                          g.players[g.nowid].identity.defense+lastAct.defense)
                g.players[g.nowid].identity.energy+=lastAct.defense
            elif lastAct.mov != 0:
                dir = g.chooseMovingDir()
                through = g.moveCharacter( dir, g.nowMOV)
                if through:
                    if g.players[1-g.nowid].identity.idx == 3 and vectorHave(g.players[1-g.nowid].metamorphosis, [149]):
                        g.drawCard( 1-g.nowid)
                    elif g.players[g.nowid].identity.idx == 3 and vectorHave(g.players[g.nowid].metamorphosis, [149]):
                        g.drawCard( g.nowid)
                    elif g.players[1-g.nowid].identity.idx == 1 and vectorHave(g.players[1-g.nowid].metamorphosis, [141]):
                        g.putPosion( g.nowid)
                    elif g.players[g.nowid].identity.idx == 1 and vectorHave(g.players[1-g.nowid].metamorphosis, [141]):
                        g.putPosion( 1-g.nowid)
                g.players[g.nowid].identity.energy+=lastAct.mov
            elif len(lastAct.useskill) != 0:
                if lastAct.useskill[0][0] == 1:
                    g.players[g.nowid].identity.attackSkill[lastAct.useskill[0][1]].skill(g, lastAct.useskill[0][2], lastAct.useskill[0][3])
                elif lastAct.useskill[0][0] == 3:
                    g.players[g.nowid].identity.moveSkill[lastAct.useskill[0][1]].skill(g, lastAct.useskill[0][2], lastAct.useskill[0][3])
                else:
                    g.cheating()
            else:
                g.cheating()

        elif self.cardName == "復仇之雨":
            g.damage(1-g.nowid, 3, 3)
            g.knockback(3)
            for _ in range(3):
                g.nowid = 1-g.nowid
                g.dropCardFromHand()
                g.nowid = 1-g.nowid
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
        self.saveCard = [-1,-1,-1]
    def __init__(self, saveCard = [-1,-1,-1], **kwargs):
        self.setup()
        self.characterName = "小紅帽"
        self.picture = "沒有圖片"
        self.saveCard = saveCard
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