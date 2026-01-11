#ifndef ENTITY_H_
#define ENTITY_H_

// Standard library
#include <stdbool.h> 

// Third party
#include <SDL_keycode.h>

// Local
#include "constants.h"
#include "state_machine.h"
#include "timer.h"
#include "vector.h"


// Definitions
#define MAX_STATE_MACHINE 4

// Constants
extern const float ENTITY_MAX_VX_PPS;
extern const float ENTITY_MAX_VY_PPS;
extern const float ENTITY_VY_JUMP_PPS;
extern const double MAX_JUMP_S;


typedef struct {
    uint8_t type;                           // Entity type
    uint8_t sprite[TILE_SIZE];              // Current sprite
    uint32_t palette[PAL_LENGTH];           // Current palette
    Vector2D_t pos;                         // Position in px
    Vector2D_t vel;                         // Velocity in px/s
    Vector2D_t acc;                         // Acceleration in px/s^2
    Vector2D_t force;                       // Applied force
    Timer_t last_update;                    // Time of last position update
    uint8_t num_sm;                         // Number of state machines
    StateMachine_t *sm[MAX_STATE_MACHINE];  // State machines
} EntityGeneric_t;


void ENTITY_update(EntityGeneric_t *);
void ENTITY_update_position(EntityGeneric_t*);
void ENTITY_set_sprite(EntityGeneric_t*, uint8_t[]);
void ENTITY_set_palette(EntityGeneric_t*, uint32_t[]);
void ENTITY_register_sm(EntityGeneric_t*, StateMachine_t*);


#endif // ENTITY_H_
