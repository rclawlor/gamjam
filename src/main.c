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
#include "framerate.h"
#include "graphics.h"
#include "assets/palette.h"
#include "assets/sprite.h"
#include "object.h"
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
    m_PlayerEntity.entitys[0]->pos.x = -50.0;
    m_PlayerEntity.entitys[0]->pos.y = 80.0;
    ENTITY_set_sprite(m_PlayerEntity.entitys[0], &(*PLAYER_SPRITE)[0]);
    ENTITY_set_palette(m_PlayerEntity.entitys[0], &(*PLAYER_PAL[PLAYER_1]));
    ENTITY_register_sm(m_PlayerEntity.entitys[0], &PlayerSM);

    PlayerMgr_add_player();
    m_PlayerEntity.entitys[0]->pos.x = -50.0;
    m_PlayerEntity.entitys[1]->pos.y = 70.0;
    ENTITY_set_sprite(m_PlayerEntity.entitys[1], &(*PLAYER_SPRITE)[0]);
    ENTITY_set_palette(m_PlayerEntity.entitys[1], &(*PLAYER_PAL[PLAYER_2]));
    ENTITY_register_sm(m_PlayerEntity.entitys[1], &PlayerSM);

    // Flags
    FlagMgr_init();
    ObjectSpr_e animation_frame = FLAG_1;
    SpriteAnimation_t flag_animation;
    ANIMATION_start(&flag_animation, 0.1, 2);

    Timer_set_now(&m_PlayerEntity.entitys[0]->last_update);
    Timer_set_now(&m_PlayerEntity.entitys[1]->last_update);
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
        DRAW_map(LEVEL_1_MAP[0], BACKGROUND_SPRITE, BACKGROUND_PAL);

        int i, j;
        for (i = 0; i < m_PlayerEntity.num_player; i++)
        {
            ENTITY_update(m_PlayerEntity.entitys[i]);
            COLLISION_resolve_map(m_PlayerEntity.entitys[i], LEVEL_1_MAP[0], BACKGROUND_SPRITE);
            for (j = 0; j < m_PlayerEntity.num_player; j++)
            {
                if (j == i) {
                    continue;
                }
                COLLISION_resolve_entity(m_PlayerEntity.entitys[j], m_PlayerEntity.entitys[i]);
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
