#ifndef STATE_MACHINE_H_
#define STATE_MACHINE_H_

// Standard library
#include <stdbool.h>

#define MAX_TRANSITIONS 5


typedef struct StateMachine_t StateMachine_t;
typedef struct GuardedTransition_t GuardedTransition_t;
typedef void (*ActionFn_t)(void);
typedef bool (*GuardFn_t)(StateMachine_t *sm);
typedef struct State_t State_t;


struct GuardedTransition_t {
    GuardFn_t guard;
    int next_state;
};


struct State_t {
    ActionFn_t on_entry;
    ActionFn_t on_exit;
    GuardedTransition_t transititons[MAX_TRANSITIONS];
};


struct StateMachine_t {
    int current_state;
    State_t *state_table;
    void *user_data;
};


void SM_run(StateMachine_t*);


#endif // STATE_MACHINE_H_
