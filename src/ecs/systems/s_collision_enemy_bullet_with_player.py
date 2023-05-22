import esper
import pygame
from src.create.prefab_creator import create_explosion
#from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import  CTagEnemyBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator

def system_collision_enemy_bullet_with_player(world: esper.World, player_entity:int, explosion_info:dict):
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_p = world.component_for_entity(player_entity, CTagPlayer)
    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)
    components_bullet = world.get_components(CSurface, CTransform, CTagEnemyBullet)


    for bullet_entity, (c_b_s, c_b_t, c_t_b) in components_bullet:
        bull_rect = c_b_s.area.copy()
        bull_rect.topleft = c_b_t.pos
        
        if pl_rect.colliderect(bull_rect):
                world.delete_entity(bullet_entity)
                pos_x = pl_t.pos.x-(pl_rect.w/2)
                pos_y = pl_t.pos.y-(pl_rect.h/2)
                pl_s.visible = False            
                create_explosion(world, pygame.Vector2(pos_x, pos_y), explosion_info["player_explosion"])
                pl_p.show = False

                
        
               


         