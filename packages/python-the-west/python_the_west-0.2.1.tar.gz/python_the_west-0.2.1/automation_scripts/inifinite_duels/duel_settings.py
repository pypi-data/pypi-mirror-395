from dataclasses import dataclass

from the_west_inner.equipment import Equipment


@dataclass
class DuelClothesSettings:
    
    regen : Equipment 
    duel_equipment : Equipment
    duel_equipment_reflex : Equipment | None
    duel_equipment_rezistance : Equipment | None
    duel_equipment_powerfull : Equipment | None
    