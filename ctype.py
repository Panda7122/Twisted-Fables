import cstruct

class vector(cstruct.MemCStruct):
    __def__ = """
    struct vector {
        int32_t array[256];
        uint32_t SIZE;
    };
    """
    def __setitem__(self, key, value):
        self.array[key] = value
        if key >= self.SIZE:
            for i in range(self.SIZE, key):
                self.array[i] = 0
            self.SIZE = key + 1
    def __delitem__(self, key):
        for i in range(key, self.SIZE - 1):
            self.array[key] = self.array[key + 1]
        self.SIZE-=1
    def __getitem__(self, key):
        return self.array[key]
    def __len__(self):
        return self.SIZE
    def append(self, value):
        self.array[self.SIZE] = value
        self.SIZE+=1
    def to_list(self)->list:
        return list(self.array[:self.SIZE])
    @classmethod
    def from_list(cls, ls:list):
        return cls(array=ls, SIZE = len(ls))
class CbuyDeck(cstruct.MemCStruct):
    __def__ = """
    struct buyDeck{
        struct vector cards;
        // Scheherazade
        uint32_t destiny_TOKEN;  // 0:none 1:blue 2:red
    };
    """

class Cplayer(cstruct.MemCStruct):
    __def__ = """
    struct player {
        int8_t team;  // for 2v2 mode
        uint8_t locate[2];
        uint8_t character;
        uint8_t maxlife;
        uint8_t life;
        uint8_t maxdefense;
        uint8_t defense;
        uint8_t energy;
        uint8_t specialGate;
        struct vector hand;
        struct vector deck;
        struct vector usecards;
        struct vector graveyard;
        struct vector metamorphosis;
        struct CbuyDeck attackSkill;
        struct CbuyDeck defenseSkill;
        struct CbuyDeck moveSkill;
        struct vector specialDeck;
        // Little Red Riding Hood 0
        //struct {
            
        //} redHood;

        // Snow White 1
        struct {
            struct vector remindPosion;
        } snowWhite;

        // sleeping Beauty 2
        struct _sleepingBeauty{
            uint32_t AWAKEN_TOKEN;
            int8_t AWAKEN;  // awaken(1) or sleep(0)
            int8_t dayNightmareDrawRemind;
            int32_t atkRise;
            int32_t atkRiseTime;
            int8_t usedmeta1;
        } sleepingBeauty;

        // alice 3
        struct {
            uint8_t identity;  // 0:none 1:紅心皇后 2:瘋帽子 3:柴郡貓
            int32_t riseBasic;
            int32_t restartTurn;
        } alice;

        // Mulan 4
        struct {
            uint32_t KI_TOKEN;

        } mulan;

        // kaguya 5
        //struct {
        //} kaguya;

        // mermaid 6
        //struct {
        //} mermaid;

        // Match Girl 7
        struct {
            uint32_t remindMatch;
        } matchGirl;

        // dorothy 8
        struct {
            uint32_t COMBO_TOKEN;
            int8_t canCombo;
        } dorothy;

        // Scheherazade 9
        //struct {
        //} scheherazade;
    };
    """

class Cstate(cstruct.CEnum):
    __size__ = 4
    __def__ = """
    enum state {
        CHOOSE_IDENTITY,
        
    }
    """
class Cgame(cstruct.MemCStruct):
    __def__ = """
    struct game {
        struct Cplayer players[4];
        int8_t now_turn_player_id;
        int8_t playerMode;  // 1v1 MODE(0) or 2v2 MODE(1)
        int8_t relicMode;
        // mermaid
        struct vector tentacle_TOKEN_locate;

        // 1v1 MODE is from 1 to 9
        uint32_t relic[11];
        struct vector relicDeck;
        struct vector relicGraveyard;
        struct CbuyDeck basicBuyDeck[12];  // attack(0) LV1~3 defense(1) LV1~3 move(2) LV1~3 generic(3)
        enum Cstate status;
        // metadata (for using basic card)
        int32_t nowATK;
        int32_t nowDEF;
        int32_t nowMOV;
        int32_t nowUsingCardID;
        int32_t totalDamage;
    };
    """
    @property
    def nowPlayer(self):
        return self.player[self.now_turn_player_id]
    @property
    def nowTarget(self):
        return self.player[1-self.now_turn_player_id]
    @property
    def target(self):
        return 1-self.now_turn_player_id
