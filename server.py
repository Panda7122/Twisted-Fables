import socket
import random
from game import *
import copy



def settlementContinue(g:game):
    c = g.players[g.nowid].identity.idx
    if c == 0: # 小紅帽
        for i in range(len(g.players[g.nowid].usecards)):
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
        for i in range(len(g.players[g.nowid].usecards)):
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
            if g.players[p].identity.idx == 9:
                g.players[p].identity.destiny_TOKEN_locate = [] # for 山魯佐德's TOKEN
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
                    g.cheating()

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
                    g.cheating()

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
                    g.cheating()

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
                    g.status = state.CHOOSE_DESTINY_TOKEN
                    loc = svr.connectBot(g.nowid, 'int32_t', g)
                    if loc not in [-1,-2,-3,1,2,3,4,5,6,7,8,9,10]:
                        g.cheating()
                    g.players[g.nowid].identity.destiny_TOKEN_locate.append(loc)
        # draw card
        g.nowid = random.randint(0,1)
        for _ in range(4):
            g.drawCard(g.nowid)
        for _ in range(6):
            g.drawCard(1-g.nowid)


def triggerCardSkill(g:game, cardID:int, level:int):
    if (cardID-11)%12 < 3: # attack skill
        g.players[g.nowid].identity.attackSkill[(cardID-11)%3].skill(g, level)
    elif (cardID-11)%12 < 6: # defense skill
        g.players[g.nowid].identity.defenseSkill[(cardID-14)%3].skill(g, level)
    elif (cardID-11)%12 < 9: # move skill
        g.players[g.nowid].identity.moveSkill[(cardID-17)%3].skill(g, level)
        if g.players[g.nowid].identity.idx == 2 and 145 in g.players[g.nowid].metamorphosis:
            g.players[g.nowid].identity.defense += level
            g.players[g.nowid].identity.defense = min(g.players[g.nowid].identity.defense, g.players[g.nowid].identity.maxdefense)
    else:#ultra
        g.players[g.nowid].identity.ultraSkill[(cardID-17)%3].skill(g, level)
def main():
    svr.accept()

    g = game()
    try:
        initializeGame(g)
        while 1:
            # start phase
            settlementContinue(g)
            if g.players[g.nowid].identity.idx == 3:
                g.status = state.CHOOSE_IDENTITY
                ident = svr.connectBot(g.nowid, 'int8_t', g)
                if ident not in [1,2,3]:
                    g.cheating()
                if ident == g.player[g.nowid].identity.identity:
                    g.cheating()
                g.player[g.nowid].identity.identity = ident
            elif g.players[g.nowid].identity.idx == 4:
                for m in g.players[g.nowid].metamorphosis:
                    if m == 154:
                        g.players[g.nowid].identity.KI_TOKEN += 1
            # clean phase
            for i in range(len(g.players[g.nowid].usecards)):
                g.players[g.nowid].graveyard.append(g.players[g.nowid].usecards[i])
                if g.players[g.nowid].usecards[i] == 134:
                    eneragy = 1
                    for i in range(len(g.players[1-g.nowid].metamorphosis)):
                        if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                            eneragy+=1
                    g.players[1-g.nowid].energy += eneragy
                if g.players[g.nowid].usecards[i] in [131, 132, 133]:
                    posion = g.players[g.nowid].usecards[i]-131
                    for i in range(len(g.players[1-g.nowid].metamorphosis)):
                        if g.players[1-g.nowid].metamorphosis[i] == 142:
                            posion+=1
                    g.lostLife(g.nowid, posion)
            for i in range(len(g.players[g.nowid].usecards)):
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
                    if g.players[g.nowid].identity.idx == 4 and 151 in g.players[g.nowid].metamorphosis:
                        K = g.players[g.nowid].identity.spendKIforATK(g)
                        if K>3 or K<0:
                            g.cheating()
                        g.nowATK += K
                    dam = g.damage(1-g.nowid, 1, g.nowATK)
                    if g.players[g.nowid].identity.idx == 1 and dam >=2 and vectorHave(g.players[g.nowid].metamorphosis, [139]):
                        g.putPosion( 1-g.nowid)
                    lastAct.atk = lastAction(g.nowATK,0, 0, [])
                    g.nowATK = 0
                elif select == 2: # basic cards
                    # choose a basic card from hand
                    g.USEDEFBASIC()
                    if g.players[g.nowid].identity.idx != 2 or g.players[g.nowid].identity.AWAKEN != 1: 
                        g.players[g.nowid].identity.defense +=g.nowDEF
                        g.players[g.nowid].identity.defense = min(g.players[g.nowid].defense, g.players[g.nowid].maxdefense)
                    lastAct.atk = lastAction(0, g.nowDEF, 0, [])
                    g.nowDEF = 0
                elif select == 3: # basic cards
                    # choose a basic card from hand
                    g.USEDEFBASIC()
                    dir = g.chooseMovingDir()
                    through = g.moveCharacter( dir, g.nowMOV)
                    if through:
                        if g.players[1-g.nowid].identity.idx == 3 and g.players[1-g.nowid].identity.identity == 3 and vectorHave(g.players[1-g.nowid].metamorphosis, [149]):
                            g.drawCard( 1-g.nowid)
                        elif g.players[g.nowid].identity.idx == 3 and g.players[g.nowid].identity.identity == 3 and vectorHave(g.players[g.nowid].metamorphosis, [149]):
                            g.drawCard( g.nowid)
                        elif g.players[1-g.nowid].identity.idx == 1 and vectorHave(g.players[1-g.nowid].metamorphosis, [141]):
                            g.putPosion( g.nowid)
                        elif g.players[g.nowid].identity.idx == 1 and vectorHave(g.players[g.nowid].metamorphosis, [141]):
                            g.putPosion( 1-g.nowid)
                    lastAct.atk = lastAction(0, 0,g.nowMOV, [])
                        
                    g.nowMOV = 0
                elif select == 4: # use a skill
                    # choose a skill card from hand
                    
                    card = g.USESKILL()
                    if (card-11)%12 >=9:
                        g.cheating()
                    g.nowUsingCardID = card
                    # if is dorothy
                    if g.players[g.nowid].identity.idx == 8 and g.players[g.nowid].dorothy.canCombo:
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
                        if g.players[g.nowid].identity.idx == 2 and 143 in  g.players[g.nowid].metamorphosis and g.players[g.nowid].usedmeta1 == 0:
                            s = g.status
                            g.status = state.LOST_LIFE_FOR_USESKILL
                            ret = svr.connectBot(g.nowid, 'int8_t', game)
                            g.status = s
                            if ret == 0:
                                level = g.USEBASIC()
                            elif ret in [2,4,6]:
                                g.lostLife(g.nowid, ret)
                                level = ret//2
                                g.players[g.nowid].usedmeta1 = 1
                            else:
                                g.cheating()
                        else:
                            level = g.USEBASIC()
                    triggerCardSkill(g, g.nowUsingCardID, level)
                    g.nowUsingCardID = 0
                elif select == 5: # TODO use a special card
                    card = g.USESKILL()
                    if (card-11)%12 < 9:
                        g.cheating()
                    
                    g.nowUsingCardID = card
                    triggerCardSkill(g, g.nowUsingCardID, 0)
                    g.nowUsingCardID = 0
                    pass
                elif select == 6: # buy a card
                    g.status = state.BUY_CARD_TYPE
                    ct = svr.connectBot(g.nowid, "int32_t", g)
                    if(ct not in [-1,-2,-3,1,2,3,4]):
                        g.cheating()
                    if(ct<0):
                        if ct == -1:
                            g.players[g.nowid].buyATKCard()
                        if ct == -2:
                            g.players[g.nowid].buyDEFCard()
                        if ct == -3:
                            g.players[g.nowid].buyMOVCard()
                    else:
                        if(ct == 4):
                            lv = 1
                        else:
                            g.status = state.BUY_CARD_LV
                            lv = svr.connectBot(g.nowid, "int32_t", g)
                            if(lv not in [1,2,3]):
                                g.cheating()
                        if len(g.basicBuyDeck[ct-1][lv-1]) == 0:
                            g.cheating()
                        pz = BASIC_PRIZE[ct-1][lv-1]
                        if g.players[g.nowid].identity.energy < pz:
                            g.cheating()
                        g.players[g.nowid].identity.energy -= pz
                        cd = g.basicBuyDeck[ct-1][lv-1][0]
                        del g.basicBuyDeck[ct-1][lv-1][0]
                        g.players[g.nowid].graveyard.append(cd)
                        if g.players[1-g.nowid].identity.idx == 9 and (ct-1)*3+lv in  g.players[1-g.nowid].identity.destiny_TOKEN_locate != 0:
                            g.players[1-g.nowid].identity.triggerDestiny(g, (ct-1)*3+lv)
                elif select == 7: # TODO metamorphosis
                    s = g.status
                    g.status = state.USE_METAMORPHOSIS
                    ret = svr.connectBot(g.nowid, 'int32_t', g)
                    if ret <0 or ret >= len(g.players[g.nowid].metamorphosis):
                        g.cheating()
                    if g.players[g.nowid].identity.idx < 6:
                        idx = (g.players[g.nowid].metamorphosis[ret]-135)%4
                    elif g.players[g.nowid].identity.idx == 6:
                        if g.players[g.nowid].metamorphosis[ret] <= 162:
                            idx = (g.players[g.nowid].metamorphosis[ret]-135)%4
                        else:
                            idx = (g.players[g.nowid].metamorphosis[ret]-92)%3
                    elif g.players[g.nowid].identity.idx == 7:
                        idx = (g.players[g.nowid].metamorphosis[ret]-163)%6
                    else:
                        idx = (g.players[g.nowid].metamorphosis[ret]-169)%4
                    g.players[g.nowid].identity.metamorphosisSkill[idx].skill(g, idx)
                    g.status = s
                elif select == 8: # TODO charactor special move
                    g.players[g.nowid].identity.specialMove(g)
                    pass
                elif select == 9: # drop poison
                    g.USEPOSION()
                    pass
                elif select == 10: # end
                    break
                else:
                    # cheat            
                    g.cheating()
                    pass
                moved = True
                if g.players[g.nowid].identity.idx == 8:
                    if select in [0,1,2,3,5,6]:
                        g.players[g.nowid].dorothy.canCombo = 0
            # end phase
            g.players[g.nowid].energy = 0
            g.nowATK = 0
            g.nowDEF = 0
            g.nowMOV = 0
            g.nowUsingCardID = 0
            for i in range(len(g.players[g.nowid].hand)):
                if g.players[g.nowid].hand[i] in []:
                    i+=1
                    continue
                g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[i])
                if g.players[g.nowid].usecards[i] == 134:
                    eneragy = 1
                    for i in range(len(g.players[1-g.nowid].metamorphosis)):
                        if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                            eneragy+=1
                    g.players[1-g.nowid].energy += eneragy
                if g.players[g.nowid].usecards[i] in [131, 132, 133]:
                    posion = g.players[g.nowid].usecards[i]-131
                    for i in range(len(g.players[1-g.nowid].metamorphosis)):
                        if g.players[1-g.nowid].metamorphosis[i] == 142:
                            posion+=1
                    g.lostLife( g.nowid, posion)
            for i in range(len(g.players[g.nowid].hand)):
                del g.players[g.nowid].hand[i]
            cardNum = 6
            if g.players[g.nowid].identity.idx == 2:
                g.players[g.nowid].identity.usedmeta1 = 0
                g.players[g.nowid].identity.usedmeta2 = 0
            elif g.players[g.nowid].identity.idx == 3:
                g.players[g.nowid].identity.riseBasic = 0
            if g.players[g.nowid].identity.idx == 4 and g.players[g.nowid].identity.KI_TOKEN > 0 and g.players[g.nowid].identity.extraCard > 0:
                add = g.players[g.nowid].identity.spendKIforDraw(g)
                if add > g.players[g.nowid].identity.extraCard or add < 0:
                    g.cheating()
                cardNum += add
                g.players[g.nowid].identity.extraCard = 0
            
            for _ in range(cardNum):
                g.drawCard(g.nowid)
            if g.players[g.nowid].identity.idx == 3 and g.players[g.nowid].identity.restartTurn > 0:
                g.players[g.nowid].identity.restartTurn -= 1
                while(len(g.players[g.nowid].hand) > 4):
                    d = g.dropCardFromHand()
                    id = g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[id])
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
            elif g.players[g.nowid].identity.idx == 3:
                g.players[g.nowid].identity.restartTurn = 0
                g.players[g.nowid].identity.havedrestart = 0
            g.nowid = 1-g.nowid
    finally:    
        svr.close()
        print('Shutting down server...')
        
if __name__ == "__main__":
    main()