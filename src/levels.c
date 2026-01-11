// Local
#include "assets/palette.h"
#include "flag.h"
#include "graphics.h"
#include "levels.h"
#include "player.h"


const LevelData_t m_Levels[] = {
    {
        .num_players = 1,
        .player_pos = {{ .x = 0, .y = 0 }},
        .flag_pos = {{ .x = 10, .y = 10}}
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
        ENTITY_set_palette(m_PlayerEntity.entitys[i], &(*PLAYER_PAL[PLAYER_1]));
        ENTITY_register_sm(m_PlayerEntity.entitys[i], &PlayerSM);

        FlagMgr_add_flag(data.flag_pos[i]);
    }
}
