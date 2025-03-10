import sys 
sys.path.append("..")
from game import *
from character import *
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
            if g.players[1-g.nowid].identity.idx == 3 and vectorHave(g.players[1-g.nowid].metamorphosis, [149]):
                g.drawCard( 1-g.nowid)
            elif g.players[g.nowid].identity.idx == 3 and vectorHave(g.players[g.nowid].metamorphosis, [149]):
                g.drawCard( g.nowid)
        s = g.status 
        g.status = state.CHANGE_IDENTITY
        ch = svr.connectBot(g.nowid,"int8_t", g)
        if ch == 1:
            g.players[g.nowid].identity.identity = 3
        g.status = s
class aliceMETASkill(metaCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class aliceUltraSkill(ultraCard):
    def skill(self, g:game, level):
        # TODO not implement yet
        pass
class alice(character):
    def idx():
        return 3
    def setup(self):
        self.maxlife = 32
        self.life= self.maxlife
        self.maxdefense = 6
        self.defense = 0 
        self.energy = 0
        self.specialGate = 16   
    def __init__(self, identity = 0, **kwargs):
        self.setup()
        self.identity = identity
        self.characterName = "愛麗絲"
        self.picture = "沒有圖片"
        atklv1 =  aliceATKSkill("沒有圖片", "", 1)
        atklv2 =  aliceATKSkill("沒有圖片", "", 2)
        atklv3 =  aliceATKSkill("沒有圖片", "", 3)
        self.attackSkill.append(atklv1)
        self.attackSkill.append(atklv2)
        self.attackSkill.append(atklv3)
        deflv1 =  aliceDEFSkill("沒有圖片", "", 1)
        deflv2 =  aliceDEFSkill("沒有圖片", "", 2)
        deflv3 =  aliceDEFSkill("沒有圖片", "", 3)
        self.defenseSkill.append(deflv1)
        self.defenseSkill.append(deflv2)
        self.defenseSkill.append(deflv3)
        movlv1 =  aliceMOVSkill("沒有圖片", "", 1)
        movlv2 =  aliceMOVSkill("沒有圖片", "", 2)
        movlv3 =  aliceMOVSkill("沒有圖片", "", 3)
        self.moveSkill.append(movlv1)
        self.moveSkill.append(movlv2)
        self.moveSkill.append(movlv3)
        meta1 =  aliceMETASkill("沒有圖片", "", 0)
        meta2 =  aliceMETASkill("沒有圖片", "", 0)
        meta3 =  aliceMETASkill("沒有圖片", "", 0)
        meta4 =  aliceMETASkill("沒有圖片", "", 0)
        self.metamorphosisSkill.append(meta1)
        self.metamorphosisSkill.append(meta2)
        self.metamorphosisSkill.append(meta3)
        self.metamorphosisSkill.append(meta4)
        ultra1 =  aliceUltraSkill("沒有圖片", "", 0)
        ultra2 =  aliceUltraSkill("沒有圖片", "", 0)
        ultra3 =  aliceUltraSkill("沒有圖片", "", 0)
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
            g.basicBuyDeck[(c-1)//3][(c-1)%3].cards.pop()
        flag = 0
        if (skillType == 1 and 147 in g.players[g.nowid].metamorphosis) or (skillType == 2 and 148 in g.players[g.nowid].metamorphosis):
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