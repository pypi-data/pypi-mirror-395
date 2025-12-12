from enum import Enum,auto

class NpcDuelManagerState(Enum):
    
    DUELING_FOR_EXP = auto()
    REDUCING_DIFFICULTY = auto()
    CLEARING_NPC = auto()
    RECHARGING_MOTIVATION = auto()
    RECHARGING_ENERGY = auto()
    RECHARGING_HP = auto()