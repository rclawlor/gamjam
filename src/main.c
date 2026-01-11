// Standard library
#include <stdio.h>
#include <stdbool.h> 

// Third party
#include <SDL.h>
#include <SDL_events.h>

// Local
#include "colour.h"
#include "draw.h"
#include "event.h"
#include "framerate.h"
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

        DRAW_fill_screen(ARGB(0xff, 0xff, 0x00, 0xff));

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
