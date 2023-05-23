from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
import esper
import pygame
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_level_restart(world:esper.World, 
                        enemy_info:dict, 
                        level_info:dict, 
                        delta_time:float, 
                        restart_time:float,
                        complete_text_ent:int, 
                        get_ready_text_ent:int,
                        current_level:int):
    components = world.get_components(  CTagEnemy)
    
    if len(components)<=0:
        restart_time+=delta_time
        if restart_time >=3:
            
            system_enemy_spawner(world, enemy_info, level_info)
            world.delete_entity(complete_text_ent)
            world.delete_entity(get_ready_text_ent)
            return 0, False, current_level+1
        else:
            return restart_time, True,current_level

    return 0, False, current_level

