import esper
import pygame
from src.ecs.components.c_surface import CSurface

from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_display_player(world:esper.World, player_entity, display_time:float, delta_time:float, player_dead:bool):
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_p = world.component_for_entity(player_entity, CTagPlayer)

   
    
    if player_dead:
        display_time+=delta_time
        if display_time>2.6:
            pl_s.visible = True
            pl_p.show = True
              
            
            return 0, False
        return display_time, True
    else:
       return display_time, False
