from automation_scripts.quest_solver_scripts.quest_requirement_data.solve_quest_script_builder import build_solver_executable
from .quest_group_data import QuestGroupData

from the_west_inner.quest_requirements import (Quest_requirement_duel_quest_npc,
                                               Quest_requirement_item_to_hand_work_product_seconds,
                                               Quest_requirement_work_n_times,
                                               Quest_requirement_get_n_skill_points,
                                               Quest_requirement_work_quest_item,
                                               Quest_requirement_sell_item,
                                               Quest_requirement_execute_script,
                                               Quest_requirement_item_to_hand_work_product_hourly,
                                               Quest_requirement_travel
)
GROUP_256_blacksmith_annex = QuestGroupData(
    group_id = 256,
    required_group_id = None,
    quest_requirements = {
        3739 : [Quest_requirement_travel(x= 1728,
                                         y =  2081,
                                         employer_key= 'ghosttown',
                                            quest_id = 3739,
                                            solved = False
                                            )
                                         ],
        3742 : [Quest_requirement_item_to_hand_work_product_hourly(item_id= 1948000,
                                                                   number= 2,
                                                                   quest_id= 3742,
                                                                   solved= False
                                                                   ),
                Quest_requirement_item_to_hand_work_product_hourly(item_id= 1858000,
                                                                   number= 1,
                                                                   quest_id= 3742,
                                                                   solved= False
                                                                   ),
                Quest_requirement_item_to_hand_work_product_hourly(item_id= 1902000,
                                                                   number= 2,
                                                                   quest_id= 3742,
                                                                   solved= False
                                                                   )
                ]
    }
)
                                            
    

GROUP_256_blacksmith = QuestGroupData(
    group_id = 256,
    required_group_id = None,
    quest_requirements = {
        3738 : [Quest_requirement_execute_script(script=build_solver_executable(quest_group_data = GROUP_256_blacksmith_annex),
                                                 solved= False
                                                 )
             ]
    },
    accept_quest_requirement = {}
)