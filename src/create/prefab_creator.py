import pygame
import esper
import random
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator
from src.ecs.components.tags.c_tag_star import CTagStar
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity

def create_star(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color, blink_rate: float) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    world.add_component(cuad_entity,
                        CTagStar(blink_rate, col))
    return cuad_entity

def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity,
                        CTransform(pos))
    world.add_component(sprite_entity,
                        CVelocity(vel))
    world.add_component(sprite_entity,
                        CSurface.from_surface(surface))
    return sprite_entity

def create_enemy(world: esper.World, pos: pygame.Vector2, enemy_info: dict, enemy_type:str):
    enemy_surface = ServiceLocator.images_services.get(enemy_info[enemy_type]["image"])
    vel = pygame.Vector2(enemy_info["enemy_speed"],0)
    enemy_entity = create_sprite(world, pos, vel, enemy_surface)
    
    world.add_component(enemy_entity,
                        CAnimation(enemy_info[enemy_type]["animations"]))
    world.add_component(enemy_entity, CTagEnemy())

def create_bullet(world: esper.World,
                  start_pos: pygame.Vector2,
                  shooter_size: pygame.Vector2,
                  bullet_info: dict):

    bullet_size = pygame.Vector2(bullet_info["size"]["x"], bullet_info["size"]["y"])
    vel = pygame.Vector2(0,bullet_info["speed"])
    color = pygame.Color(bullet_info["color"]["r"],
                        bullet_info["color"]["g"],
                        bullet_info["color"]["b"])
    start_pos=pygame.Vector2(start_pos.x+shooter_size[0]/2,
                             start_pos.y+shooter_size[1])
    bullet_entity = create_square(world,bullet_size,start_pos,vel,color)
    world.add_component(bullet_entity, CTagBullet())
    