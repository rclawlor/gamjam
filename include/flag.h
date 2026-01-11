#ifndef FLAG_H_
#define FLAG_H_

// Local
#include "constants.h"
#include "entity.h"
#include "error.h"
#include "vector.h"


typedef struct {
    int num_flags;
    EntityGeneric_t* entitys[NUM_PLAYER];  // Generic entity information
} EntityFlag_t;

extern EntityFlag_t m_FlagEntity;


void FlagMgr_init();

// Utilitiy functions
Error_e FlagMgr_add_flag(Vector2D_t pos);
Error_e FlagMgr_remove_flag();
void FlagMgr_clear_flags();
bool FlagMgr_check_win();


#endif // FLAG_H_
