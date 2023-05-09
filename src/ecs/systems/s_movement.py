import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar



def system_movement(world:esper.World, delta_time:float, paused:bool):
    components = world.get_components(CTransform, CVelocity)
    c_t:CTransform
    c_v:CVelocity
    if not paused:
        for entity, ( c_t, c_v) in components:
            c_t.pos.x+= c_v.vel.x * delta_time
            c_t.pos.y+= c_v.vel.y * delta_time
    else:
        star_components = world.get_components(CTransform, CVelocity, CTagStar)
        for entity, ( c_t, c_v, c_e) in star_components:
            c_t.pos.x+= c_v.vel.x * delta_time
            c_t.pos.y+= c_v.vel.y * delta_time