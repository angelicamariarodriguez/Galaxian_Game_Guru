import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface

def system_limit_player(world: esper.World, player_entity:int, screen:pygame.Surface):

    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)

    screen_rect = screen.get_rect()
    if pl_rect.left < 0 or pl_rect.right > screen_rect.width:
        pl_rect.clamp_ip(screen_rect)
        pl_t.pos.x = pl_rect.x
    

    
