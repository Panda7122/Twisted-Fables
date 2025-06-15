class character:
    maxlife:int
    life:int
    maxdefense:int
    defense:int
    energy:int
    specialGate:int
    picture:str
    characterName:str
    attackSkill:list
    defenseSkill:list
    moveSkill:list
    metamorphosisSkill:list
    ultraSkill:list
    __subclasses = {
        0: "littleRed",
        1: "snowWhite",
        2: "sleepingBeauty",
        3: "alice",
        4: "mulan",
        5: "kaguya",
        6: "mermaid",
        7: "matchGirl",
        8: "dorothy",
        9: "scheherazade"
    }
    def __init__(self):
        self.attackSkill = []
        self.defenseSkill = []
        self.moveSkill = []
        self.metamorphosisSkill = []
        self.ultraSkill = []
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        while cls.__name__ in cls.__subclasses.values():
            cls.__subclasses[list(cls.__subclasses.keys())[list(cls.__subclasses.values()).index(cls.__name__)]] = cls
    @property 
    def idx(self)->int:
        raise NotImplementedError
    @classmethod
    def getClass(cls, idx):
        return cls.__subclasses.get(idx)
    def setup():
        raise NotImplementedError
    def specialMove(self, g):
        raise NotImplementedError
        