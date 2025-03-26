from __future__ import annotations
import cstruct
import dataclasses
import socket
import copy
import random
import enum
from ctype import *
from characters.character import *
BASIC_PRIZE = [[1,3,6],[1,3,6],[1,3,6],[2]]
SKILL_PRIZE = [[0,2,4],[0,2,4],[0,2,4]]

@dataclasses.dataclass
class lastAction:
    atk:int = 0
    defense:int = 0
    mov:int = 0
    useskill:list[tuple[int]] = []
lastAct:lastAction

@dataclasses.dataclass
class player:
    team:int
    identity:character
    locate:int
    hand:list[int]
    deck:list[int]
    usecards:list[int]
    graveyard:list[int]
    metamorphosis:list[int]
    attackSkill:list[int]
    defenseSkill:list[int]
    moveSkill:list[int]
    ULTDeck:list[int]
    def to_Cplayer(self)->Cplayer:
        ret = Cplayer(team = self.team,
                locate = [0, self.locate],
                character=self.identity.idx,
                maxlife=self.identity.maxlife,
                life=self.identity.life,
                maxdefense=self.identity.maxdefense,
                defense=self.identity.defense,
                energy = self.identity.energy,
                specialGate= self.identity.specialGate,
                hand = vector.from_list(self.hand),
                deck = vector.from_list(self.deck),
                usecards = vector.from_list(self.usecards),
                graveyard = vector.from_list(self.graveyard),
                metamorphosis = vector.from_list(self.metamorphosis),
                attackSkill = vector.from_list(self.attackSkill),
                defenseSkill = vector.from_list(self.defenseSkill),
                moveSkill = vector.from_list(self.moveSkill),
                specialDeck = vector.from_list(self.ULTDeck),
                )
        if self.identity.idx == 0:
            ret.redHood.saveCard = vector.from_list(self.identity.saveCard)
            pass
        elif self.identity.idx == 1:
            ret.snowWhite.remindPosion = vector.from_list(self.identity.remindPosion)
        elif self.identity.idx == 2:
            ret.sleepingBeauty.AWAKEN_TOKEN = self.identity.AWAKEN_TOKEN
            ret.sleepingBeauty.AWAKEN = self.identity.AWAKEN
            ret.sleepingBeauty.dayNightmareDrawRemind = self.identity.dayNightmareDrawRemind
            ret.sleepingBeauty.usedmeta1 = self.identity.usedmeta1
            ret.sleepingBeauty.usedmeta2 = self.identity.usedmeta2
        elif self.identity.idx == 3:
            ret.alice.identity = self.identity.identity
        elif self.identity.idx == 4:
            ret.mulan.KI_TOKEN = self.identity.KI_TOKEN
            ret.mulan.extraCard = self.identity.extraCard
        elif self.identity.idx == 5:
            pass
        elif self.identity.idx == 6:
            pass
        elif self.identity.idx == 7:
            ret.matchGirl.remindMatch = self.identity.remindMatch
        elif self.identity.idx == 8:
            ret.dorothy.COMBO_TOKEN = self.identity.COMBO_TOKEN
            ret.dorothy.canCombo = self.identity.canCombo
        elif self.identity.idx == 9:
            pass
    @classmethod
    def from_Cplayer(cls, p:Cplayer):
        char :character = character.getClass(p.character)(**{
                    "saveCard" : p.snowWhite.saveCard.to_list(),
                    "remindPosion" : p.snowWhite.remindPosion.to_list(),
                    "AWAKEN_TOKEN" : p.sleepingBeauty.AWAKEN_TOKEN,
                    "AWAKEN" : p.sleepingBeauty.AWAKEN,
                    "atkRise":p.sleepingBeauty.atkRise,
                    "atkRiseTime":p.sleepingBeauty.atkRiseTime,
                    "usedmeta1":p.sleepingBeauty.usedmeta1,
                    "usedmeta2":p.sleepingBeauty.usedmeta2,
                    "dayNightmareDrawRemind" : p.sleepingBeauty.dayNightmareDrawRemind,
                    "identity":p.alice.identity,
                    "KI_TOKEN":p.mulan.KI_TOKEN,
                    "extraCard":p.mulan.extraCard,
                    "remindMatch":p.matchGirl.remindMatch,
                    "COMBO_TOKEN":p.dorothy.COMBO_TOKEN,
                    "canCombo":p.dorothy.canCombo,
                    "destiny_TOKEN_locate":p.scheherazade.destiny_TOKEN_locate.to_list(),
                    "destiny_TOKEN_type":p.scheherazade.destiny_TOKEN_type.to_list()
                })
        char.maxlife = p.maxlife
        char.life= p.life
        char.maxdefense = p.maxdefense
        char.defense = p.defense
        char.energy = p.energy
        char.specialGate = p.specialGate
        return cls(
            team = p.team,
            identity = char,
            locate = p.locate[1],
            hand = p.hand.to_list(),
            deck = p.deck.to_list(),
            usecards = p.usecards.to_list(),
            graveyard = p.graveyard.to_list(),
            metamorphosis = p.metamorphosis.to_list(),
            attackSkill = p.attackSkill.to_list(),
            defenseSkill = p.defenseSkill.to_list(),
            moveSkill = p.moveSkill.to_list(),
            ULTDeck = p.specialDeck.to_list()
        )
    def buyATKCard(self, g:game):
        if len(self.attackSkill.cards) == 0:
            g.cheating()
        if self.attackSkill.cards[0] >=135:
            g.cheating()
        lv = (self.attackSkill.cards[0]-10-1)%3+1
        cost = 2*lv
        if self.identity.energy < cost:
            g.cheating()
        self.identity.energy -= cost
        self.graveyard.append(self.attackSkill.cards[0])
        del self.attackSkill.cards[0]
        if self.attackSkill.cards[0] >=135:
            if self.attackSkill.cards[0] in [146,162,176]:
                if self.attackSkill.cards[0] == 146:
                    self.identity.life += 5
                    self.identity.life = min(self.identity.maxlife, self.identity.life)
                elif self.attackSkill.cards[0] == 146: # TODO 暗潮湧動
                    pass
                else: # TODO 童話編織者
                    pass
            else:
                self.metamorphosis.append(self.attackSkill.cards[0])
            del self.attackSkill.cards[0]
            
    def buyDEFCard(self, g:game):
        if len(self.defenseSkill.cards) == 0:
            g.cheating()
        if self.defenseSkill.cards[0] >=135:
            g.cheating()
        lv = (self.defenseSkill.cards[0]-10-1)%3+1
        cost = 2*lv
        if self.identity.energy < cost:
            g.cheating()
        self.identity.energy -= cost
        self.graveyard.append(self.defenseSkill.cards[0])
        del self.defenseSkill.cards[0]
        if self.defenseSkill.cards[0] >=135:
            if self.defenseSkill.cards[0] in [146,162,176]:
                if self.defenseSkill.cards[0] == 146:
                    self.identity.life += 5
                    self.identity.life = min(self.identity.maxlife, self.identity.life)
                elif self.defenseSkill.cards[0] == 146: # TODO 暗潮湧動
                    pass
                else: # TODO 童話編織者
                    pass
            else:
                self.metamorphosis.append(self.defenseSkill.cards[0])
            del self.defenseSkill.cards[0]
    def buyMOVCard(self, g:game):
        if len(self.moveSkill.cards) == 0:
            g.cheating()
        if self.moveSkill.cards[0] >=135:
            g.cheating()
        lv = (self.moveSkill.cards[0]-10-1)%3+1
        cost = 2*lv
        if self.identity.energy < cost:
            g.cheating()
        self.identity.energy -= cost
        self.graveyard.append(self.moveSkill.cards[0])
        del self.moveSkill.cards[0]
        if self.moveSkill.cards[0] >=135:
            if self.moveSkill.cards[0] in [146,162,176]:
                if self.moveSkill.cards[0] == 146:
                    self.identity.life += 5
                    self.identity.life = min(self.identity.maxlife, self.identity.life)
                elif self.moveSkill.cards[0] == 146: # TODO 暗潮湧動
                    pass
                else: # TODO 童話編織者
                    pass
            else:
                self.metamorphosis.append(self.moveSkill.cards[0])
            del self.moveSkill.cards[0]
class state(enum.IntEnum):
    pass # TODO states
class game:
    players:list[player]
    nowid:int
    playerMode:int
    relicMode:int
    tentacle_TOKEN_locate:list[int]
    relic:list[int]
    relicDeck:list[int]
    relicGraveyard:list[int]
    basicBuyDeck:list[list[int]]
    status:state
    nowATK:int
    nowDEF:int
    nowMOV:int
    nowUsingCardID:int
    nowShowingCards:list[int]
    totalDamage:int
    def to_Cgame(self)->Cgame:
        return Cgame(
            players = list(map(player.to_Cplayer, self.players)),
            now_turn_player_id = self.nowid,
            playerMode = self.playerMode,
            relicMode = self.relicMode,
            tentacle_TOKEN_locate = vector.from_list(self.tentacle_TOKEN_locate),
            relic = self.relic,
            relicDeck = vector.from_list(self.relicDeck),
            relicGraveyard = vector.from_list(self.relicGraveyard),
            basicBuyDeck = list(map(vector.from_list, [x for xs in self.basicBuyDeck for x in xs])),
            status = self.status,
            nowATK = self.nowATK,
            nowDEF = self.nowDEF,
            nowMOV = self.nowMOV,
            nowUsingCardID = self.nowUsingCardID,
            nowShowingCards =vector.from_list(self.nowShowingCards),
            totalDamage = self.totalDamage
        )
    @classmethod
    def from_Cgame(cls, cg:Cgame):
        ls = list(map(vector.from_list, cg.basicBuyDeck))
        bbd = [[] for _ in range(4)]
        for i in range(4):
            for j in range(3):
                bbd[i].append(ls[i*4+j])
        return cls(
            player = list(map(player.from_Cplayer, cg.players)),
            nowid = cg.now_turn_player_id,
            playerMode = cg.playerMode,
            relicMode = cg.relicMode,
            tentacle_TOKEN_locate = cg.tentacle_TOKEN_locate.to_list(),
            relic = cg.relic,
            relicDeck = cg.relicDeck.to_list(),
            relicGraveyard = cg.relicGraveyard.to_list(),
            basicBuyDeck = bbd,
            status = cg.status,
            nowATK = cg.nowATK,
            nowDEF = cg.nowDEF,
            nowMOV = cg.nowMOV,
            nowUsingCardID = cg.nowUsingCardID,
            nowShowingCards = cg.nowShowingCards.to_list(),
            totalDamage = cg.totalDamage
        )
    def lose(self):
        for p in range(2):
            if self.players[p].identity.life <= 0:
                print(f"Game over. player {2-p} WIN.")
                svr.close()
                exit()
    def cheating(self):
        self.players[self.nowid].identity.life = 0
        self.lose()
    def hideGameStatus(self):
        retg = copy.deepcopy(self)
        for i in range(len(retg.players[0].deck)):
            retg.players[0].deck[i] = -1
        for i in range(len(retg.players[1].deck)):
            retg.players[1].deck[i] = -1
        for i in range(len(retg.players[1-self.nowid].hand)):
            retg.players[0].hand[i] = -1
        return retg
    def getRange(self):
        return abs(self.players[0].locate- self.players[1].locate)
    def countDestinyTOKEN(self):
        if self.players[0].identity.idx == 9:
            return len(self.players[0].identity.destiny_TOKEN_locate)
        elif self.players[1].identity.idx == 9:
            return len(self.players[1].identity.destiny_TOKEN_locate)
    def drawCard(self, target):
        if len(self.players[target].deck) == 0:
            for i in range(len(self.players[target].graveyard)):
                self.players[target].deck.append(self.players[target].graveyard[i])
            for i in range(len(self.players[target].graveyard)):
                del self.players[target].graveyard[i]
            random.shuffle(self.players[target].deck)
        top = self.players[target].deck[0]
        del self.players[target].deck[0]
        self.players[target].hand.append(top)
    def getlastcard(self):
        return self.players[self.nowid].usecards[len( self.players[self.nowid].usecards)-2]
    def lostLife(self, target:int, atk:int):
        for i in range(len(self.players[target].usecards)):
            if self.players[target].usecards[i] == 80:
                return
        if self.players[target].life<=atk:
            self.players[target].life = 0
            # target lose
            self.lose()
            pass
        self.players[target].life -= atk
    def getDamage(self,target:int,  dam:int):
        #TODO done get Damage
        c = self.players[target].identity.idx
        if c == 0: # 小紅帽
           pass
        elif c == 1: # 白雪公主
            pass
        elif c == 2: # 睡美人
            if self.players[target].identity.AWAKEN == 0:
                self.players[target].identity.AWAKEN_TOKEN = \
                    max(self.players[target].identity.AWAKEN_TOKEN,
                        min(6,self.players[target].identity.AWAKEN_TOKEN+dam))
                if self.players[target].identity.AWAKEN_TOKEN == 6:
                    self.players[target].identity.AWAKEN = 1
            pass
        elif c == 3: # 愛麗絲
            pass
        elif c == 4: # 花木蘭
            pass
        elif c == 5: # 輝夜姬
            pass
        elif c == 6: # 美人魚
            pass
        elif c == 7: # 火柴女孩
            pass
        elif c == 8: # 桃樂絲
            pass
        elif c == 9: # 山魯佐德
            pass
        
        if target == 0: # 小紅帽
            pass
        elif target == 1: # 白雪公主
            pass
        elif target == 2: # 睡美人
            for i in range(len(self.players[1-self.nowid].usecards)):
                if self.players[1-self.nowid].usecards[i] == 45:
                    for _ in range(min(self.players[1-self.nowid].identity.dayNightmareDrawRemind, dam)):
                        self.drawCard(target)
                    self.players[1-self.nowid].identity.dayNightmareDrawRemind-=min(self.players[1-self.nowid].identity.dayNightmareDrawRemind, dam)
            pass
        elif target == 3: # 愛麗絲
            pass
        elif target == 4: # 花木蘭
            pass
        elif target == 5: # 輝夜姬
            self.nowid = 1-self.nowid
            use = self.players[target].identity.useSpecialMove(self)
            if use == 1:
                card = self.players[target].identity.specialMove(self)
                if self.players[target].hand[card] not in [1,2,3,10]:
                    self.cheating()
                if self.players[target].hand[card] == 10:
                    lv = 1
                else :
                    lv = self.players[target].hand[card]
                self.players[target].graveyard.append(self.players[target].hand[card])
                del self.players[target].hand[card]
                self.damage(1-target, 11, lv)
                self.drawCard(target)
            self.nowid = 1-self.nowid
        elif target == 6: # 美人魚
            pass
        elif target == 7: # 火柴女孩
            pass
        elif target == 8: # 桃樂絲
            pass
        elif target == 9: # 山魯佐德
            pass
    def damage(self, target:int,  distanse:int, atk:int):
        for i in range(len(self.players[target].usecards)):
            if self.players[target].usecards[i] == 80:
                return
        if(self.getRange()<=distanse):
            dam = atk - self.players[target].defense
            if self.players[target].identity.idx == 0: # little red
                self.nowid = 1-self.nowid
                X = 0
                if 136 in self.players[target].metamorphosis:
                    s = self.status
                    us = self.nowUsingCardID
                    self.nowUsingCardID = 135
                    self.status = state.DROP_CARD
                    drop = svr.connectBot(self.nowid, "int32_t", self)
                    if drop > len(self.players[self.nowid].hand) or drop < 0:
                        # cheat
                        self.cheating()
                    drop -= 1
                    self.status = s
                    if drop != -1:
                        if self.players[self.nowid].hand[drop] in [20,21,22,1,2,3,4,5,6,7,8,9,10,131,132,133,134]:
                            self.cheating()
                        X = (self.players[self.nowid].hand[drop]-11)%3+1
                        self.players[self.nowid].graveyard.append(self.players[self.nowid].hand[drop])
                        del self.players[self.nowid].hand[drop]
                    else:
                        X=0
                    self.nowUsingCardID = us
                dam -= X
                self.nowid = 1-self.nowid
                
            if self.players[target].identity.idx == 4: # KI
                self.nowid = 1-self.nowid
                use = self.players[target].identity.askUseKI(self)
                if use == 1:
                    card = self.players[target].identity.useKI(self)
                    if self.players[target].hand[card] not in [4,5,6,10]:
                        self.cheating()
                    if self.players[target].hand[card] == 10:
                        lv = 1
                    else :
                        lv = self.players[target].hand[card]-3
                    dam -= lv
                    self.players[target].graveyard.append(self.players[target].hand[card])
                    del self.players[target].hand[card]
                self.nowid = 1-self.nowid
            
            if dam <= 0:
                self.players[target].identity.defense -= atk
            else:
                self.players[target].identity.defense = 0
                if self.players[target].identity.life < dam:
                    self.players[target].identity.life = 0
                    # target lose
                    self.lose()
                self.players[target].identity.life -= dam
                self.totalDamage += dam
                if self.players[self.nowid].identity.idx == 2 and 144 in self.players[self.nowid].metamorphosis and self.players[self.nowid].identity.usedmeta2 == 0:
                    s = self.status
                    self.status = state.RECYCLE_CARD
                    ret = svr.connectBot(self.nowid, 'int32_t', self)
                    if ret != 0:
                        ret -=1
                        if ret >= len(self.players[self.nowid].graveyard) or ret < 0:
                            self.cheating()
                        card = self.players[self.nowid].graveyard[ret]
                        del self.players[self.nowid].graveyard[ret]
                        self.players[self.nowid].hand.append(card)
                        self.players[self.nowid].identity.usedmeta2 = 1
                    self.status = s                    
                self.getDamage(target, dam)
                if self.players[self.nowid].usecards[-1] in [1,2,3] and dam>2 and self.players[self.nowid].identity.idx == 1:
                    self.putPosion(target)
        else:
            self.cheating()
        return dam
    def setLocate(self, target:int, locate:int):
        if locate > 9 or locate < 1:
            # cheat
            self.cheating()                    
        self.players[target].locate[1] = locate
    def chooseMove(self):
        s = self.status
        self.status = state.CHOOSE_MOVE
        ret = svr.connectBot(self.nowid, "int32_t", self)
        self.status = s
        return ret
    def chooseCardFromHandorGraveyard(self):
        s = self.status
        self.status = state.REMOVE_HG
        ret = svr.connectBot(self.nowid, "int32_t", self)
        if ret == 0:
            # cheat
            self.cheating()
        sign = 1 if ret > 0 else 0
        ret = abs(ret)-1
        if sign:
            if ret >= len(self.players[self.nowid].hand):
                # cheat
                self.cheating()
        else:
            if ret >= len(self.players[self.nowid].graveyard):
                # cheat
                self.cheating()
        self.status = s
        return (sign, ret)
    def dropCardFromHand(self):
        s = self.status
        self.status = state.DROP_H
        ret = svr.connectBot(self.nowid, "int32_t", self)
        if ret >= len(self.players[self.nowid].hand) or ret <= 0:
            # cheat
            self.cheating()
        ret -= 1
        self.status = s
        return ret
    def knockback(self, dis:int):
        aloc = self.players[self.nowid].locate[1]
        bloc = self.players[1-self.nowid].locate[1]
        if bloc-aloc > 0:
            self.players[1-self.nowid].locate[1] = min(9, self.players[1-self.nowid].locate[1]+dis)
        elif bloc-aloc < 0:
            self.players[1-self.nowid].locate[1] = max(1, self.players[1-self.nowid].locate[1]-dis)
        else:
            self.cheating()
        return
    def dropDeck(self, target:int):
        if len(self.players[target].deck) == 0:
            for i in range(len(self.players[target].graveyard)):
                self.players[target].deck.append(self.players[target].graveyard[i])
            for i in range(len(self.players[target].graveyard)):
                del self.players[target].graveyard[i]
            random.shuffle(self.players[target].deck)
        top = self.players[target].deck[0]
        del self.players[target].deck[0]
        self.players[target].graveyard.append(top)
        if top == 134:
            eneragy = 1
            for i in range(len(self.players[1-self.nowid].metamorphosis)):
                if self.players[1-self.nowid].metamorphosis[i] in [166,167,168]:
                    eneragy+=1
            self.players[1-self.nowid].energy += eneragy
        if top in [131, 132, 133]:
            posion = top-131
            for i in range(len(self.players[1-self.nowid].metamorphosis)):
                if self.players[1-self.nowid].metamorphosis[i] == 142:
                    posion+=1
            self.lostLife( self.nowid, posion)
    def USEPOSION(self, g):
        s = self.status
        self.status = state.USE_POSION
        c = svr.connectBot(self.nowid, "int32_t", g)
        if c >= len(self.players[self.nowid].hand) or c < 0 or self.players[self.nowid].hand[c] not in [131,132,133]:
            self.cheating()
        self.players[self.nowid].identity.energy+=1
        p =  self.players[self.nowid].hand[c]-131
        for m in self.players[1-self.nowid].metamorphosis:
            if m == 142:
                p+=1
        self.lostLife(self.nowid, p)
        self.players[self.nowid].graveyard.append(self.players[self.nowid].hand[c])
        del self.players[self.nowid].hand[c]
    def USEATKBASIC(self):
        s = self.status
        self.status = state.USE_ATK
        self.nowATK = 0
        basicATK = [1,2,3, 10]
        if self.players[1-self.nowid].identity.idx == 7 and not vectorHave(self.players[1-self.nowid].metamorphosis, [166]):
            basicATK.append(134)
        while True:
            if self.players[self.nowid].identity.idx == 2 and 143 in  self.players[self.nowid].metamorphosis and self.players[self.nowid].usedmeta1 == 0:
                s = self.status
                self.status = state.LOST_LIFE_FOR_USESKILL
                ret = svr.connectBot(self.nowid, 'int8_t', game)
                self.status = s
                if ret == 0:
                    c = svr.connectBot(self.nowid, "int32_t", self)
                    if c >= len(self.players[self.nowid].hand) or c < 0 or self.players[self.nowid].hand[c] not in basicATK:
                        # cheat
                        self.cheating()
                    if c == 0:
                        break
                    self.players[self.nowid].usecards.append(self.players[self.nowid].hand[c])
                    self.nowATK += self.players[self.nowid].hand[c] if self.players[self.nowid].hand[c] not in [134, 10] else 1
                    if self.players[self.nowid].identity.idx == 3 and self.players[self.nowid].identity.identity == 1:
                        self.nowATK += 1
                        
                    if self.players[self.nowid].identity.idx == 3 and self.players[self.nowid].identity.identity == 2:
                        self.nowATK -= 1
                    if self.players[self.nowid].hand[c] !=134:
                        self.players[self.nowid].identity.energy+=self.players[self.nowid].hand[c] if self.players[self.nowid].hand[c] not in [10] else 1
                    del self.players[self.nowid].hand[c]
                elif ret in [2,4,6]:
                    self.lostLife(self.nowid, ret)
                    level = ret//2
                    self.nowATK += level
                    self.players[self.nowid].usedmeta1 = 1
                else:
                    self.cheating()
            
            
        self.status = s
    def USEDEFBASIC(self):
        s = self.status
        self.status = state.USE_DEF
        self.nowDEF = 0
        basicDEF = [4,5,6, 10]
        if self.players[1-self.nowid].identity.idx == 7 and not vectorHave(self.players[1-self.nowid].metamorphosis, [167]):
            basicDEF.append(134)
        while True:
            if self.players[self.nowid].identity.idx == 2 and 143 in  self.players[self.nowid].metamorphosis and self.players[self.nowid].usedmeta1 == 0:
                s = self.status
                self.status = state.LOST_LIFE_FOR_USESKILL
                ret = svr.connectBot(self.nowid, 'int8_t', game)
                self.status = s
                if ret == 0:
                    c = svr.connectBot(self.nowid, "int32_t", self)
                    if c >= len(self.players[self.nowid].hand) or c < 0 or self.players[self.nowid].hand[c] not in basicDEF:
                        # cheat
                        self.cheating()
                    if c == 0:
                        break
                    self.players[self.nowid].usecards.append(self.players[self.nowid].hand[c])
                    if not (self.players[self.nowid].identity.idx == 2 and self.players[self.nowid].AWAKEN == 1):
                        self.nowDEF += (self.players[self.nowid].hand[c] - 3) if self.players[self.nowid].hand[c] not in [134, 10] else 1
                    if self.players[self.nowid].identity.idx == 3 and self.players[self.nowid].identity.identity == 2:
                        self.nowDEF += 1
                    if self.players[self.nowid].identity.idx == 3 and self.players[self.nowid].identity.identity == 3:
                        self.nowDEF -= 1
                    if self.players[self.nowid].hand[c] !=134:
                        self.players[self.nowid].identity.energy+=(self.players[self.nowid].hand[c] - 3) if self.players[self.nowid].hand[c] not in [10] else 1
                    del self.players[self.nowid].hand[c]
                elif ret in [2,4,6]:
                    self.lostLife(self.nowid, ret)
                    level = ret//2
                    self.nowDEF += level
                    self.players[self.nowid].usedmeta1 = 1
                else:
                    self.cheating()
            
        self.status = s
    def USEMOVBASIC(self):
        s = self.status
        self.status = state.USE_MOV
        self.nowMOV = 0
        basicMOV = [7,8,9, 10]
        if self.players[1-self.nowid].identity.idx == 7 and not vectorHave(self.players[1-self.nowid].metamorphosis, [168]):
            basicMOV.append(134)
        while True:
            if self.players[self.nowid].identity.idx == 2 and 143 in  self.players[self.nowid].metamorphosis and self.players[self.nowid].usedmeta1 == 0:
                s = self.status
                self.status = state.LOST_LIFE_FOR_USESKILL
                ret = svr.connectBot(self.nowid, 'int8_t', game)
                self.status = s
                if ret == 0:
                    c = svr.connectBot(self.nowid, "int32_t", self)
                    if c >= len(self.players[self.nowid].hand) or c < 0 or self.players[self.nowid].hand[c] not in basicMOV:
                        # cheat
                        self.cheating()
                    if c == 0:
                        break
                    self.players[self.nowid].usecards.append(self.players[self.nowid].hand[c])
                    self.nowMOV += (self.players[self.nowid].hand[c] - 6) if self.players[self.nowid].hand[c] not in [134, 10] else 1
                    if self.players[self.nowid].identity.idx == 3 and self.players[self.nowid].identity.identity == 3:
                        self.nowMOV += 1
                        
                    if self.players[self.nowid].identity.idx == 3 and self.players[self.nowid].identity.identity == 1:
                        self.nowMOV -= 1
                    if self.players[self.nowid].hand[c] != 134:
                        self.players[self.nowid].identity.energy+=(self.players[self.nowid].hand[c] - 6) if self.players[self.nowid].hand[c] not in [10] else 1
                    del self.players[self.nowid].hand[c]
                elif ret in [2,4,6]:
                    self.lostLife(self.nowid, ret)
                    level = ret//2
                    self.nowMOV += level
                    self.players[self.nowid].usedmeta1 = 1
                else:
                    self.cheating()
        self.status = s
    def USESKILL(self):
        s = self.status
        self.status = state.USE_SKILL
        c = svr.connectBot(self.nowid, "int32_t", self)
        skillC = [(self.players[self.nowid].identity.idx*12+11+j) for j in range(12)]
        if c >= len(self.players[self.nowid].hand) or c < 0 or self.players[self.nowid].hand[c] not in skillC:
            # cheat
            self.cheating()
        
        self.nowUsingCardID = self.players[self.nowid].hand[c]
        self.players[self.nowid].usecards.append(self.players[self.nowid].hand[c])
        del self.players[self.nowid].hand[c]
        self.status = s
    def USEBASIC(self):
        s = self.status
        self.status = state.USE_BASIC
        c = svr.connectBot(self.nowid, "int32_t", self)
        typeC = self.nowUsingCardID - 11 - 12*self.players[self.nowid].identity.idx
        if typeC == [0,1,2]:
            basic = [1,2,3]
            if self.players[1-self.nowid].identity.idx == 7 and not vectorHave(self.players[1-self.nowid].metamorphosis, [166]):
                basic.append(134)
        elif typeC == [3,4,5]:
            basic = [4,5,6]
            if self.players[1-self.nowid].identity.idx == 7 and not vectorHave(self.players[1-self.nowid].metamorphosis, [167]):
                basic.append(134)
        elif typeC == [6,7,8]:
            basic = [7,8,9]
            if self.players[1-self.nowid].identity.idx == 7 and not vectorHave(self.players[1-self.nowid].metamorphosis, [168]):
                basic.append(134)
        if c >= len(self.players[self.nowid].hand) or c < 0 or self.players[self.nowid].hand[c] not in basic:
            # cheat
            self.cheating()
        self.status = s
        ret = self.players[self.nowid].hand[c]
        self.players[self.nowid].usecards.append(self.players[self.nowid].hand[c])
        del self.players[self.nowid].hand[c]
        return (ret-1)%3+1
    def chooseMovingDir(self):
        s = self.status
        self.status = state.CHOOSE_MOVING_DIR
        c = svr.connectBot(self.nowid, "int8_t", self)
        if c not in [0,1]:
            self.cheating()
        self.status = s
        return c
    def moveCharacter(self, dir:int, dis:int):
        dif = (dir*2-1)*dis
        ret = False
        while self.players[self.nowid].locate[1]+dif >9 or self.players[self.nowid].locate[1]+dif<1:
            dis -=1
            dif = (dir*2-1)*dis
        if self.getRange()==dis:
            dis-=1
            dif = (dir*2-1)*dis
        elif self.getRange()>dis:
            ret = True
        self.players[self.nowid].locate[1]+=dif
        return ret
    def putPosion(self, target):
        if len(self.players[1-target].identity.remindPosion) == 0:
            return
        now = self.players[1-target].identity.remindPosion[0]
        del self.players[1-target].identity.remindPosion[0]
        self.players[target].graveyard.append(now)
        self.players[1-target].identity.remindPosion-=1
        posion = self.players[target].usecards[i]-131
        for i in range(len(self.players[1-self.nowid].metamorphosis)):
            if self.players[1-self.nowid].metamorphosis[i] == 142:
                posion+=1
        self.lostLife(self.nowid, posion)
    def putTargetPosition(self):
        s = self.status
        self.status = state.PUTTARGETPOSITION
        loc = svr.connectBot(self.nowid, "int32_t", self)
        card = self.getlastcard()
        if card in [29,30,31]:
            if loc not in [self.players[self.nowid].locate[1]+1, self.players[self.nowid].locate[1]-1] or loc<1 or loc>9:
                self.cheating()
        self.nowTarget.locate[1] = loc
def vectorHave(vec:list, ls:list):
    for i in range(len(vec)):
        if vec[i] in ls:
            return True
    return False
@dataclasses.dataclass
class skillCard:
    picture:str
    cardName:str
    def skill(self):
        raise NotImplementedError("skill didn't implement")
@dataclasses.dataclass
class atkCard(skillCard):
    level:int
    def skill(self):
        raise NotImplementedError("atk skill didn't implement")
@dataclasses.dataclass
class defCard(skillCard):
    level:int
    def skill(self):
        raise NotImplementedError("atk skill didn't implement")
@dataclasses.dataclass
class movCard(skillCard):
    level:int
    def skill(self):
        raise NotImplementedError("atk skill didn't implement")
@dataclasses.dataclass
class metaCard(skillCard):
    def skill(self):
        raise NotImplementedError("metamorphosis didn't implement")
@dataclasses.dataclass
class ultraCard(skillCard):
    def skill(self):
        raise NotImplementedError("metamorphosis didn't implement")
    
class server:
    host = None
    ip = None
    port = 8080
    server_socket = None
    bots:list[socket.socket]
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)       
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        print(f"Server started and listening on host {self.host}({self.ip}) port {self.port}")
    def accept(self):
        self.bots[0], addr1 = self.server_socket.accept()
        print(f"BOT1 Connection accepted from {addr1}")
        self.bots[1], addr2 = self.server_socket.accept()
        print(f"BOT2 Connection accepted from {addr2}")
    def close(self):
        self.bot1.close()
        self.bot2.close()
        self.server_socket.close()
    def connectBot(self, which, rettype, g:game):
        self.bots[which].send(g.hideGameStatus().to_Cgame().pack())
        if rettype == 'int32_t':
            return int.from_bytes(self.bots[which].recv(4), "little", True)
        elif rettype == 'int8_t':
            return int.from_bytes(self.bots[which].recv(1), "little", True)
        elif rettype == 'uint32_t':
            return int.from_bytes(self.bots[which].recv(4), "little", False)
        elif rettype == 'uint8_t':
            return int.from_bytes(self.bots[which].recv(1), "little", False)
        elif rettype == 'game':
            return game.from_Cgame(Cgame.unpack(self.bots[which].recv(cstruct.sizeof(Cgame))))
svr:server = server()

