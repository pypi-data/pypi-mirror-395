from datetime import datetime
import concurrent.futures
from copy import deepcopy

from the_west_inner.duels import NpcDuelManager,NpcDuelList
from the_west_inner.equipment import Equipment, Equipment_manager
from the_west_inner.requests_handler import requests_handler


from automation_scripts.inifinite_duels.duel_settings import DuelClothesSettings
from automation_scripts.inifinite_duels.duel_npc_rule import build_npc_duel_rule_composer, DuelNpcSelectionComposer



class DuelNpcSelectorManager:
    
    def __init__(self, duel_rule_composer : DuelNpcSelectionComposer):
        
        self.duel_rule_composer = duel_rule_composer
    
    def select_npc(self,npc_list : NpcDuelList):
        
        preliminary_list = self.duel_rule_composer.select_npc(
            npc_list= npc_list
        )
        
        if len(preliminary_list) != 0:
            
            return preliminary_list[:]


class DuelRestartManager:
    
    def __init__(self,
                 duel_manager : NpcDuelManager ,
                 equipment_manger : Equipment_manager ,
                 handler : requests_handler ):
        
        self.duel_manager = duel_manager
        self.equipment_manager = equipment_manger
        self.handler = handler
        
        self._initial_equipment = self.equipment_manager.current_equipment.copy()
    
    def _equip_equipment(self, equipment : Equipment):
        
        self.equipment_manager.equip_equipment(
            equipment= equipment,
            handler= self.handler
        )
    
    def _equip_hp_equipment(self, hp_equipment : Equipment):
        
        self._equip_equipment(equipment = hp_equipment)
    
    
    def select_npc(self) :
        
        npc_list = self.duel_manager.npc_list
        
        