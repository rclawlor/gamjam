// Third party
#include <SDL.h>
#include <SDL_events.h>

// Local
#include "event.h"
#include "vector.h"
#include "window.h"


/**
 * Poll incoming events
**/
void EVENT_poll()
{
    SDL_Event e;
    Coordinate_t mouse_pos;
    while (SDL_PollEvent(&e))
    {
        switch (e.type)
        {
            case SDL_QUIT:
                WindowMgr_quit();
                break;
            case SDL_WINDOWEVENT:
                /* Unused */
                break;
            case SDL_KEYDOWN:
                break;
            case SDL_KEYUP:
                break;
            case SDL_MOUSEBUTTONDOWN:
                mouse_pos.x = e.button.x;
                mouse_pos.y = e.button.y;
                WindowMgr_map_screen_to_px(&mouse_pos);
                break;
            default:
                break;
        }
    }
}
