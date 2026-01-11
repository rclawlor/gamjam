// Local
#include "state_machine.h"


/**
 * Run the state machine
 *
 * @param sm        state machine to run
**/
void SM_run(StateMachine_t *sm)
{
    int i;
    State_t *current = &sm->state_table[sm->current_state];
    GuardedTransition_t transititon;
    for (i = 0; i < MAX_TRANSITIONS; ++i)
    {
        transititon = current->transititons[i];
        if (!transititon.guard || transititon.guard(sm))
        {
            // Don't run entry for looping transition
            if (transititon.next_state == sm->current_state)
            {
                break;
            }

            // Run exit
            if (current->on_exit)
            {
                current->on_exit();
            }

            // Update state
            sm->current_state = transititon.next_state;
            current = &sm->state_table[sm->current_state];

            // Run entry
            if (current->on_entry)
            {
                current->on_entry();
            }

            break;
        }
    }
}
