#ifndef PLAYER_H_
#define PLAYER_H_

// Local
#include "entity.h"
#include "error.h"
#include "observer.h"
#include "state_machine.h"
#include "vector.h"


// Constants
extern const float PLAYER_VY_JUMP_PPS;
extern const float ENTITY_AX_PPS;
extern const float ENTITY_AY_PPS;


typedef struct {
    int num_player;
    EntityGeneric_t* entitys[NUM_PLAYER];  // Generic entity information
} EntityPlayer_t;

extern EntityPlayer_t m_PlayerEntity;


void PlayerMgr_init();

// Observer
void PlayerMgr_on_keydown(KeyEvent_t*);
void PlayerMgr_on_keyup(KeyEvent_t*);

// State machine
typedef enum {
    STATE_IDLE = 0,
    STATE_MOVING,
    NUM_PLAYER_STATES
} PlayerState_e;

// Player state machine entry/exit functions
void PlayerSM_idle_entry();
void PlayerSM_moving_entry();

// Player state machine guards
bool PlayerSM_is_moving();
bool PlayerSM_is_stationary();

// Utility functions
void PlayerMgr_set_acc(Vector2D_t acc);
void PlayerMgr_set_x_acc(double acc);
void PlayerMgr_set_y_acc(double acc);
Error_e PlayerMgr_add_player();
Error_e PlayerMgr_remove_player();

extern StateMachine_t PlayerSM;


#endif // PLAYER_H_
