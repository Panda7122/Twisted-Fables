import socket
import random
from game import *
import copy
import gui
from characters import alice, dorothy, kaguya, littleRed, matchGirl, mermaid, mulan, scheherazade, sleepingBeauty, snowWhite
import threading
import time

def settlementContinue(g:game):
    from game import svr
    c = g.players[g.nowid].identity.idx
    if c == 0: # 小紅帽
        for i in range(len(g.players[g.nowid].usecards)):
            if g.players[g.nowid].usecards[i] in [14,15,16]:
                if g.players[g.nowid].identity.defense>=0:
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
                if g.players[g.nowid].identity.defense > g.players[1-g.nowid].identity.defense:
                    g.lostLife(1-g.nowid, g.players[g.nowid].identity.defense-g.players[1-g.nowid].identity.defense)
            elif g.players[g.nowid].usecards[i] == 82:
                s = g.status
                g.status = state.SET_TARGET_LOCATE_TO_NEARBY
                loc = svr.connectBot(g.nowid, "int8_t", g)
                g.status = s
                if abs(g.players[g.nowid].locate - loc) != 1 and g.players[1-g.nowid].locate != loc:
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
    from game import svr
    # initialize
    # init metadata
    g.nowATK = 0
    g.nowDEF = 0
    g.nowMOV = 0
    g.totalDamage = 0
    g.nowUsingCardID = 0
    # which character client implement 
    bot1CharList = svr.bots[0].recv(10)
    bot1CharList = [i for i,v in enumerate(bot1CharList) if v==1]
    # bot1CharList = [1]
    bot2CharList = svr.bots[1].recv(10)
    bot2CharList = [i for i,v in enumerate(bot2CharList) if v==1]
    # bot2CharList = [8]
    # random choice charactor
    g.players = [player(), player(), player(), player()]
    g.players[0].identity=character.getClass(random.choice(bot1CharList))()
    g.players[1].identity=character.getClass(random.choice(bot2CharList))()
    g.players[2].identity=character.getClass(0)()
    g.players[3].identity=character.getClass(0)()
    while(g.players[0].identity.idx == g.players[1].identity.idx):
        g.players[0].identity = character.getClass(random.choice(bot1CharList))()
        g.players[1].identity = character.getClass(random.choice(bot2CharList))()
    
    # initialize player's location
    g.players[0].locate = 4
    g.players[1].locate = 6
    # set up player's init_deck and skill_buy_deck
    for p in range(2):
        # initialize init_deck
        g.players[p].deck.append(11+(g.players[p].identity.idx)*12+0) # lv1 attack skill
        g.players[p].deck.append(11+(g.players[p].identity.idx)*12+3) # lv1 defense skill
        g.players[p].deck.append(11+(g.players[p].identity.idx)*12+6) # lv1 move skill
        for _ in range(3):
            g.players[p].deck.append(1) # lv1 attack*3
            g.players[p].deck.append(4) # lv1 defense*3
            g.players[p].deck.append(7) # lv1 move*3
        # initialize skill_buy_deck
        for i in [1,2]:
            for _ in range(i+1):# lv2*2, lv3*3
                g.players[p].attackSkill.append(11+(g.players[p].identity.idx)*12 + i) # lv.i attack skill
                g.players[p].defenseSkill.append(11+(g.players[p].identity.idx)*12 + i+3) # lv.i defense skill
                g.players[p].moveSkill.append(11+(g.players[p].identity.idx)*12 + i+6) # lv.i move skill
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
            g.players[p].ULTDeck.append(11+(g.players[p].identity.idx)*12 + i)
    # initialize basic buy deck
    for i in range(10):
        # 1,4,7 is lv1基本牌，take 3 for each player init deck
        for j in range(18 if i not in [0,3,6] else 12):  
            g.basicBuyDeck[i].append(i+1)
    # shuffle init_deck
    random.shuffle(g.players[0].deck)
    random.shuffle(g.players[1].deck)
    
    
    #reset graveyard, usecards, metamorphosis
    for p in range(2):
        g.players[p].usecards = []
        g.players[p].graveyard = []
        g.players[p].metamorphosis = []
    g.canUpdate = 1
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

            g.players[p].identity.identity = ident
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
            s = g.status
            g.status = state.CHOOSE_SPECIAL_CARD
            card = svr.connectBot(g.nowid, 'int32_t', g)
            g.status = s
            for i in range(len(g.players[p].ULTDeck)):
                if g.players[p].ULTDeck[i] == card:
                    del g.players[p].ULTDeck[i]
                    break
            if len(g.players[p].ULTDeck) == 3:
                # error
                g.cheating()

            g.players[p].deck.append(card)
            random.shuffle(g.players[p].deck)
            
            g.players[p].identity.COMBO_TOKEN = 0
            g.players[p].identity.canCombo = False
        elif c == 9: # 山魯佐德
            for _ in range(3):
                s = g.status
                g.status = state.APPEND_DESTINY_TOKEN
                loc = svr.connectBot(g.nowid, 'int32_t', g)
                g.status = s
                if loc not in [-1,-2,-3,1,2,3,4,5,6,7,8,9,10]:
                    g.cheating()
                g.players[g.nowid].identity.destiny_TOKEN_locate.append(loc)
                g.players[g.nowid].identity.destiny_TOKEN_type.append(1)
                
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
root = None
def ui_thread(g:game):
    global root
    root = gui.buildScreen(1920, 1080)
    # root = gui.buildScreen(2560, 1440)
    root.after(0, gui.updateScreen, root, g)
    root.mainloop()

    
def main():
    global lastAct, root
    from game import svr
    svr.accept()
    g = game()
    threading.Thread(target=ui_thread, args=(g,), daemon=True).start()
    while root is None:
        time.sleep(0.01)
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
                if ident == g.players[g.nowid].identity.identity:
                    g.cheating()
                g.players[g.nowid].identity.identity = ident
            elif g.players[g.nowid].identity.idx == 4:
                for m in g.players[g.nowid].metamorphosis:
                    if m == 154:
                        g.players[g.nowid].identity.KI_TOKEN += 1
            elif g.players[g.nowid].identity.idx == 9:
                for t in g.players[g.nowid].identity.destiny_TOKEN_type:
                    if t == 2:
                        g.lostLife(1-g.nowid, 1)
                for i in range(len(g.players[g.nowid].identity.destiny_TOKEN_type)):
                    g.players[g.nowid].identity.destiny_TOKEN_type[i] = 1
                    g.players[g.nowid].identity.selectToken = i
                    s = g.status
                    g.status = state.TOKEN_GOAL
                    dloc = svr.connectBot(g.nowid, 'int8_t', g)
                    if dloc not in [-1,-2,-3,1,2,3,4,5,6,7,8,9,10]:
                        g.cheating()
                    if dloc == g.players[g.nowid].identity.destiny_TOKEN_locate[i]:
                        g.cheating()
                    g.players[g.nowid].identity.destiny_TOKEN_locate[i] = dloc
                    g.status = s

            # clean phase
            for i in range(len(g.players[g.nowid].usecards)):
                g.players[g.nowid].graveyard.append(g.players[g.nowid].usecards[i])
                if g.players[g.nowid].usecards[i] == 134:
                    eneragy = 1
                    for i in range(len(g.players[1-g.nowid].metamorphosis)):
                        if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                            eneragy+=1
                    g.players[1-g.nowid].identity.energy += eneragy
                if g.players[g.nowid].usecards[i] in [131, 132, 133]:
                    posion = g.players[g.nowid].usecards[i]-131
                    for i in range(len(g.players[1-g.nowid].metamorphosis)):
                        if g.players[1-g.nowid].metamorphosis[i] == 142:
                            posion+=1
                    g.lostLife(g.nowid, posion)
            for i in range(len(g.players[g.nowid].usecards)):
                del g.players[g.nowid].usecards[i]
            if g.players[g.nowid].identity.idx == 5 and 156 in g.players[g.nowid].metamorphosis:
                for _ in range(g.players[g.nowid].identity.defense//3):
                    g.drawCard(g.nowid)
            g.players[g.nowid].identity.defense = 0

            # move phase
            moved:bool = False
            while True:
                select = g.chooseMove()
                if select == 0: # focus
                    # remove a card from hand/graveyard
                    if moved == False:
                        where, c = g.chooseCardFromHandorGraveyard()
                        if where: # hand
                            if g.players[g.nowid].hand[c]  == 134:
                                g.cheating()
                            del g.players[g.nowid].hand[c]
                        else: # graveyard
                            if g.players[g.nowid].graveyard[c]  == 134:
                                g.cheating()
                            del g.players[g.nowid].graveyard[c]
                        break
                    else:
                        # cheat
                        g.cheating()
                elif select == 1: # basic atk cards
                    # choose a basic card from hand
                    
                    g.USEATKBASIC()
                    if g.players[g.nowid].identity.idx == 7 and 163 in g.players[g.nowid].metamorphosis:
                        r = g.players[g.nowid].identity.recycle_match(g, 1)
                        if r == 1:
                            nowATK += 2
                    if g.players[g.nowid].identity.idx == 4 and 151 in g.players[g.nowid].metamorphosis:
                        K = g.players[g.nowid].identity.spendKIforATK(g)
                        if K>3 or K<0:
                            g.cheating()
                        if K > g.players[g.nowid].identity.KI_TOKEN:
                            g.cheating()
                        g.players[g.nowid].identity.KI_TOKEN -= K
                            
                        g.nowATK += K
                    if g.players[g.nowid].identity.idx == 6 and 159 in g.players[g.nowid].metamorphosis:
                        dam = g.damage(1-g.nowid, 18, g.nowATK)
                    else:
                        dam = g.damage(1-g.nowid, 1, g.nowATK)
                    if g.players[g.nowid].identity.idx == 1 and dam >=2 and 139 in g.players[g.nowid].metamorphosis:
                        g.putPosion( 1-g.nowid)
                    if g.players[g.nowid].identity.idx ==8 and 169 in g.players[g.nowid].metamorphosis and lastAct.dam != 0:
                        if dam > lastAct.dam:
                            c = 1
                            for m in g.players[g.nowid]:
                                if m == 169:
                                    c+=1
                            g.players[g.nowid].identity.COMBO_TOKEN += c
                            g.players[g.nowid].identity.COMBO_TOKEN = min(12, g.players[g.nowid].identity.COMBO_TOKEN)
                    if g.players[g.nowid].identity.idx == 8:
                        g.players[g.nowid].identity.canCombo = 0
                    if g.players[g.nowid].identity.idx == 9:
                        if 173 in g.players[g.nowid].metamorphosis:
                            if dam >= 3:
                                g.players[g.nowid].identity.flipTOKEN(g)
                            
                    lastAct = lastAction(g.nowATK,0, 0,dam, [])
                    g.nowATK = 0
                elif select == 2: # basic def cards
                    # choose a basic card from hand
                    g.USEDEFBASIC()
                    if g.players[g.nowid].identity.idx != 2 or g.players[g.nowid].identity.AWAKEN != 1: 
                        g.players[g.nowid].identity.defense +=g.nowDEF
                        g.players[g.nowid].identity.defense = min(g.players[g.nowid].identity.defense, g.players[g.nowid].identity.maxdefense)
                    lastAct = lastAction(0, g.nowDEF, 0,0, [])
                    if g.players[g.nowid].identity.idx == 8:
                        g.players[g.nowid].identity.canCombo = 0
                    g.nowDEF = 0
                elif select == 3: # basic mov cards
                    # choose a basic card from hand
                    g.USEMOVBASIC()
                    dir = g.chooseMovingDir()
                    if g.players[g.nowid].identity.idx == 4 and 153 in g.players[g.nowid].metamorphosis:
                        K = g.players[g.nowid].identity.spendKIforATK(g)
                        if K>3 or K<0:
                            g.cheating()
                        if K > g.players[g.nowid].identity.KI_TOKEN:
                            g.cheating()
                        g.players[g.nowid].identity.KI_TOKEN -= K
                            
                        g.nowMOV += K
                    through = g.moveCharacter( dir, g.nowMOV)
                    if through:
                        if g.players[1-g.nowid].identity.idx == 3 and g.players[1-g.nowid].identity.identity == 3 and 149 in g.players[1-g.nowid].metamorphosis:
                            g.drawCard( 1-g.nowid)
                        elif g.players[g.nowid].identity.idx == 3 and g.players[g.nowid].identity.identity == 3 and  149 in g.players[g.nowid].metamorphosis:
                            g.drawCard( g.nowid)
                        elif g.players[1-g.nowid].identity.idx == 1 and 141 in g.players[1-g.nowid].metamorphosis:
                            g.putPosion( g.nowid)
                        elif g.players[g.nowid].identity.idx == 1 and  141 in g.players[g.nowid].metamorphosis:
                            g.putPosion( 1-g.nowid)
                    lastAct = lastAction(0, 0,g.nowMOV, 0,[])
                    if g.players[g.nowid].identity.idx == 6 and 161 in g.players[g.nowid].metamorphosis:
                        g.players[g.nowid].identity.moveTantacle(g, g.nowMOV//2, 0)
                    if g.players[g.nowid].identity.idx == 8:
                        g.players[g.nowid].identity.canCombo = 0
                    g.nowMOV = 0
                elif select == 4: # use a skill
                    # choose a skill card from hand
                    
                    card = g.USESKILL()
                    if (card-11)%12 >=9:
                        g.cheating()
                    # print(card)
                    # if is dorothy
                    if g.players[g.nowid].identity.idx == 8 and g.players[g.nowid].identity.canCombo:
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
                            t = 1
                            for m in g.players[g.nowid].metamorphosis:
                                if m == 172:
                                    t+=1
                            g.players[g.nowid].identity.COMBO_TOKEN += t
                            
                            if 170 in g.players[g.nowid].metamorphosis and lastAct.useskill != []:
                                if (card-11%3)+1 > lastAct.useskill[0][1]:
                                    g.players[g.nowid].identity.COMBO_TOKEN += 1
                            g.players[g.nowid].identity.COMBO_TOKEN = min(12, g.players[g.nowid].identity.COMBO_TOKEN)
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
                            if g.players[g.nowid].identity.idx == 8:
                                g.players[g.nowid].identity.canCombo = 1
                    triggerCardSkill(g, g.nowUsingCardID, level)
                    if g.players[g.nowid].identity.idx == 8 and 171 in g.players[g.nowid].metamorphosis:
                        total = 0
                        u = g.nowUsingCardID
                        while 1:
                            d = g.dropCardFromHand()
                            if d == -1:
                                break
                            basic =[7,8,9,10]
                            if g.players[1-g.nowid].identity.idx == 7 and 168 not in g.players[1-g.nowid].metamorphosis:
                                basic.append(134)
                            if d not in basic:
                                g.cheating()
                            if g.players[g.nowid].hand[card] in [10,134]:
                                total += 1 
                            else:
                                total += basic-6 
                            if g.players[g.nowid].hand[card] == 134:
                                eneragy = 1
                                for i in range(len(g.players[1-g.nowid].metamorphosis)):
                                    if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                                        eneragy+=1
                                g.players[1-g.nowid].identity.energy += eneragy
                        s = g.status
                        g.status = state.MOVE_TARGET
                        lr = svr.connectBot(g.nowid, 'int8_t', g)
                        if lr == 0 or abs(lr) >total:
                            g.cheating()
                        if g.players[1-g.nowid].locate+lr > 9 or g.players[1-g.nowid].locate+lr < 1:
                            g.cheating()
                        if g.players[1-g.nowid].locate+lr == g.players[g.nowid].locate:
                            g.cheating()
                        if (g.players[1-g.nowid].locate>g.players[g.nowid].locate and g.players[1-g.nowid].locate+lr < g.players[g.nowid].locate )or \
                            (g.players[1-g.nowid].locate<g.players[g.nowid].locate and g.players[1-g.nowid].locate+lr > g.players[g.nowid].locate):
                            if g.players[1-g.nowid].identity.idx == 3 and g.players[1-g.nowid].identity.identity == 3 and 149 in g.players[1-g.nowid].metamorphosis:
                                g.drawCard( 1-g.nowid)
                            elif g.players[g.nowid].identity.idx == 3 and g.players[g.nowid].identity.identity == 3 and  149 in g.players[g.nowid].metamorphosis:
                                g.drawCard( g.nowid)
                            elif g.players[1-g.nowid].identity.idx == 1 and 141 in g.players[1-g.nowid].metamorphosis:
                                g.putPosion( g.nowid)
                            elif g.players[g.nowid].identity.idx == 1 and  141 in g.players[g.nowid].metamorphosis:
                                g.putPosion( 1-g.nowid)
                        g.players[1-g.nowid].locate+=lr
                        g.status = s 
                        g.nowUsingCardID = u
                        
                            
                    g.nowUsingCardID = 0
                elif select == 5: # use a special card
                    card = g.USESKILL()
                    if (card-11)%12 < 9:
                        g.cheating()
                    
                    g.nowUsingCardID = card
                    triggerCardSkill(g, g.nowUsingCardID, 0)
                    g.nowUsingCardID = 0
                    pass
                elif select == 6: # buy a card
                    s = g.status
                    g.status = state.BUY_CARD_TYPE
                    ct = svr.connectBot(g.nowid, "int32_t", g)
                    g.status = s
                    if(ct not in [-1,-2,-3,1,2,3,4,5,6,7,8,9,10]):
                        g.cheating()
                    if(ct<0):
                        if ct == -1:
                            g.players[g.nowid].buyATKCard(g)
                        if ct == -2:
                            g.players[g.nowid].buyDEFCard(g)
                        if ct == -3:
                            g.players[g.nowid].buyMOVCard(g)
                    else:
                        lv = (ct-1)%3+1
                        locate = (ct-1) // 3
                        if len(g.basicBuyDeck[ct-1]) == 0:
                            g.cheating()
                        pz = BASIC_PRIZE[locate][lv-1]
                        if g.players[g.nowid].identity.energy < pz:
                            g.cheating()
                        g.players[g.nowid].identity.energy -= pz
                        cd = g.basicBuyDeck[ct-1][0]
                        del g.basicBuyDeck[ct-1][0]
                        g.players[g.nowid].graveyard.append(cd)
                    if g.players[1-g.nowid].identity.idx == 9 and ct in g.players[1-g.nowid].identity.destiny_TOKEN_locate :
                        g.players[1-g.nowid].identity.triggerDestiny(g, ct)
                    if g.players[1-g.nowid].identity.idx == 9 and 174 in g.players[1-g.nowid].metamorphosis:
                        for loc in g.players[1-g.nowid].identity.destiny_TOKEN_locate:
                            if loc == -3:
                                if ct == loc:
                                    g.lostLife(g.nowid, 1)
                elif select == 7: # metamorphosis
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
                elif select == 8: # charactor special move
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
                        g.players[g.nowid].identity.canCombo = 0
    
            # end phase
            g.players[g.nowid].identity.energy = 0
            g.nowATK = 0
            g.nowDEF = 0
            g.nowMOV = 0
            g.nowUsingCardID = 0
            lastAct = lastAction()
            for i in range(len(g.players[g.nowid].usecards)):
                if g.players[g.nowid].usecards[i] not in [14,15,16,
                                                          45,
                                                          78,79,80,81,82,
                                                          122,123,124]:
                    g.players[g.nowid].graveyard.append(g.players[g.nowid].usecards[i])
                    if g.players[g.nowid].usecards[i] == 134:
                        eneragy = 1
                        for i in range(len(g.players[1-g.nowid].metamorphosis)):
                            if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                                eneragy+=1
                        g.players[1-g.nowid].identity.energy += eneragy
            for i in range(len(g.players[g.nowid].usecards)-1, -1, -1):
                if g.players[g.nowid].usecards[i] not in [14,15,16,
                                                          45,
                                                          78,79,80,81,82,
                                                          122,123,124]:
                    del g.players[g.nowid].usecards[i]
                else:
                    i+=1
            for i in range(len(g.players[g.nowid].hand)):
                # if g.players[g.nowid].hand[i] in []:
                #     i+=1
                #     continue
                g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[i])
                # if g.players[g.nowid].hand[i] == 134:
                #     eneragy = 1
                #     for i in range(len(g.players[1-g.nowid].metamorphosis)):
                #         if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                #             eneragy+=1
                #     g.players[1-g.nowid].identity.energy += eneragy
                if g.players[g.nowid].hand[i] in [131, 132, 133]:
                    posion = g.players[g.nowid].hand[i]-131
                    for i in range(len(g.players[1-g.nowid].metamorphosis)):
                        if g.players[1-g.nowid].metamorphosis[i] == 142:
                            posion+=1
                    g.lostLife( g.nowid, posion)
            for i in range(len(g.players[g.nowid].hand)):
                del g.players[g.nowid].hand[0]
            if g.players[g.nowid].identity.idx == 2:
                g.players[g.nowid].identity.usedmeta1 = 0
                g.players[g.nowid].identity.usedmeta2 = 0
            elif g.players[g.nowid].identity.idx == 3:
                g.players[g.nowid].identity.riseBasic = 0
            elif g.players[g.nowid].identity.idx == 6:
                if 92 in g.players[g.nowid].metamorphosis:
                    g.players[g.nowid].identity.life += 2
                    g.players[g.nowid].identity.life = min(g.players[g.nowid].identity.maxlife, g.players[g.nowid].identity.life)
                if 93 in g.players[g.nowid].metamorphosis:
                    g.lostLife(g.nowid, 1)
            cardNum = 6
            if g.players[g.nowid].identity.idx == 4 and g.players[g.nowid].identity.KI_TOKEN > 0 and g.players[g.nowid].identity.extraCard > 0:
                add = g.players[g.nowid].identity.spendKIforDraw(g)
                if add > g.players[g.nowid].identity.extraCard or add < 0:
                    g.cheating()
                if add > g.players[g.nowid].identity.KI_TOKEN:
                    g.cheating()
                g.players[g.nowid].identity.KI_TOKEN -= add
                cardNum += add
                g.players[g.nowid].identity.extraCard = 0
            if g.players[1-g.nowid].identity.idx == 9 and 175 in g.players[1-g.nowid].metamorphosis:
                top2 = g.players[g.nowid].deck[:2]
                for i in range(1, -1, -1):
                    if top2[i] <= 10:
                        locateFrom = top2[i]
                    elif top2[i] not in [131, 132,133,134]:
                        locateFrom = -((((top2[i]-11)%12) // 3) + 1)
                    else:
                        continue
                    if locateFrom == 4:
                        continue
                    for l in g.players[1-g.nowid].identity.destiny_TOKEN_locate:
                        g.lostLife(g.nowid, 1)
                        g.players[g.nowid].graveyard.append(g.players[g.nowid].deck[i])
                        del g.players[g.nowid].deck[i]
            for _ in range(cardNum):
                g.drawCard(g.nowid)
            if g.players[g.nowid].identity.idx == 3 and g.players[g.nowid].identity.restartTurn > 0:
                g.players[g.nowid].identity.restartTurn -= 1
                while(len(g.players[g.nowid].hand) > 4):
                    id = g.dropCardFromHand()
                    g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[id])
                    if g.players[g.nowid].hand[id] == 134:
                        eneragy = 1
                        for i in range(len(g.players[1-g.nowid].metamorphosis)):
                            if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                                eneragy+=1
                        g.players[1-g.nowid].identity.energy += eneragy
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
            if g.players[g.nowid].identity.idx == 4 and g.players[g.nowid].identity.extraDraw == 4:
                for _ in range(g.players[g.nowid].identity.extraDraw):
                    g.drawCard(g.nowid)
                g.players[g.nowid].identity.extraDraw = 0
            if g.players[g.nowid].identity.idx == 4 and 152 in g.players[g.nowid].metamorphosis:
                s = g.status
                g.status = state.DROP_ONE_DRAW_ONE
                id = svr.connectBot(g.nowid, 'int32_t', g)
                if id >= len(g.players[g.nowid].hand) or id < 0:
                    # cheat
                    g.cheating()
                id -= 1
                if(id != -1):
                    g.players[g.nowid].graveyard.append(g.players[g.nowid].hand[id])
                    if g.players[g.nowid].hand[id] == 134:
                        eneragy = 1
                        for i in range(len(g.players[1-g.nowid].metamorphosis)):
                            if g.players[1-g.nowid].metamorphosis[i] in [166,167,168]:
                                eneragy+=1
                        g.players[1-g.nowid].identity.energy += eneragy
                    if g.players[g.nowid].hand[id] in [131, 132, 133]:
                        posion = g.players[g.nowid].hand[id]-131
                        for i in range(len(g.players[1-g.nowid].metamorphosis)):
                            if g.players[1-g.nowid].metamorphosis[i] == 142:
                                posion+=1
                        g.lostLife( g.nowid, posion)    
                    del g.players[g.nowid].hand[id]
                    g.drawCard(g.nowid)
                g.status = s
            if g.players[g.nowid].identity.idx == 5:
                g.players[g.nowid].identity.useDefenseAsATK = 0
                g.players[g.nowid].identity.useMoveTarget = 0
                for m in g.players[g.nowid].metamorphosis:
                    if m == 158:
                        g.players[g.nowid].identity.defense += 2
                        g.players[g.nowid].identity.defense = min(g.players[g.nowid].identity.maxdefense, g.players[g.nowid].identity.defense)
            g.nowid = 1-g.nowid

            # update screen
    finally:    
        svr.close()
        if root is not None:
            root.quit()
        print('Shutting down server...')
        
if __name__ == "__main__":
    # import game as _game

    # _game.svr = _game.server()
    
    main()