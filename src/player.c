// Local
#include "error.h"
#include "vector.h"
#include "player.h"


// Constants
const float PLAYER_A_PPS = 35.0;


// Module variables
EntityPlayer_t m_PlayerEntity = {0};
Timer_t jump_timer;

// Player state machine transitions
State_t player_state_table[NUM_PLAYER_STATES] = {
    [STATE_IDLE] = {
        .on_entry = PlayerSM_idle_entry,
        .on_exit = NULL,
        .transititons = {
            { .guard = PlayerSM_is_moving, .next_state = STATE_MOVING },
            { .guard = NULL, .next_state = STATE_IDLE }
        }
    },
    [STATE_MOVING] = {
        .on_entry = PlayerSM_moving_entry,
        .on_exit = NULL,
        .transititons = {
            { .guard = PlayerSM_is_stationary, .next_state = STATE_IDLE },
            { .guard = NULL, .next_state = STATE_MOVING }
        }
    },
};
StateMachine_t PlayerSM = {
    .current_state = STATE_IDLE,
    .state_table = player_state_table,
    .user_data = NULL
};


// Player state machine entry/exit functions
void PlayerSM_idle_entry() {}
void PlayerSM_moving_entry() {}

bool PlayerSM_is_moving()
{
    int i;
    bool moving = false;

    for (i = 0; i < m_PlayerEntity.num_player; i++)
    {
        moving |= (
            fabs(m_PlayerEntity.entitys[i]->vel.x) >= 1
            || fabs(m_PlayerEntity.entitys[i]->vel.y) >= 1
        );

    }
    return moving;
}

bool PlayerSM_is_stationary() {
    return !PlayerSM_is_moving();
}


/**
 * Initialise player manager
**/
void PlayerMgr_init()
{
    PlayerMgr_add_player();

    OBSERVER_Subscribe_KEYDOWN(PlayerMgr_on_keydown);
    OBSERVER_Subscribe_KEYUP(PlayerMgr_on_keyup);
}


/**
 * Called on key down event from TOPIC_KEYDOWN
 *
 * @param evt       key event from topic
**/
void PlayerMgr_on_keydown(KeyEvent_t *evt)
{
    switch (evt->key)
    {
        case SDLK_LEFT:
            PlayerMgr_set_x_acc(-PLAYER_A_PPS);
            break;
        case SDLK_RIGHT:
            PlayerMgr_set_x_acc(PLAYER_A_PPS);
            break;
        case SDLK_UP:
            PlayerMgr_set_y_acc(PLAYER_A_PPS);
            break;
        case SDLK_DOWN:
            PlayerMgr_set_y_acc(-PLAYER_A_PPS);
            break;
        default:
            break;
    }
}


/**
 * Called on key up event from TOPIC_KEYUP
 *
 * @param evt       key event from topic
**/
void PlayerMgr_on_keyup(KeyEvent_t *evt)
{
    switch (evt->key)
    {
        case SDLK_LEFT:
        case SDLK_RIGHT:
            PlayerMgr_set_x_acc(0.0);
            break;
        case SDLK_UP:
        case SDLK_DOWN:
            PlayerMgr_set_y_acc(0.0);
            break;
        default:
            break;
    }
}


/**
 * Set acceleration for all player entities
 *
 * @param acc       acceleration to set
**/
void PlayerMgr_set_acc(Vector2D_t acc)
{
    int i;
    for (i = 0; i < m_PlayerEntity.num_player; i++)
    {
        m_PlayerEntity.entitys[i]->acc = acc;
    }
}


/**
 * Set x acceleration for all player entities
 *
 * @param acc       acceleration to set
**/
void PlayerMgr_set_x_acc(double acc)
{
    int i;
    for (i = 0; i < m_PlayerEntity.num_player; i++)
    {
        m_PlayerEntity.entitys[i]->acc.x = acc;
    }
}


/**
 * Set y acceleration for all player entities
 *
 * @param acc       acceleration to set
**/
void PlayerMgr_set_y_acc(double acc)
{
    int i;
    for (i = 0; i < m_PlayerEntity.num_player; i++)
    {
        m_PlayerEntity.entitys[i]->acc.y = acc;
    }
}


/**
 * Add player entity
**/
Error_e PlayerMgr_add_player()
{
    Vector2D_t nil = { .x = 0, .y = 0 };

    // Allocate memory for the entity before using it
    int idx = m_PlayerEntity.num_player;
    if (idx >= NUM_PLAYER)
    {
        return ERROR_OUT_OF_BOUNDS;
    }
    m_PlayerEntity.entitys[idx] = malloc(sizeof(EntityGeneric_t));
    if (m_PlayerEntity.entitys[idx] == NULL) {
        // Handle allocation failure
        fprintf(stderr, "Failed to allocate memory for player entity\n");
        return ERROR_OUT_OF_BOUNDS;
    }
    m_PlayerEntity.num_player += 1;
    m_PlayerEntity.entitys[idx]->pos = nil;
    m_PlayerEntity.entitys[idx]->vel = nil;
    m_PlayerEntity.entitys[idx]->acc.x = 0;
    m_PlayerEntity.entitys[idx]->acc.y = 0;
    m_PlayerEntity.entitys[idx]->force = nil;

    Timer_set_now(&m_PlayerEntity.entitys[idx]->last_update);

    return OK;
}


/**
 * Remove player entity at index
**/
Error_e PlayerMgr_remove_player()
{
    free(m_PlayerEntity.entitys[m_PlayerEntity.num_player]);
    m_PlayerEntity.num_player -= 1;

    return OK;
}
