import socket
import random
from game import *
import copy



def settlementContinue(g:game):
    c = g.players[g.nowid].identity.idx
    if c == 0: # 小紅帽
        for i in range(g.players[g.nowid].usecards.SIZE):
            if g.players[g.nowid].usecards[i] in [14,15,16]:
                if g.players[g.nowid].defense>=0:
                    g.damage(1-g.nowid, g.players[g.nowid].usecards[i]-13, 2*(g.players[g.nowid].usecards[i]-13))
    elif c == 1: # 白雪公主
        pass
    elif c == 2: # 睡美人
        pass
    elif c == 3: # 愛麗絲
        pass
    elif c == 4: # 花木蘭
        pass
    elif c == 5: # 輝夜姬
        for i in range(g.players[g.nowid].usecards.SIZE):
            if g.players[g.nowid].usecards[i] in [78,79]:
                o = g.players[g.nowid].usecards[i+1]-6 # the basic move card level
                if g.getRange()>4-o:
                    g.damage(1-g.nowid, 18, 2*(g.players[g.nowid].usecards[i]-76))
            elif g.players[g.nowid].usecards[i] == 81:
                if g.players[g.nowid].defense > g.players[1-g.nowid].defense:
                    g.lostLife(1-g.nowid, g.players[g.nowid].defense-g.players[1-g.nowid].defense)
            elif g.players[g.nowid].usecards[i] == 82:
                g.status = state.SET_TARGET_LOCATE_TO_NEARBY
                loc = svr.connectBot(g.nowid, "int8_t", g)
                if abs(g.players[g.nowid].locate[1] - loc) != 1 and g.players[1-g.nowid].locate[1] != loc:
                    # cheat
                    g.cheating()
                g.setLocate(1-g.nowid, loc)
                g.damage(1-g.nowid, 18, 3)
    elif c == 6: # 美人魚
        pass
    elif c == 7: # 火柴女孩
        pass
    elif c == 8: # 桃樂絲
        pass
    elif c == 9: # 山魯佐德
        pass
    return


def initializeGame(g:game):
    # initialize
        # init metadata
        g.nowATK = 0
        g.nowDEF = 0
        g.nowMOV = 0
        g.nowUsingCardID = 0
        # which character client implement 
        bot1CharList = svr.bot1.recv(10)
        bot1CharList = [i for i,v in enumerate(bot1CharList) if v==1]
        bot2CharList = svr.bot2.recv(10)
        bot2CharList = [i for i,v in enumerate(bot2CharList) if v==1]
        # random choice charactor
        g.players[0] = character.getClass(random.choice(bot1CharList))()
        g.players[1] = character.getClass(random.choice(bot2CharList))()
        while(g.players[0].identity.idx == g.players[1].identity.idx):
            g.players[0] = character.getClass(random.choice(bot1CharList))()
            g.players[1] = character.getClass(random.choice(bot2CharList))()
        
        # initialize player's location
        g.players[0].locate = 4
        g.players[1].locate = 6
        # set up player's init_deck and skill_buy_deck
        for p in range(2):
            # initialize init_deck
            g.players[p].deck.append(11+(g.players[p].identity.idx-1)*12+0) # lv1 attack skill
            g.players[p].deck.append(11+(g.players[p].identity.idx-1)*12+1) # lv1 defense skill
            g.players[p].deck.append(11+(g.players[p].identity.idx-1)*12+2) # lv1 move skill
            for _ in range(3):
                g.players[p].deck.append(1) # lv1 attack*3
                g.players[p].deck.append(4) # lv1 defense*3
                g.players[p].deck.append(7) # lv1 move*3
            # initialize skill_buy_deck
            for i in [1,2]:
                for _ in range(i+1):# lv2*2, lv3*3
                    g.players[p].attackSkill.append(11+(g.players[p].identity.idx-1)*12 + i) # lv.i attack skill
                    g.players[p].defenseSkill.append(11+(g.players[p].identity.idx-1)*12 + i+3) # lv.i defense skill
                    g.players[p].moveSkill.append(11+(g.players[p].identity.idx-1)*12 + i+6) # lv.i move skill
                if i == 1: # metamorphosis 1
                    if g.players[p].identity.idx <= 6:# before 火柴女孩
                        g.players[p].attackSkill.append(135 + (g.players[p].identity.idx)*4 + 0)
                        g.players[p].defenseSkill.append(135 + (g.players[p].identity.idx)*4 + 1)
                        g.players[p].moveSkill.append(135 + (g.players[p].identity.idx)*4 + 2)
                    elif g.players[p].identity.idx == 7:# 火柴女孩
                        g.players[p].attackSkill.append(135 + (g.players[p].identity.idx)*4 + 0)
                        g.players[p].defenseSkill.append(135 + (g.players[p].identity.idx)*4 + 1)
                        g.players[p].moveSkill.append(135 + (g.players[p].identity.idx)*4 + 2)
                    else:# after 火柴女孩
                        g.players[p].attackSkill.append(169 + (g.players[p].identity.idx-8)*4 + 0)
                        g.players[p].defenseSkill.append(169 + (g.players[p].identity.idx-8)*4 + 1)
                        g.players[p].moveSkill.append(169 + (g.players[p].identity.idx-8)*4 + 2)
                else: # metamorphosis 2
                    if g.players[p].identity.idx <= 6:# before 火柴女孩
                        g.players[p].attackSkill.append(135 + (g.players[p].identity.idx)*4 + 3)
                        g.players[p].defenseSkill.append(135 + (g.players[p].identity.idx)*4 + 3)
                        g.players[p].moveSkill.append(135 + (g.players[p].identity.idx)*4 + 3)
                    elif g.players[p].identity.idx == 7:# 火柴女孩
                        g.players[p].attackSkill.append(135 + (g.players[p].identity.idx)*4 + 3)
                        g.players[p].defenseSkill.append(135 + (g.players[p].identity.idx)*4 + 4)
                        g.players[p].moveSkill.append(135 + (g.players[p].identity.idx)*4 + 5)
                    else:# after 火柴女孩
                        g.players[p].attackSkill.append(169 + (g.players[p].identity.idx-8)*4 + 3)
                        g.players[p].defenseSkill.append(169 + (g.players[p].identity.idx-8)*4 + 3)
                        g.players[p].moveSkill.append(169 + (g.players[p].identity.idx-8)*4 + 3)
            # initialize special skill
            for i in range(9,12):
                g.players[p].specialDeck.append(11+(g.players[p].identity.idx-1)*12 + i)
        # initialize basic buy deck
        for i in range(10):
            # 1,4,7 is lv1基本牌，take 3 for each player init deck
            for j in range(18 if i not in [1,4,7] else 12):  
                g.basicBuyDeck[i].cards[j] = i+1
            g.basicBuyDeck[i].destiny_TOKEN = 0 # for 山魯佐德's TOKEN
        # shuffle init_deck
        random.shuffle(g.players[0].deck)
        random.shuffle(g.players[1].deck)
        
        
        #reset graveyard, usecards, metamorphosis
        for p in range(2):
            g.players[p].usecards = []
            g.players[p].graveyard = []
            g.players[p].metamorphosis = []
        # charactor special rule
        for p in range(2):
            g.nowid = p
            c = g.players[p].identity.idx
            if c == 0: # 小紅帽
                pass
            elif c == 1: # 白雪公主
                pass
            elif c == 2: # 睡美人
                pass
            elif c == 3: # 愛麗絲
                g.status = state.CHOOSE_IDENTITY
                ident = svr.connectBot(g.nowid, 'int8_t', g)
                if ident not in [1,2,3]:
                    return -1
                g.player[p].alice.identity = ident
                pass
            elif c == 4: # 花木蘭
                pass
            elif c == 5: # 輝夜姬
                pass
            elif c == 6: # 美人魚
                g.status = state.CHOOSE_TENTACLE_LOCATION
                location = svr.connectBot(g.nowid, 'int32_t', g)
                if location <1 or location > 9:
                    return -1
                g.tentacle_TOKEN_locate.append(location)
            elif c == 7: # 火柴女孩
                pass
            elif c == 8: # 桃樂絲
                g.status = state.CHOOSE_SPECIAL_CARD
                card = svr.connectBot(g.nowid, 'int32_t', g)
                for i in range(3):
                    if g.players[p].specialDeck[i] == card:
                        del g.players[p].specialDeck[i]
                        break
                if len(g.players[p].specialDeck) == 3:
                    # error
                    return -1
                g.players[p].deck.append(card)
                random.shuffle(g.players[p].deck)
                
                g.players[p].dorothy.COMBO_TOKEN = 0
                g.players[p].dorothy.canCombo = False
            elif c == 9: # 山魯佐德
                g.players[1-g.nowid].attackSkill.destiny_TOKEN=0
                g.players[1-g.nowid].defenseSkill.destiny_TOKEN=0
                g.players[1-g.nowid].moveSkill.destiny_TOKEN=0
                for d in range(10):
                    g.basicBuyDeck[d].destiny_TOKEN=0
                for _ in range(3):
                    g.status = state.CHOOSE_SPECIAL_CARD
                    gtmp = svr.connectBot(g.nowid, 'game', g)
                    if gtmp.nowid != g.nowid:
                        g.cheating()
                    if gtmp.countDestinyTOKEN() == g.countDestinyTOKEN()+1:
                        g = gtmp
                    else:
                        # error
                        g.cheating()
        # draw card
        g.nowid = random.randint(0,1)
        for _ in range(4):
            g.drawCard(g.nowid)
        for _ in range(6):
            g.drawCard(1-g.nowid)


def triggerCardSkill(g:game, cardID:int, level:int):
    
    if cardID in [11,12,13]: # 小紅帽
        g.players[g.nowid].identity.atkSkill[cardID-11].skill(g, level)
    elif cardID in [14,15,16]: 
        g.players[g.nowid].identity.defSkill[cardID-14].skill(g, level)
    elif cardID in [17,18,19]:
        g.players[g.nowid].identity.movSkill[cardID-17].skill(g, level)
    elif cardID in [23,24,25]: # 白雪公主
        g.players[g.nowid].identity.atkSkill[cardID-23].skill(g, level)
    elif cardID in [26,27,28]:
        g.players[g.nowid].identity.defSkill[cardID-26].skill(g, level)
    elif cardID in [29,30,31]:
        g.players[g.nowid].identity.movSkill[cardID-29].skill(g, level)
    elif cardID in [35,36,37]: # TODO 睡美人
        g.players[g.nowid].identity.atkSkill[cardID-35].skill(g, level)
        pass
    elif cardID in [38,39,40]:
        pass
    elif cardID in [41,42,43]:
        pass
    elif cardID in [47,48,49]: # TODO 愛麗絲
        pass
    elif cardID in [50,51,52]:
        pass
    elif cardID in [53,54,55]:
        pass
    elif cardID in [59,60,61]: # TODO 花木蘭
        pass
    elif cardID in [62,63,64]:
        pass
    elif cardID in [65,66,67]:
        pass
    elif cardID in [71,72,73]: # TODO 輝夜姬
        pass
    elif cardID in [74,75,76]:
        pass
    elif cardID in [77,78,79]:
        pass
    elif cardID in [83,84,85]: # TODO 美人魚
        pass
    elif cardID in [86,87,88]:
        pass
    elif cardID in [89,90,91]:
        pass
    elif cardID in [95,96,97]: # TODO 火柴女孩
        pass
    elif cardID in [98,99,100]:
        pass
    elif cardID in [101,102,103]:
        pass
    elif cardID in [107,108,109]: # TODO 桃樂絲
        pass
    elif cardID in [110,111,112]:
        pass
    elif cardID in [113,114,115]:
        pass
    elif cardID in [119,120,121]: # TODO 山魯佐德
        pass
    elif cardID in [122,123,124]:
        pass
    elif cardID in [125,126,127]:
        pass
    return
def main():
    svr.accept()

    g = game()
    try:
        initializeGame(g)
        while 1:
            # start phase
            settlementContinue(g)
            # clean phase
            for i in range(g.players[g.nowid].usecards.SIZE):
                g.players[g.nowid].graveyard.append(g.players[g.nowid].usecards[i])
                if g.players[g.nowid].usecards[i] == 134:
                    eneragy = 1
                    for i in range(g.players[1-g.nowid].metamorphosis.SIZE):
                        if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                            eneragy+=1
                    g.players[1-g.nowid].energy += eneragy
                if g.players[g.nowid].usecards[i] in [131, 132, 133]:
                    posion = g.players[g.nowid].usecards[i]-131
                    for i in range(g.players[1-g.nowid].metamorphosis.SIZE):
                        if g.players[1-g.nowid].metamorphosis[i] == 142:
                            posion+=1
                    g.lostLife(g.nowid, posion)
            for i in range(g.players[g.nowid].usecards.SIZE):
                del g.players[g.nowid].usecards[i]
            g.players[g.nowid].defense = 0
            # TODO move phase
            moved:bool = False
            while True:
                select = g.chooseMove()
                if select == 0: # focus
                    # remove a card from hand/graveyard
                    if moved == False:
                        where, c = g.chooseCardFromHandorGraveyard()
                        if where: # hand
                            del g.players[g.nowid].hand[c]
                        else: # graveyard
                            del g.players[g.nowid].graveyard[c]
                        break
                    else:
                        # cheat
                        g.cheating()
                elif select == 1: # basic atk cards
                    # choose a basic card from hand
                    g.USEATKBASIC()
                    dam = g.damage(1-g.nowid, 1, g.nowATK)
                    if g.players[g.nowid].character == 1 and dam >=2 and vectorHave(g.players[g.nowid].metamorphosis, [139]):
                        g.putPosion( 1-g.nowid)
                    g.nowATK = 0
                elif select == 2: # basic cards
                    # choose a basic card from hand
                    g.USEDEFBASIC()
                    g.players[g.nowid].defense +=g.nowDEF
                    g.players[g.nowid].defense = min(g.players[g.nowid].defense, g.players[g.nowid].maxdefense)
                    g.nowDEF = 0
                elif select == 3: # basic cards
                    # choose a basic card from hand
                    g.USEDEFBASIC()
                    dir = g.chooseMovingDir()
                    through = g.moveCharactor( dir, g.nowMOV)
                    if through:
                        if g.players[1-g.nowid].charactor == 3 and vectorHave(g.players[1-g.nowid].metamorphosis, [149]):
                            g.drawCard( 1-g.nowid)
                        elif g.players[g.nowid].charactor == 3 and vectorHave(g.players[g.nowid].metamorphosis, [149]):
                            g.drawCard( g.nowid)
                        elif g.players[1-g.nowid].charactor == 1 and vectorHave(g.players[1-g.nowid].metamorphosis, [141]):
                            g.putPosion( g.nowid)
                        elif g.players[g.nowid].charactor == 1 and vectorHave(g.players[1-g.nowid].metamorphosis, [141]):
                            g.putPosion( 1-g.nowid)
                    g.nowMOV = 0
                elif select == 4: # use a skill
                    # choose a skill card from hand
                    card = g.USESKILL()
                    # if is dorothy
                    if g.players[g.nowid].charactor == 8 and g.players[g.nowid].dorothy.canCombo:
                        # ask combo
                        s = g.status
                        g.status = state.TRIGGER_COMBO
                        trigger = svr.connectBot(g.nowid, 'int8_t', g)
                        g.status = s
                        if trigger not in [0,1]:
                            g.cheating()
                        if trigger == 0:
                            # choose a basic card from hand
                            level = g.USEBASIC()
                        else:
                            level = 0
                    else:
                        # choose a basic card from hand
                        level = g.USEBASIC()
                    triggerCardSkill(g, g.nowUsingCardID, level)
                    g.nowUsingCardID = 0
                elif select == 5: # TODO use a special card
                    pass
                elif select == 6: # TODO buy a card
                    pass
                elif select == 7: # TODO metamorphosis
                    pass
                elif select == 8: # TODO charactor special move
                    pass
                elif select == 9: # end
                    break
                else:
                    # cheat            
                    g.cheating()
                    pass
                move = True
                if g.players[g.nowid].charactor == 8:
                    if select in [0,1,2,3,5,6]:
                        g.players[g.nowid].dorothy.canCombo = 0
            # end phase
            g.players[g.nowid].energy = 0
            g.nowATK = 0
            g.nowDEF = 0
            g.nowMOV = 0
            g.nowUsingCardID = 0
            for i in range(g.players[g.nowid].hand.SIZE):
                if g.players[g.nowid].hand[i] in []:
                    i+=1
                    continue
                g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[i])
                if g.players[g.nowid].usecards[i] == 134:
                    eneragy = 1
                    for i in range(g.players[1-g.nowid].metamorphosis.SIZE):
                        if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                            eneragy+=1
                    g.players[1-g.nowid].energy += eneragy
                if g.players[g.nowid].usecards[i] in [131, 132, 133]:
                    posion = g.players[g.nowid].usecards[i]-131
                    for i in range(g.players[1-g.nowid].metamorphosis.SIZE):
                        if g.players[1-g.nowid].metamorphosis[i] == 142:
                            posion+=1
                    g.lostLife( g.nowid, posion)
            for i in range(g.players[g.nowid].hand.SIZE):
                del g.players[g.nowid].hand[i]
            for _ in range(6):
                g.drawCard(g.nowid)
            g.nowid = 1-g.nowid
    finally:    
        svr.close()
        print('Shutting down server...')
        
if __name__ == "__main__":
    main()