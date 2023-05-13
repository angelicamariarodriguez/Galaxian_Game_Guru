import esper
#from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import  CTagEnemyBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_collision_enemy_bullet_with_player(world: esper.World, player_entity:int):
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)
    components_bullet = world.get_components(CSurface, CTransform, CTagEnemyBullet)

    for bullet_entity, (c_b_s, c_b_t, c_t_b) in components_bullet:
        bull_rect = c_b_s.area.copy()
        bull_rect.topleft = c_b_t.pos
        if pl_rect.colliderect(bull_rect):
                world.delete_entity(player_entity)
                world.delete_entity(bullet_entity)
                #create_explosion(world, c_t.pos, explosion_info)
        
               


         