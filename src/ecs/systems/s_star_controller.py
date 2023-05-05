from src.ecs.components.tags.c_tag_star import CTagStar
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
import esper
import pygame

def system_star_controller(world:esper.World, screen:pygame.Surface, delta_time:float, window_bg_color:pygame.Color):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagStar)

    for star_entity, (c_t, c_s, c_e) in components:
        cuad_rect = c_s.area.copy()
        cuad_rect.topleft = c_t.pos
        c_e.blink_time+=delta_time
        
        if cuad_rect.top > screen_rect.height: 
            c_t.pos.y = 0

        if c_e.blink_time>c_e.blink_rate and c_e.show:
            c_e.blink_time=0.0
            c_e.show = False
            fill(c_s.surf, window_bg_color)
            
        elif c_e.blink_time>c_e.blink_rate and not c_e.show: 
            c_e.blink_time=0.0
            c_e.show = True 
            fill(c_s.surf, c_e.orig_color)
            

def fill(surface, color):
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

        

