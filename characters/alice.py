import sys 
sys.path.append("..")
from game import *
from characters.character import *
class aliceATKSkill(atkCard):
    def skill(self, g:game, level):
        ls = g.showhands(1-g.nowid, level+2)
        atk = self.level
        for x in ls:
            if x == -1:
                atk +=level
        st = set(ls)
        if -1 in st:
            st.remove(-1)
        g.damage(1-g.nowid, self.level, atk)
        g.players[g.nowid].identity.getFreeCard(g, list(st), 1)
        s = g.status 
        g.status = state.CHANGE_IDENTITY
        ch = svr.connectBot(g.nowid,"int8_t", g)
        if ch == 1:
            g.players[g.nowid].identity.identity = 1
        g.status = s
        pass
class aliceDEFSkill(defCard):
    def skill(self, g:game, level):
        where, c = g.chooseCardFromHandorGraveyard()
        if where: # hand
            del g.players[g.nowid].hand[c]
        else: # graveyard
            del g.players[g.nowid].graveyard[c]
        g.players[g.nowid].identity.getFreeCard(g, [i for i in range(1, 11) if (i-1)%3 < level], 2)
        
        s = g.status 
        g.status = state.CHANGE_IDENTITY
        ch = svr.connectBot(g.nowid,"int8_t", g)
        if ch == 1:
            g.players[g.nowid].identity.identity = 2
        g.status = s
class aliceMOVSkill(movCard):
    def skill(self, g:game, level):
        dir = g.chooseMovingDir()
        s = self.status
        self.status = state.CHOOSE_MOVE_DIS
        dis = svr.connectBot(self.nowid, "int8_t", self)
        if dis > self.level+level or dis<0:
            self.cheating()
        self.status = s
        through = g.moveCharacter(dir, dis)
        if through:
            for _ in range(self.level):
                g.drawCard( g.nowid)
            if g.players[1-g.nowid].identity.idx == 3 and g.players[1-g.nowid].identity.identity == 3 and 149 in g.players[1-g.nowid].metamorphosis:
                g.drawCard( 1-g.nowid)
            elif g.players[g.nowid].identity.idx == 3 and g.players[g.nowid].identity.identity == 3 and 149 in g.players[g.nowid].metamorphosis:
                g.drawCard( g.nowid)
            elif g.players[1-g.nowid].identity.idx == 1 and 141 in g.players[1-g.nowid].metamorphosis:
                g.putPosion( g.nowid)
                    
        s = g.status 
        g.status = state.CHANGE_IDENTITY
        ch = svr.connectBot(g.nowid,"int8_t", g)
        if ch == 1:
            g.players[g.nowid].identity.identity = 3
        g.status = s
class aliceMETASkill(metaCard):
    def skill(self, g:game, level):
        g.cheating()
        pass
class aliceUltraSkill(ultraCard):
    def skill(self, g:game, level):
        if self.cardName == '精彩的奇妙日':
            g.players[g.nowid].identity.riseBasic = 1
        elif self.cardName == '無休止的派對':
            g.players[g.nowid].identity.restartTurn = 1
            g.players[g.nowid].identity.havedrestart += 1
            if(g.players[g.nowid].identity.havedrestart>3):
                g.cheating()
        elif self.cardName == '遊戲盡在掌控':
            g.damage(1-g.nowid, 3, 3)
            for _ in range(5):
                s = g.status
                g.status = state.SEND_CARD
                ret = svr.connectBot(g.nowid, "int32_t", self)
                if ret == 0:
                    break
                sign = 1 if ret > 0 else 0
                ret = abs(ret)-1
                if sign:
                    if ret >= len(g.players[g.nowid].hand):
                        # cheat
                        g.cheating()
                else:
                    if ret >= len(g.players[g.nowid].graveyard):
                        # cheat
                        g.cheating()
                g.status = s
                if sign == 1:
                    g.players[1-g.nowid].deck.append(g.players[g.nowid].hand[ret])
                    del g.players[g.nowid].hand[ret]
                else:
                    g.players[1-g.nowid].deck.append(g.players[g.nowid].graveyard[ret])
                    del g.players[g.nowid].graveyard[ret]
                random.shuffle(g.players[1-g.nowid].deck)
        pass
class alice(character):
    @property
    def idx(self):
        return 3
    def setup(self):
        self.maxlife = 32
        self.life= self.maxlife
        self.maxdefense = 6
        self.defense = 0 
        self.energy = 0
        self.specialGate = 16   
        self.riseBasic = 0
        self.restartTurn = 0
        self.havedrestart = 0
    def __init__(self, identity = 0, riseBasic = 0, restartTurn = 0,havedrestart = 0, **kwargs):
        super().__init__()
        self.setup()
        self.identity = identity
        self.riseBasic = riseBasic
        self.restartTurn = restartTurn
        self.havedrestart = havedrestart
        self.characterName = "愛麗絲"
        self.picture = "./picture/character/alice/character.png"
        atklv1 =  aliceATKSkill("沒有圖片", "開啟牌局", 1)
        atklv2 =  aliceATKSkill("沒有圖片", "扭轉牌局", 2)
        atklv3 =  aliceATKSkill("沒有圖片", "操控牌局", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 = aliceDEFSkill("沒有圖片", "魔力技巧", 1)
        deflv2 = aliceDEFSkill("沒有圖片", "精神幻術", 2)
        deflv3 = aliceDEFSkill("沒有圖片", "帽子戲法", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  aliceMOVSkill("沒有圖片", "詭異的敏捷", 1)
        movlv2 =  aliceMOVSkill("沒有圖片", "詭異的隱蔽", 2)
        movlv3 =  aliceMOVSkill("沒有圖片", "詭異的詭異", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 = aliceMETASkill("沒有圖片", "砍掉她的頭")
        meta2 = aliceMETASkill("沒有圖片", "我們全是瘋子")
        meta3 = aliceMETASkill("沒有圖片", "仙境降臨")
        meta4 = aliceMETASkill("沒有圖片", "開始我的表演")
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 = aliceUltraSkill("沒有圖片", "無休止的派對")
        ultra2 =  aliceUltraSkill("沒有圖片", "精彩的奇妙日")
        ultra3 =  aliceUltraSkill("沒有圖片", "遊戲盡在掌控")
        self.ultraSkill.append(ultra1)
        self.ultraSkill.append(ultra2)
        self.ultraSkill.append(ultra3)
    def getFreeCard(self, g:game, canChoose:list, skillType:int):
        if(len(canChoose) == 0):
            return
        g.nowShowingCards = canChoose
        g.status = state.CHOOSECARDS
        c = svr.connectBot(g.nowid, "int32_t", g)
        if c not in canChoose:
            g.cheating()
        if c <= 10:
            if len(g.basicBuyDeck[(c-1)//3][(c-1)%3]) == 0:
                g.cheating()
            del g.basicBuyDeck[(c-1)//3][(c-1)%3][0]
        else:
            if (c-11)%12 in [0,1,2]:
                if len(g.players[g.nowid].attackSkill) == 0:
                    g.cheating()
                del g.players[g.nowid].attackSkill[0]
            elif (c-11)%12 in [3,4,5]:
                if len(g.players[g.nowid].identity.defenseSkill) == 0:
                    g.cheating()
                del g.players[g.nowid].identity.defenseSkill[0]
            elif (c-11)%12 in [6,7,8]:
                if len(g.players[g.nowid].moveSkill) == 0:
                    g.cheating()
                del g.players[g.nowid].moveSkill[0]
        flag = 0
        if (self.identity == 1 and skillType == 1 and 147 in g.players[g.nowid].metamorphosis) or (self.identity == 2 and skillType == 2 and 148 in g.players[g.nowid].metamorphosis):
            g.status = state.TAKE_TO_HAND
            c = svr.connectBot(g.nowid, "int8_t", g)
            if c == 1:
                flag = 1
        if flag:
            g.players[g.nowid].hand.append(c)
        else:
            g.players[g.nowid].graveyard.append(c)
        g.nowShowingCards = []
        pass