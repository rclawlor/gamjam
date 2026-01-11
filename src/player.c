// Local
#include "entity.h"
#include "vector.h"
#include "player.h"


// Constants
const float PLAYER_VY_JUMP_PPS = 60.0;
const float PLAYER_AX_PPS = 35.0;
const float PLAYER_AY_PPS = 25.0;


// Module variables
EntityPlayer_t m_PlayerEntity = {0};
Timer_t jump_timer;

// Player state machine transitions
State_t player_state_table[NUM_PLAYER_STATES] = {
    [STATE_IDLE] = {
        .on_entry = PlayerSM_idle_entry,
        .on_exit = NULL,
        .transititons = {
            { .guard = PlayerSM_should_jump, .next_state = STATE_JUMPING },
            { .guard = NULL, .next_state = STATE_IDLE }
        }
    },
    [STATE_JUMPING] = {
        .on_entry = PlayerSM_jumping_entry,
        .on_exit = NULL,
        .transititons = {
            { .guard = PlayerSM_should_fall, .next_state = STATE_FALLING },
            { .guard = NULL, .next_state = STATE_JUMPING }
        }
    },
    [STATE_FALLING] = {
        .on_entry = PlayerSM_falling_entry,
        .on_exit = NULL,
        .transititons = {
            { .guard = PlayerSM_on_ground, .next_state = STATE_IDLE },
            { .guard = NULL, .next_state = STATE_FALLING }
        }
    }
};
StateMachine_t PlayerSM = {
    .current_state = STATE_IDLE,
    .state_table = player_state_table,
    .user_data = NULL
};


// Player state machine entry/exit functions
void PlayerSM_idle_entry() {}
void PlayerSM_jumping_entry() {
    m_PlayerEntity.entity.vel.y = PLAYER_VY_JUMP_PPS;
    m_PlayerEntity.entity.force.y += 1;
    Timer_set_now(&jump_timer);
}
void PlayerSM_falling_entry() {
    m_PlayerEntity.entity.force.y = 0;
    m_PlayerEntity.entity.acc.y = ENTITY_G_STRONG_PPS;
}

// Player state machine guards
bool g_jump_pressed = false;


bool PlayerSM_should_jump()
{
    return g_jump_pressed;
}


bool PlayerSM_should_fall()
{
    return Timer_get_elapsed_time(&jump_timer) > MAX_JUMP_S || !g_jump_pressed;
}

bool PlayerSM_on_ground()
{
    return fabs(m_PlayerEntity.entity.vel.y) < 1e-3 && PlayerSM.current_state != STATE_JUMPING;
}


bool moving()
{
    return fabs(m_PlayerEntity.entity.vel.x) >= 1;
}


bool jumping()
{
    return PlayerSM.current_state == STATE_JUMPING || PlayerSM.current_state == STATE_FALLING;
}


/**
 * Initialise player manager
**/
void PlayerMgr_init()
{
    Vector2D_t nil = { .x = 0, .y = 0 };
    m_PlayerEntity.entity.pos = nil;
    m_PlayerEntity.entity.vel = nil;
    m_PlayerEntity.entity.acc.x = 0;
    m_PlayerEntity.entity.acc.y = ENTITY_G_STRONG_PPS;
    m_PlayerEntity.entity.force = nil;

    OBSERVER_Subscribe_KEYDOWN(PlayerMgr_on_keydown);
    OBSERVER_Subscribe_KEYUP(PlayerMgr_on_keyup);

    Timer_set_now(&m_PlayerEntity.entity.last_update);
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
            m_PlayerEntity.entity.acc.x = -PLAYER_AX_PPS;
            break;
        case SDLK_RIGHT:
            m_PlayerEntity.entity.acc.x = PLAYER_AX_PPS;
            break;
        case SDLK_UP:
            if (PlayerSM.current_state != STATE_JUMPING && PlayerSM.current_state != STATE_FALLING)
            {
                g_jump_pressed = true;
            }
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
            m_PlayerEntity.entity.acc.x = 0.0;
            break;
        case SDLK_UP:
            g_jump_pressed = false;
            break;
        default:
            break;
    }
}
