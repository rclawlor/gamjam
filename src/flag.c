// Local
#include "collision.h"
#include "flag.h"
#include "entity.h"
#include "player.h"
#include "vector.h"
#include "graphics.h"
#include "assets/sprite.h"


// Module variables
EntityFlag_t m_FlagEntity = {0};


/**
 * Initialise flag manager
**/
void FlagMgr_init()
{
    Vector2D_t pos = { .x = 0, .y = 0 };
    FlagMgr_add_flag(pos);
}


/**
 * Add flag entity
**/
Error_e FlagMgr_add_flag(Vector2D_t pos)
{
    Vector2D_t nil = { .x = 0, .y = 0 };

    // Allocate memory for the entity before using it
    int idx = m_FlagEntity.num_flags;
    if (idx >= NUM_PLAYER)
    {
        return ERROR_OUT_OF_BOUNDS;
    }
    m_FlagEntity.entitys[idx] = malloc(sizeof(EntityGeneric_t));
    if (m_FlagEntity.entitys[idx] == NULL) {
        // Handle allocation failure
        fprintf(stderr, "Failed to allocate memory for flag entity\n");
        return ERROR_OUT_OF_BOUNDS;
    }
    memset(m_FlagEntity.entitys[idx], 0, sizeof(EntityGeneric_t));
    m_FlagEntity.num_flags += 1;
    m_FlagEntity.entitys[idx]->pos = pos;
    m_FlagEntity.entitys[idx]->vel = nil;
    m_FlagEntity.entitys[idx]->acc.x = 0;
    m_FlagEntity.entitys[idx]->acc.y = 0;
    m_FlagEntity.entitys[idx]->force = nil;

    ENTITY_set_sprite(m_FlagEntity.entitys[idx], &(*OBJECT_SPRITE[FLAG_1]));
    ENTITY_set_palette(m_FlagEntity.entitys[idx], &(*PLAYER_PAL[idx]));

    return OK;
}


/**
 * Remove flag entity
**/
Error_e FlagMgr_remove_flag()
{
    free(m_FlagEntity.entitys[m_FlagEntity.num_flags - 1]);
    m_FlagEntity.entitys[m_FlagEntity.num_flags - 1] = NULL;
    m_FlagEntity.num_flags -= 1;

    return OK;
}


/**
* Check win
**/
bool FlagMgr_check_win() {
    int i;
    Vector2D_t vec;
    bool win = true;
    for (i = 0; i < m_PlayerEntity.num_player; i++)
    {
        vec = COLLISION_check_entity(m_PlayerEntity.entitys[i], m_FlagEntity.entitys[i]);
        win &= (vec.x != 0 && vec.y != 0);
    }

    return win;
}


/**
* Clear all flags
**/
void FlagMgr_clear_flags()
{
    while (m_FlagEntity.num_flags != 0) {
        FlagMgr_remove_flag();
    }
}
