#ifndef LEVELS_H_
#define LEVELS_H_

// Standard library
#include <stdint.h>

// Local
#include "constants.h"
#include "vector.h"

typedef struct {
    int level;
    int num_players;
    Vector2D_t player_pos[NUM_PLAYER];
    Vector2D_t flag_pos[NUM_PLAYER];
} LevelData_t;

extern const LevelData_t m_Levels[];
extern uint8_t (*LevelMaps[])[2][1000];

void LoadLevelEntities(int level);


#endif // LEVELS_H_
