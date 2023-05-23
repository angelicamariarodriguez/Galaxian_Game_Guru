from src.ecs.components.tags.c_tag_star import CTagStar
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
import esper
import pygame

def system_star_controller(world:esper.World, screen:pygame.Surface, delta_time:float, window_bg_color:pygame.Color):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagStar)

    for _, (c_t, c_s, c_e) in components:
        cuad_rect = c_s.area.copy()
        cuad_rect.topleft = c_t.pos
        c_e.blink_time+=delta_time
        
        if cuad_rect.top > screen_rect.height: 
            c_t.pos.y = 0

        if c_e.blink_time>c_e.blink_rate and c_e.show:
            c_e.blink_time=0.0
            c_e.show = False            
            c_s.visible=False
            
            
        elif c_e.blink_time>c_e.blink_rate and not c_e.show: 
            c_e.blink_time=0.0
            c_e.show = True        
            c_s.visible=True
            
        

