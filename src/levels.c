// Standard library
#include <stdint.h>

// Local
#include "flag.h"
#include "graphics.h"
#include "levels.h"
#include "player.h"


uint8_t (*LevelMaps[])[2][1000] = {
    LEVEL_1_MAP,
    LEVEL_2_MAP,
    LEVEL_3_MAP,
    LEVEL_4_MAP,
};


const LevelData_t m_Levels[] = {
    {
        .level = 1,
        .num_players = 1,
        .player_pos = {
            { .x = -60, .y = -8 },
        },
        .flag_pos = {
            { .x = -60, .y = 24},
        }
    },
    {
        .level = 2,
        .num_players = 2,
        .player_pos = {
            { .x = 24, .y = -24 },
            { .x = -32, .y = 32 }
        },
        .flag_pos = {
            { .x = -44, .y = 32},
            { .x = 36, .y = -24}
        }
    },
    {
        .level = 3,
        .num_players = 3,
        .player_pos = {
            { .x = 0, .y = 0 },
            { .x = 10, .y = 0 },
            { .x = 20, .y = 0 },
        },
        .flag_pos = {
            { .x = -82, .y = 8},
            { .x = 68, .y = 24},
            { .x = 68, .y = -8},
        }
    },
    {
        .level = 4,
        .num_players = 4,
        .player_pos = {
            { .x = 10, .y = 32 },
            { .x = 0, .y = 32 },
            { .x = -10, .y = 32 },
            { .x = -20, .y = 32 },
        },
        .flag_pos = {
            { .x = -32, .y = -16},
            { .x = -22, .y = -16},
            { .x = -12, .y = -16},
            { .x = -2, .y = -16},
        }
    }
};


/**
 * Load all players and flags
**/
void LoadLevelEntities(int level)
{
    LevelData_t data = m_Levels[level];
    PlayerMgr_clear_players();
    FlagMgr_clear_flags();

    int i;
    for (i = 0; i < data.num_players; i++)
    {
        PlayerMgr_add_player();
        m_PlayerEntity.entitys[i]->pos.x = data.player_pos[i].x;
        m_PlayerEntity.entitys[i]->pos.y = data.player_pos[i].y;
        ENTITY_set_sprite(m_PlayerEntity.entitys[i], &(*PLAYER_SPRITE)[0]);
        ENTITY_set_palette(m_PlayerEntity.entitys[i], &(*PLAYER_PAL[i]));
        ENTITY_register_sm(m_PlayerEntity.entitys[i], &PlayerSM);

        FlagMgr_add_flag(data.flag_pos[i]);
    }
}
