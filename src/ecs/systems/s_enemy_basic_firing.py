import esper
import pygame
import random

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator import create_bullet

def system_enemy_basic_firing(world:esper.World, bullet_info:dict):
    components = world.get_components(CTransform, CSurface, CTagEnemy)

    for _, (c_t, c_s, c_e) in components:
        random_fire = random.randint(0,10000)
        cuad_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        
        if random_fire > 9998:
            fire_pos = pygame.Vector2(c_t.pos.x,c_t.pos.y)
            
            create_bullet(world,fire_pos,c_s.area.size,bullet_info)
