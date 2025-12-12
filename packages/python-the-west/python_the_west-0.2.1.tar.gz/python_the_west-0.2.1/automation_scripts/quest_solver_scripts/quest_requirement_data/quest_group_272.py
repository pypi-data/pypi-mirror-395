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



GROUP_256_blacksmith = QuestGroupData(
    group_id = 272,
    required_group_id = None,
    quest_requirements = {
        3738 : [],
        4148 : []
    },
    accept_quest_requirement = {}
)