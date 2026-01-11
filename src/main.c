// Standard library
#include <stdio.h>
#include <stdbool.h> 

// Third party
#include <SDL.h>
#include <SDL_events.h>

// Local
#include "animation.h"
#include "collision.h"
#include "colour.h"
#include "draw.h"
#include "entity.h"
#include "event.h"
#include "flag.h"
#include "framerate.h"
#include "graphics.h"
#include "text.h"
#include "levels.h"
#include "assets/sprite.h"
#include "flag.h"
#include "player.h"
#include "window.h"


// Function definitions
int initialise_SDL();


int main(int argc, char* args[])
{
    if (initialise_SDL())
    {
        return 1;
    }

    // Create window
    WindowMgr_init();

    // Player
    PlayerMgr_init();
    // Flags
    FlagMgr_init();

    int level = 0;
    LoadLevelEntities(level);

    ObjectSpr_e animation_frame = FLAG_1;
    SpriteAnimation_t flag_animation;
    ANIMATION_start(&flag_animation, 0.1, 2);

    bool win;
    int i, j;
    char msg[64] = {};
    while (!WindowMgr_should_quit())
    {
        // Update FPS
        FramerateMgr_frame_start();
        FramerateMgr_update_average();

        // Handle events
        EVENT_poll();

        if (WindowMgr_should_resize())
        {
            WindowMgr_resize_window();
        }

        DRAW_fill_screen(ARGB(0xff, 0x00, 0x00, 0x00));
        DRAW_map(*LevelMaps[level], BACKGROUND_SPRITE, BACKGROUND_PAL);

        if (!win)
        {
            for (i = 0; i < m_PlayerEntity.num_player; i++)
            {
                ENTITY_update(m_PlayerEntity.entitys[i]);
                COLLISION_resolve_map(m_PlayerEntity.entitys[i], *LevelMaps[level], BACKGROUND_SPRITE);
                for (j = 0; j < m_PlayerEntity.num_player; j++)
                {
                    if (j == i) {
                        continue;
                    }
                    COLLISION_resolve_entity(m_PlayerEntity.entitys[j], m_PlayerEntity.entitys[i]);
                }
            }
        }
        for (i = 0; i < m_PlayerEntity.num_player; i++)
        {
            DRAW_entity(m_PlayerEntity.entitys[i], false);
        }

        ANIMATION_step(&flag_animation);
        for (i = 0; i < m_FlagEntity.num_flags; i++)
        {
            ENTITY_set_sprite(m_FlagEntity.entitys[i], &(*OBJECT_SPRITE[flag_animation.current_frame]));
            DRAW_entity(m_FlagEntity.entitys[i], false);
        }

        win = FlagMgr_check_win();
        if (win)
        {
            DRAW_apply_blur();
            DRAW_desaturate(0.8);
            sprintf(msg, "LEVEL %d COMPLETE", level + 1),
            TEXT_render(
                160,
                100,
                ALIGN_CENTRE,
                msg,
                FONT_SPRITE,
                &(*PLAYER_PAL[0])
            );
        }
        WindowMgr_render();
        FramerateMgr_fix_framerate();
    }

    // Destroy window
    WindowMgr_destroy();

    // Quit SDL subsystems
    SDL_Quit();

    return 0;
}


/**
 * Initialise SDL
**/
int initialise_SDL()
{
    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0)
    {
        printf("SDL could not initialise! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    return 0;
}
