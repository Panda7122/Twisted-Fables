import socket
import random
from typedef import *
from simulator import *
import copy
host = None
ip = None
port = 8080
server_socket = None
def initServer():
    global server_socket, host, ip
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    ip = socket.gethostbyname(host)       
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f"Server started and listening on host {host}({ip}) port {port}")
def lose(g:game, bot1:socket, bot2:socket):
    for p in range(2):
        if g.players[p].life <= 0:
            print(f"Game over. player {2-p} WIN.")
            bot1.close()
            bot2.close()
            server_socket.close()
            exit()
def cheating(g:game, bot1:socket, bot2:socket):
    g.nowPlayer.life = 0
    lose(g, bot1, bot2)
def hideGameStatus(g:game):
    retg = copy.deepcopy(g)
    for i in range(retg.players[0].deck.SIZE):
        retg.players[0].deck[i] = -1
    for i in range(retg.players[1].deck.SIZE):
        retg.players[0].deck[i] = -1
    for i in range(retg.nowTarget.hand.SIZE):
        retg.players[0].hand[i] = -1
    return retg
def getRange(g:game):
    return abs(g.players[0].locate[1] - g.players[1].locate[1])
def lostLife(g:game, target:int, atk:int, bot1:socket, bot2:socket):
    for i in range(g.players[target].usecards.SIZE):
        if g.players[target].usecards[i] == 80:
            return
    if g.players[target].life<=atk:
        g.players[target].life = 0
        # target lose
        lose(g, bot1, bot2)
        pass
    g.players[target].life -= atk
def damage(g:game, target:int,  distanse:int, atk:int, bot1:socket, bot2:socket):
    for i in range(g.players[target].usecards.SIZE):
        if g.players[target].usecards[i] == 80:
            return
    if(getRange(g)<=distanse):
        dam = atk - g.players[target].defense
        if dam <= 0:
            g.players[target].defense -= atk
        else:
            g.players[target].defense = 0
            if g.players[target].life < dam:
                g.players[target].life = 0
                # target lose
                lose(g, bot1, bot2)
            g.players[target].life -= dam
            getDamage(g, target, dam)
    else:
        cheating(g, bot1, bot2)
    return dam
def setLocate(g:game, target:int, locate:int, bot1:socket, bot2:socket):
    if locate > 9 or locate < 1:
        # cheat
        cheating(g, bot1, bot2)                    
    g.players[target].locate[1] = locate
def getDamage(g:game,target:int,  dam:int, bot1:socket, bot2:socket):
    #TODO done get Damage
    c = g.players[target].character
    if c == 0: # 小紅帽
        pass
    elif c == 1: # 白雪公主
        pass
    elif c == 2: # 睡美人
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
        for i in range(g.nowTarget.usecards.SIZE):
            if g.nowTarget.usecards[i] == 45:
                for _ in range(min(g.nowTarget.sleepingBeauty.dayNightmareDrawRemind, dam)):
                    drawCard(g, target)
                g.nowTarget.sleepingBeauty.dayNightmareDrawRemind-=min(g.nowTarget.sleepingBeauty.dayNightmareDrawRemind, dam)
        pass
    elif target == 3: # 愛麗絲
        pass
    elif target == 4: # 花木蘭
        pass
    elif target == 5: # 輝夜姬
        pass
    elif target == 6: # 美人魚
        pass
    elif target == 7: # 火柴女孩
        pass
    elif target == 8: # 桃樂絲
        pass
    elif target == 9: # 山魯佐德
        pass

def settlementContinue(g:game, bot1:socket, bot2:socket):
    c = g.nowPlayer.character
    bot = bot1 if g.now_turn_player_id == 0 else bot2
    if c == 0: # 小紅帽
        for i in range(g.nowPlayer.usecards.SIZE):
            if g.nowPlayer.usecards[i] in [14,15,16]:
                if g.nowPlayer.defense>=0:
                    damage(g,g.targe, g.nowPlayer.usecards[i]-13, 2*(g.nowPlayer.usecards[i]-13), bot1, bot2)
    elif c == 1: # 白雪公主
        pass
    elif c == 2: # 睡美人
        pass
    elif c == 3: # 愛麗絲
        pass
    elif c == 4: # 花木蘭
        pass
    elif c == 5: # 輝夜姬
        for i in range(g.nowPlayer.usecards.SIZE):
            if g.nowPlayer.usecards[i] in [78,79]:
                o = g.nowPlayer.usecards[i+1]-6 # the basic move card level
                if getRange(g)>4-o:
                    damage(g, 1-g.now_turn_player_id, 18, 2*(g.nowPlayer.usecards[i]-76))
            elif g.nowPlayer.usecards[i] == 81:
                if g.nowPlayer.defense > g.players[1-g.now_turn_player_id].defense:
                    lostLife(g, 1-g.now_turn_player_id, g.nowPlayer.defense-g.players[1-g.now_turn_player_id].defense)
            elif g.nowPlayer.usecards[i] == 82:
                g.status = state.SET_TARGET_LOCATE_TO_NEARBY
                bot.send(hideGameStatus(g).pack())
                loc = int.from_bytes(bot.recv(1), "little", True)
                if abs(g.nowPlayer.locate[1] - loc) != 1 and g.nowTarget.locate[1] != loc:
                    # cheat
                    cheating(g, bot1, bot2)
                setLocate(g, 1-g.now_turn_player_id, loc, bot1, bot2)
                damage(g, 1-g.now_turn_player_id, 18, 3, bot1, bot2)
        pass
    elif c == 6: # 美人魚
        pass
    elif c == 7: # 火柴女孩
        pass
    elif c == 8: # 桃樂絲
        pass
    elif c == 9: # 山魯佐德
        pass
    return

def setupCharacter(player):
    if player.character == 0: # 小紅帽
        player.maxlife = 30
        player.life= player.maxlife
        player.maxdefense = 6
        player.defense = 0 
        player.energy = 0
        player.specialGate = 15     
    elif player.character == 1: # 白雪公主 
        player.maxlife = 34
        player.life= player.maxlife
        player.maxdefense = 6
        player.defense = 0 
        player.energy = 0
        player.specialGate = 17  
    elif player.character == 2: # 睡美人
        player.maxlife = 42
        player.life= player.maxlife
        player.maxdefense = 6
        player.defense = 0 
        player.energy = 0
        player.specialGate = 21
    elif player.character == 3: # 愛麗絲
        player.maxlife = 32
        player.life= player.maxlife
        player.maxdefense = 6
        player.defense = 0 
        player.energy = 0
        player.specialGate = 16  
    elif player.character == 4: # 花木蘭
        player.maxlife = 34
        player.life= player.maxlife
        player.maxdefense = 3
        player.defense = 0 
        player.energy = 0
        player.specialGate = 17
    elif player.character == 5: # 輝夜姬
        player.maxlife = 32
        player.life= player.maxlife
        player.maxdefense = 6
        player.defense = 0 
        player.energy = 0
        player.specialGate = 16 
    elif player.character == 6: # 美人魚
        player.maxlife = 36
        player.life= player.maxlife
        player.maxdefense = 3
        player.defense = 0 
        player.energy = 0
        player.specialGate = 18
    elif player.character == 7: # 火柴女孩
        player.maxlife = 36
        player.life= player.maxlife
        player.maxdefense = 6
        player.defense = 0 
        player.energy = 0
        player.specialGate = 18
    elif player.character == 8: # 桃樂絲
        player.maxlife = 40
        player.life= player.maxlife
        player.maxdefense = 6
        player.defense = 0 
        player.energy = 0
        player.specialGate = 20
    elif player.character == 9: # 山魯佐德
        player.maxlife = 36
        player.life= player.maxlife
        player.maxdefense = 6
        player.defense = 0 
        player.energy = 0
        player.specialGate = 18
def shuffle(v:vector):
    random.shuffle(v.array[:v.SIZE])
def countDestinyTOKEN(g:game):
    ret = 0
    ret += g.players[1-g.now_turn_player_id].attackSkill.destiny_TOKEN
    ret += g.players[1-g.now_turn_player_id].defenseSkill.destiny_TOKEN
    ret += g.players[1-g.now_turn_player_id].moveSkill.destiny_TOKEN
    for d in range(10):
        ret += g.basicBuyDeck[d].destiny_TOKEN
    return ret
def drawCard(g:game, target):
    if len(g.players[target].deck) == 0:
        for i in range(g.players[target].graveyard.SIZE):
            g.players[target].deck.append(g.players[target].graveyard[i])
        for i in range(g.players[target].graveyard.SIZE):
            del g.players[target].graveyard[i]
        shuffle(g.players[target].deck)
    top = g.players[target].deck[0]
    del g.players[target].deck[0]
    g.players[target].hand.append(top)
def getlastcard(g:game):
    return g.nowPlayer.usecards[len(g.nowPlayer.usecards)-2]
def initializeGame(g:game, bot1:socket, bot2:socket):
    # initialize
        # init metadata
        g.nowATK = 0
        g.nowDEF = 0
        g.nowMOV = 0
        g.nowUsingCardID = 0
        # which character client implement 
        bot1CharList = bot1.recv(10)
        bot1CharList = [i for i,v in enumerate(bot1CharList) if v==1]
        bot2CharList = bot2.recv(10)
        bot2CharList = [i for i,v in enumerate(bot2CharList) if v==1]
        # random choice charactor
        while(g.players[0].character == g.players[1].character):
            g.players[0].character = random.choice(bot1CharList)
            g.players[1].character = random.choice(bot2CharList)
        # set up life, defense, ... etc.
        setupCharacter(g.players[0])
        setupCharacter(g.players[1])
        # initialize player's location
        g.players[0].locate[0] = 0
        g.players[0].locate[1] = 4
        g.players[1].locate[0] = 0
        g.players[1].locate[1] = 6
        # set up player's init_deck and skill_buy_deck
        for p in range(2):
            # initialize init_deck
            g.players[p].deck.append(11+(g.players[p].character-1)*12+0) # lv1 attack skill
            g.players[p].deck.append(11+(g.players[p].character-1)*12+1) # lv1 defense skill
            g.players[p].deck.append(11+(g.players[p].character-1)*12+2) # lv1 move skill
            for _ in range(3):
                g.players[p].deck.append(1) # lv1 attack*3
                g.players[p].deck.append(4) # lv1 defense*3
                g.players[p].deck.append(7) # lv1 move*3
            # initialize skill_buy_deck
            for i in [1,2]:
                for _ in range(i+1):# lv2*2, lv3*3
                    g.players[p].attackSkill.append(11+(g.players[p].character-1)*12 + i) # lv.i attack skill
                    g.players[p].defenseSkill.append(11+(g.players[p].character-1)*12 + i+3) # lv.i defense skill
                    g.players[p].moveSkill.append(11+(g.players[p].character-1)*12 + i+6) # lv.i move skill
                if i == 1: # metamorphosis 1
                    if g.players[p].character <= 6:# before 火柴女孩
                        g.players[p].attackSkill.append(135 + (g.players[p].character)*4 + 0)
                        g.players[p].defenseSkill.append(135 + (g.players[p].character)*4 + 1)
                        g.players[p].moveSkill.append(135 + (g.players[p].character)*4 + 2)
                    elif g.players[p].character == 7:# 火柴女孩
                        g.players[p].attackSkill.append(135 + (g.players[p].character)*4 + 0)
                        g.players[p].defenseSkill.append(135 + (g.players[p].character)*4 + 1)
                        g.players[p].moveSkill.append(135 + (g.players[p].character)*4 + 2)
                    else:# after 火柴女孩
                        g.players[p].attackSkill.append(169 + (g.players[p].character-8)*4 + 0)
                        g.players[p].defenseSkill.append(169 + (g.players[p].character-8)*4 + 1)
                        g.players[p].moveSkill.append(169 + (g.players[p].character-8)*4 + 2)
                else: # metamorphosis 2
                    if g.players[p].character <= 6:# before 火柴女孩
                        g.players[p].attackSkill.append(135 + (g.players[p].character)*4 + 3)
                        g.players[p].defenseSkill.append(135 + (g.players[p].character)*4 + 3)
                        g.players[p].moveSkill.append(135 + (g.players[p].character)*4 + 3)
                    elif g.players[p].character == 7:# 火柴女孩
                        g.players[p].attackSkill.append(135 + (g.players[p].character)*4 + 3)
                        g.players[p].defenseSkill.append(135 + (g.players[p].character)*4 + 4)
                        g.players[p].moveSkill.append(135 + (g.players[p].character)*4 + 5)
                    else:# after 火柴女孩
                        g.players[p].attackSkill.append(169 + (g.players[p].character-8)*4 + 3)
                        g.players[p].defenseSkill.append(169 + (g.players[p].character-8)*4 + 3)
                        g.players[p].moveSkill.append(169 + (g.players[p].character-8)*4 + 3)
            # initialize special skill
            for i in range(9,12):
                g.players[p].specialDeck.append(11+(g.players[p].character-1)*12 + i)
        # initialize basic buy deck
        for i in range(10):
            # 1,4,7 is lv1基本牌，take 3 for each player init deck
            for j in range(18 if i not in [1,4,7] else 12):  
                g.basicBuyDeck[i].cards[j] = i+1
            g.basicBuyDeck[i].destiny_TOKEN = 0 # for 山魯佐德's TOKEN
        # shuffle init_deck
        shuffle(g.players[0].deck)
        shuffle(g.players[1].deck)
        
        #reset graveyard, usecards, metamorphosis
        for p in range(2):
            g.players[p].usecards.SIZE = 0
            g.players[p].graveyard.SIZE = 0
            g.players[p].metamorphosis.SIZE = 0
        # charactor special rule
        for p in range(2):
            g.now_turn_player_id = p
            c = g.players[p].character
            bot = bot1 if p == 0 else bot2
            if c == 0: # 小紅帽
                pass
            elif c == 1: # 白雪公主
                g.players[p].snowWhite.remindPosion.SIZE = 0
                for _ in range(6):
                    g.players[p].snowWhite.remindPosion.append(131)
                for _ in range(6):
                    g.players[p].snowWhite.remindPosion.append(132)
                for _ in range(6):
                    g.players[p].snowWhite.remindPosion.append(133)
            elif c == 2: # 睡美人
                g.players[p].sleepingBeauty.AWAKEN = 0
                g.players[p].sleepingBeauty.AWAKEN_TOKEN = 0
                g.players[p].sleepingBeauty.dayNightmareDrawRemind = 0
            elif c == 3: # 愛麗絲
                g.status = state.CHOOSE_IDENTITY
                bot.send(hideGameStatus(g).pack())
                ident = int.from_bytes(bot.recv(1), "little", True)
                if ident not in [1,2,3]:
                    return -1
                g.player[p].alice.identity = ident
                pass
            elif c == 4: # 花木蘭
                g.players[p].mulan.KI_TOKEN = 0
            elif c == 5: # 輝夜姬
                pass
            elif c == 6: # 美人魚
                g.status = state.CHOOSE_TENTACLE_LOCATION
                bot.send(hideGameStatus(g).pack())
                location = int.from_bytes(bot.recv(4), "little", True)
                if location <1 or location > 9:
                    return -1
                g.tentacle_TOKEN_locate.append(location)
            elif c == 7: # 火柴女孩
                g.players[p].matchGirl.remindMatch = 12
            elif c == 8: # 桃樂絲
                g.status = state.CHOOSE_SPECIAL_CARD
                bot.send(hideGameStatus(g).pack())
                card = int.from_bytes(bot.recv(4), "little", True)
                for i in range(3):
                    if g.players[p].specialDeck[i] == card:
                        del g.players[p].specialDeck[i]
                        break
                if len(g.players[p].specialDeck) == 3:
                    # error
                    return -1
                g.players[p].deck.append(card)
                shuffle(g.players[p].deck)
                g.players[p].dorothy.COMBO_TOKEN = 0
                g.players[p].dorothy.canCombo = False
            elif c == 9: # 山魯佐德
                g.players[1-g.now_turn_player_id].attackSkill.destiny_TOKEN=0
                g.players[1-g.now_turn_player_id].defenseSkill.destiny_TOKEN=0
                g.players[1-g.now_turn_player_id].moveSkill.destiny_TOKEN=0
                for d in range(10):
                    g.basicBuyDeck[d].destiny_TOKEN=0
                for _ in range(3):
                    g.status = state.CHOOSE_SPECIAL_CARD
                    bot.send(hideGameStatus(g).pack())
                    gtmp = game()
                    gtmp.unpack(bot.recv(cstruct.sizeof(game)))
                    if gtmp.now_tuen_player_id != g.gtmp.now_tuen_player_id:
                        return -1
                    if countDestinyTOKEN(gtmp) == countDestinyTOKEN(g)+1:
                        g = gtmp
                    else:
                        # error
                        return -1
        # draw card
        g.now_turn_player_id = random.randint(0,1)
        for _ in range(4):
            drawCard(g,g.now_turn_player_id)
        for _ in range(6):
            drawCard(g, 1-g.now_turn_player_id)
def chooseMove(g:game, bot1:socket, bot2:socket):
    s = g.status
    bot = bot1 if g.now_turn_player_id == 0 else bot2
    g.status = state.CHOOSE_MOVE
    bot.send(hideGameStatus(g).pack())
    ret = int.from_bytes(bot.recv(4), "little", True)
    g.status = s
    return ret
def chooseCardFromHandorGraveyard(g:game, bot1:socket, bot2:socket):
    s = g.status
    bot = bot1 if g.now_turn_player_id == 0 else bot2
    g.status = state.REMOVE_HG
    bot.send(hideGameStatus(g).pack())
    ret = int.from_bytes(bot.recv(4), "little", True)
    if ret == 0:
        # cheat
        cheating(g, bot1, bot2)
    sign = 1 if ret > 0 else 0
    ret = abs(ret)-1
    if sign:
        if ret >= g.nowPlayer.hand.SIZE:
            # cheat
            cheating(g, bot1, bot2)
    else:
        if ret >= g.nowPlayer.graveyard.SIZE:
            # cheat
            cheating(g, bot1, bot2)
    g.status = s
    return (sign, ret)
def dropCardFromHand(g:game, bot1:socket, bot2:socket):
    s = g.status
    bot = bot1 if g.now_turn_player_id == 0 else bot2
    g.status = state.DROP_H
    bot.send(hideGameStatus(g).pack())
    ret = int.from_bytes(bot.recv(4), "little", True)
    if ret >= g.nowPlayer.hand.SIZE or ret <= 0:
        # cheat
        cheating(g, bot1, bot2)
    ret -= 1
    g.status = s
    return ret
def knockback(g:game, bot1:socket, bot2:socket, dis):
    aloc = g.nowPlayer.locate[1]
    bloc = g.nowTarget.locate[1]
    if bloc-aloc > 0:
        g.nowTarget.locate[1] = min(9, g.nowTarget.locate[1]+dis)
    elif bloc-aloc < 0:
        g.nowTarget.locate[1] = max(9, g.nowTarget.locate[1]-dis)
    else:
        cheating(g, bot1, bot2)
    return
def dropDeck(g:game, target:int, bot1:socket, bot2:socket):
    if len(g.players[target].deck) == 0:
        for i in range(g.players[target].graveyard.SIZE):
            g.players[target].deck.append(g.players[target].graveyard[i])
        for i in range(g.players[target].graveyard.SIZE):
            del g.players[target].graveyard[i]
        shuffle(g.players[target].deck)
    top = g.players[target].deck[0]
    del g.players[target].deck[0]
    g.players[target].graveyard.append(top)
    return
def USEATKBASIC(g:game, bot1:socket, bot2:socket):
    s = g.status
    bot = bot1 if g.now_turn_player_id == 0 else bot2
    g.status = state.USE_ATK
    g.nowATK = 0
    basicATK = [1,2,3]
    if g.nowTarget.charactor == 7 and not vectorHave(g.nowTarget.metamorphosis, [166]):
        basicATK.append(134)
    while True:
        
        bot.send(hideGameStatus(g).pack())
    
        c = int.from_bytes(bot.recv(4), "little", True)
        if c >= g.nowPlayer.hand.SIZE or c < 0 or g.nowPlayer.hand[c] not in basicATK:
            # cheat
            cheating(g, bot1, bot2)
        if c == 0:
            break
        
        g.nowPlayer.usecards.append(g.nowPlayer.hand[c])
        g.nowATK += g.nowPlayer.hand[c] if g.nowPlayer.hand[c] !=134 else 1
        if g.nowPlayer.hand[c] !=134:
            g.nowPlayer.energy+=g.nowPlayer.hand[c]
        del g.nowPlayer.hand[c]
    g.status = s
def USEDEFBASIC(g:game, bot1:socket, bot2:socket):
    s = g.status
    bot = bot1 if g.now_turn_player_id == 0 else bot2
    g.status = state.USE_DEF
    g.nowDEF = 0
    basicDEF = [1,2,3]
    if g.nowTarget.charactor == 7 and not vectorHave(g.nowTarget.metamorphosis, [167]):
        basicDEF.append(134)
    while True:
        bot.send(hideGameStatus(g).pack())
        c = int.from_bytes(bot.recv(4), "little", True)
        if c >= g.nowPlayer.hand.SIZE or c < 0 or g.nowPlayer.hand[c] not in basicDEF:
            # cheat
            cheating(g, bot1, bot2)
        if c == 0:
            break
        g.nowPlayer.usecards.append(g.nowPlayer.hand[c])
        g.nowDEF += (g.nowPlayer.hand[c] - 3) if g.nowPlayer.hand[c] !=134 else 1
        if g.nowPlayer.hand[c] !=134:
            g.nowPlayer.energy+=(g.nowPlayer.hand[c] - 3)
        del g.nowPlayer.hand[c]
    g.status = s
def USEMOVBASIC(g:game, bot1:socket, bot2:socket):
    s = g.status
    bot = bot1 if g.now_turn_player_id == 0 else bot2
    g.status = state.USE_MOV
    g.nowMOV = 0
    basicMOV = [1,2,3]
    if g.nowTarget.charactor == 7 and not vectorHave(g.nowTarget.metamorphosis, [168]):
        basicMOV.append(134)
    while True:
        bot.send(hideGameStatus(g).pack())
        c = int.from_bytes(bot.recv(4), "little", True)
        if c >= g.nowPlayer.hand.SIZE or c < 0 or g.nowPlayer.hand[c] not in basicMOV:
            # cheat
            cheating(g, bot1, bot2)
        if c == 0:
            break
        g.nowPlayer.usecards.append(g.nowPlayer.hand[c])
        g.nowMOV += (g.nowPlayer.hand[c] - 6) if g.nowPlayer.hand[c] !=134 else 1
        if g.nowPlayer.hand[c] !=134:
            g.nowPlayer.energy+=(g.nowPlayer.hand[c] - 6)
        
        del g.nowPlayer.hand[c]
    g.status = s
def USESKILL(g:game, bot1:socket, bot2:socket):
    s = g.status
    bot = bot1 if g.now_turn_player_id == 0 else bot2
    g.status = state.USE_SKILL
    bot.send(hideGameStatus(g).pack())
    c = int.from_bytes(bot.recv(4), "little", True)
    skillC = [(g.nowPlayer.charactor*12+11+j) for j in range(9)]
    if c >= g.nowPlayer.hand.SIZE or c < 0 or g.nowPlayer.hand[c] not in skillC:
        # cheat
        cheating(g, bot1, bot2)
    
    g.nowUsingCardID = g.nowPlayer.hand[c]
    g.nowPlayer.usecards.append(g.nowPlayer.hand[c])
    del g.nowPlayer.hand[c]
    g.status = s
    return
def USEBASIC(g:game, bot1:socket, bot2:socket):
    s = g.status
    bot = bot1 if g.now_turn_player_id == 0 else bot2
    g.status = state.USE_BASIC
    bot.send(hideGameStatus(g).pack())
    c = int.from_bytes(bot.recv(4), "little", True)
    typeC = g.nowUsingCardID - 11 - 12*g.nowPlayer.charactor
    if typeC == [0,1,2]:
        basic = [1,2,3]
        if g.nowTarget.charactor == 7 and not vectorHave(g.nowTarget.metamorphosis, [166]):
            basic.append(134)
    elif typeC == [3,4,5]:
        basic = [4,5,6]
        if g.nowTarget.charactor == 7 and not vectorHave(g.nowTarget.metamorphosis, [167]):
            basic.append(134)
    elif typeC == [6,7,8]:
        basic = [7,8,9]
        if g.nowTarget.charactor == 7 and not vectorHave(g.nowTarget.metamorphosis, [168]):
            basic.append(134)
    if c >= g.nowPlayer.hand.SIZE or c < 0 or g.nowPlayer.hand[c] not in basic:
        # cheat
        cheating(g, bot1, bot2)
    g.status = s
    ret = g.nowPlayer.hand[c]
    g.nowPlayer.usecards.append(g.nowPlayer.hand[c])
    del g.nowPlayer.hand[c]
    return (ret-1)%3+1
def chooseMovingDir(g:game, bot1:socket, bot2:socket):
    s = g.status
    bot = bot1 if g.now_turn_player_id == 0 else bot2
    g.status = state.CHOOSE_MOVING_DIR
    bot.send(hideGameStatus(g).pack())
    c = int.from_bytes(bot.recv(1), "little", True)
    if c not in [0,1]:
        cheating(g, bot1, bot2)
    g.status = s
    return c
def moveCharactor(g:game, dir:int, dis:int):
    dif = (dir*2-1)*dis
    ret = False
    while g.nowPlayer.locate[1]+dif >9 or g.nowPlayer.locate[1]+dif<1:
        dis -=1
        dif = (dir*2-1)*dis
    if getRange(g)==dis:
        dis-=1
        dif = (dir*2-1)*dis
    elif getRange(g)>dis:
        ret = True
    g.nowPlayer.locate[1]+=dif
    return ret
def putPosion(g:game, target):
    if g.players[1-target].snowWhite.remindPosion.SIZE == 0:
        return
    now = g.players[1-target].snowWhite.remindPosion[0]
    g.nowPlayer.graveyard.append(now)
    g.players[1-target].snowWhite.remindPosion-=1
    posion = g.nowPlayer.usecards[i]-131
    for i in range(g.nowTarget.metamorphosis.SIZE):
        if g.nowTarget.metamorphosis[i] == 142:
            posion+=1
    lostLife(g, g.now_turn_player_id, posion)
def putTargetPosition(g:game, bot1:socket, bot2:socket):
    s = g.status
    bot = bot1 if g.now_turn_player_id == 0 else bot2
    g.status = state.PUTTARGETPOSITION
    bot.send(hideGameStatus(g).pack())
    loc = int.from_bytes(bot.recv(4), "little", True)
    card = getlastcard(g)
    if card in [29,30,31]:
        if loc not in [g.nowPlayer.locate[1]+1, g.nowPlayer.locate[1]-1] or loc<1 or loc>9:
            cheating(g, bot1, bot2)
    g.nowTarget.locate[1] = loc
def triggerCardSkill(g:game, bot1:socket, bot2:socket, cardID:int, level:int):
    bot = bot1 if g.now_turn_player_id == 0 else bot2
    
    if cardID in [11,12,13]: # 小紅帽
        if getRange(g)> cardID-10:
            cheating(g, bot1, bot2)
        damage(g, 1-g.now_turn_player_id, cardID-10, cardID-10+level, bot1, bot2)
    elif cardID in [14,15,16]: 
        if getRange(g)> cardID-13:
            cheating(g, bot1, bot2)
        damage(g, 1-g.now_turn_player_id, cardID-13, cardID-13, bot1, bot2)
        g.nowPlayer.defense+=1
        g.nowPlayer.defense = min(g.nowPlayer.maxdefense, g.nowPlayer.defense)
    elif cardID in [17,18,19]:
        if getRange(g)> cardID-16:
            cheating(g, bot1, bot2)
        damage(g, 1-g.now_turn_player_id, cardID-16, cardID-16, bot1, bot2)
        g.status = state.KNOCKBACK
        bot.send(hideGameStatus(g).pack())
        dis = int.from_bytes(bot.recv(4), "little", True)
        if dis > cardID-16 or dis < 0:
            cheating(g, bot1, bot2)
        knockback(g, bot1, bot2, dis)
    elif cardID in [23,24,25]: # 白雪公主
        if getRange(g)> 1:
            cheating(g, bot1, bot2)
        dam = damage(g, 1-g.now_turn_player_id, 1, cardID-22+level, bot1, bot2)
        if dam >=2 and vectorHave(g.nowPlayer.metamorphosis, [139]):
            putPosion(g, 1-g.now_turn_player_id)
        for _ in range(cardID-22):
            dropDeck(g, 1-g.now_turn_player_id, bot1, bot2)
    elif cardID in [26,27,28]:
        if getRange(g)> 1:
            cheating(g, bot1, bot2)
        damage(g, 1-g.now_turn_player_id, 1, cardID-25, bot1, bot2)
        s = g.status
        g.status = state.DEFPUSHPOSION
        bot.send(hideGameStatus(g).pack())
        p = int.from_bytes(bot.recv(4), "little", True)
        for _ in range(p):
            putPosion(g, 1-g.now_turn_player_id)
        g.status = s
    elif cardID in [29,30,31]:
        if getRange(g)> level+cardID-29:
            cheating(g, bot1, bot2)
        damage(g, 1-g.now_turn_player_id, level+cardID-29, cardID-28, bot1, bot2)
        putTargetPosition(g, bot1, bot2)
    elif cardID in [35,36,37]: # TODO 睡美人
        
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
    initServer()
    bot1, addr1 = server_socket.accept()
    print(f"BOT1 Connection accepted from {addr1}")
    bot2, addr2 = server_socket.accept()
    print(f"BOT2 Connection accepted from {addr2}")

    g = game()
    try:
        initializeGame(g, bot1, bot2)
        while 1:
            # start phase
            settlementContinue(g, bot1, bot2)
            # clean phase
            for i in range(g.nowPlayer.usecards.SIZE):
                g.nowPlayer.graveyard.append(g.nowPlayer.usecards[i])
                if g.nowPlayer.usecards[i] == 134:
                    eneragy = 1
                    for i in range(g.nowTarget.metamorphosis.SIZE):
                        if g.nowTarget.metamorphosis[i] in [166,167,168]:
                            eneragy+=1
                    g.nowTarget.energy += eneragy
                if g.nowPlayer.usecards[i] in [131, 132, 133]:
                    posion = g.nowPlayer.usecards[i]-131
                    for i in range(g.nowTarget.metamorphosis.SIZE):
                        if g.nowTarget.metamorphosis[i] == 142:
                            posion+=1
                    lostLife(g, g.now_turn_player_id, posion, bot1, bot2)
            for i in range(g.nowPlayer.usecards.SIZE):
                del g.nowPlayer.usecards[i]
            g.nowPlayer.defense = 0
            # TODO move phase
            moved:bool = False
            while True:
                bot = bot1 if g.now_turn_player_id == 0 else bot2
                select = chooseMove(g, bot1, bot2)
                if select == 0: # focus
                    # remove a card from hand/graveyard
                    if moved == False:
                        where, c = chooseCardFromHandorGraveyard(g, bot1, bot2)
                        if where: # hand
                            del g.nowPlayer.hand[c]
                        else: # graveyard
                            del g.nowPlayer.graveyard[c]
                        break
                    else:
                        # cheat
                        cheating(g, bot1, bot2)
                elif select == 1: # basic atk cards
                    # choose a basic card from hand
                    USEATKBASIC(g, bot1, bot2)
                    dam = damage(g, 1-g.now_turn_player_id, 1, g.nowATK)
                    if g.nowPlayer.character == 1 and dam >=2 and vectorHave(g.nowPlayer.metamorphosis, [139]):
                        putPosion(g, 1-g.now_turn_player_id)
                    g.nowATK = 0
                elif select == 2: # basic cards
                    # choose a basic card from hand
                    USEDEFBASIC(g, bot1, bot2)
                    g.nowPlayer.defense +=g.nowDEF
                    g.nowPlayer.defense = min(g.nowPlayer.defense, g.nowPlayer.maxdefense)
                    g.nowDEF = 0
                elif select == 3: # basic cards
                    # choose a basic card from hand
                    USEDEFBASIC(g, bot1, bot2)
                    dir = chooseMovingDir(g, bot1, bot2)
                    through = moveCharactor(g, dir, g.nowMOV)
                    if through:
                        if g.nowTarget.charactor == 3 and vectorHave(g.nowTarget.metamorphosis, [149]):
                            drawCard(g, 1-g.now_turn_player_id)
                        elif g.nowPlayer.charactor == 3 and vectorHave(g.nowPlayer.metamorphosis, [149]):
                            drawCard(g, g.now_turn_player_id)
                        elif g.nowTarget.charactor == 1 and vectorHave(g.nowTarget.metamorphosis, [141]):
                            putPosion(g, g.now_turn_player_id)
                        elif g.nowPlayer.charactor == 1 and vectorHave(g.nowTarget.metamorphosis, [141]):
                            putPosion(g, 1-g.now_turn_player_id)
                    g.nowMOV = 0
                elif select == 4: # use a skill
                    # choose a skill card from hand
                    card = USESKILL(g, bot1, bot2)
                    # if is dorothy
                    if g.nowPlayer.charactor == 8 and g.nowPlayer.dorothy.canCombo:
                        # ask combo
                        s = g.status
                        g.status = state.TRIGGER_COMBO
                        bot.send(hideGameStatus(g).pack())
                        trigger = int.from_bytes(bot.recv(1), "little", True)
                        g.status = s
                        if trigger not in [0,1]:
                            cheating(g, bot1, bot2)
                        if trigger == 0:
                            # choose a basic card from hand
                            level = USEBASIC(g, bot1, bot2)
                        else:
                            level = 0
                    else:
                        # choose a basic card from hand
                        level = USEBASIC(g, bot1, bot2)
                    triggerCardSkill(g, bot1, bot2, g.nowUsingCardID, level)
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
                    cheating(g, bot1, bot2)
                    pass
                move = True
                if g.nowPlayer.charactor == 8:
                    if select in [0,1,2,3,5,6]:
                        g.nowPlayer.dorothy.canCombo = 0
            # end phase
            g.nowPlayer.energy = 0
            g.nowATK = 0
            g.nowDEF = 0
            g.nowMOV = 0
            g.nowUsingCardID = 0
            for i in range(g.nowPlayer.hand.SIZE):
                if g.nowPlayer.hand[i] in []:
                    i+=1
                    continue
                g.nowPlayer.graveyard.append(g.nowPlayer.hand[i])
                if g.nowPlayer.usecards[i] == 134:
                    eneragy = 1
                    for i in range(g.nowTarget.metamorphosis.SIZE):
                        if g.nowTarget.metamorphosis[i] in [166,167,168]:
                            eneragy+=1
                    g.nowTarget.energy += eneragy
                if g.nowPlayer.usecards[i] in [131, 132, 133]:
                    posion = g.nowPlayer.usecards[i]-131
                    for i in range(g.nowTarget.metamorphosis.SIZE):
                        if g.nowTarget.metamorphosis[i] == 142:
                            posion+=1
                    lostLife(g, g.now_turn_player_id, posion)
            for i in range(g.nowPlayer.hand.SIZE):
                del g.nowPlayer.hand[i]
            for _ in range(6):
                drawCard(g, g.now_turn_player_id)
            g.now_turn_player_id = 1-g.now_turn_player_id
    finally:    
        bot1.close()
        bot2.close()
        print('Shutting down server...')
        server_socket.close()
if __name__ == "__main__":
    main()