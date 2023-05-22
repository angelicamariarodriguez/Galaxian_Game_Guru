import esper
import pygame
from src.create.prefab_creator import TextAlignment, create_text
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_display_player(world:esper.World, player_entity, display_time:float, delta_time:float):
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_p = world.component_for_entity(player_entity, CTagPlayer)
    display_time+=delta_time
    
    
    if display_time>4 and pl_p.show == False:
        pl_s.visible = True
        pl_p.show = True
        return 0
    
    else:
       return display_time
