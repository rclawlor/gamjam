// Standard library
#include <math.h>

// Third party
#include <SDL.h>
#include <SDL_keycode.h>

// Local
#include "constants.h"
#include "entity.h"
#include "state_machine.h"
#include "timer.h"
#include "utils.h"


// Constants
const float ENTITY_MAX_VX_PPS = 25.0;
const float ENTITY_MAX_VY_PPS = 50.0;
const float ENTITY_G_STRONG_PPS = -45.0;
const float ENTITY_G_WEAK_PPS = -35.0;
const double MAX_JUMP_S = 0.2;


/**
 * Update entity's position, animations and states
 *
 * @param entity    the entity to update
**/
void ENTITY_update(EntityGeneric_t *entity)
{
    int i;
    for (i = 0; i < entity->num_sm; i++)
    {
        if (entity->sm[i] != NULL)
        {
            SM_run(entity->sm[i]);
        }
    }

    ENTITY_update_position(entity);
}


/**
 * Update player position based on state
 *
 * @param entity    the entity to update
**/
void ENTITY_update_position(EntityGeneric_t *entity)
{
    double dt = 1000 * Timer_get_elapsed_time(&entity->last_update);
    if (dt <= 0)
    {
        return;
    }

    float mass = 1.0;

    // Scale based on time delta
    float scale = 1.0 / (float) dt;

    // Update acceleration based on forces
    entity->acc.y = -45.0 / mass + entity->force.y * scale / mass;

    // Update velocity based on acceleration
    entity->vel.x += (entity->acc.x * scale);
    entity->vel.y += (entity->acc.y * scale);
    entity->vel.y = flimit(entity->vel.y, ENTITY_MAX_VY_PPS);

    // Update position based on velocity
    float dx = entity->vel.x * scale;
    float dy = entity->vel.y * scale;
    entity->pos.x += dx;
    entity->pos.y += dy;

    // For example, a simple friction:
    float friction = 3.0;
    if (entity->acc.x == 0) 
    {
        entity->vel.x *= (1.0 - friction * scale);
    }

    // Limit maximum speed
    if (entity->vel.x < 0)
    {
        entity->vel.x = fmaxf(entity->vel.x, -ENTITY_MAX_VX_PPS);
    }
    else
    {
        entity->vel.x = fminf(entity->vel.x, ENTITY_MAX_VX_PPS);
    }

    Timer_set_now(&entity->last_update);
}


/**
 * Set entity's sprite
 *
 * @param entity    entity to update
 * @param sprite    sprite to use
**/
void ENTITY_set_sprite(EntityGeneric_t *entity, uint8_t sprite[])
{
    memcpy(
        entity->sprite,
        sprite,
        sizeof(uint8_t) * TILE_SIZE
    );
}


/**
 * Set entity's palette
 *
 * @param entity    entity to update
 * @param palette   palette to use
**/
void ENTITY_set_palette(EntityGeneric_t *entity, uint32_t palette[])
{
    memcpy(
        entity->palette,
        palette,
        sizeof(uint32_t) * PAL_LENGTH
    );
}


/**
 * Register state machine for entity
 *
 * @param entity    entity to update
 * @param sm        state machine to register
**/
void ENTITY_register_sm(EntityGeneric_t *entity, StateMachine_t *sm)
{
    if (entity->num_sm < MAX_STATE_MACHINE)
    {
        entity->sm[entity->num_sm] = sm;
        entity->num_sm += 1;
    }
}
