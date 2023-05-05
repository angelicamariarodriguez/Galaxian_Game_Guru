import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_screen_bouncer(world:esper.World, screen:pygame.Surface, movement_right:bool, enemy_speed:int):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy)
    temp_mov:bool =movement_right
    
    for enemy_entity, (c_t, c_v, c_s, c_e) in components:
        
        
        cuad_rect = c_s.area.copy()
        cuad_rect.topleft = c_t.pos
        
        if temp_mov:
            c_v.vel.x = enemy_speed

        else:
            c_v.vel.x = enemy_speed*-1
        
        if not temp_mov and  cuad_rect.left < 10:          
            temp_mov= True
        elif temp_mov and  cuad_rect.right > screen_rect.width-10:
            temp_mov = False
        else:
            temp_mov = temp_mov
        
        return temp_mov