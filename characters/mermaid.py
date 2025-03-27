import sys 
sys.path.append("..")
from game import *
from character import *
class mermaidATKSkill(atkCard):
    def skill(self, g:game, level):
        dam =self.level+level
        if g.players[1-g.nowid].locate in g.tentacle_TOKEN_locate:
            dam +=self.level
        if g.players[g.nowid].locate in g.tentacle_TOKEN_locate:
            g.players[g.nowid].identity.energy+= 2
        g.damage(1-g.nowid, self.level, self.level+level, dam)
class mermaidDEFSkill(defCard):
    def skill(self, g:game, level):
        if g.players[1-g.nowid].locate in g.tentacle_TOKEN_locate:
            g.damage(1-g.nowid, 11, self.level+level, level)
        s = g.status
        g.status = state.MOVE_TO_TANTACLE
        loc = svr.connectBot(g.nowid, 'int32_t', g)
        if loc not in g.tentacle_TOKEN_locate+[g.players[g.nowid].locate]:
            g.cheating()
        g.players[g.nowid].locate = loc
        g.players[g.nowid].identity.defense += self.level
        g.players[g.nowid].identity.defense = min(g.players[g.nowid].identity.defense, g.players[g.nowid].identity.maxdefense)
        g.status = s            
        pass
class mermaidMOVSkill(movCard):
    def skill(self, g:game, level):
        g.players[g.nowid].identity.moveTantacle(g, level, 1)
        if g.players[g.nowid].locate in g.tentacle_TOKEN_locate:
            for _ in range(self.level):
                g.drawCard(g.nowid)
        if self.level>1 and g.players[1-g.nowid].locate in g.tentacle_TOKEN_locate:
            g.nowid = 1-g.nowid
            id = g.dropCardFromHand()
            g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[id])
            if g.players[g.nowid].hand[id] == 134:
                eneragy = 1
                for i in range(len(g.players[1-g.nowid].metamorphosis)):
                    if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                        eneragy+=1
                g.players[1-g.nowid].energy += eneragy
            if g.players[g.nowid].hand[id] in [131, 132, 133]:
                posion = g.players[g.nowid].hand[id]-131
                for i in range(len(g.players[1-g.nowid].metamorphosis)):
                    if g.players[1-g.nowid].metamorphosis[i] == 142:
                        posion+=1
                g.lostLife( g.nowid, posion)    
            del g.players[g.nowid].hand[id]
            g.nowid = 1-g.nowid
class mermaidMETASkill(metaCard):
    def skill(self, g:game, level):
        g.cheating()

class mermaidUltraSkill(ultraCard):
    def skill(self, g:game, level):
        g.cheating()

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
        atklv1 =  mermaidATKSkill("沒有圖片", "海妖的召喚", 1)
        atklv2 =  mermaidATKSkill("沒有圖片", "海妖的歌聲", 2)
        atklv3 =  mermaidATKSkill("沒有圖片", "海妖的尖嘯", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  mermaidDEFSkill("沒有圖片", "洶湧之怒", 1)
        deflv2 =  mermaidDEFSkill("沒有圖片", "噴薄之怒", 2)
        deflv3 =  mermaidDEFSkill("沒有圖片", "復仇之怒", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  mermaidMOVSkill("沒有圖片", "深淵的蠶食", 1)
        movlv2 =  mermaidMOVSkill("沒有圖片", "深淵的入侵", 2)
        movlv3 =  mermaidMOVSkill("沒有圖片", "深淵的征服", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  mermaidMETASkill("沒有圖片", "暴風之蝕", 0)
        meta2 =  mermaidMETASkill("沒有圖片", "神秘共鳴", 0)
        meta3 =  mermaidMETASkill("沒有圖片", "海的女兒", 0)
        meta4 =  mermaidMETASkill("沒有圖片", "暗潮湧動", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  mermaidUltraSkill("沒有圖片", "人魚復興", 0)
        ultra2 =  mermaidUltraSkill("沒有圖片", "遠古甦醒", 0)
        ultra3 =  mermaidUltraSkill("沒有圖片", "淨化之潮", 0)
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)
    def specialMove(self, g:game):
        s = g.status
        g.status = state.DROPCARD_MOVE_TANTACLE
        cid = svr.connectBot(g.nowid, 'int32_t', g)
        if cid<1 or cid > len(g.players[g.nowid].hand):
            g.cheating()
        cid -= 1
        if g.players[g.nowid].hand[cid] not in [7,8,9,10]:
            g.cheating()
        lv = g.players[g.nowid].hand[cid] - 6 if g.players[g.nowid].hand[cid] != 10 else 1
        self.moveTantacle(g, lv, 0)
        g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[cid])
        del g.players[g.nowid].hand[cid]
        g.status = s
    def moveTantacle(self, g:game, maxDis, minDis = 0):
        s = g.status
        g.status = state.CHOOSE_TANTACLE
        t = svr.connectBot(g.nowid, 'int32_t', g)
        if t >= len(g.tentacle_TOKEN_locate) or t < 0:
            g.cheating()
        
        g.status = state.MOVE_TANTACLE
        mov = svr.connectBot(g.nowid, 'int32_t', g)
        if abs(mov-g.tentacle_TOKEN_locate[t]) > maxDis or abs(mov-g.tentacle_TOKEN_locate[t]) < minDis:
            g.cheating()
        if mov > 9 or mov < 1:
            g.cheating()
        g.tentacle_TOKEN_locate[t] = mov
        if 94 in g.players[1-g.nowid].metamorphosis and g.tentacle_TOKEN_locate[t] == g.players[1-g.nowid].locate:
            g.lostLife(1-g.nowid, 1)
        g.status = s