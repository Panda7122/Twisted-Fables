import sys 
sys.path.append("..")
from game import *
from characters.character import *
class scheherazadeATKSkill(atkCard):
    def skill(self, g:game, level):
        g.damage(1-g.nowid, self.level, self.level+level)
        for i in range(self.level):
            ret = g.players[g.nowid].identity.flipTOKEN(g)
            if ret == 0:
                break
class scheherazadeDEFSkill(defCard):
    def skill(self, g:game, level):
        g.players[g.nowid].identity.defense+=level
        g.players[g.nowid].identity.defense = min(g.players[g.nowid].identity.maxdefense, g.players[g.nowid].identity.defense)
        for _ in range(self.level):
            ret = g.players[g.nowid].identity.moveTOKEN(g)
            if ret == 0:
                break
        
class scheherazadeMOVSkill(movCard):
    def skill(self, g:game, level):
        g.damage(1-g.nowid, self.level, self.level)
        waiting_queue = []
        for _ in range(level):
            card = g.players[1-g.nowid].deck[0]
            del g.players[1-g.nowid].deck[0]
            if card <= 10:
                loc = card
            else:
                loc = -(((card-11)%3)+1)
            if loc in g.players[g.nowid].identity.destiny_TOKEN_locate:
                for i in range(len(g.players[g.nowid].identity.destiny_TOKEN_locate)):
                    if g.players[g.nowid].identity.destiny_TOKEN_locate[i] == loc and g.players[g.nowid].identity.destiny_TOKEN_type[i] == 1:
                        g.players[g.nowid].identity.destiny_TOKEN_type[i] = 2
                        break
            c = g.nowUsingCardID
            g.nowUsingCardID = card
            s = g.status
            g.status = state.KEEP_OR_BACK
            ret = svr.connectBot(g.nowid, 'int8_t', g)
            g.status = s
            g.nowUsingCardID = c
            if ret == 1:
                waiting_queue.append(card)
            else:
                g.players[1-g.nowid].graveyard.append(card)
                if card == 134:
                    eneragy = 1
                    for i in range(len(g.players[1-g.nowid].metamorphosis)):
                        if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                            eneragy+=1
                    g.players[1-g.nowid].identity.energy += eneragy
                if card in [131, 132, 133]:
                    posion = card-131
                    for i in range(len(g.players[1-g.nowid].metamorphosis)):
                        if g.players[1-g.nowid].metamorphosis[i] == 142:
                            posion+=1
                    g.lostLife( g.nowid, posion)
        for c in reversed(waiting_queue):
            g.players[1-g.nowid].deck.append(c)
        pass
class scheherazadeMETASkill(metaCard):
    def skill(self, g:game, level):
        g.cheating()

class scheherazadeUltraSkill(ultraCard):
    def skill(self, g:game, level):
        if self.cardName == '系統刪除':
            s = g.status
            g.status = state.CHOOSE_TOKEN
            idx = svr.connectBot(g.nowid, 'int8_t', g)
            if idx ==-1:
                return 0
            if idx <0 or idx >= len(g.players[g.nowid].identity.destiny_TOKEN_locate):
                g.cheating()
            loc = g.players[g.nowid].identity.destiny_TOKEN_locate[idx]
            X = 0
            for i in range(len(g.players[1-g.nowid].deck)-1, -1, -1):
                if g.players[1-g.nowid].deck[i] <= 10:
                    locateFrom = g.players[1-g.nowid].deck[i]
                elif g.players[1-g.nowid].deck[i] not in [131, 132,133,134]:
                    locateFrom = -((((g.players[1-g.nowid].deck[i]-11)%12) // 3) + 1)
                else:
                    continue
                if locateFrom == loc:
                    g.players[1-g.nowid].graveyard.append(g.players[1-g.nowid].deck[i])
                    del g.players[1-g.nowid].deck[i]
                    X +=1
            g.damage(3, X+3)
            random.shuffle(g.players[1-g.nowid].deck)
        elif self.cardName == '無法自拔':
            s = g.status
            g.status = state.CHOOSE_TOKEN
            idx = svr.connectBot(g.nowid, 'int8_t', g)
            if idx ==-1:
                return 0
            if idx <0 or idx >= len(g.players[g.nowid].identity.destiny_TOKEN_locate):
                g.cheating()
            loc = g.players[g.nowid].identity.destiny_TOKEN_locate[idx]
            X = 0
            for i in range(len(g.players[1-g.nowid].graveyard)-1, -1, -1):
                if g.players[1-g.nowid].graveyard[i] <= 10:
                    locateFrom = g.players[1-g.nowid].graveyard[i]
                elif g.players[1-g.nowid].graveyard[i] not in [131, 132,133,134]:
                    locateFrom = -((((g.players[1-g.nowid].graveyard[i]-11)%12) // 3) + 1)
                else:
                    continue
                if locateFrom == loc:
                    if g.players[g.nowid].identity.destiny_TOKEN_type[i] == 2:
                        X += 2
                    else:
                        X += 1
            g.damage(1 - g.nowid, 3, 3 + X)
        elif self.cardName == '切斷通路':
            X = 0
            for _ in range(3):
                loc = g.players[g.nowid].identity.flipTOKEN(g)
                if loc != -1:
                    X += 1
            g.damage(1-g.nowid, 3, X)
class scheherazade(character):
    @property
    def idx(self):
        return 9
    def setup(self):
        self.maxlife = 36
        self.life= self.maxlife
        self.maxdefense = 6
        self.defense = 0
        self.energy = 0
        self.specialGate = 18
        self.destiny_TOKEN_locate = []
        self.destiny_TOKEN_type = []
        self.selectToken = 0
    def __init__(self, destiny_TOKEN_locate=[],destiny_TOKEN_type=[], selectToken = 0, **kwargs):
        super().__init__()
        self.setup()
        self.destiny_TOKEN_locate = destiny_TOKEN_locate
        self.destiny_TOKEN_type = destiny_TOKEN_type
        self.selectToken = selectToken
        self.characterName = "山魯佐德"
        self.picture = "./picture/character/scheherazade/character.png"
        atklv1 =  scheherazadeATKSkill("沒有圖片", "消除夢境", 1)
        atklv2 =  scheherazadeATKSkill("沒有圖片", "銷毀記憶", 2)
        atklv3 =  scheherazadeATKSkill("沒有圖片", "扼殺存在", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  scheherazadeDEFSkill("沒有圖片", "浸沒之網", 1)
        deflv2 =  scheherazadeDEFSkill("沒有圖片", "沈迷之網", 2)
        deflv3 =  scheherazadeDEFSkill("沒有圖片", "消融之網", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  scheherazadeMOVSkill("沒有圖片", "監視之眼", 1)
        movlv2 =  scheherazadeMOVSkill("沒有圖片", "操縱之手", 2)
        movlv3 =  scheherazadeMOVSkill("沒有圖片", "支配之腦", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  scheherazadeMETASkill("沒有圖片", "命運之手")
        meta2 =  scheherazadeMETASkill("沒有圖片", "改寫欲望")
        meta3 =  scheherazadeMETASkill("沒有圖片", "重組思想")
        meta4 =  scheherazadeMETASkill("沒有圖片", "童話編織者")
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  scheherazadeUltraSkill("沒有圖片", "系統刪除")
        ultra2 =  scheherazadeUltraSkill("沒有圖片", "無法自拔")
        ultra3 =  scheherazadeUltraSkill("沒有圖片", "切斷通路")
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)
    def triggerDestiny(self, g:game, cardType):
        for i in range(len(self.destiny_TOKEN_locate)):
            if self.destiny_TOKEN_locate[i] == cardType:
                if self.destiny_TOKEN_type[i] == 2:
                    self.destiny_TOKEN_type[i] = 1
                    return
    def flipTOKEN(self, g:game):
        s = g.status
        g.status = state.FLIP_TOKEN_TO_RED
        loc = svr.connectBot(g.nowid, 'int8_t', g)
        if loc !=-1:
            # return 0
            if loc <0 or loc >= len(g.players[g.nowid].identity.destiny_TOKEN_locate):
                g.cheating()
            g.players[g.nowid].identity.destiny_TOKEN_type[loc] = 2
        g.status = s
        return loc
    def moveTOKEN(self, g:game):
        s = g.status
        g.status = state.CHOOSE_TOKEN
        idx = svr.connectBot(g.nowid, 'int8_t', g)
        if idx ==-1:
            return 0
        if idx <0 or idx >= len(self.destiny_TOKEN_locate):
            g.cheating()
        self.selectToken = idx
        g.status = state.TOKEN_GOAL
        loc = svr.connectBot(g.nowid, 'int8_t', g)
        if loc not in [-1,-2,-3,1,2,3,4,5,6,7,8,9,10]:
            g.cheating()
        self.destiny_TOKEN_locate[idx] = loc
        g.status = s
        return 1