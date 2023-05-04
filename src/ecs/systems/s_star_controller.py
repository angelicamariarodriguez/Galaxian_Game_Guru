from src.ecs.components.tags.c_tag_star import CTagStar
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
import esper
import pygame

def system_star_controller(world:esper.World, screen:pygame.Surface, star_info:dict):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagStar)

    for star_entity, (c_t, c_s, c_e) in components:
        cuad_rect = c_s.area.copy()
        cuad_rect.topleft = c_t.pos
        if cuad_rect.top > screen_rect.height:
            
            c_t.pos.y = 0

